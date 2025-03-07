---
title: >-
    MyPackage: A Very Cool Python Application
authors:
  - name: Jane Doe
    affiliation: 1
    orcid: 0000-0000-0000-0001
    email: jane@doe.com
    corresponding: true
  - name: John L. Doe
    orcid: 0000-0000-0000-0001
    affiliation: [ 1, 2 ]
    equal-contrib: true
  - name: John Smith
    orcid: 0000-0000-0000-0001
    affiliation: [ 2, 3 ]
    equal-contrib: true
  - given-names: Ludwig
    dropping-particle: van
    surname: Beethoven
    suffix: Jr
    affiliation: 3
    email: email@example.com
    orcid: 0000-0000-0000-0001
    corresponding: true
  - given-names: Ludwig
    non-dropping-particle: van
    surname: Beethoven
    suffix: Jr
    affiliation: 3
    email: email1@example.com
    orcid: 0000-0000-0000-0001
  - name: Ludwig Beethoven
    given-names: Ludwig
    non-dropping-particle: van
    surname: Beethoven
    suffix: Jr
    affiliation: 3
    email: email2@example.com
    orcid: 0000-0000-0000-0001
affiliations:
  - index: 1
    name: Independent Researcher, Country
  - index: 2
    name: Institution Name, Country
  - index: 3
    name: Lyman Spitzer, Jr. Fellow, Princeton University, United States
    ror: 00hx57361
tags:
  - first keyword
  - second keyword
  - third keyword
software_repository_url: https://github.com/repodynamics/pypackit
archive_doi: 10.5281/zenodo.12345678
date: 11 November 2024
bibliography: ../paper.bib
---

# Summary

Begin your paper with a summary of the high-level functionality
of your software for a non-specialist reader.
Avoid jargon in this section.

JOSS welcomes submissions from broadly diverse research areas.
For this reason, we require that authors include in the paper some sentences
that explain the software functionality and domain of use to a non-specialist reader.
We also require that authors explain the research applications of the software.
The paper should be between 250-1000 words.
Authors submitting papers significantly longer than 1000 words
may be asked to reduce the length of their paper.

JOSS papers are only expected to contain a limited set of metadata,
a Statement of need, Summary, Acknowledgements, and References sections.
Given this format, a “full length” paper is not permitted,
and software documentation such as API (Application Programming Interface) functionality
should not be in the paper and instead should be outlined in the software documentation.

# Statement of Need

A Statement of need section that clearly illustrates the research purpose
of the software and places it in the context of related work.

# Other Sections

Other than a **Summary** and a **Statement of Need** section,
your paper can also contain other main sections and sub-sections.

## Citations

Citations can be used like this [@michaud-agrawal2011mdanalysis] [@oliver_beckstein-proc-scipy-2016] [@alibay2023building],
or this [@pedregosa2011scikitlearn], or this @pedregosa2011scikitlearn.

## Math Equations

For inline math, use single dollars `$`; for example $f(x) = e^{\pi/x}$.

For block math, use \LaTeX:

\begin{equation}
\label{eq:fourier}
\hat f(\omega) = \int_{-\infty}^{\infty} f(x) e^{i\omega x} dx
\end{equation}

Math blocks can be referenced like this \autoref{eq:fourier} or this \ref{eq:fourier}.

## Markdown

Links can be used like [this](https://example.com).

For long dashes---like this one---use three hyphens.

### Inline Markup

Inline markup in Markdown should be semantic, not presentations.
It can be used to make *italic*, **bold**, ~~strikethrough~~, ~sub~script, ^super^script,
[underline]{.ul}, [Small Caps]{.sc}, and `inline code`.

### Lists

- apples
- citrus fruits
  - lemons
  - oranges

### Ordered Lists

0. If two systems are each in thermal equilibrium with a third, they are
   also in thermal equilibrium with each other.
1. In a process without transfer of matter, the change in internal
   energy, $\Delta U$, of a thermodynamic system is equal to the energy
   gained as heat, $Q$, less the thermodynamic work, $W$, done by the
   system on its surroundings. $$\Delta U = Q - W$$


### Tables

Read the [pandoc manual](https://pandoc.org/MANUAL.html#tables) for more details.

Tables can be given captions like this:

: This is the caption of the table;
  it must start with a colon and be separated from the table by one empty line.\label{tab:example}

| Header 1      | Header 2      |
|---------------|---------------|
| Row 1, Cell 1 | Row 1, Cell 2 |
| Row 2, Cell 1 | Row 2, Cell 2 |

and referenced from text using \autoref{tab:example} or \ref{tab:example}.

### Inline Images

Inline images can be used like this ![](../full_light.png){height="9pt"} inside a paragraph.

### Figures

Figures can be included like this:

![This is the caption of the figure.\label{fig:example}](../full_light.png){ width=50% }

and referenced from text using \autoref{fig:example} or \ref{fig:example}.

### Code Blocks

Read the [pandoc manual](https://pandoc.org/MANUAL.html#verbatim-code-blocks) for more details.

```{.python .numberLines}
def f(x):
    return x
```


### Footnotes

Footnotes can be defined anywhere (see end of document) and referenced using [^first-footnote].


# Acknowledgements

# References

[^first-footnote]: This is a footnote.
