# coding: utf8
from bs4 import BeautifulSoup
from requests import get
from tag_mapper import TagMapper


class MediumToMarkdown:
    def __init__(self, post_url):
        self.post_url = post_url

    def transform(self):
        responses, url = self.medium_post()
        fname = '-'.join(url.split('/')[-1].split('-')[:-1])

        markdown_file = open(f"{fname}.md", "w+", encoding="utf8")
        for section in responses:
            for tag in section:
                # skip author infomation
                if tag.name == 'div' and 'uiScale-caption--regular' in tag["class"]:
                    continue
                markdown_tag = TagMapper(tag).to_markdown()
                if markdown_tag:
                    markdown_file.write(markdown_tag)
                markdown_file.write("\n\n")

        markdown_file.close()

    def medium_post(self):
        responses = self.medium_post_response()
        post_content = responses.content
        soup = BeautifulSoup(post_content, 'html.parser')
        return soup.find_all("div", {"class": "sectionLayout--insetColumn"}), responses.url

    def medium_post_response(self):
        return get(self.post_url, stream=True)
