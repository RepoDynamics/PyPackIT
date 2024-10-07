---
ccid: intro
---

# Introduction





Computational Science and Engineering (CSE) \cite{CSE, CSE2} is a rapidly growing discipline 
that uses numerical algorithms and simulations for scientific inquiry, 
offering insights unattainable through theory and physical experimentation \cite{Bramley2000, EssenceOfCompSci, PillarsOfScience}. 
Software plays a critical role in CSE \cite{RolesOfCodeInCSE}, 
serving as the primary tool for performing simulations, data analysis, 
and other scientific computing tasks \cite{DevelopingSciSoft}. 
Thus, as CSE becomes an integral part of diverse scientific fields \cite{ResearchAndEdInCSE}, 
publications increasingly involve the development and use of 
research software—scientific software produced as research outputs \cite{NamingThePainInDevSciSoft, UKResearchSoftwareSurvey2014, HowScientistsDevAndUseSciSoft, HowScientistsReallyUseComputers, HowScientistsDevSciSoftExternalRepl}. 
Inevitably, the replicability, validity, and extensibility of these computational studies 
strongly rely on the availability and quality of the underlying research software \cite{CompSciDemandsNewParagdim}. 


Research software development is a complex and resource-intensive task, 
often faced with challenges regarding funding, time, staffing, and technical expertise \cite{SurveySEPracticesInScience2, HowToSupportOpenSource, ManagingChaos, BetterSoftwareBetterResearch, SoftDevEnvForSciSoft}. 
Requiring extensive domain knowledge, delegating it to software engineers is a challenging task \cite{SomeChallengesFacingSoftEngsDevSoftForSci, DevelopingSciSoft, ChallengesFacingSoftEngInSci, WhenEngineersMetScientists}. 
Research software is thus commonly produced by scientists \cite{NamingThePainInDevSciSoft, BetterSoftwareBetterResearch, SoftEngForCompSci, HowScientistsDevAndUseSciSoft} 
who are self-taught developers \cite{HowScientistsDevAndUseSciSoft, SurveySEPracticesInScience2, HowScientistsReallyUseComputers}. 
However, the growing intricacy of scientific computing and software engineering 
has created a chasm between the two practices \cite{SoftwareChasm, HowScientistsDevAndUseSciSoft, SciCompGridlock, SoftEngForCompSci}, 
leaving scientists with little exposure to modern software engineering methodologies 
that can greatly simplify and improve the development process \cite{BestPracticesForSciComp, CompSciError, WheresTheRealBottleneck, SelfPerceptions}. 
Additionally, in contrast to the software industry where each task is carried out by specialized teams, 
the entire responsibility of research software development is typically borne 
by a small group of novice developers \cite{SoftEngForCompSci, AnalyzingGitHubRepoOfPapers, 10RuleForSoftwareInCompBio, HowScientistsReallyUseComputers} 
who have to spend the majority of their time on the scientific aspects of their projects \cite{SurveySEPracticesInScience2, HowScientistsDevSciSoftExternalRepl}. 
Therefore, the amount of effort and skills required to produce high-quality research software 
in accordance with engineering best practices often far exceeds the capabilities of their developers \cite{SoftEngForCompSci, CompSciError, AdoptingSoftEngConceptsInSciResearch, BridgingTheChasm, SurveySEPracticesInScience, SurveySEPracticesInScience2, HowScientistsDevAndUseSciSoft, UnderstandingHPCCommunity, ProblemsOfEndUserDevs, ManagingChaos}. 
This results in research software lacking in terms of accessibility, ease of installation and use, 
documentation, interoperability, extensibility, maintainability, and correctness, among others \cite{BetterSoftwareBetterResearch, ProblemsOfEndUserDevs, SoftEngForCompSci, SciSoftwareAccuracy}. 
Enabled by unrewarding cultural values \cite{SurveySEPracticesInScience2, BetterSoftwareBetterResearch, RecommendOnResearchSoftware, SoftEngForCompSci, DealingWithRiskInSciSoft, ManagingChaos, ProblemsOfEndUserDevs} 
and a lack of publication standards \cite{TowardReproducibleCompResearch, ReprodResearchInCompSci, RecommendOnResearchSoftware, CaseForOpenCompProg}, 
such issues led to the so-called research software crisis, 
negatively impacting the scientific progress in CSE \cite{TroublingTrendsInSciSoftware, SoftEngForCompSci, BridgingTheChasm, ReprodResearchInCompSci, ReproducibleResearchForSciComp, AccessibleReproducibleResearch, SciSoftwareAccuracy, SciSoftwareExtensibility, CompSciError, ExtensibilityAndLibrarization, HowToSupportOpenSource, ShiningLight, TExperiments, WhyJohnnyCantBuild, ImprovingScienceThatUsesCode}. 
Acknowledging the importance and challenges of research software development, 
efforts have been made to improve the status quo. 
These include the introduction of research software engineering as a new academic role \cite{RSEIntro, RSEReportUK, RSEHistory, WhyScienceNeedsMoreRSE, SoftwareSustainabilityInstitute}, 
and the establishment of various guidelines \cite{FAIR4RS, 4SimpleRecs, 10MetricsForSciSoftware, BestPracticesForSciComp, RecommendOnResearchSoftware, ELIXIRSoftwareManagementPlan, NLeScienceSoftDevGuide, BestPracticesInBioinfSoftware, 10RuleForSoftwareInCompBio, SustainableResearchSoftwareHandOver, QuickGuideToOrgCompBioProjects, EnhancingReproducibility, SciSoftDevIsNotOxymoron, 5RecommendedPracticesForCompSci, 10SimpleRulesOnWritingCleanAndReliableSciSoft, BarelySufficientPracticesInSciComp} 
and workshops \cite{SoftwareCarpentryOriginal, SoftwareCarpentry, SoftEngForSci} 
to promote software engineering best practices among scientists. 
However, widespread adoption of such initiatives is often hindered by increased production costs \cite{RSEPillars, RSEinUnis, HowToSupportOpenSource, SoftDevEnvForSciSoft, NamingThePainInDevSciSoft}. 
For example, employing engineering best practices often fails due to a lack of supporting tools, 
which places an additional implementation burden on scientists \cite{ConfigManageForLargescaleSciComp}. 
Therefore, an ideal solution must be readily accessible and adoptable by all scientists, 
enabling them to immediately employ research software engineering best practices with minimal overhead \cite{ManagingChaos, SoftEngForCompSci}.


