import cv2
import numpy as np
import os
from PIL import Image
player_dir = "wiki_players"
px = 150

new_dir = "downsize_player"
if not os.path.exists(new_dir):
	os.makedirs(new_dir)

for player_file in os.listdir(player_dir):
	bgr_img = cv2.imread(os.path.join(player_dir, player_file))
	img = cv2.cvtColor(bgr_img, cv2.COLOR_BGR2RGB)
	height, width, colors = img.shape
	smaller = min(height, width)
	downsample = smaller / px
	res = cv2.resize(img, dsize=(int(width / downsample), int(height / downsample)), interpolation=cv2.INTER_CUBIC)
	im = Image.fromarray(res)
	im.save(os.path.join(new_dir, player_file))
