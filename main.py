from typing import Union
from fastapi import FastAPI
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import cv2
from numpy.lib.polynomial import poly
from PIL import Image, ImageDraw
#from sklearn.cluster import KMeans
import urllib.request

app = FastAPI()

@app.post("/process_image/")
async def process_image(image_url: str):
    try:
        req = urllib.request.urlopen(image_url)
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
        
        return {"processed_number": str(len(cnt))}
    
    except Exception as e:
        return {"error": str(e)}
