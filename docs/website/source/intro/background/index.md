# Background

This section outlines current advancements, challenges, and requirements
in open-source software engineering


## FAIRness

Research software is vital for computational studies but often lacks Findability, Accessibility, Interoperability, and Reusability—key aspects of the FAIR principles \cite{FAIR4RS}—impacting reproducibility and reuse of scientific studies\cite{AccessibleReproducibleResearch, ShiningLight, CaseForOpenCompProg, SciSoftwareAccuracy, SurveySEPracticesInScience}. \textbf{Findability} requires that research software is searchable by its functionalities and attributes, necessitating its permanent distribution to related public indexing repositories along with comprehensive metadata and unique identifiers like DOIs \cite{10MetricsForSciSoftware, WhatMakesCompSoftSuccessful, 10SimpleRulesForOpenDevOfSciSoft, 4SimpleRecs, BarelySufficientPracticesInSciComp, ELIXIRSoftwareManagementPlan}. \textbf{Accessibility} involves adopting an open-source model under a permissive license \cite{BusinessOfOpenSource}—ideally from the start \cite{BetterSoftwareBetterResearch, PublishYourCode, POVHowOpenSciHelps}, to enable transparent peer review, facilitate progress tracking, and promote trust, adoption, and collaboration \cite{SharingDetailedResData, CaseForOpenCompProg, 10SimpleRulesForOpenDevOfSciSoft}. For \textbf{interoperability}, a key factor is using a well-suited and popular programming language in the target community \cite{RolesOfCodeInCSE, SoftDevEnvForSciSoft}. Python is now the leading language for research software development \cite{SurveySEPracticesInScience2, AnalyzingGitHubRepoOfPapers, DevOpsInSciSysDev}, recommended due to its simplicity, versatility, and ability to quickly implement complex tasks that are hard to address in low-level languages \cite{PythonBatteriesIncluded, PythonForSciComp, PythonForSciAndEng, PythonJupyterEcosystem, SciCompWithPythonOnHPC, PythonEcosystemSciComp, WhatMakesPythonFirstChoice}. Python's extensive ecosystem offers performance-optimized libraries for various scientific applications \cite{NumPy, SciPy, pandas, PyTorch, Top5MLLibPython, ScikitLearn, scikitImage, Matplotlib, Mayavi, IPython, Jupyter, Jupyter2, DaskAndNumba, DaskApplications, Cython, Numba, Pythran, PyCUDA, Astropy, SunPy, Pangeo, MDAnalysis, Biopython, NIPY}, with features for parallel distributed computing  \cite{SciCompWithPythonOnHPC, ParallelDistCompUsingPython, ScientistsGuideToCloudComputing, DemystPythonPackageWithCondaEnvMod, PythonAcceleratorsForHPC, DistWorkflowsWithJupyter, InteractiveSupercomputingWithJupyter} that even allows high-performance computing communities such as CERN \cite{IntroducingPythonAtCERN, PythonAtCERN} and NASA \cite{PythonAtNASA} to use it for key scientific achievements \cite{PythonScientificSuccessStories, GravWaveDiscovery, BlackHoleImage}. Lastly, \textbf{reusability} is enabled by employing DRY (Don't Repeat Yourself) principles and modularizing code into applications with clear programming and user interfaces \cite{FAIR4RS, 5RecommendedPracticesForCompSci, BestPracticesForSciComp, RolesOfCodeInCSE}. Applications must then be packaged into as many distribution formats as possible, to ensure compatibility with different hardware and software environments. This can also greatly simplify the setup process for users \cite{10RuleForSoftwareInCompBio, ELIXIRSoftwareManagementPlan, WhyJohnnyCantBuild}, which is a common problem in research software \cite{NamingThePainInDevSciSoft, CompSciError}. Despite its importance, research software is infrequently published \cite{AnalyzingGitHubRepoOfPapers, BridgingTheChasm, PublishYourCode, CompSciError}, leading to controversies and retractions \cite{InfluentialPandemicSimulation, RetractionCOVID}, and forcing the reimplementation of computational workflows from scratch \cite{ProblemsOfEndUserDevs, BetterSoftwareBetterResearch, SurveySEPracticesInScience2, SoftEngForCompSci}. Thus, there is a growing call for an open research culture to enhance transparency and reproducibility \cite{PromotingOpenResearch, ReprodResearchInCompSci, EnhancingReproducibility, TroublingTrendsInSciSoftware}, and many journals now mandate source code submissions for peer-review and public access \cite{RealSoftwareCrisis, DoesYourCodeStandUp, TowardReproducibleCompResearch, MakingDataMaximallyAvailable, JournalOfBioStatPolicy}.

