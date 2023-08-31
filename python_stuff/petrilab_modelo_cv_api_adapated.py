import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import cv2
from numpy.lib.polynomial import poly
from PIL import Image, ImageDraw
from sklearn.cluster import KMeans
import zipfile
import urllib.request
#from cvlib.object_detection import draw_bbox
#import cvlib as cv

req = urllib.request.urlopen('https://storage.googleapis.com/kagglesdsdata/datasets/819682/1402384/IMG_0865.JPG?X-Goog-Algorithm=GOOG4-RSA-SHA256&X-Goog-Credential=databundle-worker-v2%40kaggle-161607.iam.gserviceaccount.com%2F20230831%2Fauto%2Fstorage%2Fgoog4_request&X-Goog-Date=20230831T132432Z&X-Goog-Expires=345600&X-Goog-SignedHeaders=host&X-Goog-Signature=20f4fa3cc43b40238cf1aa3c14f3026e448a01423b92c60fd64ee5fd3c4862ae322ba3155bef84c0f75cd8ecbe8b31a8c930922b25d4410d567a64d776eb6f0d9665db1b2679002103cea84ceab85a5b76a12a9c1caa63b1671384738b7aff6a28d00675a884e1a509dc70ebf1c2b6f0e1847c97dc0690b194f3436f895682e64d8d259e6a055f747cb7b01877bded5102bbc40f94b4b2cd2503c24b901370d3721b14b6ed21dd381cb9b8bd1f8064312104698b21ab5d8ce87696ec821cbd6af618212751e74435e1f2b17f8dd78d7ec6d5829b764ed9caf33ffc3d240aa24363f14af24f4c373d6e2404227250b9e4e2cfc8794aec999d259db9932010e2de')
arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
img = cv2.imdecode(arr, -1) # 'Load it as it is'

#cv2_imshow(img)
if cv2.waitKey() & 0xff == 27: quit()

if img.shape[::2] != (400,400):
  crop = cv2.resize(img, (int(int(img.shape[1]) * 400/int(img.shape[1])), int(int(img.shape[0]) * 400/int(img.shape[0]))), cv2.INTER_AREA)

gray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)

blur = cv2.GaussianBlur(gray, (7, 7), 0)

canny = cv2.Canny(blur, 15, 75, 3)

dilated = cv2.dilate(canny, (1,1), iterations = 2)

h = dilated.shape[0]
w = dilated.shape[1]
lum_img = Image.new('L',[h,w] ,0)
draw = ImageDraw.Draw(lum_img)
draw.pieslice([(45,45),(h-45,w-45)],0,360,fill=255)
img_arr = np.array(dilated)
lum_img_arr = np.array(lum_img)

x = cv2.subtract(img_arr, lum_img_arr)

final_img_arr = cv2.subtract(dilated,x)
deganger = (Image.fromarray(final_img_arr))

"""
final_img_arr = np.dstack((img_arr, lum_img_arr))
deganger = (Image.fromarray(final_img_arr))
open_cv_image = np.array(deganger)
# Convert RGB to BGR
open_cv_image = open_cv_image[:, :, ::-1].copy()
"""
x = cv2.subtract(img_arr, lum_img_arr)

final_img_arr = cv2.subtract(dilated,x)
deganger = (Image.fromarray(final_img_arr))

print("Cantidad de colonias : " + str(len(cnt)))