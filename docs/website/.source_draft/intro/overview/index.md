# Background

PyPackIT leverages GHA and GitHub’s other rich functionalities 
to provide a comprehensive environment for collaborative cloud development of research software, 
implementing specialized workflows and Actions to streamline repetitive engineering 
and management tasks throughout the software life cycle.

%CCA: PyPackIT implements a similar system, providing a user-friendly control center 
for defining, customizing, synchronizing, and maintaining project metadata, 
making project management and configuration more efficient and automated.

%version control: PyPackIT addresses these needs by automating version control tasks 
with a specialized branching model and version scheme.

PyPackIT addresses these challenges by offering a comprehensive set of 
ready-to-use CI/CD pipelines on GHA, designed according to best practices 
to streamline the integration and deployment of research software 
through an Agile development process 
\cite{HighwaysToCD, OopsAnalysisOfTravisCI, ProblemsCausesSolutionsCD, CDSoftIntensive, OnRapidRelease, UnderstandingSimilAndDiffinSoftDev}.

To prevent these issues, quality assurance and maintenance tasks 
should be automated and enforced from the beginning of the project \cite{SoftEngForCompSci}. 
PyPackIT achieves this by implementing Continuous Maintenance (CM) \cite{ContinuousMaintenance}, 
Refactoring (CR) \cite{ContRefact}, and Testing (CT) \cite{ContinuousSoftEng} pipelines 
that periodically perform various automated tasks, 
such as updating dependencies and development tools, 
to continuously maintain the health of the software and its development environment.
PyPackIT mitigates maintenance challenges by implementing automated 
Continuous Maintenance (CM), Refactoring (CR), and Testing (CT) pipelines 
from the project's inception to ensure software and environment health
\cite{SoftEngForCompSci, ContinuousMaintenance, ContRefact, ContinuousSoftEng}.

To address these issues, PyPackIT emphasizes providing infrastructure and automated solutions 
for maintaining high-quality documentation with minimal effort.

PyPackIT offers fully designed issue forms based on best practices 
and uses their inputs to automate challenging activities like 
ticket labeling and organization, task assignment, documentation, 
and creating issue–commit links 
\cite{WhatMakesAGoodBugReport, NeedsInBugReports, QualityOfBugReportsInEclipse}, 
thus providing an automated pull-based development workflow.

PyPackIT leverages these forms to automate ticket labeling, 
task assignment, and documentation, 
thus, creating an automated and efficient pull-based workflow 
\cite{WhatMakesAGoodBugReport, QualityOfBugReportsInEclipse}.

PyPackIT addresses these needs by offering an automated quality assurance 
and testing infrastructure for the entire development life-cycle, 
including coverage monitoring and test-suite distribution.


## FAIRness

