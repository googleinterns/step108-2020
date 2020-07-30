from bs4 import BeautifulSoup
import requests
import os
import shutil

OK = 200

img_dir = "logos"
if img_dir and not os.path.exists(img_dir):
	os.makedirs(img_dir)

url = "https://logoeps.com/all-nba-team-logos/31287/"
response = requests.get(url)
if response.status_code != OK:
	print(f"Could not fetch HTML from {url}")
	exit(1)

html = response.content
soup = BeautifulSoup(html, features="lxml").find("main")
imgs = soup.findAll("img")
for img in imgs:
	img_url = img.attrs["src"]
	img_name = img.attrs["alt"].replace(" logo vector", '')
	img_extension = img_url.split('.')[-1]
	# Stream the file without reading it into memory at once
	img_response = requests.get(img_url, stream=True)
	if img_response.status_code == OK:
		with open(os.path.join(img_dir, f'{img_name}.{img_extension}'), "wb") as f:
			shutil.copyfileobj(img_response.raw, f)