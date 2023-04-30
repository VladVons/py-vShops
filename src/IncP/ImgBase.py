# Created: 2023.04.18
# Author:  Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from Task.SrvImg.Api import TApiImg, TApiImgConf


class TImgBase():
    def __init__(self, aApiImg: TApiImg):
        self.ApiImg = aApiImg
        self.Conf: TApiImgConf

    def _init_(self):
        self.Conf = self.ApiImg.Conf
