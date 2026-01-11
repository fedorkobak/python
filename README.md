# Python

This is a part of personal knowledge base related to the python programming language. Check more details on project on the [main site](https://fedorkobak.github.io/knowledge/intro.html).

Build site with command:

```bash
pip3 install jupyter-book
jb build .
```

Commit to `gh-pages` branch using:

```bash
pip3 install gph-import
ghp-import -n _build/html
```

Some notebooks use special tools to avoid boilerplate code. Add these tools to your environment with `pip install -e .`.
