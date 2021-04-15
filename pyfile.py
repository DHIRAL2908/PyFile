#Imports.
import os
from pathlib import Path
from urllib.parse import urlparse, urljoin
import requests
from bs4 import BeautifulSoup

#Some important functions. Reference: https://stackoverflow.com/questions/2573670/download-whole-directories-in-python-simplehttpserver
def get_links(content):
    soup = BeautifulSoup(content, 'lxml')
    for a in soup.findAll('a'):
        yield a.get('href')

def download(url):
    path = urlparse(url).path.lstrip('/')
    print(path)
    r = requests.get(url)
    if r.status_code != 200:
        raise Exception('Status code is {} for {}.'.format(r.status_code, url))
    content = r.text
    if path.endswith('/'):
        Path(path.rstrip('/')).mkdir(parents=True, exist_ok=True)
        for link in get_links(content):
            download(urljoin(url, link))
    else:
        path = "Received/" + path[9:]
        if not os.path.exists(path):
            os.system("mkdir -p ./" + "/".join(path.split("/")[:-1]) + " 2>/dev/null")
        with open(path, 'w') as f:
            f.write(content)

#Start of program.
print("[+] Welcome to PyFile!")
print("[!] Please select an option: ")
print("    (1) Send files.")
print("    (2) Recieve files")

choice = int(input())

#Make the required directories.
os.system("mkdir ./ToBeSent 2>/dev/null")
os.system("mkdir ./Received 2>/dev/null")

if choice == 1:
	print("[+] Copy the files you want to send in the 'ToBeSent' folder. Then press enter!")
	input()
	print("[+] Starting the server!")
	print("[!] Tell the client your ip address from the output of the `ifconfig` command.")
	print()
	print("[!] Press CTRL+C to exit anytime.")
#Start the server at port 8780.
	os.system("python3 -m http.server 8780")

elif choice == 2:
	print("[+] Enter the ip address of the server: ")
	print()
	ip = input()
	download("http://"+ip+":8780/ToBeSent/")

else:
	print("[-] Please enter valid choice.")