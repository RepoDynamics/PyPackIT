---
sd_hide_title: true
---
# Documentation
:::{toctree}
:hidden:

website
readme-files
health-files
:::


## Working on Documentation

To make the development process easier, you can install the
[sphinx-autobuild](https://github.com/executablebooks/sphinx-autobuild) extension.
It will generate a live preview of the built documentation website,
so that every change made to the source files is immediately applied to the preview,
without the need to manually rebuilding every time.

The option to use the extension is already [incorporated(https://github.com/executablebooks/sphinx-autobuild#using-with-makefile)]
into the Sphinx Makefile.
This means that all you have to do to use this extension is to first install it:

pip install sphinx-autobuild

and then in terminal in the sphinx folder, instead of `make html`, execute the command:

make livehtml
