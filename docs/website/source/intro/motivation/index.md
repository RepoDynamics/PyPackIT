(motivation)=
# Motivation

Free and Open Source Software (FOSS)
is a cornerstone of modern science and technology,
fueling innovation by granting users the freedom to access, 
enhance, and redistribute source code {cite}`FOSS, BriefHistoryOfFOSS`.
Its impact spans diverse fields—from computational sciences and engineering
to healthcare, education, and cybersecurity 
{cite}`RolesOfCodeInCSE, DevelopingSciSoft, UKResearchSoftwareSurvey2014, HowScientistsDevAndUseSciSoft, CompSciDemandsNewParagdim`.
FOSS promotes collaboration, security, and transparency 
while reducing costs and dependency on proprietary software.
This inclusive model not only supports economic efficiency,
but is also a vital element in shaping a more open and sustainable technological future.

In contrast to the software industry where each task is carried out by specialized teams,
the entire responsibility of FOSS development is typically in the hands of small groups of developers
{cite}`AnalyzingGitHubRepoOfPapers, HowScientistsReallyUseComputers, NamingThePainInDevSciSoft`
with little time and exposure to modern software engineering methodologies
{cite}`SoftwareChasm, SciCompGridlock, WheresTheRealBottleneck, SelfPerceptions, SurveySEPracticesInScience2, HowScientistsDevSciSoftExternalRepl`.
As software development is a complex and resource-intensive task {cite}`MythicalManMonth`,
FOSS is often faced with challenges regarding funding, time, staffing, and technical expertise 
{cite}`HowToSupportOpenSource, ManagingChaos, BetterSoftwareBetterResearch, SoftDevEnvForSciSoft`.
Therefore, the amount of effort and skills required to produce high-quality software
in accordance with the latest software engineering best practices 
often far exceeds the capabilities of FOSS development teams
{cite}`SoftEngForCompSci, AdoptingSoftEngConceptsInSciResearch, BridgingTheChasm, SurveySEPracticesInScience, HowScientistsDevAndUseSciSoft, UnderstandingHPCCommunity, ProblemsOfEndUserDevs`.
This can lead to FOSS lacking in areas like accessibility, ease of installation and use,
documentation, interoperability, extensibility, and maintainability,
significantly hampering scientific and technological advancements
{cite}`TroublingTrendsInSciSoftware, ReprodResearchInCompSci, ReproducibleResearchForSciComp, AccessibleReproducibleResearch, SciSoftwareExtensibility, CompSciError, SciSoftwareAccuracy, ExtensibilityAndLibrarization, ShiningLight, TExperiments, WhyJohnnyCantBuild, ImprovingScienceThatUsesCode`. 

Acknowledging the importance and challenges of FOSS development, 
efforts have been made to improve the status quo.
These include the introduction of research software engineering 
as a new academic discipline 
{cite}`RSEIntro, RSEReportUK, RSEHistory, WhyScienceNeedsMoreRSE, SoftwareSustainabilityInstitute`, 
and the establishment of various guidelines 
{cite}`FAIR4RS, 4SimpleRecs, 10MetricsForSciSoftware, BestPracticesForSciComp, RecommendOnResearchSoftware, ELIXIRSoftwareManagementPlan, NLeScienceSoftDevGuide, BestPracticesInBioinfSoftware, 10RuleForSoftwareInCompBio, SustainableResearchSoftwareHandOver, QuickGuideToOrgCompBioProjects, EnhancingReproducibility, SciSoftDevIsNotOxymoron, 5RecommendedPracticesForCompSci, 10SimpleRulesOnWritingCleanAndReliableSciSoft, BarelySufficientPracticesInSciComp, GoodEnoughPracticesInSciComp, TuringWay` 
and workshops 
{cite}`SoftwareCarpentryOriginal, SoftwareCarpentry, SoftEngForSci` 
to promote software engineering best practices among developers.
However, widespread adoption of such initiatives is often hindered by increased production costs
{cite}`RSEPillars, RSEinUnis, HowToSupportOpenSource, SoftDevEnvForSciSoft, NamingThePainInDevSciSoft`. 
For example, employing engineering best practices can be challenging 
due to a lack of supporting tools and limited time and knowledge {cite}`ConfigManageForLargescaleSciComp`. 
To improve this situation, we need solutions that are readily accessible and adoptable by all developers, 
empowering them to employ software engineering best practices
with ease and minimal overhead {cite}`ManagingChaos, SoftEngForCompSci`.

