# M2M or Medium to Markdown

A project to transform a Medium post into a Markdown file

## Environment Variables

This project uses 2 environment variables: `GITHUB_USERNAME` and `GITHUB_PASSWORD`. They are used in the `GistToCodeblock` class to authenticate user in the [Github API](https://developer.github.com/v3/gists/).

Copy the `.sample-env` and update the variables with your Github username and password

```bash
cp .sample-env .env
```

## Requirements

Create your virtual environment

```bash
virtualenv m2menv
```

Activate your virtualenv

```base
source m2menv/bin/activate
```

Run this command to install all required libraries

```bash
pip install -r requirements.txt
```

- [Python 3](https://docs.python.org/3/)
- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/): Easily parse HTML
- [Python DotEnv](https://github.com/theskumar/python-dotenv): Store environment variables
- [Requests](https://github.com/requests/requests): Access public APIs & HTML pages

## Usage

To do the Medium to Markdown transformation, call the `core.py` passing the post url

```bash
# Method One: single url
python m2m/core.py http://bit.ly/2FG5GgT

# Method Two: a lot of urls, a file like input_file.txt
python m2m/core.py input_file.txt
```

If you not pass the post url, the `core.py` will use the default post url.

**Note**

- The `output` md file is the title of the article.
- The `input_file.txt` is one url per line.