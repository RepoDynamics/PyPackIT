# Citation

|{% if 'dois' not in ccc %}|

|{{ ccc.name }}| has currently no available citation data.
Please contact us if you need to cite |{{ ccc.name }}| in your work.

|{% else %}|

|{% set suffix = 's' if ccc.dois | length > 1 else '' %}|

Please cite |{{ ccc.name }}| in your work
using the following reference|{{ suffix }}|:

<ul id="project-citations-rendered">
    <!-- Rendered API responses will be displayed here -->
</ul>

<div>
  <select id="citation-style-dropdown" onchange="fetchAPI()" style="visibility: hidden;">
    <option value="" disabled selected>Select a citation style</option>
    <!-- Options will be dynamically loaded here -->
  </select>
</div>

Select a [citation style](https://github.com/citation-style-language/styles)
from the menu to reformat the reference|{{ suffix }}|.
You can then either [copy](#help-copy-button) the updated plain text above,
or the corresponding HTML code below.
Alternatively, select the BibTeX, RIS, or CiteProc JSON tabs
to copy the reference|{{ suffix }}| in the desired citation database file format.
The reference|{{ suffix }}| correspond|{{ 's' if ccc.dois | length < 2 else '' }}| to:

|{% for doi in ccc.dois -%}|
- |{{ doi.description }}|
|{% endfor %}|


:::::{tab-set}

::::{tab-item} HTML

<!--
Wrap in `<div><pre>` to add coppy button.
Ref: https://sphinx-copybutton.readthedocs.io/en/latest/use.html#add-or-remove-copy-buttons-to-any-element-with-a-css-selector
-->
<div class="highlight">
    <pre><div id="project-citations-html"><!-- API response will be displayed here --></div></pre>
</div>
::::


::::{tab-item} BibTeX

<div class="highlight">
    <pre><div id="project-citations-bib"><!-- API response will be displayed here --></div></pre>
</div>
::::


::::{tab-item} RIS

<div class="highlight">
    <pre><div id="project-citations-ris"><!-- API response will be displayed here --></div></pre>
</div>
::::


::::{tab-item} CiteProc JSON

<div class="highlight">
    <pre><div id="project-citations-citeproc"><!-- API response will be displayed here --></div></pre>
</div>
::::


:::::


|{% endif %}|
