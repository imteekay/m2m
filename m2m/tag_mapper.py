from functools import reduce
from gist_to_codeblock import GistToCodeblock
from urllib.parse import unquote


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

    def parse_text(self, result_text, current_text):
        if current_text.name == "code":
            return f"{result_text}`{current_text.text}`"
        elif current_text.name == "a":
            anchor_url = unquote(current_text['href']
                                 .replace("https://medium.com/r/?url=", ""))
            return f"{result_text}[{current_text.text}]({anchor_url})"
        elif current_text.name == "strong":
            return f"{result_text}**{current_text.text.strip()}**"
        elif current_text.name == "em":
            return result_text + current_text.text
        else:
            return result_text + current_text

    def markdown_paragraph(self):
        return reduce(lambda result_text, current_text: self.parse_text(result_text, current_text), self.tag, "")

    def markdown_image(self):
        if self.tag.img:
            return f"![]({self.tag.img['src']})"
        elif self.tag.iframe:
            return GistToCodeblock(self.tag).transform()

    def markdown_blockquote(self):
        return f"> {self.tag.text}"

    def markdown_unordered_list(self):
        unordered_lists = self.tag.find_all("li")
        lists_texts = [
            f"* {reduce(lambda result_text, current_text: self.parse_text(result_text, current_text), li, '')}" for li in unordered_lists]
        return "\n\n".join(lists_texts)

    def markdown_ordered_list(self):
        ordered_lists = self.tag.find_all("ol")
        lists_texts = [f"1. {li.text}" for li in ordered_lists]
        return "\n\n".join(lists_texts)
