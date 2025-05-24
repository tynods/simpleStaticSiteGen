
from textnode import *
from htmlnode import *



def main():
    l = TextNode("This is some anchor text",
                 TextType.LINK,
                 "https://www.boot.dev")
    print(l)

if __name__=="__main__" :
    main()