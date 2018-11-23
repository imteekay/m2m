import os

from bs4 import BeautifulSoup
from dotenv import load_dotenv
from medium_to_markdown import MediumToMarkdown
from requests import get

domain_name = "https://medium.freecodecamp.org/"
post_slug = "an-introduction-to-the-basic-principles-of-functional-programming-a2c2a15c84"
post_url = domain_name + post_slug

m2m = MediumToMarkdown(post_url)
m2m.transform()
