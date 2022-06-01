"""
Inspired by https://stackoverflow.com/questions/55981369/printing-the-content-of-all-html-files-in-a-directory-with-beautifulsoup

This is really bad since I did it in a rush lol

This program will prettify all `.html` files in the directory the file is located in. It will also recursively call itself to prettify all `.html` files in sub-directories too.
"""

from os import listdir
from os.path import dirname, isdir
from sys import argv

from bs4 import BeautifulSoup

cwd = dirname(argv[0])

cwd = cwd if cwd == "" else f"{cwd}/"


def prettify(file_path: str) -> None:
    print(f"Prettifying: {file_path}")
    with open(file_path, "r+", encoding="cp437") as f:
        html = f.read()
        soup = BeautifulSoup(html, "html.parser")
        pretty_html = soup.prettify()
        f.seek(0)
        f.truncate()
        f.write(pretty_html)


def controller(cwd: str) -> None:
    for path in [f"{cwd}{obj}" for obj in listdir(cwd)]:
        if ".git" in path:
            print(f"Skipping {path}")
        elif isdir(path):
            print(f"Recursive call to: {path}")
            controller(path if path == "" else f"{path}/")
        elif path.split(".")[-1] == "html":
            prettify(path)


controller(cwd)
