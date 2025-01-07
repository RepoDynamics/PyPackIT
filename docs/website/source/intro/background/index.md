# Background

Nevertheless, research software engineering remains a complex and multi-faceted practice, requiring a broad range of skills and expertise, and an up-to-date knowledge of the ever-evolving standards and best practices. In contrast to the industry, academic research groups often lack the luxury of dedicated software engineering teams to aid with the numerous technical and non-scientific aspects of the process. This can act as a significant barrier to producing sustainable software that can be effortlessly and reliably used by other practicing researchers in the field, resulting in a limited potential for building upon existing work, and hampering the overall progress of scientific research across the diverse fields of computational sciences. 


## Cloud-Native Automation

Research software often faces evolving requirements and specifications so that determining the exact requirements and specifications of the end product is usually not possible in advance \cite{SoftDevEnvForSciSoft, ProblemsOfEndUserDevs}. Consequently, as traditional development methodologies may not accommodate effectively for research software \cite{DevelopingSciSoft, SoftEngForCompSci, DealingWithRiskInSciSoft, BalancingAgilityAndDiscipline}, cloud-native practices such as Agile development, Continuous software engineering, and DevOps are recommended \cite{AdoptingSoftEngConceptsInSciResearch, LitRevAgileInSciSoftDev, BestPracticesForSciComp}.
Agile development \cite{AgileSoftDev}, based on iterative enhancement and short feedback cycles, aligns well with the experimental nature of research software \cite{WhenEngineersMetScientists, SoftDevEnvForSciSoft, SurveySEPracticesInScience}, effectively managing high rates of change, complexity, and risk \cite{AgileSoftDevMethodAndPractices, AgileSoftDevEcosystems}. In tandem, Continuous software engineering practices including Continuous Integration (CI), Continuous Delivery (CDE), and Continuous Deployment (CD)—collectively called CI/CD—enhance the efficiency, scalability, and reliability of Agile development through automation \cite{ContSoftEngineering, ContinuousSoftEng, CICDSystematicReview}. They provide numerous benefits, including decreased errors, more efficient bug discovery, and a high level of control over applied changes, allowing projects to produce higher quality software more rapidly, efficiently, and reliably \cite{UsageCostsAndBenefitsOfCI, CDatFacebook, EffectsOfCIOnSoftDev, QualityAndProductivityCI, ImpactOfCI, ExpBenefitsOfCI, UncoveringBenefitsAndChallengesOfCI, ModelingCI, ExtremeProgExplained, StairwayToHeaven, CDReliableSoftReleaseBook, CDatFBandOANDA, CDHugeBenefits, StudyImpactAdoptCIOnPR}. DevOps extends these practices by automating the integration of Development (Dev) and Operations (Ops) phases, further benefiting research software projects \cite{WhatIsDevOps, DevOpsInSciSysDev, ResearchOps}. While cloud-native methodologies are considered crucial \cite{EffectsOfCIOnSoftDev, CICDSystematicReview, AnalysisOfTrendsInProductivity} and are well-established in industry \cite{EmpEvAgile, AgileAdoptionSurvey, Top10AdagesInCD, SynthCDPractices} and some large research institutions \cite{IntroducingAgileInBioInf, AgileInBioMedSoftDev, UsingAgileToDevCompBioSoft, ExploringXPForSciRes}, their adoption in academia presents opportunities for growth \cite{SurveySEPracticesInScience2, SelfPerceptions, AdoptingSoftEngConceptsInSciResearch, DevelopingSciSoft}. As implementing Continuous pipelines is complex and ready-to-use solutions are scarce \cite{ModelingCI, CICDSystematicReview, UncoveringBenefitsAndChallengesOfCI, StairwayToHeaven, CDHugeBenefits, HowDoSoftDevsUseGHA, DevPerceptionOfGHA, EffectsOfCIOnSoftDev}, many open-source projects are in need of solutions to integrate cloud-native practices \cite{CITheater, AutoSecurityAssessOfGHAWorkflows, AmbushFromAllSides, OnOutdatednessOfWorkflowsInGHA}. \href{https://github.com}{GitHub} offers public repositories free integration with \href{https://github.com/features/actions}{GitHub Actions} (GHA), an event-driven cloud computing platform for execution of automated software development \href{https://docs.github.com/en/actions/using-workflows/about-workflows}{workflows}, modularizable into reusable components called \href{https://docs.github.com/en/actions/creating-actions/about-custom-actions}{Actions} \cite{GitHubDevWorkflowAutoEcoBook, HandsOnGHA}. Currently the most popular CI/CD service on GitHub \cite{RiseAndFallOfCIinGH, OnUsageAndMigrationOfCITools, OnUseOfGHA}, GHA grants workflows full control of all repository components, enabling automation well beyond conventional CI/CD practices \cite{DevPerceptionOfGHA, GitHubDevWorkflowAutoEcoBook}. However, implementing GHA workflows and Actions involves challenges related to tooling, configuration, testability, debugging, maintenance, and security \cite{HowDoSoftDevsUseGHA, EvolutionOfGHAWorkflows, OnOutdatednessOfWorkflowsInGHA, AutoSecurityAssessOfGHAWorkflows}. Consequently, most projects do not make use of these advanced features that can greatly improve the software development process \cite{OnUseOfGHA, LetsSuperchargeWorkflows}.


## Collaborative Workflow

Software development is increasingly collaborative and distributed, requiring a robust workflow for effective communication and coordination \cite{ScaleAndEvolOfCoordNeeds, GlobalSoftEng, InfluenceOfSocialAndTechnicalFactors, UnderstandingCommunitySmells, GlobalSoftDevChallenges, ConfigManageForLargescaleSciComp, CollabSoftEngBookConcepts, StateOfArtInEndUserSoftEng}. Many research software projects suffer from management and maintenance issues due to lacking workflows \cite{ProblemsOfEndUserDevs, DevelopingSciSoft, SurveySEPracticesInScience, NamingThePainInDevSciSoft, ConfigManageForLargescaleSciComp}. Cloud-based social coding platforms (SCPs) address these challenges by providing essential software engineering tools in a transparent mutual environment \cite{OpenSourceSoftHostingPlatforms, CharacterizingProjEvolOnSocialCodingPlat, SocialCodingInGitHub}, including distributed version control systems (VCSs) like \href{https://git-scm.com/}{Git} \cite{VCSReview}. GitHub, currently the largest SCP \cite{GitHubOctoverse2023}, is especially recommended for research projects \cite{10RuleForSoftwareInCompBio, BestPracticesForSciComp, 10SimpleRulesGitAndGitHub} as it provides special features like software citation and free upgrades for academic use \cite{GitHubForScience}. GitHub's pull-based development workflow offers an effective solution by enabling community contributions through issuing tickets and pull requests (PRs), while maintainers review and integrate changes \cite{ExplorStudyPullBased, WorkPractPullBased, CharacterizingProjEvolOnSocialCodingPlat}. 
This accelerates development and enhances code quality through reviews \cite{5RecommendedPracticesForCompSci, 10MetricsForSciSoftware, BestPracticesForSciComp}, but also requires careful management in terms of task assignment, issue–commit linkage, and documentation \cite{WhatMakesCompSoftSuccessful, DealingWithRiskInSciSoft, 5RecommendedPracticesForCompSci, CharacterizingProjEvolOnSocialCodingPlat, SciSoftDevIsNotOxymoron, 4SimpleRecs, SustainableResearchSoftwareHandOver, ConfigManageForLargescaleSciComp}. Issue tracking systems (ITSs) like GitHub Issues (GHI) help document and organize tasks, but need significant setup to function effectively \cite{SurveySEPracticesInScience, DLRSoftEngGuidelines, ELIXIRSoftwareManagementPlan, EmpAnalysisOfIssueTemplatesOnGitHub}. By default, GHI only offers a single option for opening unstructured issue tickets, which can lead to problems such as missing crucial information that complicate issue triage \cite{EmpAnalysisOfIssueTemplatesOnGitHub}. To facilitate issue management, GitHub offers labeling features to help categorize and prioritize tickets \cite{GiLaGitHubLabelAnalyzer, ExploringCharacIssueRelatedGitHub}. However, these tasks must be done manually, which is time-consuming and prone to errors \cite{WhereIsTheRoadForIssueReports, GotIssues, ExploringTheUseOfLabels, FillingTheGapsOfDevLogs, MissingLinksBugsAndBugFix}, motivating the development of machine-learning tools for automatic ticket classification \cite{PredictingIssueTypesOnGitHub, ImpactOfDataQualityForAutomaticIssueClassification} and issue–commit link recovery \cite{IssueCommitLink-DeepLink, FRLink}. Recently, GitHub introduced  \href{https://github.blog/changelog/2021-06-23-issues-forms-beta-for-public-repositories/}{issue forms}; customizable web forms that enable the collection of machine-readable user inputs \cite{EmpAnalysisOfIssueTemplatesOnGitHub, FirstLookAtBugReportTempOnGitHub, UnderstandingIssueTemplateOnGitHub}. While they can be used in conjunction with GHA to automate issue management tasks without the need for machine-learning tools, these capabilities are often not exploited due to the initial implementation barrier.


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

