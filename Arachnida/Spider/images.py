# imports
import requests
from pathlib import Path
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
from dataclasses import dataclass
from PIL import Image
from io import BytesIO


# config
EXTS = ["jpg", "jpeg", "png", "gif", "bmp"]


# class
@dataclass
class Stats:
    n_img: int = 0


# functions
def is_valid_img(type: str, img: bytes) -> bool:
    for ext in EXTS:
        if type.startswith("image/" + ext):
            try:
                with Image.open(BytesIO(img)) as im:
                    im.verify()
                return True
            except Exception:
                return False
    return False


def save_img(link: str, path: str, img: bytes) -> bool:
    filename = Path(urlparse(link).path).name
    p = Path(path) / filename  # "/" operator of object Path()
    try:
        with p.open("xb") as f:  # wb overwrite silently, xb raise FileExistsError if needed
            f.write(img)
            print(f"{filename} saved")
            return True
    except FileExistsError:
        print(f"{filename} already exists")
        return False
    except OSError as e:
        print(f"{p} not saved: {e}")
        return False


def get_img(url: str, path: str, headers: dict[str, str], timeout: int, stats: Stats, soup: BeautifulSoup) -> None:
    n = 0
    for img in soup.find_all('img'):  # only img tag
        src = img.get('src')
        if src is None or src == "":
            continue
        try:
            img_link = urljoin(url, src)
            rep = requests.get(img_link, headers=headers, timeout=timeout)
            rep.raise_for_status()  # print(rep.status_code)
            if is_valid_img(rep.headers.get("Content-Type", ""), rep.content):
                if save_img(img_link, path, rep.content):
                    n += 1
        except requests.exceptions.RequestException as e:
            print(f"Request Error: {e}")
    print(f"{n} images saved")
    stats.n_img += n
