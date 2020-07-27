from bs4 import BeautifulSoup
import requests
import os
import shutil

OK = 200

img_dir = "players"
if img_dir and not os.path.exists(img_dir):
	os.makedirs(img_dir)

url = "https://ak-static.cms.nba.com/wp-content/uploads/headshots/nba/latest/260x190/{0}.png"

with open("players.html", "r") as f:
	html = f.read()
soup = BeautifulSoup(html, features="lxml").find("section", {"class": "nba-player-index__row"})
imgs = soup.findAll("img")
for img in imgs:
	try:
		img_url = img.attrs["src"]
	except KeyError:
		img_url = img.attrs["data-src"]
	finally:
		img_name = img_url.split('/')[-1].split('.')[0]
		img_extension = img_url.split('.')[-1]
		if img_url[:2] == "//":
			# Stream the file without reading it into memory at once
			img_response = requests.get(f"https:{img_url}", stream=True)
			if img_response.status_code == OK:
				with open(os.path.join(img_dir, f'{img_name}.{img_extension}'), "wb") as f:
					shutil.copyfileobj(img_response.raw, f)