FOSS is a valuable asset for technological innovations and scientific advancements, 
but often lacks Findability, Accessibility, Interoperability, and Reusability
{cite}`AccessibleReproducibleResearch, ShiningLight, CaseForOpenCompProg, SciSoftwareAccuracy, SurveySEPracticesInScience`—key
aspects of the FAIR principles {cite}`FAIR4RS`.
**Findability** requires that research software is searchable by its functionalities and attributes,
necessitating its permanent distribution to related public indexing repositories
along with comprehensive metadata and unique global identifiers like DOIs
{cite}`10MetricsForSciSoftware, SustainableResearchSoftwareHandOver, WhatMakesCompSoftSuccessful, 10SimpleRulesForOpenDevOfSciSoft, 4SimpleRecs, BarelySufficientPracticesInSciComp, ELIXIRSoftwareManagementPlan`.
**Accessibility** involves adopting an open-source model
under a permissive license {cite}`BusinessOfOpenSource`—ideally
from the start {cite}`BetterSoftwareBetterResearch, PublishYourCode, POVHowOpenSciHelps`—to
enable transparent peer review, facilitate progress tracking,
and promote trust, adoption, and collaboration {cite}`SharingDetailedResData, CaseForOpenCompProg, 10SimpleRulesForOpenDevOfSciSoft`.
For **interoperability**, a key factor is using a well-suited
and popular programming language in the target community {cite}`RolesOfCodeInCSE, SoftDevEnvForSciSoft`.
Python is now the leading language for research software development
\cite{SurveySEPracticesInScience2, AnalyzingGitHubRepoOfPapers, DevOpsInSciSysDev},
recommended due to its simplicity, versatility,
and ability to quickly implement complex tasks that are hard to address
in low-level languages \cite{PythonBatteriesIncluded, PythonForSciComp, PythonForSciAndEng, PythonJupyterEcosystem, SciCompWithPythonOnHPC, PythonEcosystemSciComp, WhatMakesPythonFirstChoice}.
Python's extensive ecosystem offers performance-optimized libraries 
for various scientific applications \cite{NumPy, SciPy, pandas, PyTorch, Top5MLLibPython, ScikitLearn, scikitImage, Matplotlib, Mayavi, IPython, Jupyter, Jupyter2, DaskAndNumba, DaskApplications, Cython, Numba, Pythran, PyCUDA, Astropy, SunPy, Pangeo, MDAnalysis, Biopython, NIPY},
with features for parallel distributed computing \cite{SciCompWithPythonOnHPC, ParallelDistCompUsingPython, ScientistsGuideToCloudComputing, DemystPythonPackageWithCondaEnvMod, PythonAcceleratorsForHPC, DistWorkflowsWithJupyter, InteractiveSupercomputingWithJupyter} 
that even allows high-performance computing communities 
such as CERN \cite{IntroducingPythonAtCERN, PythonAtCERN} and NASA \cite{PythonAtNASA} 
to use it for key scientific achievements \cite{PythonScientificSuccessStories, GravWaveDiscovery, BlackHoleImage}. 
Lastly, **reusability** is enabled by employing DRY (Don't Repeat Yourself) principles 
and modularizing code into applications with clear programming 
and user interfaces {cite}`FAIR4RS, 5RecommendedPracticesForCompSci, BestPracticesForSciComp, RolesOfCodeInCSE`. 
Applications must then be packaged into as many distribution formats as possible, 
to ensure compatibility with different hardware and software environments. 
This can also greatly simplify the setup process for users 
{cite}`10RuleForSoftwareInCompBio, ELIXIRSoftwareManagementPlan, WhyJohnnyCantBuild`, 
which is a common problem in research software {cite}`NamingThePainInDevSciSoft, CompSciError`. 

Despite its importance, research software is infrequently published \cite{AnalyzingGitHubRepoOfPapers, BridgingTheChasm, PublishYourCode, CompSciError}, 
leading to controversies and retractions \cite{InfluentialPandemicSimulation, RetractionCOVID}, 
and forcing the reimplementation of computational workflows from scratch \cite{ProblemsOfEndUserDevs, BetterSoftwareBetterResearch, SurveySEPracticesInScience2, SoftEngForCompSci}. 
Thus, there is a growing call for an open research culture 
to enhance transparency and reproducibility \cite{PromotingOpenResearch, ReprodResearchInCompSci, EnhancingReproducibility, TroublingTrendsInSciSoftware}, 
and many journals now mandate source code submissions 
for peer-review and public access \cite{RealSoftwareCrisis, DoesYourCodeStandUp, TowardReproducibleCompResearch, MakingDataMaximallyAvailable, JournalOfBioStatPolicy}.

## FAIR Research Software

Despite this, research software has been rarely published
\cite{BridgingTheChasm, CaseForOpenCompProg, 4SimpleRecs, PublishYourCode, CompSciError}, 
leading to controversies \cite{InfluentialPandemicSimulation} and retractions \cite{RetractionCOVID}, 
preventing software reuse \cite{SurveySEPracticesInScience, SciSoftwareAccuracy}, 
and forcing scientists to re-implement computational workflows from scratch in each new project \cite{ProblemsOfEndUserDevs, BetterSoftwareBetterResearch}, 
which is an error-prone process yielding low-quality results \cite{SurveySEPracticesInScience2, SoftEngForCompSci}. 
In response, widespread appeals have emerged for an open research culture,
promoting transparency and reproducibility \cite{PublishYourCode, PromotingOpenResearch, ReprodResearchInCompSci, CaseForOpenCompProg, EnhancingReproducibility, ShiningLight, TroublingTrendsInSciSoftware}. 
While more publications now include links to source code and data, 
this is still strongly biased toward a handful of institutions 
working in specific computer science fields \cite{AnalyzingGitHubRepoOfPapers}. 
Common obstacles to publishing research software include 
the lack of efficient mechanisms and tools for packaging, 
distribution, and indexing \cite{CaseForOpenCompProg, SurveySEPracticesInScience, ReprodResearchInCompSci}, 
as well as code quality concerns and technical challenges to refactor, document, 
and maintain the software \cite{BarelySufficientPracticesInSciComp, BetterSoftwareBetterResearch, PublishYourCode}. 
To sustain scientific progress in CSE, it is thus crucial to address these challenges 
and ensure that research software is FAIR \cite{FAIR4RS}: findable, accessible, interoperable, and reusable.

 
For reproducibility of research results, each distribution must be permanently available 
and uniquely indexed with a persistent global identifier that enables reliable citations, 
such as a Digital Object Identifier (DOI) \cite{BarelySufficientPracticesInSciComp, BestPracticesInBioinfSoftware, ELIXIRSoftwareManagementPlan, BestPracticesInBioinfSoftware, 4SimpleRecs}. 



Packaging code into software libraries can also greatly simplify 
the setup process for users \cite{10RuleForSoftwareInCompBio, ELIXIRSoftwareManagementPlan, WhyJohnnyCantBuild}, 
which is a common problem in research software \cite{NamingThePainInDevSciSoft, CompSciError}. 

Therefore, PyPackIT is focused on the production of open-source and FAIR scientific Python libraries, 
and implements automated solutions to facilitate above-mentioned challenges, 
such as licensing, packaging, distribution, and indexing \cite{BarelySufficientPracticesInSciComp, ELIXIRSoftwareManagementPlan, SustainableResearchSoftwareHandOver, ShiningLight, 10RuleForSoftwareInCompBio}.

