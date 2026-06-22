# imports
import requests
from bs4 import BeautifulSoup
from pathlib import Path
from urllib.parse import urlparse, urljoin
from dataclasses import dataclass


# config
EXTS = ["jpg", "jpeg", "png", "gif", "bmp"]


# class
@dataclass
class Stats:
    n_img: int = 0
    

# functions
def is_img(src: str, type: str) -> bool:
    has_a_valid_ext = False
    for ext in EXTS:
        if src.endswith("." + ext):
             has_a_valid_ext = True    
    for ext in EXTS:
        if type.startswith("image/" + ext) and has_a_valid_ext:
            return(True)
    return(False)


def save_img(link: str, path: str, img: bytes) -> bool:
    filename = Path(urlparse(link).path).name
    p = Path(path) / filename # "/" operator of object Path()
    try:
        with p.open("xb") as f: # wb overwrite silently, xb raise FileExistsError if needed
            f.write(img)
            print(f"{filename} saved")
            return(True)
    except FileExistsError:
        # print(f"{p} already exists")
        return(False)   
    except OSError as e:
        print(f"{p} not saved: {e}")
        return(False)   


def get_img(url: str, path: str, headers: dict[str,str], timeout: int, stats: Stats) -> None:
    n = 0
    try:
        r = requests.get(url, headers=headers, timeout=timeout)
        r.raise_for_status() # 404 403 500
        soup = BeautifulSoup(r.text, 'html.parser')        
        for img in soup.find_all('img'): # only img tag
            src = img.get('src')
            if src is None or src == "":
                continue
            try:
                img_link = urljoin(url, src)
                rep = requests.get(img_link, headers=headers, timeout=timeout)
                rep.raise_for_status()
                # print(rep.status_code)        
                if is_img(src, rep.headers.get("Content-Type", "")) and n < 2: # #######to remove ###############3
                    if save_img(img_link, path, rep.content):
                        n = n + 1                
            except requests.exceptions.RequestException as e:
                print(f"Request Error: {e}")        
    except requests.exceptions.RequestException as e:
        print(f"Request Error: {e}")
    print(f"{n} images saved")    
    stats.n_img += n