## FAIR Research Software

Research software is a valuable asset that can be readily reused as a building block in numerous computational studies. As software is complex and intangible in nature \cite{MythicalManMonth}, such studies cannot be replicated, verified, or built upon without full access to the underlying source code, input data, and parameters \cite{ReprodResearchInCompSci, AccessibleReproducibleResearch, BarelySufficientPracticesInSciComp, ShiningLight, PublishYourCode, CaseForOpenCompProg}. Despite this, research software has been rarely published \cite{BridgingTheChasm, CaseForOpenCompProg, 4SimpleRecs, PublishYourCode, CompSciError}, leading to controversies \cite{InfluentialPandemicSimulation} and retractions \cite{RetractionCOVID}, preventing software reuse \cite{SurveySEPracticesInScience, SciSoftwareAccuracy}, and forcing scientists to re-implement computational workflows from scratch in each new project \cite{ProblemsOfEndUserDevs, BetterSoftwareBetterResearch}, which is an error-prone process yielding low-quality results \cite{SurveySEPracticesInScience2, SoftEngForCompSci}. In response, widespread appeals have emerged for an open research culture, promoting transparency and reproducibility \cite{PublishYourCode, PromotingOpenResearch, ReprodResearchInCompSci, CaseForOpenCompProg, EnhancingReproducibility, ShiningLight, TroublingTrendsInSciSoftware}. While more publications now include links to source code and data, this is still strongly biased toward a handful of institutions working in specific computer science fields \cite{AnalyzingGitHubRepoOfPapers}. Common obstacles to publishing research software include the lack of efficient mechanisms and tools for packaging, distribution, and indexing \cite{CaseForOpenCompProg, SurveySEPracticesInScience, ReprodResearchInCompSci}, as well as code quality concerns and technical challenges to refactor, document, and maintain the software \cite{BarelySufficientPracticesInSciComp, BetterSoftwareBetterResearch, PublishYourCode}. To sustain scientific progress in CSE, it is thus crucial to address these challenges and ensure that research software is FAIR \cite{FAIR4RS}: findable, accessible, interoperable, and reusable.

