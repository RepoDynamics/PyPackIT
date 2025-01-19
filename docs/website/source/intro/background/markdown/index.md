(bg-markdown)=
# Markdown

Markdown is a lightweight markup language 
designed to simplify formatting for web-based documents. 
Created by **John Gruber** in 2004, 
Markdown aims to make writing for the web 
as easy as writing plain text 
while ensuring that the content 
is easily convertible to structured HTML. 
Its intuitive syntax allows users 
to create headings, lists, links, images, 
and other elements with minimal effort. 
Markdown has since evolved into a cornerstone 
for documentation, content management systems, 
and collaborative platforms.

Markdown has become a standard across various platforms 
for creating and managing content. 
Blogging platforms like **Ghost** and **Hugo**, 
note-taking apps like **Obsidian** and **Notion**, 
and collaborative tools like **Slack** and **Trello** 
all rely on Markdown or its variants for formatting. 
The adaptability of Markdown ensures 
that users can create structured content efficiently 
across different tools and environments.

As Markdown's popularity grew, 
various platforms and communities 
introduced their own extensions and variations, 
commonly referred to as **flavors** of Markdown. 
These flavors add functionality tailored to specific needs, 
from supporting task lists to enabling math expressions. 
This document explores Markdown's core features 
and the unique characteristics of its most notable flavors.


## Standard Markdown

[Standard Markdown](https://daringfireball.net/projects/markdown/syntax),
also known as Classic Markdown, 
is the original version introduced by John Gruber. 
Its simplicity is one of its key strengths, 
providing a small set of formatting options 
that cover common needs for creating web content. 
Standard Markdown includes:

- Headings (`# Heading 1`, `## Heading 2`, etc.)
- Bold (`**bold**`) and italic (`*italic*`) text
- Lists, including ordered (`1. Item`) and unordered (`- Item`)
- Links (`[text](url)`) and images (`![alt text](url)`)
- Blockquotes (`> Quote`)
- Code blocks (`\`\`\`code\`\`\``) and inline code (`\`code\``)

While Standard Markdown is sufficient for basic formatting, 
it lacks features for more advanced use cases, 
such as tables, task lists, or inline HTML rendering. 
This limitation paved the way for extended flavors of Markdown 
that address these needs.


## CommonMark

[CommonMark](https://commonmark.org/) is a standardized version of Markdown 
that addresses inconsistencies and ambiguities in the original syntax. 
Developed to create a consistent and well-defined specification, 
CommonMark ensures that Markdown documents render uniformly 
across different platforms and implementations.
CommonMark retains the simplicity of Standard Markdown 
while introducing a formal grammar for parsing and rendering content. 
This makes it a popular choice for platforms aiming 
to ensure compatibility and predictability in Markdown rendering.


(bg-gfmd)=
## GitHub-Flavored Markdown (GFM)

[GitHub-Flavored Markdown](https://github.github.com/gfm/) (GFM) 
is a strict superset of CommonMark designed specifically for 
[writing on GitHub]((https://docs.github.com/en/get-started/writing-on-github). 
It builds upon CommonMark by adding extensions to support
tables, task lists, autolinks, syntax highlighting for code blocks,
and other typography features.
GFM thus serves as a versatile tool for creating and managing technical documents 
across repositories, issues, pull requests, and discussions,
including [README files](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes),
[community health files](#bg-gh-health-files), and project wikis.
On the other hand, GFM also imposes additional restrictions on
raw HTML content allowed within Markdown documents,
[disallowing HTML elements](https://github.github.com/gfm/#disallowed-raw-html-extension-) 
such as `<title>`, `<iframe>`, `<style>`, and `<script>`.


## Pandoc Markdown

[Pandoc Markdown](https://pandoc.org/MANUAL.html#pandocs-markdown)
is the Markdown flavor supported by the [Pandoc](https://github.com/jgm/pandoc) document converter. 
It extends Standard Markdown with features for generating complex documents, 
such as inline LaTeX for mathematical equations,
metadata blocks for specifying document properties,
and customizable export formats like HTML, PDF, and DOCX.
Pandoc Markdown is flexible and can be further
extend with custom extensions. It serves as a bridge 
between Markdown and other markup languages, 
making it suitable for creating professional documents in multiple formats.


## MyST Markdown

[MyST (Markedly Structured Text) Markdown](https://mystmd.org/)
is an extended flavor of Markdown 
specifically designed for technical and scientific documentation. 
It combines the simplicity of Markdown 
with additional features inspired by reStructuredText (reST), 
making it compatible with tools like Sphinx.

MyST Markdown introduces directives and roles, 
which are powerful tools for creating rich content. 
Directives are block-level elements that add functionality, 
such as including code examples, inserting figures, 
or embedding external content. 
Roles, on the other hand, are inline elements used for cross-referencing, 
styling, or adding annotations. 

MyST Markdown also supports math rendering, 
allowing users to write LaTeX-style equations 
directly within Markdown files. 
This makes it an excellent choice for scientific and technical projects 
that require precise formatting and advanced features.


## Markdown in Sphinx

Sphinx, a documentation generator traditionally associated with reStructuredText, 
has adopted Markdown as a supported format through extensions 
like [MyST Parser](https://myst-parser.readthedocs.io/en/latest/). 
This integration enables users to write Sphinx-compatible documentation 
using Markdown instead of reST, 
making Sphinx more accessible to those already familiar with Markdown syntax.

Markdown in Sphinx allows users to benefit from Sphinx's advanced capabilities, 
such as cross-referencing, search functionality, and extensibility, 
without learning the more complex reST syntax. 
By using MyST Markdown, Sphinx projects can include rich directives, 
roles, and structured elements, ensuring compatibility 
with Sphinx features like table of contents, indexing, and PDF generation.

Sphinx projects using Markdown maintain the same modular and extensible structure, 
supporting multi-page documentation sites, technical manuals, and even API references. 
This combination of Markdown's simplicity and Sphinx's power 
makes it a popular choice for modern documentation workflows.