Software engineering involves multiple phases 
including planning, development, and operations, 
requiring a well-coordinated workflow that depends on 
various tools and technologies \cite{CollabSoftEngBookConcepts, StateOfArtInEndUserSoftEng}. 
By far, the most common problems faced by research software developers are technical issues 
regarding management, tooling, testing, documentation, deployment, and maintenance of software \cite{NamingThePainInDevSciSoft}. 
Thus, automation tools that streamline such repetitive engineering tasks 
according to research software needs can significantly accelerate development, 
improve quality, and lower production costs at the same time \cite{SoftEngForCompSci, BestPracticesForSciComp, AdoptingSoftEngConceptsInSciResearch}. 
An example proven successful in large-scale scientific initiatives \cite{TrilinosProject} 
are project skeletons \cite{Bertha, MolSSITemplate, SSCTemplate} 
that provide basic infrastructure for research software development \cite{ProjectSkeletonsReview}. 
While these are great automation tools for project initiation, 
the bulk of repetitive engineering activities is carried out 
throughout the development process \cite{CollabSoftEngBookConcepts, StateOfArtInEndUserSoftEng} 
with increasing complexity and frequency \cite{ConfigManageForLargescaleSciComp}. 
Although other general-purpose tools exist that can help with streamlining such individual tasks in isolation, 
to the best of our knowledge, there is currently no freely available comprehensive solution, 
particularly for research software. 

To fill the current gap, in this work we leveraged our prior experience in research software \cite{TeachOpenCADD} 
to develop PyPackIT, an open-source, ready-to-use, cloud-based automation tool to streamline 
the entire research software development process, from initiation to publication and support, 
according to the latest guidelines and engineering best practices. 
The rest of this section outlines PyPackIT's main motivations and aims, 
highlighting the most challenging aspects of research software engineering that are addressed by our solution. 

\hyperref[section-overview]{Section 2} provides a high-level overview of PyPackIT's key features 
and capabilities, while \hyperref[section-summary]{Section 3} summarizes our work. 
Additionally, detailed user manuals and technical information are available on PyPackIT's online documentation website at \url{https://repodynamics.github.io/PyPackIT}.
















