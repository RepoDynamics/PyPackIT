# Project License

{{ ccc.name }} greatly facilitates project licensing and copyright management,
in accordance with best practices for {term}`FOSS`
{cite}`QuickGuideToLicensing, BarelySufficientPracticesInSciComp, ELIXIRSoftwareManagementPlan, SustainableResearchSoftwareHandOver, ShiningLight, 10RuleForSoftwareInCompBio`,
including the upcoming [PEP 639](https://peps.python.org/pep-0639/). 
To do so, {{ ccc.name }} implements the System Package Data Exchange ([SPDX](https://spdx.org/)) license standard,
allowing users to define complex licenses for their projects
using a simple [SPDX license expression](https://spdx.github.io/spdx-spec/v3.0.1/annexes/spdx-license-expressions/).
{{ ccc.name }} supports all entries in the [SPDX License List](https://spdx.org/licenses/),
as well as custom license definitions.
It can process SPDX licenses in their
[native XML format](https://github.com/spdx/license-list-XML/blob/779bbe079ca2595e2d91fae30733f5b40eaf60e1/DOCS/xml-fields.md),
to automatically replace placeholder texts with project-specific information
and produce customized and visually appealing license files in Markdown format,
that are valid under the SPDX License List
[matching guidelines](https://spdx.github.io/spdx-spec/v3.0.1/annexes/license-matching-guidelines-and-templates/).





The specified license is automatically integrated throughout the project:

- Licence and copyright notices are customized with project information 
  like name, owner, and start date.
- A license file is added to the repository, where GitHub can recognize and display it.
- The license file is incorporated in all package releases.
- License identifiers are added to the package metadata.
- Full license and copyright information are featured on the documentation website.
- A full copyright notice is included in library source files.
- A short copyright notice is added to the footer of all README files.


An SPDX [short-form identifier](https://spdx.dev/learn/handling-license-info/)
is added to all source files, communicating license information in a standard human and machine-readable manner.


that support the commercialization of scientific software \cite{SettingUpShop} 
and fulfil the Bayh–Dole requirements for patenting publicly funded products {cite}`BayhDole`. 

For a shortlist of recommended licenses, see https://choosealicense.com/appendix/

In the control center, users can select a license either from the included options, 
or by inputting details for any other license. 

By default, the [GNU Affero General Public License v3.0](https://www.gnu.org/licenses/agpl-3.0) 
is selected for new projects, which is an [OSI-approved](https://opensource.org/licenses),
[FSF Free](https://www.gnu.org/licenses/license-list.en.html),
strong copyleft license promoting open science
by enforcing downstream source disclosure.


Other available options include \href{https://spdx.org/licenses/MIT.html}{MIT}, 
\href{https://spdx.org/licenses/BSL-1.0.html}{BSL}, 
and various other \href{https://www.gnu.org/licenses/licenses.html}{GNU licenses}. 