Software engineering involves multiple phases including planning, development, and operations, 
requiring a well-coordinated workflow using various tools and technologies
{cite}`CollabSoftEngBookConcepts, StateOfArtInEndUserSoftEng`.
By far, the most common problems faced by FOSS developers are technical issues regarding management,
tooling, testing, documentation, deployment, and maintenance of software 
{cite}`NamingThePainInDevSciSoft, ShiningLight, PublishYourCode, BetterSoftwareBetterResearch, SurveySEPracticesInScience, ReprodResearchInCompSci, CaseForOpenCompProg`.
Thus, automation tools that streamline such repetitive engineering tasks
can significantly accelerate development, improve quality, and lower production costs at the same time 
{cite}`SoftEngForCompSci, BestPracticesForSciComp, AdoptingSoftEngConceptsInSciResearch`.
An example proven successful in large-scale scientific initiatives {cite}`TrilinosProject`
are project skeletons that provide basic infrastructure for software development 
{cite}`ProjectSkeletonsReview, Bertha, MolSSITemplate, SSCTemplate`.
While these are great automation tools for project initiation, 
the bulk of repetitive engineering activities is carried out throughout the development process 
with increasing complexity and frequency 
{cite}`CollabSoftEngBookConcepts, StateOfArtInEndUserSoftEng, ConfigManageForLargescaleSciComp`.
Although existing general-purpose tools can help streamline individual tasks, 
comprehensive solutions to automate the entire software development process are lacking.

In the following, we outline key requirements and challenges
in FOSS development, highlighting |{{ ccc.name }}|'s solutions to them.


(motiv-cloud-auto)=
## Cloud-Native Automation

