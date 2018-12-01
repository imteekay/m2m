from bs4 import BeautifulSoup
from requests import get
from tag_mapper import TagMapper

post_url = "https://medium.freecodecamp.org/learning-ruby-from-zero-to-hero-90ad4eecc82d"
post_content = get(post_url, stream=True).content
soup = BeautifulSoup(post_content, 'html.parser')
medium_post = soup.find_all("div", {"class": "sectionLayout--insetColumn"})
medium_post[0]

markdown_file = open("post.md", "w+")

for section in medium_post:
    new_section = [tag for tag in section if tag.name != 'div']
    for tag in section:
        markdown_tag = TagMapper(tag).to_markdown()
        markdown_file.write(markdown_tag)
        markdown_file.write("\n\n")

markdown_file.close()
