from bs4 import BeautifulSoup
from requests import get

url = "https://medium.freecodecamp.org/an-introduction-to-the-basic-principles-of-functional-programming-a2c2a15c84"

response = get(url, stream=True)
print(response.text)

a = BeautifulSoup(response.content, 'html.parser')
post = a.findAll("div", {"class": "sectionLayout--insetColumn"})[0]

h1 = post.find("h1")
figures = post.findAll("figure")  # images, but also gists
paragraphs = post.findAll("p")
h3s = post.findAll("h3")
h4s = post.findAll("h4")
blockquotes = post.findAll("blockquote")

# h1, h3, h4, p, figure (images, but also gists), blockquote, unordered list (ul), ordered list (ol)


def markdown_h1(tag):
    return f"# {tag.text}"


def markdown_h3(tag):
    return f"### {tag.text}"


def markdown_h4(tag):
    return f"#### {tag.text}"


def markdown_paragraph(tag):
    return tag.text


def markdown_image(tag):
    return f"![]({tag.img['src']})"


def markdown_blockquote(tag):
    return f"> {tag.text}"


def markdown_unordered_list(tag):
    pass


def markdown_ordered_list(tag):
    pass


def tag_mapper(tag):
    if tag.name == 'h1':
        return markdown_h1(tag)
    elif tag.name == 'h3':
        return markdown_h3(tag)
    elif tag.name == 'h4':
        return markdown_h4(tag)
    elif tag.name == 'p':
        return markdown_paragraph(tag)
    elif tag.name == 'figure':
        return markdown_image(tag)
    elif tag.name == 'blockquote':
        return markdown_blockquote(tag)
    elif tag.name == 'ul':
        return markdown_unordered_list(tag)
    elif tag.name == 'ol':
        return markdown_ordered_list(tag)


markdown_file = open("post.md", "w+")

for tag in post:
    markdown_tag = tag_mapper(tag)
    markdown_file.write(markdown_tag)

markdown_file.close()
