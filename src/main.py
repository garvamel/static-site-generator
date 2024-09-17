from textnode import TextNode

def main():

    text = "This is a text node"
    text_type = "bold"
    url = "https://www.boot.dev"
    tn = TextNode(text, text_type, url)
    print(tn)

main()
