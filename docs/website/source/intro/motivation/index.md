(motivation)=
# Motivation

Free and Open Source Software ({term}`FOSS`)
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
{cite}`FAIR4RS, 4SimpleRecs, 10MetricsForSciSoftware, BestPracticesForSciComp, RecommendOnResearchSoftware, ELIXIRSoftwareManagementPlan, NLeScienceSoftDevGuide, BestPracticesInBioinfSoftware, 10RuleForSoftwareInCompBio, SustainableResearchSoftwareHandOver, QuickGuideToOrgCompBioProjects, EnhancingReproducibility, SciSoftDevIsNotOxymoron, 5RecommendedPracticesForCompSci, 10SimpleRulesOnWritingCleanAndReliableSciSoft, BarelySufficientPracticesInSciComp, GoodEnoughPracticesInSciComp` 
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
However, implementing GHA [workflows](#bg-gha-workflows) 
involves challenges related to tooling, configuration, 
testability, debugging, maintenance, and security
{cite}`HowDoSoftDevsUseGHA, EvolutionOfGHAWorkflows, OnOutdatednessOfWorkflowsInGHA, AutoSecurityAssessOfGHAWorkflows`.
[Action](#bg-gha-actions) reuse is also low, due to issues with compatibility, 
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
GitHub's [pull-based development model](#bg-pull-based) offers 
an effective solution by enabling community contributions 
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
Issue tracking systems (ITSs) like GitHub Issues (GHI) 
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
Moreover, in 2021 GitHub introduced
[issue forms](https://github.blog/changelog/2021-06-23-issues-forms-beta-for-public-repositories/),
allowing projects to provide multiple issue submission options
using structured web forms that enable the collection of machine-readable user inputs
{cite}`EmpAnalysisOfIssueTemplatesOnGitHub, FirstLookAtBugReportTempOnGitHub, UnderstandingIssueTemplateOnGitHub`. 
While these can be used in conjunction with GHA to automate a variety of issue management tasks,
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
Applications must then be packaged into as many distribution formats as possible, 
to ensure compatibility with different hardware and software environments. 
This can also greatly simplify the setup process for users 
{cite}`10RuleForSoftwareInCompBio, ELIXIRSoftwareManagementPlan, WhyJohnnyCantBuild`, 
which is a common problem in FOSS {cite}`NamingThePainInDevSciSoft, CompSciError`. 

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
for licensing, packaging, distribution, indexing, and maintenance of research software
{cite}`CaseForOpenCompProg, SurveySEPracticesInScience, ReprodResearchInCompSci, BarelySufficientPracticesInSciComp, BetterSoftwareBetterResearch, PublishYourCode`.


:::{admonition} |{{ ccc.name }}|'s Solution
:class: tip

|{{ ccc.name }}| is specialized in the production of FAIR Python applications,
and provides a comprehensive infrastructure and automated solutions
based on the latest guidelines and best practices
for licensing, packaging, and distribution of software to multiple indexing repositories.
:::


## Quality Assurance and Testing

Code quality assurance and testing are
crucial aspects of every software development process,
ensuring that the application is functional, correct, secure, and maintainable 
{cite}`CompSciError, BestPracticesForSciComp, 5RecommendedPracticesForCompSci, BestPracticesInBioinfSoftware, SurveySEPracticesInScience, ELIXIRSoftwareManagementPlan, DLRSoftEngGuidelines`.
To prevent the accumulation of errors into complex problems,
it is highly recommended to use test-driven development methodologies
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
Other crucial quality assurance routines include formatting
to improve readability and establish a consistent coding style,
as well as static code analysis such as linting and type checking
to identify issues undetected by tests
and refactor code to improve quality, security, and maintainability
{cite}`DLRSoftEngGuidelines, BestPracticesForSciComp, SurveySEPracticesInScience, 10SimpleRulesOnWritingCleanAndReliableSciSoft, NLeScienceSoftDevGuide`.

To warrant consistent and effective quality assurance,
code analysis and testing practices need to be automated 
in the project's development workflow
and carried out on configurable virtual machines
{cite}`BestPracticesForSciComp, 10MetricsForSciSoftware, 10SimpleRulesOnWritingCleanAndReliableSciSoft`.
This ensures that all changes in the project pass the same checks and standards,
and that the code is always tested in the same reproducible and transparent environment.
While the Python ecosystem offers powerful code analysis and testing tools,
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

|{{ ccc.name}}| provides a ready-to-use test suite,
where users only need to add test cases in the provided skeleton files.
The test suite benefits from the same features as the project's main Python package,
and can be automatically distributed in each release as a stand-alone package.
All quality assurance and testing routines are automated
in the provided Continuous Integration, Refactoring, and Testing pipelines,
with feature such as code style formatting, linting and automatic refactoring,
coverage monitoring, and comprehensive report generation.
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


To address these issues, |{{ ccc.name }}| emphasizes providing infrastructure and automated solutions 
for maintaining high-quality documentation with minimal effort.


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



:::{admonition} |{{ ccc.name }}|'s Solution
:class: tip

|{{ ccc.name }}| addresses these needs by automating version control tasks 
with a specialized branching model and version scheme.
:::


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

|{{ ccc.name }}| implements a similar system, providing a user-friendly control center 
for defining, customizing, synchronizing, and maintaining project metadata, 
making project management and configuration more efficient and automated.
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


:::{admonition} |{{ ccc.name }}|'s Solution
:class: tip

|{{ ccc.name }}| addresses these needs by offering an automated quality assurance 
and testing infrastructure for the entire development life-cycle, 
including coverage monitoring and test-suite distribution.

To prevent these issues, quality assurance and maintenance tasks 
should be automated and enforced from the beginning of the project {cite}`SoftEngForCompSci`. 
|{{ ccc.name }}| achieves this by implementing Continuous Maintenance (CM) {cite}`ContinuousMaintenance`, 
Refactoring (CR) {cite}`ContRefact`, and Testing (CT) {cite}`ContinuousSoftEng` pipelines 
that periodically perform various automated tasks, 
such as updating dependencies and development tools, 
to continuously maintain the health of the software and its development environment.
|{{ ccc.name }}| mitigates maintenance challenges by implementing automated 
Continuous Maintenance (CM), Refactoring (CR), and Testing (CT) pipelines 
from the project's inception to ensure software and environment health
{cite}`SoftEngForCompSci, ContinuousMaintenance, ContRefact, ContinuousSoftEng`.
:::