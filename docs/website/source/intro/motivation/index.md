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


:::{admonition} PyPackIT's Solution
:class: tip

|{{ ccc.name }}| exploits the full potential of GHA
to enable a cloud-native Agile development process
by providing a full set of ready-to-use and
highly customizable automation pipelines for
[Continuous configuration automation](#overview-cc),
[Continuous integration](#overview-ci) and [deployment](#overview-cd), and 
[Continuous maintenance, refactoring, and testing](#overciew-cm),
designed according to the latest guidelines and engineering best practices
{cite}`HighwaysToCD, ExtremeProgExplained, OopsAnalysisOfTravisCI, ProblemsCausesSolutionsCD, CDSoftIntensive, OnRapidRelease, QualityAndProductivityCI, UsageCostsAndBenefitsOfCI, CIImprovingSoftQualBook, CIBlogPost, ModelingCI, UnderstandingSimilAndDiffinSoftDev, EffectsOfCIOnSoftDev, AgileSoftDevMethodAndPractices, ContinuousSoftEng, CICDSystematicReview`.
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


:::{admonition} PyPackIT's Solution
:class: tip

PyPackIT is built on top of GitHub, making use of its rich functionalities 
to provide a comprehensive environment for collaborative cloud development of research software.

PyPackIT provides an automated development workflow based on a well-tested strategy 
for collaborative research software projects \cite{ConfigManageForLargescaleSciComp}. 
It uses distributed VCSs and issue tracking systems (ITSs) to establish a pull-based development model

PyPackIT makes extensive use of these features to streamline its pull-based development workflow. 
It offers fully designed issue forms based on best practices 
\cite{WhatMakesAGoodBugReport, NeedsInBugReports, QualityOfBugReportsInEclipse}, 
and uses their inputs to automate activities like ticket labeling and organization, 
task assignment, documentation, and creating issue–commit links.
:::



