FOSS often faces evolving requirements and specifications so that 
determining the exact requirements and specifications of the end product 
is usually not possible in advance {cite}`SoftDevEnvForSciSoft, ProblemsOfEndUserDevs`.
Consequently, as [traditional development methodologies](#bg-traditional-methodologies)
may not effectively accommodate the experimental nature of FOSS development 
{cite}`DevelopingSciSoft, SoftEngForCompSci, DealingWithRiskInSciSoft`, 
[Agile development](#bg-agile) and [cloud-native practices](#bg-cloud-native) such as 
[Continuous software engineering](#bg-continuous) and [DevOps](#bg-devops) are recommended
to reduce variance, complexity, cost, and risk in the development process
and produce higher quality software more rapidly, efficiently, and reliably
{cite}`AdoptingSoftEngConceptsInSciResearch, LitRevAgileInSciSoftDev, BestPracticesForSciComp, WhenEngineersMetScientists, SoftDevEnvForSciSoft, SurveySEPracticesInScience`.

While Agile and cloud-native methodologies are considered crucial 
in collaborative software development
{cite}`EffectsOfCIOnSoftDev, CICDSystematicReview, AnalysisOfTrendsInProductivity`
and are well-established in industry
{cite}`EmpEvAgile, AgileAdoptionSurvey, Top10AdagesInCD, SynthCDPractices` 
and some large research institutions
{cite}`IntroducingAgileInBioInf, AgileInBioMedSoftDev, UsingAgileToDevCompBioSoft, ExploringXPForSciRes`, 
their adoption in FOSS projects presents opportunities for growth 
{cite}`SurveySEPracticesInScience2, ProblemsOfEndUserDevs, SelfPerceptions, AdoptingSoftEngConceptsInSciResearch, DevelopingSciSoft`. 
A major barrier to adoption is implementing Continuous pipelines, 
which is a complex task {cite}`StairwayToHeaven, ContSoftEngineeringBookStairway` 
faced with challenges such as lack of consensus on a single well-defined standard 
and limited availability of tools, technologies, instructions, and resources 
{cite}`ModelingCI, CICDSystematicReview, UncoveringBenefitsAndChallengesOfCI`.
For example, GitHub offers public repositories free integration with [GitHub Actions](#bg-gha) (GHA),
which can be used to for automation well beyond conventional CI/CD practices 
{cite}`DevPerceptionOfGHA, GitHubDevWorkflowAutoEcoBook`.
However, implementing GHA [workflows](#bg-gha-workflow) 
involves challenges related to tooling, configuration, 
testability, debugging, maintenance, and security
{cite}`HowDoSoftDevsUseGHA, EvolutionOfGHAWorkflows, OnOutdatednessOfWorkflowsInGHA, AutoSecurityAssessOfGHAWorkflows`.
[Action](#bg-gha-action) reuse is also low, due to issues with compatibility, 
functionality, and findability {cite}`DevPerceptionOfGHA`.
Consequently, most projects do not make use of these advanced features that can 
greatly improve the software development process {cite}`OnUseOfGHA, LetsSuperchargeWorkflows`.
As free and ready-to-use solutions are scarce
{cite}`CDHugeBenefits, CICDSystematicReview, HowDoSoftDevsUseGHA, DevPerceptionOfGHA, EffectsOfCIOnSoftDev`, 
many FOSS projects do not follow Continuous practices or use outdated pipelines 
that can compromise the development process or introduce security vulnerabilities into the project
{cite}`CITheater, OnOutdatednessOfWorkflowsInGHA, AutoSecurityAssessOfGHAWorkflows, AmbushFromAllSides`. 


:::{admonition} |{{ ccc.name }}|'s Solution
:class: tip

|{{ ccc.name }}| exploits the full potential of GHA
to enable a cloud-native Agile development process
by providing a comprehensive set of ready-to-use and
highly customizable automation pipelines for
[Continuous configuration automation](#overview-cc),
[Continuous integration](#overview-ci) and [deployment](#overview-cd), and 
[Continuous maintenance, refactoring, and testing](#overciew-cm),
designed according to the latest guidelines and engineering best practices
{cite}`HighwaysToCD, ExtremeProgExplained, OopsAnalysisOfTravisCI, ProblemsCausesSolutionsCD, CDSoftIntensive, OnRapidRelease, QualityAndProductivityCI, UsageCostsAndBenefitsOfCI, CIImprovingSoftQualBook, CIBlogPost, ModelingCI, UnderstandingSimilAndDiffinSoftDev, EffectsOfCIOnSoftDev, AgileSoftDevMethodAndPractices, ContinuousSoftEng, CICDSystematicReview`.
These pipelines fully integrate with various repository components
to automate numerous repetitive engineering and management tasks
throughout the entire software life cycle.
:::


(motiv-workflow)=
## Collaborative Workflow

Software development has become a highly collaborative and distributed process
{cite}`ScaleAndEvolOfCoordNeeds, GlobalSoftEng`.
The additional social aspects increase project complexity,
requiring high degrees of communication and coordination
{cite}`InfluenceOfSocialAndTechnicalFactors, UnderstandingCommunitySmells, CollabSoftEngBookChallenges, GlobalSoftDevChallenges`,
as well as a robust workflow to orchestrate the development process
{cite}`CollabSoftEngBookConcepts, StateOfArtInEndUserSoftEng`. 
Consequently, effective collaboration and project management 
are major challenges in FOSS development
{cite}`NamingThePainInDevSciSoft, ConfigManageForLargescaleSciComp`,
where lacking workflows result in using non-standard and error-prone development processes
{cite}`ProblemsOfEndUserDevs, DevelopingSciSoft, SurveySEPracticesInScience`.

Cloud-based social coding platforms (SCPs) address these challenges 
by providing essential software engineering tools in a transparent mutual environment 
{cite}`OpenSourceSoftHostingPlatforms, CharacterizingProjEvolOnSocialCodingPlat, SocialCodingInGitHub`, 
including distributed version control systems (VCSs) like 
[Git](https://git-scm.com/) {cite}`VCSReview`. 
GitHub, currently the largest SCP {cite}`GitHubOctoverse2023`, 
is especially recommended for FOSS projects 
{cite}`10RuleForSoftwareInCompBio, BestPracticesForSciComp, 10SimpleRulesGitAndGitHub` 
as it provides special features like software citation 
and free upgrades for academic use {cite}`GitHubForScience`.
A [GitHub repository](#bg-gh-repo) serves as much more 
than a code-hosting platform—it functions 
as the central hub for a project. 
It’s where contributors meet to discuss issues and ideas,
review work, and plan for future development.
Additionally, the repository acts as the project’s public face, 
allowing users to learn about the software, 
follow its progress, provide feedback, and contribute. 
A well-structured GitHub repository is crucial for a software project's success, 
directly impacting adoption, growth, and long-term sustainability.
However, setting up a robust repository is a non-trivial task
involving multiple steps such as configuration of various features
and customization with project metadata.

GitHub's [pull-based development model](#bg-pull-based) offers 
an effective solution for collaboration by enabling community contributions 
through issuing tickets and pull requests (PRs), 
while maintainers review and integrate changes. 
This accelerates development and enhances code quality through reviews, 
but also requires careful management
{cite}`CharacterizingProjEvolOnSocialCodingPlat, SciSoftDevIsNotOxymoron`.
For example, projects need a well-defined governance model
to facilitate task assignment
{cite}`4SimpleRecs, SustainableResearchSoftwareHandOver`.
Another crucial aspect is documenting the development process
to record a clear overview of the project evolution and
ensure that the implementation matches the expected design
{cite}`WhatMakesCompSoftSuccessful, 5RecommendedPracticesForCompSci, BestPracticesForSciComp, BestPracticesInBioinfSoftware, DealingWithRiskInSciSoft`.

Issue tracking systems (ITSs) like [GitHub Issues](#bg-ghi) (GHI) 
help document and organize tasks, 
but need significant setup to function effectively 
{cite}`SurveySEPracticesInScience, DLRSoftEngGuidelines, ELIXIRSoftwareManagementPlan, EmpAnalysisOfIssueTemplatesOnGitHub`. 
By default, GHI only offers a single option for opening unstructured issue tickets, 
which can lead to problems such as missing crucial information that complicate issue triage 
{cite}`EmpAnalysisOfIssueTemplatesOnGitHub`.
Another problem is maintaining links between issue tickets 
and the corresponding commits resolving the issues in the VCS,
which is important for tracing changes back to their associated tickets 
and accompanied documentation and discussion {cite}`ConfigManageForLargescaleSciComp`.
To facilitate issue management, GitHub offers labeling features 
to help categorize and prioritize tickets 
{cite}`GiLaGitHubLabelAnalyzer, ExploringCharacIssueRelatedGitHub`. 
However, labeling and issue–commit linkage tasks must be done manually, 
which is time-consuming and prone to errors 
{cite}`WhereIsTheRoadForIssueReports, GotIssues, ExploringTheUseOfLabels, FillingTheGapsOfDevLogs`,
resulting in the loss of a large portion of the project's evolution history {cite}`MissingLinksBugsAndBugFix`.
Such problems have even motivated the development of machine-learning tools
for automatic ticket classification
{cite}`PredictingIssueTypesOnGitHub, ImpactOfDataQualityForAutomaticIssueClassification`
and issue–commit link recovery {cite}`IssueCommitLink-DeepLink, FRLink`. 
In 2021 GitHub introduced
[issue forms](https://github.blog/changelog/2021-06-23-issues-forms-beta-for-public-repositories/),
allowing projects to provide multiple issue submission options
using structured web forms that enable the collection of machine-readable user inputs
{cite}`EmpAnalysisOfIssueTemplatesOnGitHub, FirstLookAtBugReportTempOnGitHub, UnderstandingIssueTemplateOnGitHub`. 
While these can be used in conjunction with GHA to automate a variety of issue management tasks
without the need for machine-learning tools,
such capabilities are often not exploited due to the initial implementation barrier.


:::{admonition} |{{ ccc.name }}|'s Solution
:class: tip

|{{ ccc.name }}| establishes a [comprehensive development workflow](#overview-its)
for collaborative and distributed cloud development
using a well-tested pull-based strategy {cite}`ConfigManageForLargescaleSciComp`.
It provides dynamically-maintained type-specific issue forms
designed according to best practices
to collect machine-readable user inputs
{cite}`WhatMakesAGoodBugReport, NeedsInBugReports, QualityOfBugReportsInEclipse`.
|{{ ccc.name }}| then uses these inputs
to automate issue management activities on GHA, including 
ticket labeling and organization, task assignment, documentation, 
and creating issue–commit links.
:::


(motiv-fairness)=
## FAIRness

FOSS is a valuable asset for technological innovations and scientific advancements, 
but often lacks findability, accessibility, interoperability, and reusability
{cite}`AccessibleReproducibleResearch, ShiningLight, CaseForOpenCompProg, SciSoftwareAccuracy, SurveySEPracticesInScience`—key
aspects of the FAIR principles {cite}`FAIR4RS`.

**Findability** requires that software is searchable by its functionalities and attributes.
This necessitates distribution to permanent public indexing repositories
along with comprehensive metadata and unique global identifiers like DOIs
to enable reliable citations
{cite}`10MetricsForSciSoftware, SustainableResearchSoftwareHandOver, WhatMakesCompSoftSuccessful, 10SimpleRulesForOpenDevOfSciSoft, 4SimpleRecs, BarelySufficientPracticesInSciComp, ELIXIRSoftwareManagementPlan`.

**Accessibility** involves adopting an open-source model
under a permissive license {cite}`BusinessOfOpenSource`—ideally
from the start {cite}`BetterSoftwareBetterResearch, PublishYourCode, POVHowOpenSciHelps`—to
enable transparent peer reviews, facilitate progress tracking,
and promote trust, adoption, and collaboration 
{cite}`SharingDetailedResData, CaseForOpenCompProg, 10SimpleRulesForOpenDevOfSciSoft`.
The license determines the legal status of the project
and defines the terms and conditions
under which the software can be used, modified, and distributed.
It is an important aspect of software projects
and can have a significant impact on their adoption and growth.
A suitable license protects the rights of the creator 
while encouraging use and contribution from others.
Therefore, it is crucial for developers 
to carefully choose a license that best suits their needs,
and correctly add it to their project so that 
it can be automatically detected by other services and indexing repositories.
This makes it clear to users and collaborators
under which terms they can use and contribute to the project.

For **interoperability**, a key factor is using a well-suited
and popular programming language in the target community
{cite}`RolesOfCodeInCSE, SoftDevEnvForSciSoft`.
While low-level languages like C still dominate 
legacy high-performance computing (HPC) communities 
due to their speed and hardware integration 
{cite}`SoftEngForCompSci, UnderstandingHPCCommunity, SciCompGridlock`, 
their complexity can obstruct software extension and maintenance
{cite}`PythonEcosystemSciComp, SoftEngForCompSci, SciCompGridlock`.
Therefore, higher-level languages are commonly advised
to improve development, collaboration, and productivity
{cite}`SoftEngForCompSci, BestPracticesForSciComp`. 
[Python](#bg-py) is now the most popular and recommended programming language
due to its simplicity, versatility, extensive ecosystem of performance-optimized libraries,
and the ability to quickly implement complex tasks
that are hard to address in low-level languages
{cite}`PythonBatteriesIncluded, PythonForSciComp, PythonForSciAndEng, PythonJupyterEcosystem, SciCompWithPythonOnHPC, PythonEcosystemSciComp, WhatMakesPythonFirstChoice`.

Lastly, **reusability** is enabled by employing DRY (Don't Repeat Yourself) principles 
and modularizing code into applications with clear programming 
and user interfaces 
{cite}`FAIR4RS, 5RecommendedPracticesForCompSci, BestPracticesForSciComp, RolesOfCodeInCSE`. 
Applications must then be [packaged](#bg-packaging) into as many distribution formats as possible, 
to ensure compatibility with different hardware and software environments. 
This can also greatly simplify the setup process for users 
{cite}`10RuleForSoftwareInCompBio, ELIXIRSoftwareManagementPlan, WhyJohnnyCantBuild`, 
which is a common problem in FOSS {cite}`NamingThePainInDevSciSoft, CompSciError`.
On the other hand, to ensure the reproducibility of results,
consistent execution and predictable outcomes must be guaranteed 
regardless of the runtime environment. 
This is achieved through containerization—a cloud-native approach 
using technologies like Docker to encapsulate applications 
and all their dependencies into isolated, portable images
{cite}`AdoptingSoftEngConceptsInSciResearch, 10RuleForSoftwareInCompBio, ELIXIRSoftwareManagementPlan, Docker`.

Despite its importance, FAIRness is often overlooked in FOSS projects
{cite}`AnalyzingGitHubRepoOfPapers, BridgingTheChasm, PublishYourCode, CompSciError`,
leading to unsustainable prototypes unfit for production environments
{cite}`SustainableResearchSoftwareHandOver, 10RuleForSoftwareInCompBio, PublishYourCode`. 
This hampers FOSS adoption {cite}`SurveySEPracticesInScience, SciSoftwareAccuracy`
and forces projects to reimplement algorithms from scratch
{cite}`ProblemsOfEndUserDevs, BetterSoftwareBetterResearch`, 
which can lead to errors and redundancy issues 
{cite}`SurveySEPracticesInScience2, SoftEngForCompSci`. 
In scientific fields that rely heavily on research software,
FAIRness issues have resulted in many controversies and paper retractions
{cite}`InfluentialPandemicSimulation, RetractionCOVID`.
Thus, there is a growing call for a FAIR and open research culture 
to enhance transparency and reproducibility 
{cite}`PromotingOpenResearch, ReprodResearchInCompSci, EnhancingReproducibility, TroublingTrendsInSciSoftware`, 
and many journals now mandate source code submissions 
for peer-review and public access 
{cite}`RealSoftwareCrisis, DoesYourCodeStandUp, TowardReproducibleCompResearch, MakingDataMaximallyAvailable, JournalOfBioStatPolicy`.
This highlights the need for efficient tools and mechanisms
for licensing, packaging, containerization, distribution, indexing, and maintenance—key 
challenges in publishing FAIR software
{cite}`CaseForOpenCompProg, SurveySEPracticesInScience, ReprodResearchInCompSci, BarelySufficientPracticesInSciComp, BetterSoftwareBetterResearch, PublishYourCode`.


:::{admonition} |{{ ccc.name }}|'s Solution
:class: tip

|{{ ccc.name }}| is specialized in the production of FAIR Python applications,
and provides a comprehensive [package infrastructure](#overview-pkg) and automated solutions
based on the latest guidelines and best practices
for [licensing](#overview-license), build, containerization,
and distribution of software to multiple indexing repositories
with comprehensive metadata and identifiers.
:::


(motiv-testing)=
## Quality Assurance and Testing

Code quality assurance and testing are
crucial aspects of every software development process,
ensuring that the application is functional, correct, secure, and maintainable 
{cite}`CompSciError, BestPracticesForSciComp, 5RecommendedPracticesForCompSci, BestPracticesInBioinfSoftware, SurveySEPracticesInScience, ELIXIRSoftwareManagementPlan, DLRSoftEngGuidelines`.
As projects grow in complexity over time, 
it becomes increasingly challenging to ensure 
that the software functions as expected in all scenarios 
and that changes do not introduce new bugs or disrupt existing functionality.
To prevent the accumulation of errors into complex problems,
it is highly recommended to use [test-driven development](#bg-tdd) (TDD) methodologies
{cite}`10SimpleRulesOnWritingCleanAndReliableSciSoft, SciSoftDevIsNotOxymoron, SurveySEPracticesInScience`.
This involves early and frequent unit and regression testing
to validate new code components and 
ensure existing features remain functional after changes 
{cite}`10SimpleRulesOnWritingCleanAndReliableSciSoft, SurveySEPracticesInScience, BarelySufficientPracticesInSciComp, 10SimpleRulesOnWritingCleanAndReliableSciSoft, BestPracticesForSciComp`.
To ensure testing effectiveness, coverage metrics must be frequently monitored 
to identify untested components 
{cite}`DLRSoftEngGuidelines, 10SimpleRulesOnWritingCleanAndReliableSciSoft`.
Users should also be able to run tests locally
to verify software functionality and performance on their machines {cite}`ELIXIRSoftwareManagementPlan, DLRSoftEngGuidelines`,
necessitating the tests to be packaged and distributed along with the software 
{cite}`BarelySufficientPracticesInSciComp, 10MetricsForSciSoftware, BestPracticesInBioinfSoftware`.

Other crucial quality assurance routines include 
{cite}`DLRSoftEngGuidelines, BestPracticesForSciComp, SurveySEPracticesInScience, 10SimpleRulesOnWritingCleanAndReliableSciSoft, NLeScienceSoftDevGuide`:

- **Code Formatting**:
  Python imposes few restrictions on the formatting of source code,
  leaving developers free to decide how to structure their programs. 
  This flexibility can lead to inconsistent styles,
  making codebases harder to read, review, and maintain, 
  particularly in collaborative projects.
  Python's official style guide, 
  [PEP 8](https://peps.python.org/pep-0008/),
  addresses these issues by outlining best practices for naming conventions, 
  indentation, line length, whitespace usage, and other layout rules.
  Compliant code formatting tools such as [Black](https://github.com/psf/black) and [YAPF](https://github.com/google/yapf) 
  can thus be used to establish a consistent code style by automatically reformatting files.
- **Static Code Analysis**:
  Static code analysis, or linting, involves inspecting code for potential errors, 
  code smells, and style violations without executing it. 
  This process is an essential first line of defense in maintaining code quality,
  promoting code refactoring according to best practices. 
  Tools like [Ruff](https://github.com/astral-sh/ruff), [Pylint](https://github.com/pylint-dev/pylint), [Flake8](https://github.com/PyCQA/flake8), and [Bandit](https://github.com/PyCQA/bandit)
  are popular examples that can help
  to detect security vulnerabilities, syntax errors, unused imports, and non-compliant code structures.
- **Type Checking**:
  Although Python is a dynamically typed language,
  it supports optional type annotations introduced in [PEP 484](https://www.python.org/dev/peps/pep-0484/). 
  These improve code readability and documentation while enabling static type checking. 
  Tools like [Mypy](https://github.com/python/mypy) analyze type annotations to identify type-related errors, 
  ensuring that functions and variables conform to their expected types.
  Static type checking helps developers catch potential bugs early in the development cycle, 
  especially in large and complex codebases.
  

To warrant consistent and effective quality assurance,
code analysis and testing practices need to be automated 
in the project's development workflow
and carried out on configurable virtual machines
{cite}`BestPracticesForSciComp, 10MetricsForSciSoftware, 10SimpleRulesOnWritingCleanAndReliableSciSoft`.
This ensures that all changes in the project pass the same checks and standards,
and that the code is always tested in the same reproducible and transparent environment.
While the Python ecosystem offers powerful code analysis and testing tools like [Pytest](https://github.com/pytest-dev/pytest),
assembling the right set of tools into a comprehensive automated pipeline
is still a challenging task {cite}`StairwayToHeaven`,
resulting in the prevalence of slow and ineffective testing methods in FOSS projects
{cite}`ProblemsOfEndUserDevs, TestingResearchSoftwareSurvey, SoftEngForCompSci, SurveySEPracticesInScience, SurveySEPracticesInScience2`.
Consequently, software products may contain hidden bugs
that do not interrupt the execution of the program
but generate incorrect outputs.
In sensitive areas like governmental and military applications,
such bugs can compromise critical scientific conclusions
and result in multi-million-dollar losses
{cite}`CompSciError, SoftwareChasm, ApproxTowerInCompSci, NightmareRetraction, RetractionChang, RetractionMa, RetractionChang2, RetractionJAmCollCardiol, RetractionMeasuresOfCladeConfidence, RetractionsEffectOfAProgram, CorrectionHypertension, CommentOnError, CommentOnError2, CommentOnError3, CommentOnError4, CommentOnError5, ClusterFailureFMRI`.


:::{admonition} |{{ ccc.name}}|'s Solution
:class: tip

|{{ ccc.name}}| provides a ready-to-use [test suite](#overview-testsuite),
where users only need to add test cases in the provided skeleton files.
The test suite benefits from the same features as the project's main Python package,
and can be automatically distributed in each release as a stand-alone package.
All quality assurance and testing routines are automated
in the provided [Continuous Integration](#overview-ci), [Refactoring, and Testing pipelines](#overview-cm),
with feature such as code style formatting, linting and automatic refactoring,
coverage monitoring, and comprehensive report generation.
:::


(motiv-doc)=
## Documentation

Documentation is a key factor in software quality and success,
ensuring users understand how to install, use, and exploit the software's capabilities
while recognizing its limitations 
{cite}`10SimpleRulesForOpenDevOfSciSoft, BestPracticesForSciComp, GoodEnoughPracticesInSciComp, WhatMakesCompSoftSuccessful, SciSoftDevIsNotOxymoron, NamingThePainInDevSciSoft, CompSciError, BarelySufficientPracticesInSciComp`.
This is especially important for FOSS,
which often suffers from knowledge loss due to high developer turnover rates 
{cite}`HowToSupportOpenSource, RecommendOnResearchSoftware, EmpStudyDesignInHPC, SoftwareSustainabilityInstitute`.
As software evolves, documenting and publishing changelogs with each release
allows existing users to assess the update impact and helps new users and contributors 
understand the software's progression {cite}`ELIXIRSoftwareManagementPlan, GoodEnoughPracticesInSciComp, SustainableResearchSoftwareHandOver`.
As community building is crucial for FOSS success 
{cite}`HowToSupportOpenSource, WhatMakesCompSoftSuccessful`,
project documentation should also include contribution guidelines,
developer guides, governance models, and codes of conduct 
{cite}`SurveySEPracticesInScience, BestPracticesForSciComp, BestPracticesInBioinfSoftware, SustainableResearchSoftwareHandOver, 4SimpleRecs, ELIXIRSoftwareManagementPlan, DLRSoftEngGuidelines, NLeScienceSoftDevGuide`.
Other important documents include README files for both the source code repository
and other indexing repositories hosting binary distributions.
Acting as the front page of the repository,
README files should provide visitors with a concise
and visually appealing overview of the project,
including a short description, keywords, 
and links to important resources and documents.
Ideally, they should also include dynamic information
such as project statistics and status indicators
that are automatically updated to reflect the current project state.

However, high-quality documentation requires time, effort, and skills,
including web development knowledge to create user-friendly websites
that stay up to date with the latest project developments 
{cite}`SurveySEPracticesInScience, WhatMakesCompSoftSuccessful`. 
Although tools exist to aid documentation 
{cite}`TenSimpleRulesForDocumentingSciSoft, WhatMakesCompSoftSuccessful, BestPracticesForSciComp`,
developers must still invest time in setting them up.
A more important issue is the lack of automation,
requiring developers to manually document
a large amount of specifications, instructions,
design decisions, implementation details, changelogs,
and other essential essential documentation.
Consequently, FOSS is often not well-documented
{cite}`SoftEngForCompSci, ProblemsOfEndUserDevs, AnalyzingGitHubRepoOfPapers, DealingWithRiskInSciSoft`,
creating barriers to use and leading to software misuse and downstream issues
{cite}`HowScientistsReallyUseComputers, HowScientistsDevSciSoftExternalRepl, CompSciError`.


:::{admonition} |{{ ccc.name}}|'s Solution
:class: tip

|{{ ccc.name}}| provides a fully designed [website](#overview-docs) filled with automatically 
generated documentation such as project information, package metadata, 
installation guides, API reference, changelogs, release notes, contribution guides, 
and citation data. The website can be automatically deployed to 
GitHub Pages and Read The Docs platforms,
and is easily customizable via the control center with no web development knowledge. 
PyPackIT can also dynamically generate standalone documents in various Markdown formats, 
such as community health files and READMEs for different indexing repositories.
:::


## Version Control

Version control practices such as branching, merging, tagging, and history management
are vital yet challenging tasks in software development 
{cite}`10MetricsForSciSoftware, ELIXIRSoftwareManagementPlan, EffectOfBranchingStrategies, BranchUseInPractice`.
Branching provides isolation for development and testing of individual changes,
which must then be merged back into the project's mainline
with information-rich commit messages to maintain a clear history.
Moreover, tags allow to annotate specific states of the code with version numbers
to clearly communicate and reference changes 
{cite}`ImportanceOfBranchingModels, CICDSystematicReview`.

While established versioning schemes like [Semantic Versioning](#bg-semver)
and branching models like trunk-based development {cite}`TrunkBasedDev`,
git-flow {cite}`GitFlow`, GitHub flow {cite}`GitHubFlow`,
and GitLab flow {cite}`GitLabFlow` exist,
enforcing their consistent and effective application in the project
still requires implementing them into automated workflows.
Moreover, these general-purpose strategies 
may require adjustments to fully align with the evolving nature of FOSS,
which often begins as a prototype and undergoes significant changes 
{cite}`UnderstandingHPCCommunity`.
For example, a suitable model for FOSS development should support 
simultaneous development and long-term maintenance of multiple versions,
to facilitate rapid evolution while ensuring the availability 
and sustainability of earlier releases
{cite}`ConfigManageForLargescaleSciComp`.


:::{admonition} |{{ ccc.name }}|'s Solution
:class: tip

|{{ ccc.name }}| automates [version control](#overview-vcs) tasks
such as branching, pull request creation, commit message generation,
versioning, tagging, and merging,
with a branching model and versioning scheme
specialized for FOSS requirements.
:::


(motiv-cca)=
## Configuration Management

Software projects rely on various tools and services 
throughout the development life cycle,
each requiring separate configuration 
via specific files or user interfaces.
This can lead to several maintenance challenges 
{cite}`BestPracticesForSciComp, DevOpsInSciSysDev`:
Tool-specific formats and requirements result in data redundancy,
since many settings are shared.
As configuration files are often static,
they require manual intervention to reflect each change.
Otherwise they quickly fall out of sync with the current state of the project,
leading to conflicts and inconsistencies.
Moreover, configurations via interactive user interfaces
complicate the tracking and replication of settings,
as they must be manually recorded and applied.
These issues complicate project initialization, configuration,
and customization, hampering the growth of sustainability of FOSS projects.

DevOps practices such as Continuous Configuration Automation (CCA)
and Infrastructure-as-Code (IaC) were developed to tackle these issues,
enabling dynamic configuration management of hardware and software infrastructures
through machine-readable definition files {cite}`InfrastructureAsCode`.
While these practices are more prevalent in server and network management applications,
they can greatly benefit software development projects as well.
Nevertheless, due to a lack of publicly available tools,
most projects still rely on a combination of 
different configuration files and manual settings,
which are hard to manage, modify, and reproduce.


:::{admonition} |{{ ccc.name}}|'s Solution
:class: tip

|{{ ccc.name }}| provides a centralized user interface 
for automatic configuration, customization, 
and management of the entire project, 
and even multiple projects at once.
|{{ ccc.name }}|’s [control center](#overview-cc) 
consolidates all project configurations 
into a unified data structure, 
supporting both declarative definitions 
and dynamic data generation at runtime 
via built-in templating, scripting, 
and online retrieval features. 
Configurations are automatically applied to related components, 
eliminating redundancy and rendering the entire project dynamic.
:::


## Maintenance

Modern software can remain useful and operational
for decades {cite}`SoftwareSustainabilityInstitute, SoftEngForCompSci`.
Considering the amounts of time and effort required
to develop high-quality software from scratch,
ensuring the long-term sustainability of available software
is crucial {cite}`BarelySufficientPracticesInSciComp`.
This requires continuous feedback from the community and active maintenance
to fix existing issues, improve functionalities, and add new features.
Maintaining software dependencies is equally important {cite}`FortyYearsOfSoftwareReuse`,
as software must remain compatible with diverse computer environments
and future dependency versions {cite}`EmpComparisonOfDepNetEvolution`.
However, many projects overlook outdated dependencies {cite}`DoDevsUpdateDeps`,
leading to incompatibilities and bugs {cite}`MeasuringDepFreshness, ThouShaltNotDepend, OnImpactOfSecVulnInDepNet`.

Challenges such as funding {cite}`ManagingChaos, BetterSoftwareBetterResearch`,
small team sizes {cite}`SoftEngForCompSci, HowScientistsReallyUseComputers`,
and high developer turnover rates {cite}`RecommendOnResearchSoftware, EmpStudyDesignInHPC`
further hinder maintenance of FOSS projects,
exacerbated by technical debt and increased software entropy
from neglected software engineering best practices
{cite}`BetterSoftwareBetterResearch, ProblemsOfEndUserDevs, SoftEngForCompSci, ManagingTechnicalDebt, 10SimpleRulesForOpenDevOfSciSoft, SoftDesignForEmpoweringSci, ManagingChaos, SoftwareSustainabilityInstitute`.
Consequently, the extra effort required for maintenance is a major barrier
to publicly releasing software {cite}`BetterSoftwareBetterResearch, PublishYourCode`,
often leaving it as an unsustainable prototype 
{cite}`SustainableResearchSoftwareHandOver, 10RuleForSoftwareInCompBio, PublishYourCode`.
To prevent such issues, quality assurance and maintenance tasks should be automated
and enforced from the beginning of the project {cite}`SoftEngForCompSci`,
in form of Continuous Maintenance (CM) {cite}`ContinuousMaintenance`, 
Refactoring (CR) {cite}`ContRefact`, and Testing (CT) {cite}`ContinuousSoftEng` 
pipelines to periodically update dependencies and development tools, 
and automatically maintain the health of the software 
and its development environment {cite}`SoftEngForCompSci`.
Furthermore, providing a ready-to-use development environment tailored to project needs 
can greatly lower the entry barrier for future maintainers and external collaborators, 
fostering the long-term sustainability of FOSS.


:::{admonition} |{{ ccc.name}}|'s Solution
:class: tip

|{{ ccc.name }}| provides fully automated 
[Continuous Maintenance, Refactoring, and Testing](#overview-cm) pipelines
that periodically perform tasks such as 
testing previous releases with up-to-date dependencies, 
refactoring code according to the latest standards, 
upgrading development tools and project infrastructure, 
and cleaning up the repository and its development environment.
|{{ ccc.name }}| can automatically submit 
issue tickets and pull requests 
for applying updates and fixes, 
thus maintaining the health of the project 
and ensuring its long-term sustainability.
:::


## Security

Security is a crucial aspect of software development,
and should be considered at every stage of the development process.
This is especially important for open-source projects
where the source code and other project resources are publicly available.
Therefore, implementing security measures and
protocols for reporting and handling security issues in the repository
is essential for ensuring software integrity and safeguarding the project against vulnerabilities.
GitHub provides several [security features](https://docs.github.com/en/code-security/getting-started/github-security-features)
that must be correctly configured to help developers
identify, privately report, and fix potential security issues in their repositories,
such as [code scanning](https://docs.github.com/en/code-security/code-scanning/introduction-to-code-scanning/about-code-scanning),
[dependency review](https://docs.github.com/en/code-security/supply-chain-security/understanding-your-software-supply-chain/about-dependency-review),
[secret scanning](https://docs.github.com/en/code-security/secret-scanning/about-secret-scanning),
[security policies](https://docs.github.com/en/code-security/getting-started/adding-a-security-policy-to-your-repository),
and [security advisories](https://docs.github.com/en/code-security/security-advisories/working-with-repository-security-advisories/about-repository-security-advisories).
In addition, setting up various [branch protection rules](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches)
for repository's release branches is another crucial security measure,
safeguarding the main codebase and ensuring that changes are reviewed and tested before being merged.
This practice, which is especially important
for projects with multiple contributors and outside collaborators,
not only maintains code quality but also fosters a disciplined development environment.