Regarding accessibility, many journals now mandate source code submissions for peer-review and public access \cite{RealSoftwareCrisis, DoesYourCodeStandUp, CaseForOpenCompProg, TowardReproducibleCompResearch, MakingDataMaximallyAvailable, JournalOfBioStatPolicy}. It is thus highly recommended to adopt an open-source model from start \cite{BetterSoftwareBetterResearch, PublishYourCode, SurveySEPracticesInScience, BarelySufficientPracticesInSciComp, BestPracticesInBioinfSoftware, POVHowOpenSciHelps, 4SimpleRecs, ELIXIRSoftwareManagementPlan, 10RuleForSoftwareInCompBio}, making the source code freely accessible under a permissive license \cite{BusinessOfOpenSource}. This provides a full record of activities that can be crucial in tracking progress and recognition, enables transparent peer review, promotes trust and adoption, leads to more citations, and improves software quality and sustainability by encouraging community collaboration \cite{SharingDetailedResData, BetterSoftwareBetterResearch, ShiningLight, PublishYourCode, CaseForOpenCompProg, 4SimpleRecs, POVHowOpenSciHelps, BestPracticesInBioinfSoftware, SurveySEPracticesInScience, 10SimpleRulesForOpenDevOfSciSoft, BarelySufficientPracticesInSciComp}. Furthermore, to facilitate findability, research software must be searchable by its functionalities and attributes \cite{10MetricsForSciSoftware}. This requires the distribution of software to related public indexing repositories, along with comprehensive metadata and identifiers \cite{WhatMakesCompSoftSuccessful, HowToSupportOpenSource, 10SimpleRulesForOpenDevOfSciSoft, ELIXIRSoftwareManagementPlan, SustainableResearchSoftwareHandOver, BarelySufficientPracticesInSciComp, 4SimpleRecs}. For reproducibility of research results, each distribution must be permanently available and uniquely indexed with a persistent global identifier that enables reliable citations, such as a Digital Object Identifier (DOI) \cite{BarelySufficientPracticesInSciComp, BestPracticesInBioinfSoftware, ELIXIRSoftwareManagementPlan, BestPracticesInBioinfSoftware, 4SimpleRecs}. To ensure the interoperability and reusability of research software, employing DRY (Don't Repeat Yourself) Principles is encouraged to modularize code into separate methods and routines, organized into a software library with a clear API \cite{FAIR4RS, 10MetricsForSciSoftware, SciSoftDevIsNotOxymoron, 5RecommendedPracticesForCompSci, BestPracticesForSciComp}. As review articles and scientific textbooks provide an overview of recent progress and established knowledge in a field, scientific libraries do the same for code, implementing state-of-the-art algorithms and well-known procedures for use in computational studies \cite{RolesOfCodeInCSE}. Packaging code into software libraries can also greatly simplify the setup process for users \cite{10RuleForSoftwareInCompBio, ELIXIRSoftwareManagementPlan, WhyJohnnyCantBuild}, which is a common problem in research software \cite{NamingThePainInDevSciSoft, CompSciError}. Therefore, PyPackIT is focused on the production of open-source and FAIR scientific Python libraries, and implements automated solutions to facilitate above-mentioned challenges, such as licensing, packaging, distribution, and indexing \cite{BarelySufficientPracticesInSciComp, ELIXIRSoftwareManagementPlan, SustainableResearchSoftwareHandOver, ShiningLight, 10RuleForSoftwareInCompBio}.



## Quality Assurance and Testing

Code quality assurance and testing are
crucial aspects of every software development process,
ensuring that the application is functional, correct,
secure, and maintainable {cite}`CompSciError, BestPracticesForSciComp, 5RecommendedPracticesForCompSci, BestPracticesInBioinfSoftware, SurveySEPracticesInScience, ELIXIRSoftwareManagementPlan, DLRSoftEngGuidelines`.
To prevent the accumulation of errors into complex problems,
it is highly recommended to use test-driven development methodologies
{cite}`10SimpleRulesOnWritingCleanAndReliableSciSoft, SciSoftDevIsNotOxymoron, SurveySEPracticesInScience`.
This involves early and frequent unit and regression testing
to validate new code components and ensure existing features
remain functional after changes {cite}`10SimpleRulesOnWritingCleanAndReliableSciSoft, SurveySEPracticesInScience, BarelySufficientPracticesInSciComp, 10SimpleRulesOnWritingCleanAndReliableSciSoft, BestPracticesForSciComp`.
To ensure testing effectiveness, coverage metrics must be frequently monitored to identify
untested components {cite}`DLRSoftEngGuidelines, 10SimpleRulesOnWritingCleanAndReliableSciSoft`.
Users should also be able to run tests locally
to verify software functionality and performance on their machines {cite}`ELIXIRSoftwareManagementPlan, DLRSoftEngGuidelines`,
necessitating the tests to be packaged and distributed along with the software 
{cite}`BarelySufficientPracticesInSciComp, 10MetricsForSciSoftware, BestPracticesInBioinfSoftware`.
Other crucial quality assurance routines include formatting
to improve readability and establish a consistent coding style,
and static code analysis such as linting and type checking
to identify issues undetected by tests,
and refactor code to improve quality, security, and maintainability
{cite}`DLRSoftEngGuidelines, BestPracticesForSciComp, SurveySEPracticesInScience, 10SimpleRulesOnWritingCleanAndReliableSciSoft, NLeScienceSoftDevGuide`.

To ensure effective quality assurance, code analysis and testing practices
need to be automated in the project's development workflow
{cite}`BestPracticesForSciComp, 10MetricsForSciSoftware, 10SimpleRulesOnWritingCleanAndReliableSciSoft`.
This is however a challenging task {cite}`StairwayToHeaven`,
resulting in the prevalence of slow and ineffective testing methods especially in FOSS projects
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

Accordingly, PyPackIT offers a fully automated quality assurance and testing infrastructure
for the entire development life-cycle, fulfilling all requirements, including coverage monitoring,
documentation, and test-suite distribution.
:::


## Documentation

Documentation is a key factor in software quality and success,
ensuring users understand how to install, use, and exploit the software's capabilities
while recognizing its limitations {cite}`10SimpleRulesForOpenDevOfSciSoft, BestPracticesForSciComp, GoodEnoughPracticesInSciComp, WhatMakesCompSoftSuccessful, SciSoftDevIsNotOxymoron, NamingThePainInDevSciSoft, CompSciError, BarelySufficientPracticesInSciComp`.
This is especially important for {term}`FOSS`,
which often suffers from knowledge loss due to high developer turnover rates {cite}`HowToSupportOpenSource, RecommendOnResearchSoftware, EmpStudyDesignInHPC, SoftwareSustainabilityInstitute`.
As software evolves, documenting and publishing changelogs with each release
allows existing users to assess the update impact and helps new users and contributors 
understand the software's progression {cite}`ELIXIRSoftwareManagementPlan, GoodEnoughPracticesInSciComp, SustainableResearchSoftwareHandOver`.
As community building is crucial for FOSS success {cite}`HowToSupportOpenSource, WhatMakesCompSoftSuccessful`,
project documentation should also include contribution guidelines,
governance models, and codes of conduct {cite}`SurveySEPracticesInScience, BestPracticesForSciComp, BestPracticesInBioinfSoftware, SustainableResearchSoftwareHandOver, 4SimpleRecs, ELIXIRSoftwareManagementPlan, DLRSoftEngGuidelines, NLeScienceSoftDevGuide`.

However, high-quality documentation requires time, effort, and skills,
including web development knowledge to create user-friendly websites
that stay up to date with the latest project developments {cite}`SurveySEPracticesInScience, WhatMakesCompSoftSuccessful`. 
Although tools exist to aid documentation {cite}`TenSimpleRulesForDocumentingSciSoft, WhatMakesCompSoftSuccessful, BestPracticesForSciComp`,
developers must still invest time in setting them up.
Consequently, FOSS is often not well-documented {cite}`SoftEngForCompSci, ProblemsOfEndUserDevs, AnalyzingGitHubRepoOfPapers, DealingWithRiskInSciSoft`,
creating barriers to use and leading to software misuse and faulty results {cite}`HowScientistsReallyUseComputers, HowScientistsDevSciSoftExternalRepl, CompSciError`.


:::{admonition} |{{ ccc.name}}|'s Solution
:class: tip

Therefore, PyPackIT puts great emphasis on documentation,
providing infrastructure and automated solutions that enable projects to maintain
high-quality documentation with minimal effort.
:::


## Version Control

Version control practices such as branching and tagging
are vital yet challenging tasks in software development {cite}`10MetricsForSciSoftware, ELIXIRSoftwareManagementPlan, EffectOfBranchingStrategies, BranchUseInPractice`.
Branching provides isolation for development and testing of individual changes,
while tags allow to annotate specific states of the code with version numbers
to clearly communicate and reference changes {cite}`ImportanceOfBranchingModels, CICDSystematicReview`.
Although established models like GitFlow and trunk-based development exist {cite}`TrunkBasedDev, GitFlow, GitHubFlow, GitLabFlow`,
they do not fully align with the evolving nature of {term}`FOSS`,
which often begins as a prototype and undergoes significant changes {cite}`UnderstandingHPCCommunity`.
A suitable model must, thus, support simultaneous development and
long-term maintenance of multiple versions, to facilitate rapid evolution
while ensuring the availability and sustainability of earlier releases {cite}`ConfigManageForLargescaleSciComp`. 


## Configuration Management

Software projects rely on various tools and services throughout the development life cycle,
each requiring separate configuration via specific files or user interfaces.
This can lead to several maintenance challenges {cite}`BestPracticesForSciComp, DevOpsInSciSysDev`:
Tool-specific formats and requirements result in data redundancy,
since many settings are shared.
As configuration files are often static,
they require manual intervention to reflect each change.
Otherwise they quickly fall out of sync with the current state of the project,
leading to conflicts and inconsistencies.
Moreover, configurations via interactive user interfaces
complicate the tracking and replication of settings,
as they must be manually recorded and applied.

DevOps practices such as Continuous Configuration Automation (CCA)
and Infrastructure-as-Code (IaC) were developed to tackle these issues,
enabling dynamic configuration management of software infrastructure
through machine-readable definition files {cite}`InfrastructureAsCode`.
However, due to a lack of publicly available tools,
most projects still rely on a combination of different configuration files and manual settings,
which are hard to manage, modify, and reproduce.


:::{admonition} |{{ ccc.name}}|'s Solution
:class: tip

|{{ ccc.name }}| implements a similar mechanism to facilitate the definition, customization,
synchronization, and maintenance of all project metadata and settings.
It provides a user-friendly control center that renders the entire project infrastructure
and development environment dynamic, enabling automatic project management and configuration.
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

Open-source software development challenges such as funding {cite}`ManagingChaos, BetterSoftwareBetterResearch`,
small team sizes {cite}`SoftEngForCompSci, HowScientistsReallyUseComputers`,
and high developer turnover rates {cite}`RecommendOnResearchSoftware, EmpStudyDesignInHPC`
further hinder maintenance, exacerbated by technical debt and increased software entropy
from neglected software engineering best practices {cite}`BetterSoftwareBetterResearch, ProblemsOfEndUserDevs, SoftEngForCompSci, ManagingTechnicalDebt, 10SimpleRulesForOpenDevOfSciSoft, SoftDesignForEmpoweringSci, ManagingChaos, SoftwareSustainabilityInstitute`.
Consequently, the extra effort required for maintenance is a major barrier
to publicly releasing software {cite}`BetterSoftwareBetterResearch, PublishYourCode`,
often leaving it as an unsustainable prototype {cite}`SustainableResearchSoftwareHandOver, 10RuleForSoftwareInCompBio, PublishYourCode`.
To prevent such issues, quality assurance and maintenance tasks should be automated
and enforced from the beginning of the project {cite}`SoftEngForCompSci`.


:::{admonition} |{{ ccc.name}}|'s Solution
:class: tip

|{{ ccc.name }}| achieves this by several mechanisms, including its automated pull-based development model
that promotes collaboration and feedback, CI/CD pipelines that enforce software engineering best practices
throughout the development process, and Continuous Maintenance (CM) {cite}`ContinuousMaintenance`,
Refactoring (CR) {cite}`ContRefact`, and Testing (CT) {cite}`ContinuousSoftEng`
pipelines (abbreviated as CM/CR/CT) that periodically perform various automated tasks,
such as updating dependencies and development tools,
to maintain the health of the software and its development environment.
:::