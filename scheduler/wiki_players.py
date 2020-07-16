import requests
import os
import shutil
import csv
import json
import hashlib

OK = 200

img_dir = "wiki_players"
if img_dir and not os.path.exists(img_dir):
	os.makedirs(img_dir)

players = []
with open("commonplayerinfo.csv", "r", newline='') as f:
	reader = csv.DictReader(f)
	for row in reader:
		players.append({"name": f"{row['FIRST_NAME']} {row['LAST_NAME']}", "id": row["PERSON_ID"]})

url = "https://www.wikidata.org/w/api.php?action=wbgetentities&format=json&sites=enwiki&props=claims&titles={0}"
img_url = "https://upload.wikimedia.org/wikipedia/commons/{0}/{0}{1}/{2}"

for player_obj in players:
	player = player_obj["name"]
	response = requests.get(url.format(player))
	if response.status_code == OK:
		try:
			obj = json.loads(response.text)["entities"]
			img_name = obj[list(obj)[0]]["claims"]["P18"][0]["mainsnak"]["datavalue"]["value"].replace(' ', '_')
			md5 = hashlib.md5(img_name.encode('utf-8')).hexdigest()
			img_response = requests.get(img_url.format(md5[0], md5[1], img_name), stream=True)
			if img_response.status_code == OK:
				img_extension = img_name.split('.')[-1]
				player_id = player_obj["id"]
				with open(os.path.join(img_dir, f"{player_id}.{img_extension}"), "wb") as f:
					shutil.copyfileobj(img_response.raw, f)
		except KeyError:
			print(player_obj)
	# try:
	# 	img_url = img.attrs["src"]
	# except KeyError:
	# 	img_url = img.attrs["data-src"]
	# finally:
	# 	img_name = img_url.split('/')[-1].split('.')[0]
	# 	img_extension = img_url.split('.')[-1]
	# 	if img_url[:2] == "//":
	# 		# Stream the file without reading it into memory at once
	# 		img_response = requests.get(f"https:{img_url}", stream=True)
	# 		if img_response.status_code == OK:
	# 			with open(os.path.join(img_dir, f'{img_name}.{img_extension}'), "wb") as f:
	# 				shutil.copyfileobj(img_response.raw, f)
