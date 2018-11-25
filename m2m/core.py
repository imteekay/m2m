import os
import sys

from bs4 import BeautifulSoup
from dotenv import load_dotenv
from medium_to_markdown import MediumToMarkdown
from requests import get

post_url = sys.argv[1] if len(sys.argv) > 1 else "http://bit.ly/2FG5GgT"

m2m = MediumToMarkdown(post_url)
m2m.transform()
