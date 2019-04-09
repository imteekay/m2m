# coding: utf8
import os
import sys
import re
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from medium_to_markdown import MediumToMarkdown
from requests import get


def transform_md(url):
    if re.match(r'^https?:/{2}\w.+$', url):
        m2m = MediumToMarkdown(url)
        m2m.transform()
        return True
    return False


input_params = sys.argv[1] if len(sys.argv) > 1 else "http://bit.ly/2FG5GgT"

if transform_md(input_params):
    print(f'Url: {input_params} has completed!')
elif os.path.isfile(input_params):
    with open(input_params, "r", encoding="utf8") as f:
        post_urls = f.readlines()
    for post_url in post_urls:
        if transform_md(post_url):
            print(f'Url: {post_url} has completed!')
        else:
            print(f"This is not a legal url: {post_url}")
