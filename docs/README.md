# Building the Docs

The documentation in this tree is in plain text files and can be viewed using any text file viewer.

It uses ReST (reStructuredText), and the Sphinx documentation system. This allows it to be built into other forms for easier viewing and browsing.

To create an HTML version of the docs:

1) Install docs requirements: ``pip install -r docs/requirements-dev.txt``.
2) ``cd docs``
3) ``make html``
4) Open ``docs/_build/index.html`` in your browser.