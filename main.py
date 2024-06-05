import os
import zipfile
from threading import Thread

import requests
from zipfile import ZipFile
from io import BytesIO
from bs4 import BeautifulSoup


def log(id, text):
    print(f"{id}) {text}")


def urlCreator(workshopId, gameId, buildId):
    return f"http://workshop{workshopId}.abcvg.info/archive/{gameId}/{buildId}.zip"


def handle(id):
    try:
        int(id)
    except ValueError:
        log(id, "Incorrect ID")
        return
    url = f"https://steamcommunity.com/sharedfiles/filedetails/?id={id}"
    bs = BeautifulSoup(requests.get(url).text, 'html.parser')
    buildName = bs.find("div", "workshopItemTitle").text
    gameId = bs.find("div", "apphub_OtherSiteInfo").find("a", "btnv6_blue_hoverfade").get("data-appid")
    for workshopId in ["", 8, 4, 6, 0, 2, 1, 3, 5, 7, 9]:
        url = urlCreator(workshopId, gameId, id)
        # log(name, f"Trying {url}")
        dirName = buildName
        try:
            zipFile = ZipFile(BytesIO(requests.get(url).content))
        except zipfile.BadZipfile:
            continue
        if not os.path.exists(dirName):
            os.mkdir(dirName)
        with open(f"{dirName}/Vehicle.brv", 'wb') as file:
            file.write(zipFile.read(f"{id}/Vehicle.brv"))
        log(buildName, "Success")
        return
    log(id, "The download failed, contact the developer")


vehiclesDir = "Vehicles"
while True:
    id = input("Enter the ID or link\n").split("id=")[-1].split("&")[0]
    print(os.getcwd())
    if not os.getcwd().endswith(vehiclesDir):
        if not os.path.exists(vehiclesDir):
            os.mkdir(vehiclesDir)
        os.chdir(vehiclesDir)
    Thread(target=lambda: handle(id)).start()
