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

        if gist_file['language']:
            return f"```{gist_file['language'].lower()}\n{code}\n```"
        else:
            return f"```\n{code}\n```"

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
