import os
import re
from biplist import readPlist
from PIL import Image

def split(path):
	image = Image.open(os.path.splitext(path)[0]+".png")
	plist = readPlist(os.path.splitext(path)[0]+".plist")
	prefix = os.path.dirname(path)+os.sep + "Sprites_" + get_file_name(path) + os.sep
	frames: dict = plist["frames"]
	regex = re.compile("({|})")
	for k in frames:
		filename = prefix + k.replace("jpg","png")
		rectkey = "frame" if "frame" in frames[k] else "textureRect"
		rect = regex.sub("",frames[k][rectkey]).split(",")
		rotateKey = "rotated" if "rotated" in frames[k] else "textureRotated"
		rotate: bool = frames[k][rotateKey]

		orginX = int(rect[0])
		orginY = int(rect[1])
		orginW = int(rect[2])
		orginH = int(rect[3])

		x = orginX
		y = orginY
		w = orginX + orginW if not rotate else orginX + orginH
		h = orginY + orginH if not rotate else orginY + orginW
		box = (x,y,w,h)
		print(box)
		img = image.crop(box)
		if not os.path.exists(prefix):
			os.makedirs(prefix)
		if rotate:
			img = img.rotate(90, expand=1)
		img.save(filename)
		print(filename)



def get_file_name(path):
	filename: str = os.path.split(path)[-1]
	index = filename.rfind(".")
	return filename[0:index]


# while True:
# 	path = input("请将图片资源拖到此处").strip()
# 	print()
split("./game_balloon-hd.png")
	# if os.path.exists(path):
	# 	if os.path.exists(os.path.splitext(path)[0]+".plist"):
	# 		try:
				# split(path)
	# 		except Exception as e:
	# 			print("Exception ", e, "\n")
	# 			print("文件解析出错，请重试\n")
	# 		else:
	# 			print("图片资源或plist文件未找到")
	# 		finally:
	# 			print("最后了")
	# else:
	# 	print("\n文件路径异常 请重试\n")