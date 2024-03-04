"""
Réduit une image puis en extrait une partie carrée
"""

from PIL import Image

import sys

if __name__=="__main__":
    p=int(sys.argv[2])
    img=Image.open(sys.argv[1])
    scale=p/img.size[1]
    img=img.resize((int(img.size[0]*scale), int(img.size[1]*scale)))
    left=(img.size[0]-p) // 2
    right=left+p
    top=0
    bottom=p
    img=img.crop((left, top, right, bottom))
    img.save(sys.argv[1])
