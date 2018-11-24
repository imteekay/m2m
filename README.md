# M2M or Medium to Markdown

A project to transform a Medium post into a Markdown file

## Environment Variables

This project uses 2 environment variables: `GITHUB_USERNAME` and `GITHUB_PASSWORD`. They are used in the `GistToCodeblock` class to authenticate user in the [Github API](https://developer.github.com/v3/gists/).

Copy the `.sample-env` and update the variables with your Github username and password

```bash
cp .sample-env .env
```

## Requirements

Run this command to install all required libraries
```bash
pip install -r dev-requirements.txt
```

- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/): Easily parse HTML
- [Python DotEnv](https://github.com/theskumar/python-dotenv): Store environment variables
- [Requests](https://github.com/requests/requests): Access public APIs & HTML pages
