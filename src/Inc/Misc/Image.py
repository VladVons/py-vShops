# Created: 2023.04.01
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details
#
# pip3 install pillow
# TImage.ResizeFile('pic1.jpg', 'pic2.jpg', 1024, 50)
# TImage.CropBgFile('pic1.jpg', 'pic2.jpg')


import os
import io
from PIL import Image, ImageFilter


class TImage():
    @staticmethod
    def OpenFile(aFileIn: str) -> object:
        return Image.open(aFileIn)

    @staticmethod
    def OpenImg(aData: bytes) -> object:
        return Image.open(io.BytesIO(aData))

    @staticmethod
    def Resize(aImg, aMaxSize: int = 1024) -> object:
        Width, Height = aImg.size
        MaxSize = max(Width, Height)
        if (MaxSize > aMaxSize):
            Ratio = aMaxSize / MaxSize
            NewWidth = int(Width * Ratio)
            NewHeight = int(Height * Ratio)
            aImg = aImg.resize((NewWidth, NewHeight))
        return aImg

    @staticmethod
    def ResizeFile(aFileIn: str, aFileOut: str = None, aMaxSize: int = 1024, aQuality = 60) -> float:
        Img = TImage.OpenFile(aFileIn)
        Img = TImage.Resize(Img, aMaxSize)

        if (not aFileOut):
            aFileOut = aFileIn
        Img.save(aFileOut, quality = aQuality)
        SizeIn = os.path.getsize(aFileIn)
        Ratio = os.path.getsize(aFileOut) / SizeIn
        return Ratio

    @staticmethod
    def ResizeImg(aDataIn: bytes, aFileOut: str, aMaxSize: int = 1024, aQuality = 60) -> float:
        Img = TImage.OpenImg(aDataIn)
        Img = TImage.Resize(Img, aMaxSize)

        Img.save(aFileOut, quality = aQuality)
        Ratio = os.path.getsize(aFileOut) / len(aDataIn)
        return Ratio

    @staticmethod
    def CropBg(aImg) -> object:
        '''
        crop outer solid background from image
        '''

        # Convert the image to grayscale
        grayscale_image = aImg.convert("L")

        # Apply GaussianBlur to reduce noise
        blurred_image = grayscale_image.filter(ImageFilter.GaussianBlur(radius=5))

        # Use color thresholding to create a binary mask of the background
        threshold_value = 200
        mask = blurred_image.point(lambda x: 255 if x > threshold_value else 0)

        # Invert the mask to get the foreground (object)
        foreground = Image.eval(mask, lambda x: 255 - x)

        # Find the bounding box of the object
        bounding_box = foreground.getbbox()

        # Crop the image to the bounding box
        return aImg.crop(bounding_box)

    def CropBgFile(aFileIn: str, aFileOut: str):
        Img = TImage.OpenFile(aFileIn)
        Img = TImage.CropBg(Img)
        Img.save(aFileOut)
