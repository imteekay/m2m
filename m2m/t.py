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
    if tag.img:
        return f"![]({tag.img['src']})"
    elif tag.iframe:
        domain_name = "https://medium.freecodecamp.org"
        iframe_url = domain_name + tag.iframe['src']
        iframe_response = get(iframe_url, stream=True)
        iframe_soup = BeautifulSoup(iframe_response.content, 'html.parser')

        gist_id = iframe_soup.script['src'].rsplit(".", 1)[0].split("/")[-1]
        url = f"https://api.github.com/gists/{gist_id}"
        gist_response = get(url, stream=True)

        gist_file = next(iter(gist_response.json()['files'].values()))
        code = gist_file['content']
        programming_language = gist_file['language'].lower()

        codeblock = f"""```{programming_language}
        {code}
        ```
        """
        return codeblock


def markdown_blockquote(tag):
    return f"> {tag.text}"


def markdown_unordered_list(tag):
    unordered_lists = tag.findAll("li")
    lists_texts = [f"* {li.text}" for li in unordered_lists]
    return "\n\n".join(lists_texts)


def markdown_ordered_list(tag):
    ordered_lists = tag.findAll("ol")
    lists_texts = [f"1. {li.text}" for li in ordered_lists]
    return "\n\n".join(lists_texts)


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
    markdown_file.write("\n\n")

markdown_file.close()
