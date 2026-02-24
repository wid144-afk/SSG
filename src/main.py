from copystatic import copy_files_recursive
from gencontent import generate_pages_recursive
import sys

def main():
    basepath = "/"
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    copy_files_recursive("static", "docs")
    generate_pages_recursive("content", "template.html", "docs", basepath)
    

main()