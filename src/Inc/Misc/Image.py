# Created: 2023.04.01
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details
#
# Image1 = TImage()
# Image1.ResizeFile('Pic1.jpg', 'Pic2.jpg', 1024, 50)


import os
import io
from PIL import Image


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
