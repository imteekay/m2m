from bs4 import BeautifulSoup
from requests import get

domain_name = "https://medium.freecodecamp.org/"
post_slug = "an-introduction-to-the-basic-principles-of-functional-programming-a2c2a15c84"
post_url = domain_name + post_slug

post_response = get(post_url, stream=True)

soup = BeautifulSoup(post_response.content, 'html.parser')
post = soup.findAll("div", {"class": "sectionLayout--insetColumn"})[0]


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

        codeblock = f"```{programming_language}\n{code}\n```"
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
