# urlparsed = urlparse(url)
# if urlparsed.scheme not in ("http", "https"):
#     return True    

# def can_fetch(url: str) -> bool:    
#     try:
#         rep = requests.get(url, headers=HEADERS)
#         if rep.status_code == 200:
#             return(True)
#     except Exception as e:        
#         print("AssertionError:", e)
#         return(False)

# def link_abs(link:str) -> bool:
#     rep = requests.get(link, headers=HEADERS)
#     if rep.status_code == 200:
#         for ext in EXTS:
#             if rep.headers.get("Content-Type") == "image/" + ext:
#                 return(True)
#     return(False)

# def link_rel(url:str, link:str) -> bool:
#     rep = requests.get(url + link, headers=HEADERS)
#     if rep.status_code == 200:
#         for ext in EXTS:
#             if rep.headers.get("Content-Type") == "image/" + ext:
#                 return(True)
#     return(False)

# def is_valid_img(url:str, link: str) -> bool:
#     if link_abs(link) or link_rel(url, link):
#         return(True)
#     return(False)

# def img_url(scheme:str, netloc:str, src:str) -> str:
#     if is_valid_scheme(src):
#         return(src)
#     else:
#         return(urljoin(scheme, netloc, src))

# try:
    #     Path(PATH).mkdir(exist_ok=True)    
    # except OSError as e:
    #     print(f"Make directory failed: {e}")
    
    # url = scheme://netloc/path?query#fragment
    # netloc = hostname:port
    # netloc = urlparse(url).netloc
    # scheme = urlparse(url).scheme
    # url = params[3]
    # if not is_valid_scheme(url):    
    #     print("AssertionError: url not valid")
    #     print("Valid url: http[s]://netloc[/path?query#fragment]")
    #     return
     
# try:
    #     r = requests.get(url, headers=headers, timeout=timeout)
    #     r.raise_for_status() # 404 403 500
    #     soup = BeautifulSoup(r.text, 'html.parser')        
        

   
# https://villarson.com/portfolio.php

def deslash(url: str) -> str:    
    return(url.removesuffix("/"))

# has_a_valid_ext = False
#     for ext in EXTS:
#         if src.endswith("." + ext):
#              has_a_valid_ext = True
# 
# 
# print(img_link)
                # print(rep.headers.get("Content-Type"))
                # print(len(rep.content))    


# Scorpion
# gps_ifd = exif.get_ifd(ExifTags.IFD.GPSInfo)
    # print(gps_ifd)

# def check_exts(format: str, exts: list[str]) -> bool:
#     for ext in exts:
#         if format.lower() == ext:
#             return True
#     return False

# tagname = ExifTags.TAGS.get(k, f"Unknown ({k})")
            # print(f"{tagname}: deleted")

