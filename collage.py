import os
import requests
import PIL.Image


def fetch_images(user):
    url = "https://ws.audioscrobbler.com/2.0/?method=user.gettopalbums&user={}&period=7day&api_key={}&format=json"
    # fetch album data from api
    files = []
    print("Requesting data from API")
    r = requests.get(url.format(user, API_KEY))
    print("[Response {}]".format(r.status_code))
    if r.status_code == 200:
        albums = r.json()

        # create folder to store images
        if not os.path.exists("img"):
            print("Created /img folder")
            os.mkdir("img")

        # download album art for each image
        num = 0
        while len(files) < 9:
            album = albums["topalbums"]["album"][num]
            name = album["name"]
            # create safe filename
            allow = (" ", ".", "_")
            safe = "".join(c for c in name if c.isalnum() or c in allow).rstrip()
            # download image
            img_url = album["image"][3]["#text"]
            if img_url:
                files.append(safe)
                print("Downloading art for {}".format(safe))
                img_data = requests.get(img_url).content
                with open("img/" + safe + ".jpg", "wb") as f:
                    f.write(img_data)
            else:
                print("No album art for {}, skipping".format(safe))
            num += 1
    else:
        print(r.text)

    return files


def create_image(files):
    # create new image
    print("Creating final image")
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
if len(files) == 9:
    create_image(files)
else:
    print("\nSomething went wrong")
    print("({} albums retrieved, 9 required)".format(len(files)))
