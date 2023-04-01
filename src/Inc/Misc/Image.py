# Created: 2023.04.01
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details
#
# Image1 = TImage()
# Image1.ResizeFile('Pic1.jpg', 'Pic2.jpg', 1024, 50)


import os
from PIL import Image


class TImage():
    @staticmethod
    def Open(aFileIn: str) -> object:
        return Image.open(aFileIn)

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
        SizeIn = os.path.getsize(aFileIn)
        Img = TImage.Open(aFileIn)
        Img = TImage.Resize(Img, aMaxSize)

        if (not aFileOut):
            aFileOut = aFileIn
        Img.save(aFileOut, quality = aQuality)
        Ratio = os.path.getsize(aFileOut) / SizeIn
        return Ratio
