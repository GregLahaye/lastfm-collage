import os
import requests
import PIL.Image


def fetch_images(user):
    url = "https://ws.audioscrobbler.com/2.0/?method=user.gettopalbums&user={}&period=7day&limit=9&api_key={}&format=json"
    # fetch album data from api
    r = requests.get(url.format(user, API_KEY))
    albums = r.json()

    # create folder to store images
    if not os.path.exists("img"):
        os.mkdir("img")

    # download album art for each image
    files = []
    for album in albums["topalbums"]["album"]:
        name = album["name"]
        files.append(name)
        img_url = album["image"][3]["#text"]
        img_data = requests.get(img_url).content
        with open("img/" + name + ".jpg", "wb") as f:
            f.write(img_data)

    return files


def create_image(files):
    # create new image
    final = PIL.Image.new("RGB", (900, 900))

    for index, img in enumerate(files):
        # create new image from album art
        new = PIL.Image.open("img/" + img + ".jpg")
        w, h = new.size
        # calculate image position
        x = index // 3 * 300
        y = index % 3 * 300
        # append image to final
        final.paste(new, (x, y, x + w, y + h))

    # save final image
    final.save(user + ".jpg")


API_KEY = ""
user = ""

files = fetch_images(user)
create_image(files)
