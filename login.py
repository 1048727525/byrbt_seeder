import requests
from lxml import etree
import VCRmodule
from requests.cookies import RequestsCookieJar

def getimglink(html):
  imgpath='//table[@class="mainouter"]//form[@method="post"]/table[@border="0"]/tr[3]/td[@align="left"]/img/@src'
  imglink = etree.HTML(html).xpath(imgpath)
  return imglink[0]

def downloadimg(imglink,header):
  path="./img/loginimage.jpg"
  download=requests.get("https://bt.byr.cn/"+imglink,headers=header)
  with open(path,"wb") as f:
      f.write(download.content)
  f.close()
  return path

def char_set(char_new):
    res = char_new.split('=')[2]
    return res

def main(url, username, password):
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36'}

    session=requests.Session()
    r1=session.get('https://bt.byr.cn/login.php',headers=header)
    response=r1.content
    imglink=getimglink(response)
    imgpath=downloadimg(imglink,header)
    imgstring=VCRmodule.main(imgpath)
    imagehash = char_set(imglink)
    formdata = {
        'username': username,
        'password': password,
        'imagestring': imgstring,
        'imagehash': imagehash
    }
    r2=session.post('https://bt.byr.cn/takelogin.php',data=formdata, allow_redirects=True)

    r3=session.get(url, cookies = r2.cookies,  headers=header)
    return session.cookies


