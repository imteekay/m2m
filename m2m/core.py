import os

from bs4 import BeautifulSoup
from dotenv import load_dotenv
from requests import get

load_dotenv()

GITHUB_USERNAME = os.environ.get('GITHUB_USERNAME')
GITHUB_PASSWORD = os.environ.get('GITHUB_PASSWORD')


class GistToCodeblock:
    def __init__(self, tag):
        self.tag = tag

    def transform(self):
        return self.build_codeblock()

    def build_codeblock(self):
        gist_file = self.gist_file()
        code = gist_file['content']
        programming_language = gist_file['language'].lower()
        return f"```{programming_language}\n{code}\n```"

    def gist_file(self):
        gist_response = get(self.gist_api_url(),
                            auth=(GITHUB_USERNAME, GITHUB_PASSWORD))

        return next(iter(gist_response.json()['files'].values()))

    def gist_api_url(self):
        iframe_response = get(self.iframe_url(), stream=True)
        iframe_soup = BeautifulSoup(iframe_response.content, 'html.parser')
        gist_id = iframe_soup.script['src'].rsplit(".", 1)[0].split("/")[-1]
        return f"https://api.github.com/gists/{gist_id}"

    def iframe_url(self):
        return "https://medium.freecodecamp.org" + self.tag.iframe['src']


class TagMapper:
    def __init__(self, tag):
        self.tag = tag

    def to_markdown(self):
        if self.tag.name == 'h1':
            return self.markdown_h1()
        elif self.tag.name == 'h3':
            return self.markdown_h3()
        elif self.tag.name == 'h4':
            return self.markdown_h4()
        elif self.tag.name == 'p':
            return self.markdown_paragraph()
        elif self.tag.name == 'figure':
            return self.markdown_image()
        elif self.tag.name == 'blockquote':
            return self.markdown_blockquote()
        elif self.tag.name == 'ul':
            return self.markdown_unordered_list()
        elif self.tag.name == 'ol':
            return self.markdown_ordered_list()

    def markdown_h1(self):
        return f"# {self.tag.text}"

    def markdown_h3(self):
        return f"### {self.tag.text}"

    def markdown_h4(self):
        return f"#### {self.tag.text}"

    def markdown_paragraph(self):
        return self.tag.text

    def markdown_image(self):
        if self.tag.img:
            return f"![]({self.tag.img['src']})"
        elif self.tag.iframe:
            return GistToCodeblock(self.tag).transform()

    def markdown_blockquote(self):
        return f"> {self.tag.text}"

    def markdown_unordered_list(self):
        unordered_lists = self.tag.findAll("li")
        lists_texts = [f"* {li.text}" for li in unordered_lists]
        return "\n\n".join(lists_texts)

    def markdown_ordered_list(self):
        ordered_lists = self.tag.findAll("ol")
        lists_texts = [f"1. {li.text}" for li in ordered_lists]
        return "\n\n".join(lists_texts)


class MediumToMarkdown:
    def __init__(self, post_url):
        self.post_url = post_url

    def transform(self):
        markdown_file = open("post.md", "w+")

        for tag in self.medium_post():
            markdown_tag = TagMapper(tag).to_markdown()
            markdown_file.write(markdown_tag)
            markdown_file.write("\n\n")

        markdown_file.close()

    def medium_post(self):
        post_content = self.medium_post_response().content
        soup = BeautifulSoup(post_content, 'html.parser')
        return soup.findAll("div", {"class": "sectionLayout--insetColumn"})[0]

    def medium_post_response(self):
        return get(self.post_url, stream=True)


domain_name = "https://medium.freecodecamp.org/"
post_slug = "an-introduction-to-the-basic-principles-of-functional-programming-a2c2a15c84"
post_url = domain_name + post_slug

m2m = MediumToMarkdown(post_url)
m2m.transform()
