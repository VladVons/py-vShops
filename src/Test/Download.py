import asyncio
#
from Inc.Misc.Request import TDownload, TDownloadImage


async def Test_01():
    Urls = [
        'http://oster.com.ua/image/cache/catalog/products/682527-500x500.jpg',
        'https://loremflickr.com/800/600/girl',
        'https://loremflickr.com/800/600/dog'
    ]

    Download = TDownload('Temp')
    Res1 = await Download.Get(Urls, ['oster1.jpg', 'girl1.jpg', 'dog1.jpg'])
    print(Res1)

async def Test_02():
    Urls = [
        'http://oster.com.ua/image/cache/catalog/products/682527-500x500.jpg',
        'https://upload.wikimedia.org/wikipedia/commons/f/f1/Jack_Russell_Terrier_1.jpg',
        'http://elelur.com/data_images/dog-breeds/jack-russell-terrier/jack-russell-terrier-02.jpg',
    ]
    Size = [34737, 5242366, 5916180]
    ImageId   = [12, 24, 37]

    Download = TDownloadImage('Temp')
    Data = zip(Urls, Size, ImageId)
    #Res1 = await Download.Fetch(Data)
    Res1 = await Download.Get(Urls)
    print(Res1)


asyncio.run(Test_02())
