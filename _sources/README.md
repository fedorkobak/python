# python

Contains materials related to the Python programming language. There is github pages site based on this repo - check [it out](https://fedorkobak.github.io/python/intro.html).

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