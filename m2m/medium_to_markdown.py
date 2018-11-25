from bs4 import BeautifulSoup
from requests import get
from tag_mapper import TagMapper


class MediumToMarkdown:
    def __init__(self, post_url):
        self.post_url = post_url

    def transform(self):
        markdown_file = open("post.md", "w+")

        for section in self.medium_post():
            for tag in section:
                markdown_tag = TagMapper(tag).to_markdown()
                markdown_file.write(markdown_tag)
                markdown_file.write("\n\n")

        markdown_file.close()

    def medium_post(self):
        post_content = self.medium_post_response().content
        soup = BeautifulSoup(post_content, 'html.parser')
        return soup.find_all("div", {"class": "sectionLayout--insetColumn"})

    def medium_post_response(self):
        return get(self.post_url, stream=True)