Managing your repository's settings, branches, labels, issues, and pull requests;
  dynamically generating and updating all necessary configuration files;
  linting, formatting, and testing your code on the cloud;
  versioning, building, and publishing your package on PyPI;
  creating GitHub releases with detailed release notes and changelogs;
  and generating and deploying a complete documentation website on GitHub Pages,
  are just a few examples of how ${{ name }} automates your entire software development process.








PyPackIT is an open-source, ready-to-use, cloud-based automation tool
that streamlines the initiation, configuration, development, publication,
maintenance, management, and support of FAIR scientific software projects
in line with the latest research software engineering best practices. 
To facilitate interoperability, reusability, and adoption, 
PyPackIT is specialized in the production of software libraries in Python, 
the leading programming language for scientific applications. 
Promoting accessibility and collaboration, it supports open-source development on GitHub, 
one of the most popular and suitable social coding platforms for research software. 
PyPackIT is readily installable in both new and existing GitHub repositories, 
providing them with a comprehensive and robust project infrastructure, including:


After installation, PyPackIT automatically activates in response to various repository events, 
executing appropriate tasks on the GitHub Actions cloud computing platform. 
It thus establishes an automated software development workflow tailored to research software needs, 
based on a well-tested pull-based model for collaborative research software engineering. 
PyPackIT's workflow accelerates progress and innovation by promoting community engagement and feedback, 
while ensuring project continuation and sustainability by emphasizing proper task management, 
software inspection, and documentation. 
It includes comprehensive Continuous software engineering pipelines 
that use the latest tools and technologies to provide an automated Agile software development process, 
enabling the experimental and highly iterative development of research software, 
while reducing variance, complexity, cost, and risk. 
PyPackIT's workflow automates the bulk of repetitive engineering and management activities 
throughout the software life-cycle, including:


Therefore, PyPackIT's comprehensive, dynamic, and highly customizable project skeleton 
and cloud-native development environment eliminate the need for project setup and configuration, 
enabling scientific Python projects to immediately begin the actual implementation of software, 
even directly from the web browser. 
PyPackIT's automated development workflow greatly simplifies the research software development process, 
limiting manual tasks to writing issue tickets, scientific code, test cases, and minimal documentation, 
while other activities are automatically carried out on the cloud, 
consistently enforcing best practices throughout the software development life-cycle. 
Since these repetitive software engineering and management activities are 
the most common cause of problems in scientific software projects, 
their automation significantly improves product quality, 
while allowing developers to solely focus on the scientific aspects of their project. 
PyPackIT thus greatly benefits research software engineering 
that is often faced with challenges regarding funding, time, and staffing, 
by accelerating development and enabling the consistent and reliable production of high-quality software 
with minimal cost and effort. 
As the scientific inquiry process increasingly relies on research software, 
PyPackIT can be a valuable asset to computational studies 
that are now an integral part of many scientific fields. 






































Serving as a starting point for new users,
this section provides an introduction to
{{ccc.name}}, its motivations, objectives, and capabilities,
along with a summary of related fundamental concepts and useful background information.
If this is your first time using {{ccc.name}},
we highly recommend that you at least read through the [overview](overview/index.md) page,
before proceeding to the [user manual](../manual/index.md).


::::{grid} 1 1 2 2
:gutter: 3

:::{grid-item-card} Outline
:link: outline/index
:link-type: doc
:class-title: sd-text-center

An abstract of the {{ccc.name}} project,
outlining its motivations, purpose, and objectives,
along with a short summary of its capabilities and functionalities.
:::

:::{grid-item-card} Background
:link: background/index
:link-type: doc
:class-title: sd-text-center

A background review of the state of the art in the software development process
within the Python ecosystem, and its current challenges and problems.
:::

:::{grid-item-card} Overview
:link: overview/index
:link-type: doc
:class-title: sd-text-center

An in-depth high-level overview of {{ccc.name}} and all its functionalities,
the problems they address, and the value they bring to your project.
:::

:::{grid-item-card} Basics
:link: basics/index
:link-type: doc
:class-title: sd-text-center

A summary of basic concepts and related background information,
essential to fully understanding and utilizing {{ccc.name}}.
:::

::::

```{bibliography}
```