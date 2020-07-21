#writen By Younes
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import sys

_headers = {'user-agent': 'wis/0.0.1'}


if len(sys.argv) < 3:
    print('input args <url> <folder name> ')
    exit()

print('************************************')
print('************************************')
print('*********WEB IMAGES SCRAPER*********')
print('************************************')


g_url =sys.argv[1]
g_folder = sys.argv[2]


#print(g_url + g_folder)
#exit()
#https://stackoverflow.com/a/16696317/12902232
def download_file(domain,url,loc,file_name):
    
    if(not url.startswith("http")):
        # from urlparse import urlparse  # Python 2
        parsed_uri = urlparse(domain )
        result = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
        #print(result)
        url = result + url

    # NOTE the stream=True parameter below
    with requests.get(url, stream=True, headers=_headers) as r:
        r.raise_for_status()
        with open(loc+'/'+file_name, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192): 
                # If you have chunk encoded response uncomment if
                # and set chunk_size parameter to None.
                #if chunk: 
                f.write(chunk)
    return 1

def scrap_images(website,prefix):
    page = requests.get(website,timeout=5.001, headers=_headers)

    soup = BeautifulSoup(page.content, 'html.parser')
    imgs=soup.select('img')
    print("cnt:"+str(len(imgs)))

    for pi,p in enumerate(imgs):
        try:
            pic_url =  p['src'].strip()
        except:
            print("===no src attribute =>"+ p['src'])               


        ext='jpg'  
        if(pic_url.find('jpg') >1):
            ext='jpg'
        if(pic_url.find('png') >1):
            ext='png'
        if(pic_url.find('gif') >1):
            ext='gif' 

        print("[Fit]"+"|("  + "/"+str(pi)+")|"+ ext +"|" + pic_url)
        
        try:   
            #Download;
            download_file(website,pic_url,g_folder,prefix+ "_id_"+ str(pi)+"."+ext )
        except:
            print("==============link error=========="+pic_url)               





from pathlib import Path
Path(g_folder).mkdir(parents=True, exist_ok=True)


scrap_images(g_url,'img_')