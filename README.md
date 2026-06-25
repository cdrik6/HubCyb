# HubCyb
./spider [-rlp] URL
Option -r : recursively downloads the images in a URL received as a parameter.
Option -r -l [N] : indicates the maximum depth level of the recursive download.
  If not indicated, it will be 5.
Option -p [PATH] : indicates the path where the downloaded files will be saved.
  If not specified, ./data/ will be used

The program expects a fully qualified URL including the scheme (http:// or https://).

https://docs.python.org/3/library/urllib.parse.html
https://arjancodes.com/blog/using-python-urllib-module-for-web-scraping-and-url-parsing/

https://beautiful-soup-4.readthedocs.io/en/latest/#quick-start

https://requests.readthedocs.io/en/latest/user/quickstart/