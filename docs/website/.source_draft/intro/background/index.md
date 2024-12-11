# Background

Software production is a complex and resource-intensive process
involving multiple phases including planning, development, and operations,
which require a well-coordinated workflow using various tools and technologies
{cite}`CollabSoftEngBookConcepts, StateOfArtInEndUserSoftEng`.

{term}`GHA`

demanding an up-to-date knowledge
of the latest software engineering best practices and methodologies,
as well as a broad range of skills and expertise in communication, project management,
documentation, graphic and web design, user experience, and marketing, to name a few.


To deliver and maintain high-quality software, commercial software organizations
commonly employ specialized teams for each aspect of the development process.
In contrast, the entire responsibility of open-source software projects is typically
borne by small groups of amateur developers, due to funding and staffing constraints.
Consequently, the amount of time, effort, and skills required to produce high-quality open-source software
often far exceeds the capabilities of their developers.
This results in software lacking in terms of accessibility, ease of installation and use,
documentation, interoperability, extensibility, maintainability, and correctness,
which can significantly hinder the adoption and growth of open-source culture.
A representative example is the so-called <i>research software crisis</i> in academia,
especially in various fields of Computational Science and Engineering (CSE).
In these fields, researchers develop and use software as the primary tool for scientific inquiry.
Inevitably, the replicability, validity, and extensibility of computational studies
strongly rely on the availability and quality of the underlying research software.
Given the integral role of computational studies in solving critical real-life problems,
ensuring the quality and sustainability of research software is thus of utmost importance.
However,




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


often faced with challenges regarding funding, time, staffing, and technical expertise \cite{SurveySEPracticesInScience2, HowToSupportOpenSource, ManagingChaos, BetterSoftwareBetterResearch, SoftDevEnvForSciSoft}.

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





## GitHub Social Coding Platform

Software development is becoming a highly collaborative
and distributed process \cite{ScaleAndEvolOfCoordNeeds},
with contributors from diverse geographical and temporal coordinates \cite{GlobalSoftEng}.
These added social aspects increase project complexity \cite{InfluenceOfSocialAndTechnicalFactors},
requiring high degrees of communication and coordination \cite{UnderstandingCommunitySmells, CollabSoftEngBookChallenges, GlobalSoftDevChallenges}.
Consequently, effective collaboration and project management are major challenges in research software development \cite{ConfigManageForLargescaleSciComp}.
Cloud-based software hosting services aim to solve such problems \cite{OpenSourceSoftHostingPlatforms}.
These so-called social coding platforms (SCPs) offer a transparent mutual environment
for communication and collaboration \cite{CharacterizingProjEvolOnSocialCodingPlat, SocialCodingInGitHub},
equipped with crucial software engineering tools,
such as distributed version control systems (VCSs) \cite{VCSReview} like \href{https://git-scm.com/}{Git} \cite{BetterSoftwareBetterResearch, BarelySufficientPracticesInSciComp, BestPracticesInBioinfSoftware, 4SimpleRecs, 10RuleForSoftwareInCompBio, SustainableResearchSoftwareHandOver, SurveySEPracticesInScience, BestPracticesForSciComp, QuickGuideToOrgCompBioProjects, WhatMakesCompSoftSuccessful, GoodEnoughPracticesInSciComp, SciSoftDevIsNotOxymoron}.
\href{https://github.com}{GitHub}, currently the world’s largest SCP \cite{GitHubOctoverse2023},
is thus one of the most recommended platforms
for research software projects \cite{ELIXIRSoftwareManagementPlan, BetterSoftwareBetterResearch, 4SimpleRecs, 10RuleForSoftwareInCompBio, BestPracticesForSciComp, 10SimpleRulesGitAndGitHub},
providing special features for scientific applications and offering free upgrades
to students and academic researchers \cite{GitHubForScience}.
Accordingly, PyPackIT is built on top of GitHub,
making use of its rich functionalities to provide a comprehensive environment
for collaborative cloud development of research software.

Critical to PyPackIT's goals, in November 2019 GitHub introduced \href{https://github.com/features/actions}{GitHub Actions} (GHA),
an event-driven cloud computing platform for execution of automated software development \href{https://docs.github.com/en/actions/using-workflows/about-workflows}{workflows} on configurable machines,
in response to specific \href{https://docs.github.com/en/actions/using-workflows/events-that-trigger-workflows}{events}
like various activities in the repository \cite{GitHubDevWorkflowAutoEcoBook, HandsOnGHA}.
Shortly after its release, GHA became the most popular Continuous Integration (CI) service on GitHub,
due to its generous free tier for public repositories, full integration with GitHub,
and better hardware and software support \cite{RiseAndFallOfCIinGH, OnUsageAndMigrationOfCITools, OnUseOfGHA}.

Moreover, GitHub's comprehensive \href{https://docs.github.com/en/rest}{REST}
and \href{https://docs.github.com/en/graphql}{GraphQL} application programming interfaces (APIs)
grant workflows full control of all repository components,
enabling automation well beyond conventional CI practices \cite{DevPerceptionOfGHA, GitHubDevWorkflowAutoEcoBook}.
To facilitate GHA workflow development,
GitHub allows reusable components called \href{https://docs.github.com/en/actions/creating-actions/about-custom-actions}{Actions},
which act as building blocks for workflows, similar to software libraries.
Developers can host Actions on public GitHub repositories
and publish them on \href{https://github.com/marketplace}{GitHub Marketplace},
an indexing service allowing users to search for suitable options.
However, implementing workflows and Actions is a non-trivial task,
faced by challenges in tooling, resources, configuration, testability,
debugging, maintenance, and security \cite{HowDoSoftDevsUseGHA, EvolutionOfGHAWorkflows, OnUseOfGHA, OnOutdatednessOfWorkflowsInGHA, AutoSecurityAssessOfGHAWorkflows}.

Action reuse is also low, due to issues with compatibility,
functionality, performance, and findability \cite{DevPerceptionOfGHA}.
Therefore, while GHA's automation capabilities can greatly improve
the software development process \cite{HowDoSoftDevsUseGHA, LetsSuperchargeWorkflows},
most projects only use it for basic tasks \cite{OnUseOfGHA}.
On the other hand, PyPackIT makes extensive use of GHA features
and implements specialized workflows and Actions according to research software needs.
These cloud applications fully integrate with other repository components
to create comprehensive automation pipelines that streamline
numerous repetitive engineering and management tasks throughout the software life-cycle.


## Python Programming Language

The choice of programming language greatly influences software adoption and sustainability \cite{RolesOfCodeInCSE}. For scientific software, the language should be fast, stable, predictable, versatile, user-friendly, and well-known \cite{SoftDevEnvForSciSoft, PythonEcosystemSciComp}. While low-level languages like C and Fortran dominate legacy high-performance computing (HPC) due to their speed and hardware integration \cite{SoftEngForCompSci, UnderstandingHPCCommunity, SciCompGridlock}, they fall short in addressing the diverse needs of modern research software \cite{PythonEcosystemSciComp}. Additionally, their complexity can obstruct software extension and maintenance \cite{SoftEngForCompSci, SciCompGridlock}. Therefore, higher-level languages are advised to improve development, collaboration, and productivity \cite{SoftEngForCompSci, BestPracticesForSciComp}. Over the past decade, Python has emerged as the leading programming language for research software development \cite{SurveySEPracticesInScience2, AnalyzingGitHubRepoOfPapers, DevOpsInSciSysDev}, widely adopted by major organizations such as CERN \cite{IntroducingPythonAtCERN, PythonAtCERN} and NASA \cite{PythonAtNASA}, and instrumental in key scientific achievements \cite{PythonScientificSuccessStories}, including the discovery of gravitational waves \cite{GravWaveDiscovery} and black hole imaging \cite{BlackHoleImage}. Python is now the most recommended language for scientific computing due to its simplicity, versatility, and extensive ecosystem \cite{PythonBatteriesIncluded, PythonForSciComp, PythonForSciAndEng, PythonJupyterEcosystem, SciCompWithPythonOnHPC, PythonEcosystemSciComp, WhatMakesPythonFirstChoice}, which provides performance-optimized libraries for array programming \cite{NumPy}, fundamental algorithms \cite{SciPy}, data analysis \cite{pandas}, machine learning \cite{PyTorch, Top5MLLibPython, ScikitLearn}, image processing \cite{scikitImage}, visualization \cite{Matplotlib, Mayavi}, interactive distributed computing \cite{IPython, Jupyter, Jupyter2}, parallel programming \cite{DaskAndNumba, DaskApplications}, and domain-specific scientific applications \cite{Astropy, SunPy, Pangeo, MDAnalysis, Biopython, NIPY}. Python can readily handle complex tasks such as web integration and visualization, which are hard to address in low-level languages \cite{PythonEcosystemSciComp}, while bridging the performance gap via optimized compilers \cite{Cython, Numba, Pythran}, GPU run-time code generators \cite{PyCUDA}, and APIs for integrating low-level languages \cite{PythonForSciComp, PythonEcosystemSciComp}. This adaptability enables rapid prototyping of complex applications, allowing researchers to quickly evaluate various scientific models and efficiently optimize the best solution \cite{BestPracticesForSciComp}. The recent advancements in parallel distributed computing with Python \cite{SciCompWithPythonOnHPC, ParallelDistCompUsingPython, ScientistsGuideToCloudComputing, DemystPythonPackageWithCondaEnvMod, PythonAcceleratorsForHPC} and Jupyter \cite{DistWorkflowsWithJupyter} has even motivated large HPC communities to shift toward Python \cite{SoftEngForCompSci, InteractiveSupercomputingWithJupyter}. Therefore, PyPackIT is specialized in the production of research software in Python, and provides a complete infrastructure and development environment using the latest tools and standards in its ecosystem.

## FAIR Research Software

Research software is a valuable asset that can be readily reused as a building block in numerous computational studies. As software is complex and intangible in nature \cite{MythicalManMonth}, such studies cannot be replicated, verified, or built upon without full access to the underlying source code, input data, and parameters \cite{ReprodResearchInCompSci, AccessibleReproducibleResearch, BarelySufficientPracticesInSciComp, ShiningLight, PublishYourCode, CaseForOpenCompProg}. Despite this, research software has been rarely published \cite{BridgingTheChasm, CaseForOpenCompProg, 4SimpleRecs, PublishYourCode, CompSciError}, leading to controversies \cite{InfluentialPandemicSimulation} and retractions \cite{RetractionCOVID}, preventing software reuse \cite{SurveySEPracticesInScience, SciSoftwareAccuracy}, and forcing scientists to re-implement computational workflows from scratch in each new project \cite{ProblemsOfEndUserDevs, BetterSoftwareBetterResearch}, which is an error-prone process yielding low-quality results \cite{SurveySEPracticesInScience2, SoftEngForCompSci}. In response, widespread appeals have emerged for an open research culture, promoting transparency and reproducibility \cite{PublishYourCode, PromotingOpenResearch, ReprodResearchInCompSci, CaseForOpenCompProg, EnhancingReproducibility, ShiningLight, TroublingTrendsInSciSoftware}. While more publications now include links to source code and data, this is still strongly biased toward a handful of institutions working in specific computer science fields \cite{AnalyzingGitHubRepoOfPapers}. Common obstacles to publishing research software include the lack of efficient mechanisms and tools for packaging, distribution, and indexing \cite{CaseForOpenCompProg, SurveySEPracticesInScience, ReprodResearchInCompSci}, as well as code quality concerns and technical challenges to refactor, document, and maintain the software \cite{BarelySufficientPracticesInSciComp, BetterSoftwareBetterResearch, PublishYourCode}. To sustain scientific progress in CSE, it is thus crucial to address these challenges and ensure that research software is FAIR \cite{FAIR4RS}: findable, accessible, interoperable, and reusable.

Regarding accessibility, many journals now mandate source code submissions for peer-review and public access \cite{RealSoftwareCrisis, DoesYourCodeStandUp, CaseForOpenCompProg, TowardReproducibleCompResearch, MakingDataMaximallyAvailable, JournalOfBioStatPolicy}. It is thus highly recommended to adopt an open-source model from start \cite{BetterSoftwareBetterResearch, PublishYourCode, SurveySEPracticesInScience, BarelySufficientPracticesInSciComp, BestPracticesInBioinfSoftware, POVHowOpenSciHelps, 4SimpleRecs, ELIXIRSoftwareManagementPlan, 10RuleForSoftwareInCompBio}, making the source code freely accessible under a permissive license \cite{BusinessOfOpenSource}. This provides a full record of activities that can be crucial in tracking progress and recognition, enables transparent peer review, promotes trust and adoption, leads to more citations, and improves software quality and sustainability by encouraging community collaboration \cite{SharingDetailedResData, BetterSoftwareBetterResearch, ShiningLight, PublishYourCode, CaseForOpenCompProg, 4SimpleRecs, POVHowOpenSciHelps, BestPracticesInBioinfSoftware, SurveySEPracticesInScience, 10SimpleRulesForOpenDevOfSciSoft, BarelySufficientPracticesInSciComp}. Furthermore, to facilitate findability, research software must be searchable by its functionalities and attributes \cite{10MetricsForSciSoftware}. This requires the distribution of software to related public indexing repositories, along with comprehensive metadata and identifiers \cite{WhatMakesCompSoftSuccessful, HowToSupportOpenSource, 10SimpleRulesForOpenDevOfSciSoft, ELIXIRSoftwareManagementPlan, SustainableResearchSoftwareHandOver, BarelySufficientPracticesInSciComp, 4SimpleRecs}. For reproducibility of research results, each distribution must be permanently available and uniquely indexed with a persistent global identifier that enables reliable citations, such as a Digital Object Identifier (DOI) \cite{BarelySufficientPracticesInSciComp, BestPracticesInBioinfSoftware, ELIXIRSoftwareManagementPlan, BestPracticesInBioinfSoftware, 4SimpleRecs}. To ensure the interoperability and reusability of research software, employing DRY (Don't Repeat Yourself) Principles is encouraged to modularize code into separate methods and routines, organized into a software library with a clear API \cite{FAIR4RS, 10MetricsForSciSoftware, SciSoftDevIsNotOxymoron, 5RecommendedPracticesForCompSci, BestPracticesForSciComp}. As review articles and scientific textbooks provide an overview of recent progress and established knowledge in a field, scientific libraries do the same for code, implementing state-of-the-art algorithms and well-known procedures for use in computational studies \cite{RolesOfCodeInCSE}. Packaging code into software libraries can also greatly simplify the setup process for users \cite{10RuleForSoftwareInCompBio, ELIXIRSoftwareManagementPlan, WhyJohnnyCantBuild}, which is a common problem in research software \cite{NamingThePainInDevSciSoft, CompSciError}. Therefore, PyPackIT is focused on the production of open-source and FAIR scientific Python libraries, and implements automated solutions to facilitate above-mentioned challenges, such as licensing, packaging, distribution, and indexing \cite{BarelySufficientPracticesInSciComp, ELIXIRSoftwareManagementPlan, SustainableResearchSoftwareHandOver, ShiningLight, 10RuleForSoftwareInCompBio}.

## Cloud-Native Development

As research software belongs to an evolving scientific inquiry process, determining the exact requirements and design specifications of the end product is usually not possible in advance \cite{SoftDevEnvForSciSoft, ProblemsOfEndUserDevs}. Consequently, traditional software development methodologies \cite{BalancingAgilityAndDiscipline} are not suitable for research software \cite{DevelopingSciSoft, SurveySEPracticesInScience, SoftEngForCompSci, DealingWithRiskInSciSoft}. Instead, cloud-native practices such as Agile development, Continuous software engineering, and DevOps are highly recommended \cite{AdoptingSoftEngConceptsInSciResearch, HowScientistsDevAndUseSciSoft, SurveySEPracticesInScience, LitRevAgileInSciSoftDev, BestPracticesForSciComp, SciSoftDevIsNotOxymoron}. Agile development \cite{AgileSoftDev, AgileSoftDevMethodAndPractices, AgileSoftDevEcosystems, AgileSoftDevBook} is based on iterative enhancement of software via short inspect-and-adapt cycles and frequent feedback loops, suitable for research software as it typically needs to be constantly modified and evaluated in an experimental manner \cite{WhenEngineersMetScientists, SoftDevEnvForSciSoft}. Embracing the uncertain and evolving nature of research software development \cite{SurveySEPracticesInScience}, Agile methodologies accommodate higher rates of change, allowing for frequent experimentation while reducing variance, complexity, cost, and risk in the development process. Synergistically, Continuous software engineering practices enable projects to stay abreast with the fast-paced nature of Agile methods through automation \cite{ContSoftEngineering, ContinuousSoftEng}. Most common are CI \cite{ExtremeProgExplained, CIBlogPost, EffectsOfCIOnSoftDev}, Continuous Delivery (CDE) \cite{DevDepSecCloudApp, CDReliableSoftReleaseBook, CDHugeBenefits}, and Continuous Deployment (CD) \cite{DeploymentProductionLine, CDatFacebook, CDatFBandOANDA}, which build on top of each other (abbreviated as CI/CD) to eliminate the need for dedicated testing and deployment teams, while increasing the integrity, scalability, security, and transparency of development and deployment pipelines. CI/CD has numerous benefits, including decreased errors, more efficient bug discovery and resolution, and a high level of control over applied changes, allowing projects to produce, release, and maintain higher quality software more rapidly, efficiently, and reliably \cite{UsageCostsAndBenefitsOfCI, CDatFacebook, CICDSystematicReview, EffectsOfCIOnSoftDev, QualityAndProductivityCI, ImpactOfCI, HighwaysToCD, CIImprovingSoftQualBook, ExpBenefitsOfCI, UncoveringBenefitsAndChallengesOfCI, CIBlogPost, ModelingCI, ContinuousSoftEng, ExtremeProgExplained, StairwayToHeaven, CDReliableSoftReleaseBook, CDatFBandOANDA, CDHugeBenefits, StudyImpactAdoptCIOnPR}. Furthermore, DevOps extends Agile and Continuous methodologies by bridging the gap between Development (Dev) and Operations (Ops) phases of the project through automation \cite{WhatIsDevOps}, which has proven useful in research software projects \cite{DevOpsInSciSysDev, ResearchOps}.

Considered crucial in collaborative and distributed software development \cite{EffectsOfCIOnSoftDev, CICDSystematicReview, AnalysisOfTrendsInProductivity}, cloud-native methodologies are widely established in the industry \cite{EmpEvAgile, AgileAdoptionSurvey, CDatFacebook, CDatFBandOANDA, Top10AdagesInCD, ContinuousSoftEng, UsageCostsAndBenefitsOfCI, CICDSystematicReview, HighwaysToCD, StairwayToHeaven, SynthCDPractices, RiseAndFallOfCIinGH, OnUsageAndMigrationOfCITools} and some large research institutes \cite{IntroducingAgileInBioInf, AgileInBioMedSoftDev, UsingAgileToDevCompBioSoft, ExploringXPForSciRes, DevOpsInSciSysDev}. However, their adoption is challenging \cite{ContSoftEngineeringBookStairway} and not prevalent in academia \cite{SurveySEPracticesInScience2, SelfPerceptions, AdoptingSoftEngConceptsInSciResearch}, where most scientists use an impromptu software development process that negatively impacts research software quality \cite{ProblemsOfEndUserDevs, DevelopingSciSoft, SurveySEPracticesInScience}. A major barrier to adoption is implementing Continuous pipelines, which is a complex and costly task \cite{StairwayToHeaven}, faced with challenges such as lack of consensus on a single well-defined standard and limited availability of tools, technologies, instructions, and resources \cite{ModelingCI, CICDSystematicReview, UncoveringBenefitsAndChallengesOfCI}. As ready-to-use solutions are not freely available \cite{CDHugeBenefits}, projects have to either use paid services or spend considerable amounts of time and resources to implement their own pipelines \cite{CICDSystematicReview, HowDoSoftDevsUseGHA, DevPerceptionOfGHA, EffectsOfCIOnSoftDev}. As a result, the majority of open-source projects do not follow Continuous practices \cite{CITheater}, or use outdated \cite{OnOutdatednessOfWorkflowsInGHA} and faulty pipelines that can compromise the development process and introduce security vulnerabilities into the project \cite{AutoSecurityAssessOfGHAWorkflows, AmbushFromAllSides}. Therefore, PyPackIT provides a comprehensive set of ready-to-use CI/CD pipelines according to engineering best practices \cite{HighwaysToCD, ExtremeProgExplained, OopsAnalysisOfTravisCI, ProblemsCausesSolutionsCD, CDSoftIntensive, OnRapidRelease, QualityAndProductivityCI, UsageCostsAndBenefitsOfCI, CIImprovingSoftQualBook, CIBlogPost, ModelingCI, UnderstandingSimilAndDiffinSoftDev, EffectsOfCIOnSoftDev, AgileSoftDevMethodAndPractices, ContinuousSoftEng, CICDSystematicReview}, which run on GHA to automate code integration and software deployment, enabling projects to readily adopt an Agile software development process tailored to research software needs.

## Pull-Based Workflow

Efficient and consistent production of high-quality software requires a well-established workflow to orchestrate the development process \cite{CollabSoftEngBookConcepts, StateOfArtInEndUserSoftEng}. The lack of a streamlined development workflow may be the main reason why research software projects often use a non-standard development process \cite{ProblemsOfEndUserDevs, DevelopingSciSoft, SurveySEPracticesInScience} and are faced with management and maintenance problems \cite{NamingThePainInDevSciSoft, ConfigManageForLargescaleSciComp}. Therefore, PyPackIT provides an automated development workflow based on a well-tested strategy for collaborative research software projects \cite{ConfigManageForLargescaleSciComp}. It uses distributed VCSs and issue tracking systems (ITSs) to establish a pull-based development model \cite{ExplorStudyPullBased, WorkPractPullBased}, which is a bottom-up approach that separates development from integration. It enables the community to spontaneously propose changes to the project via issue tickets and pull requests (PRs), while core maintainers are responsible for reviewing and integrating the work. This accelerates development by promoting community engagement \cite{CharacterizingProjEvolOnSocialCodingPlat}, and facilitates code reviews and feedback loops between developers and maintainers, which is recognized as one of the most effective and crucial quality assessment activities for research software development \cite{5RecommendedPracticesForCompSci, 10MetricsForSciSoftware, BestPracticesForSciComp}. However, pull-based development also requires significant management effort \cite{CharacterizingProjEvolOnSocialCodingPlat}, especially for larger projects \cite{SciSoftDevIsNotOxymoron}. For example, projects need a well-defined governance model that defines the responsibilities and privileges of each member, to facilitate continuous task assignment throughout the software life-cycle \cite{4SimpleRecs, SustainableResearchSoftwareHandOver}. Another crucial aspect is documenting the development process, including plans, requirements, design decisions, and implementation details \cite{WhatMakesCompSoftSuccessful, SciSoftDevIsNotOxymoron, 5RecommendedPracticesForCompSci, BestPracticesForSciComp, BestPracticesInBioinfSoftware}, to provide a clear overview of the project evolution to both users and collaborators, ensuring that the implementation matches the expected design, and preventing the loss of critical knowledge about the software \cite{DealingWithRiskInSciSoft, BestPracticesForSciComp}.

ITSs, one of the most important tools for research software development, simplify pull-based development via functionalities for documentation, organization, and tracking of tasks in the project \cite{SurveySEPracticesInScience, BestPracticesForSciComp, DLRSoftEngGuidelines, 10RuleForSoftwareInCompBio, SciSoftDevIsNotOxymoron}. They offer a communication channel to systematically provide feedback, while recording a searchable history of all submitted issues and their corresponding information, which is crucial for thorough documentation of the software development process \cite{BarelySufficientPracticesInSciComp, ELIXIRSoftwareManagementPlan}. However, \href{https://github.com/features/issues}{GitHub Issues} (GHI), GitHub's free and well-integrated ITS, requires significant configuration and adjustment to enable these features. By default, it only offers a single option for opening issue tickets, asking users for a title and optional description in a free format. This lack of structure leads to problems such as missing crucial information in submitted tickets, which complicates triage for project maintainers \cite{EmpAnalysisOfIssueTemplatesOnGitHub}. To facilitate issue management, GitHub offers labeling features to help categorize, prioritize, and find tickets \cite{GiLaGitHubLabelAnalyzer, ExploringCharacIssueRelatedGitHub}. However, since ticket inputs are not machine readable, labeling must be done manually, which is an error-prone and time-consuming task \cite{WhereIsTheRoadForIssueReports}, and often neglected \cite{GotIssues, ExploringTheUseOfLabels}. Another problem is maintaining the links between tickets and the corresponding commits resolving the issues in the VCS, which is important for tracing changes back to their associated tickets and accompanied documentation and discussion \cite{ConfigManageForLargescaleSciComp}. These also need to be manually created and are often neglected \cite{FillingTheGapsOfDevLogs}, resulting in the loss of a large portion of the project's evolution history \cite{MissingLinksBugsAndBugFix}. Such problems have even motivated the development of machine-learning-based tools for automatic ticket classification \cite{PredictingIssueTypesOnGitHub, ImpactOfDataQualityForAutomaticIssueClassification} and issue–commit link recovery \cite{IssueCommitLink-DeepLink, FRLink}. Recently, GitHub also added new templating features to GHI, allowing projects to define separate submission options for issue types, which improves ticket organization and reduces triage workload for developers \cite{FirstLookAtBugReportTempOnGitHub, UnderstandingIssueTemplateOnGitHub}. Moreover, in 2021 GitHub introduced \href{https://github.blog/changelog/2021-06-23-issues-forms-beta-for-public-repositories/}{issue forms}, enabling projects to build structured web forms with rich input types such as dropdown menus, checkboxes, and text fields. This allows the collection of required user inputs in a structured and machine-readable format and leads to significant improvements in resolution time \cite{EmpAnalysisOfIssueTemplatesOnGitHub}. PyPackIT makes extensive use of these features to streamline its pull-based development workflow. It offers fully designed issue forms based on best practices \cite{WhatMakesAGoodBugReport, NeedsInBugReports, QualityOfBugReportsInEclipse}, and uses their inputs to automate activities like ticket labeling and organization, task assignment, documentation, and creating issue–commit links.

Another important aspect of the development workflow are version control practices \cite{10MetricsForSciSoftware, ELIXIRSoftwareManagementPlan} such as branching, which provides isolation for simultaneous development and maintenance of multiple software versions \cite{ImportanceOfBranchingModels}. For example, to support cloud-native development, short-lived branches are used to implement new changes, which are then merged into stable branches that contain production-ready code \cite{CICDSystematicReview}. While crucial for software development, branching is considered one of the most problematic practices of VCSs \cite{EffectOfBranchingStrategies}. The suitability of a branching model is also project-dependent, resulting in a variety of different strategies \cite{BranchUseInPractice}. Although several well-established models exist \cite{TrunkBasedDev, GitFlow, GitHubFlow, GitLabFlow}, they are not fully aligned with the needs of research software, which is typically first released as a proof-of-concept prototype and can undergo multiple significant changes after its initial publication \cite{UnderstandingHPCCommunity}. This requires a branching model that enables the development, release, and long-term maintenance of multiple versions of the software in parallel, to facilitate rapid evolution while ensuring the reproducibility and sustainability of the scientific results based on earlier releases \cite{ConfigManageForLargescaleSciComp}. In accordance with these requirements, PyPackIT includes automated version control in the development workflow, complete with a specialized branching model and version scheme.

## Quality Assurance and Testing

Given the integral role of computational studies in solving critical real-life problems, ensuring the reliability and correctness of scientific software is of utmost importance. As software bugs can lead to incorrect scientific results \cite{CompSciError}, software testing is one of the most crucial practices in research software development \cite{BestPracticesForSciComp, 5RecommendedPracticesForCompSci, BestPracticesInBioinfSoftware, SurveySEPracticesInScience, ELIXIRSoftwareManagementPlan, DLRSoftEngGuidelines}. It is highly recommended to use test-driven development methodologies and perform frequent testing from the beginning of the development cycle, thus preventing the accumulation of errors into complex problems \cite{10SimpleRulesOnWritingCleanAndReliableSciSoft, SciSoftDevIsNotOxymoron, SurveySEPracticesInScience}. This is especially important for research software \cite{EmpStudyDesignInHPC}, in which deviations from expected behavior may also occur due to the underlying scientific model, making it harder to identify the root cause of problems \cite{SoftDevEnvForSciSoft}. Thus, unit tests must be written parallel to code implementation, verifying the accuracy of individual code components in isolation \cite{BarelySufficientPracticesInSciComp}. They can also be used in regression testing, which is crucial for ensuring that features remain functional after each modification \cite{10SimpleRulesOnWritingCleanAndReliableSciSoft, BestPracticesForSciComp}. To ensure testing effectiveness, test coverage metrics must be monitored to identify code components and software functionalities that are not covered by the available test cases \cite{DLRSoftEngGuidelines, 10SimpleRulesOnWritingCleanAndReliableSciSoft}. To improve reproducibility and increase trust in the software \cite{ELIXIRSoftwareManagementPlan, DLRSoftEngGuidelines}, users must also be able to run the tests on their machines to asses the functionality and performance of their local installation \cite{10MetricsForSciSoftware, BestPracticesInBioinfSoftware}. To facilitate this, all tests and corresponding data should be organized into a software package \cite{BestPracticesInBioinfSoftware}, called test suite, and distributed along instructions on how to run it and information about the testing methodology \cite{BarelySufficientPracticesInSciComp, 10MetricsForSciSoftware}.

In addition to testing, static code analysis tools such as linters and type checkers must also be used to check for violations and other potential issues in the code \cite{DLRSoftEngGuidelines, BestPracticesForSciComp}. These tools help with refactoring as well, improving code quality, performance, and maintainability \cite{SurveySEPracticesInScience, 10SimpleRulesOnWritingCleanAndReliableSciSoft}. Moreover, to facilitate readability, which is a key factor in collaboration and peer review \cite{BestPracticesForSciComp}, code formatting tools must be used to establish a consistent coding style according to best practices \cite{BestPracticesForSciComp, NLeScienceSoftDevGuide}. Importantly, to ensure that these practices are consistently performed, they must be automated in the project's development workflow \cite{BestPracticesForSciComp, 10MetricsForSciSoftware, 10SimpleRulesOnWritingCleanAndReliableSciSoft}. This is a challenging task that often prevents adequate code quality assurance and testing \cite{StairwayToHeaven}, specially in research software projects \cite{TestingResearchSoftwareSurvey, SoftEngForCompSci} as they lack management support \cite{SurveySEPracticesInScience} and skills in modern software engineering and testing methodologies  \cite{HowScientistsDevAndUseSciSoft, SurveySEPracticesInScience2, ProblemsOfEndUserDevs}. Consequently, while more than half of scientists' programming time is spent on debugging code \cite{SurveySEPracticesInScience2}, only primitive methods are used that are slow, ineffective, and prone to errors \cite{SurveySEPracticesInScience2, SoftEngForCompSci, SurveySEPracticesInScience}. As code quality assurance and testing practices are usually neglected \cite{CompSciError, ProblemsOfEndUserDevs, SurveySEPracticesInScience2, SoftwareChasm}, research software may contain inapparent issues that do not interrupt the execution of the program, but result in incorrect outputs that compromise scientific findings \cite{CompSciError}. Such errors have caused numerous retractions \cite{NightmareRetraction, RetractionChang, RetractionMa, RetractionChang2, RetractionJAmCollCardiol, RetractionMeasuresOfCladeConfidence, RetractionsEffectOfAProgram}, corrections \cite{CorrectionHypertension}, and comments \cite{CommentOnError, CommentOnError2, CommentOnError3, CommentOnError4, CommentOnError5, ClusterFailureFMRI}, even in high-profile publications. Therefore, there is a current need for promoting and facilitating standard code analysis, formatting, and testing practices in research software engineering \cite{TestingResearchSoftwareSurvey, ApproxTowerInCompSci, SoftEngForCompSci} Accordingly, PyPackIT offers a fully automated quality assurance and testing infrastructure for the entire development life-cycle, fulfilling all requirements, including coverage monitoring, documentation, and test-suite distribution.

## Documentation

One of the main determining factors of software quality and success is documentation \cite{HowToSupportOpenSource, 10SimpleRulesForOpenDevOfSciSoft, BestPracticesForSciComp, GoodEnoughPracticesInSciComp, DLRSoftEngGuidelines, NLeScienceSoftDevGuide, SurveySEPracticesInScience, WhatMakesCompSoftSuccessful}. It must provide clear information on how to install and execute the software, how each part works, and how to use them correctly, thus ensuring that the capabilities and limitations of the software are understood and exploited in the intended way by its users \cite{WhatMakesCompSoftSuccessful, SciSoftDevIsNotOxymoron, ELIXIRSoftwareManagementPlan, SurveySEPracticesInScience, NamingThePainInDevSciSoft, CompSciError, BestPracticesInBioinfSoftware, BarelySufficientPracticesInSciComp, 10RuleForSoftwareInCompBio}. This is especially important for research software, where knowledge about the project is continuously lost \cite{EmpStudyDesignInHPC, SoftwareSustainabilityInstitute} due to high developer turnover rates \cite{RecommendOnResearchSoftware}. Moreover, as the software evolves, it is crucial to document all important changes in each new release compared to its earlier version. This information must be published along each release, allowing users to evaluate the update impact on their projects. Additionally, it must be recorded chronologically in a so-called \href{https://keepachangelog.com}{changelog}, providing an overview of the software evolution to new users and contributors \cite{ELIXIRSoftwareManagementPlan, GoodEnoughPracticesInSciComp, SustainableResearchSoftwareHandOver}. As building a community is crucial for research software success \cite{WhatMakesCompSoftSuccessful}, equally important as user documentation is providing collaborators with project information \cite{SurveySEPracticesInScience, BestPracticesForSciComp, BestPracticesInBioinfSoftware} including contribution guidelines, governance model, and code of conduct \cite{SustainableResearchSoftwareHandOver, GoodEnoughPracticesInSciComp, 4SimpleRecs, ELIXIRSoftwareManagementPlan}.

Producing and maintaining high-quality documentation requires significant time, effort, and skills \cite{SurveySEPracticesInScience}. In addition to writing large amounts of content, developers typically need to design, develop, and deploy a website to present the documentation in an accessible, coherent, and user-friendly format \cite{WhatMakesCompSoftSuccessful}. This is a non-trivial task, requiring a broad knowledge of web development concepts and tools, including HTML, CSS, and JavaScript, as well as web hosting services and practices. Moreover, the documentation website must always reflect the latest state of the project, requiring developers to periodically update and maintain it after each change. To facilitate software documentation, several tools and practices have been developed \cite{TenSimpleRulesForDocumentingSciSoft}. For example, it is recommended to embed the documentation of code components next to their source code, as specially annotated comments called docstrings \cite{WhatMakesCompSoftSuccessful, BestPracticesForSciComp}. The developers can then use a static site generator like \href{https://www.sphinx-doc.org}{Sphinx} to generate a website that includes the library's API documentation, automatically extracted from these comments \cite{SurveySEPracticesInScience, TenSimpleRulesForDocumentingSciSoft}. While such tools can greatly simplify the process, developers still need to invest a lot of time and effort to find, learn, set up, and configure them. Consequently, research software is typically not well-documented \cite{CompSciError, SoftEngForCompSci, ProblemsOfEndUserDevs, AnalyzingGitHubRepoOfPapers, DealingWithRiskInSciSoft}. This is one of the most common barriers to using available research software \cite{HowScientistsReallyUseComputers, HowScientistsDevSciSoftExternalRepl}, a typical cause of software misuse leading to faulty scientific results \cite{CompSciError}, and one of the main reasons why researchers refrain from publishing their software \cite{InfluentialPandemicSimulation, BetterSoftwareBetterResearch}. Therefore, PyPackIT puts great emphasis on documentation, providing infrastructure and automated solutions that enable projects to maintain high-quality documentation with minimal effort.

## Maintenance

Modern research software can often remain useful and operational for decades \cite{SoftwareSustainabilityInstitute, SoftEngForCompSci}. Thus, considering the amounts of time and effort required to develop high-quality software, it is important to sustain the available options \cite{BarelySufficientPracticesInSciComp}. This requires active maintenance \cite{SoftEngForCompSci}: The project must continuously receive feedback from its community to fix existing issues, improve functionalities, and add missing features \cite{SoftwareSustainabilityInstitute}. This is more crucial for research software, which also needs to reflect scientific advances \cite{SoftDevEnvForSciSoft}. Maintaining software dependencies \cite{FortyYearsOfSoftwareReuse} is another important aspect \cite{EmpComparisonOfDepNetEvolution}: To facilitate usability, scientific software libraries must be compatible with diverse computer environments, requiring them to remain functional with future dependency versions. However, most projects are unaware of their outdated dependencies and do not update them regularly \cite{DoDevsUpdateDeps}, leading to incompatibilities, bugs, and other issues in the software \cite{MeasuringDepFreshness, ThouShaltNotDepend, OnImpactOfSecVulnInDepNet}. Research software maintenance is particularly hindered by short-term funding options \cite{ManagingChaos, BetterSoftwareBetterResearch}, small team sizes \cite{SoftEngForCompSci, HowScientistsReallyUseComputers}, high turnover rates \cite{RecommendOnResearchSoftware, EmpStudyDesignInHPC}, and the fact that it does not lead to new publications \cite{SoftEngForCompSci}. Another main barrier is technical debt \cite{BetterSoftwareBetterResearch, ProblemsOfEndUserDevs, SoftEngForCompSci}: Neglecting software engineering best practices during the development considerably increases the workload of performing new tasks \cite{ManagingTechnicalDebt}, causing each new modification to further increase the software entropy \cite{10SimpleRulesForOpenDevOfSciSoft, SoftDesignForEmpoweringSci} and create new technical debt, making maintenance increasingly harder \cite{ManagingChaos, SoftwareSustainabilityInstitute}. Consequently, the extra time and effort required for maintenance is one of the main reasons for not publicly releasing research software \cite{BetterSoftwareBetterResearch, PublishYourCode}, which is often abandoned as an unsustainable prototype, not usable in future research projects \cite{SustainableResearchSoftwareHandOver, 10RuleForSoftwareInCompBio, PublishYourCode}. To prevent these issues, quality assurance and maintenance tasks should be automated and enforced from the beginning of the project \cite{SoftEngForCompSci}. PyPackIT achieves this by several mechanisms, including its automated pull-based development model that promotes collaboration and feedback, CI/CD pipelines that enforce software engineering best practices throughout the development process, and Continuous Maintenance (CM) \cite{ContinuousMaintenance}, Refactoring (CR) \cite{ContRefact}, and Testing (CT) \cite{ContinuousSoftEng} pipelines (abbreviated as CM/CR/CT) that periodically perform various automated tasks, such as updating dependencies and development tools, to maintain the health of the software and its development environment.

## Configuration

Software projects usually contain multiple data files
declaring metadata and settings for different project components.
The requirement for each tool to have its own configuration file
in a specific format and location complicates maintenance and organization.
Additionally, redundancy arises as some data is reused within and across projects,
hindering the rapid and reliable modification of configurations \cite{BestPracticesForSciComp}.
Manual adjustments via interactive interfaces further complicate configuration tracking and replicability,
making consistent production and management of software projects a challenge \cite{DevOpsInSciSysDev}.
To solve such issues, DevOps practices such as Infrastructure-as-Code (IaC)
and Continuous Configuration Automation (CCA) have been developed to enable dynamic configuration management
of software infrastructures using machine-readable definition files \cite{InfrastructureAsCode}.
PyPackIT implements a similar mechanism to facilitate the definition, customization, synchronization,
and maintenance of all project metadata and settings.
It provides a user-friendly control center that renders the entire project infrastructure
and development environment dynamic, enabling automatic project management and configuration.




# OLD


employing engineering best practices often fails due to a lack of supporting tools,
which places an additional implementation burden on scientists \cite{ConfigManageForLargescaleSciComp}.
Therefore, an ideal solution must be readily accessible and adoptable by all scientists,
enabling them to immediately employ research software engineering best practices with minimal overhead \cite{ManagingChaos, SoftEngForCompSci}.


The most common problems faced by amateur software developers are technical issues
regarding management, tooling, testing, documentation, deployment, and maintenance of software.



While being crucial for the ultimate success of the software project,
many aspects of the development process are not directly related
to the idea and vision behind the project itself,
and are rather repetitive, time-consuming and tedious chores
that can be automated and streamlined
to save time and effort for the development team,
allowing them to solely focus on the creative aspects of their work.


Thus, automation tools that streamline such repetitive engineering tasks according to research software needs
can significantly accelerate development, improve quality, and lower production costs at the same time.





These often act as significant barriers to smaller independent projects
that lack dedicated teams for each aspect of the development process,
inadvertently hampering innovation and growth within the Python community.


these challenges can act as significant barriers that render the goal of rapid development, publishing,
and maintenance of professional and effective software a non-trivial task,
inadvertently hampering innovation and growth within the diverse Python community.

These challenges render the goal of rapid development, publishing,
and maintenance of professional and effective Python software a non-trivial task,
particularly for smaller teams or projects that lack dedicated developers for each step of the process.

This can act as a significant barrier to producing sustainable software that can be
effortlessly and reliably used by other practicing researchers in the field,
resulting in a limited potential for building upon existing work,
and hampering the overall progress of scientific research across the diverse fields of computational sciences.


open-source projects, such as scientific software produced in academia,
are often faced with challenges regarding funding and staffing.


The Python programming language and its vibrant ecosystem have made software development
more accessible and efficient than ever before, enabling a diverse community of users,
from professional developers and researchers, to amateur programmers and enthusiasts,
to promptly implement their novel ideas and share their valuable work with the world.
In addition, the rise of comprehensive cloud-based services like GitHub has undeniably revolutionized
the software development process, making it easier to collaborate on projects and share code,
and streamlining the process of building, testing, documenting, deploying, and maintaining software.

However, despite these significant advancements, the current landscape of Python software development
is still not without its challenges; In addition to a unique and valuable idea and the ability to implement it into code,
proper development, distribution, and maintenance of useful, credible and high-quality software packages
is a complex and multi-faceted process,
involving numerous steps and





Although several tools and resources are available
to help developers with some of the involved tasks in isolation,
to the best of our knowledge, there is currently no comprehensive solution
that can seamlessly automate and streamline the entire software development process.
Therefore, developers still need to have a broad understanding of the various aspects involved,
to know which tools to use and how to configure them correctly,
and spend a significant amount of time and effort to find the right combination of tools and services,
only to be able to cover a small subset of the requirements.


This underscores the need for a fully automated, plug-and-play software project management tool,
which enables aspiring and experienced developers alike to rapidly build professional software,
readily share them with the world, and effortlessly maintain their projects,
thereby empowering the development of open-source Python projects.


To address these challenges, we introduce {{ ccc.name }},
a fully automated, plug and play, professional software project management solution
for open-source Python packages on GitHub.
It provides a comprehensive, professional, and robust infrastructure for all main components of a project,
including GitHub/Git repository, Python package, test suite,
and documentation website, according to the latest standards and best practices.
{{ ccc.name }} is a free and open-source software built on top of GitHub Actions,
and offered as a GitHub repository template that can be readily utilized
by new and existing projects.
It comes with an exhaustive set of fully-configured
continuous integration, deployment, and testing (CI/CD/CT) workflows
that automate and streamline the entire journey of creating, documenting, testing, publishing,
and maintaining Python packages, and render the entire project fully dynamic.
By eliminating all the tedious, repetitive, and time-consuming
peripheral aspects of the software development process,
{{ ccc.name }} enables aspiring and experienced developers alike to rapidly build professional software,
readily share them with the world, and effortlessly maintain their projects,
thereby empowering the development of open-source Python projects,
and fueling innovation and growth in the ecosystem.

The following sections discuss several challenges in the current landscape of software development,
which often act as significant barriers to smaller development teams,
inadvertently hampering innovation and growth within the Python community.
The focus is on common tasks and chores that are an essential part of every software development process;
these are often repetitive, time-consuming and tedious tasks
that require a significant amount of effort and resources,
and a broad range of skills and expertise to perform correctly.
While being crucial for the successful development and maintenance of every software,
these tasks are not directly related to the idea and vision behind the project itself,
and are rather chores that can be automated and streamlined to save time and effort
for the development team, allowing them to solely focus on the creative aspects of their work.



The rise of high-level, versatile programming languages, such as Python,
and the emergence of comprehensive cloud-based VCS platforms, such as GitHub,
have made software development more accessible and efficient than ever before.



## GitHub

The growth of the Python ecosystem and its open-source libraries has been further accelerated
by the emergence of cloud-based platforms for version control systems (VCSs),
such as [GitHub](https://github.com),
which marked a significant shift in how software is developed, shared, and maintained.
Their purpose is to facilitate collaborative software development,
by providing a centralized location for storing code, tracking changes,
and managing contributions from multiple developers.
They are especially crucial for open-source projects,
where developers from various backgrounds contribute to a shared codebase,
and feedback from the community is an integral part of the development process.

GitHub, launched in 2008, has quickly risen to prominence
as the world's largest host of source code,
with more than 100 million developers working on over 372 million repositories,
as of November 2023.[^github-stats]
In addition to its user-friendly interface, GitHub offers an extensive set of features
that have solidified its position in the software development landscape, including:
- **Version Control**: At its core, GitHub provides git-based version control,
  enabling developers to track changes, revert to previous states,
  and manage different versions of their code efficiently.
- **Issue Tracking**: GitHub includes an issue tracking system that allows developers
  to report bugs, request features, and discuss improvements within the platform.
- **Collaboration Tools**: Features such as pull requests, code reviews, and branch management
  facilitate collaboration among developers, making it easier to contribute to and maintain projects.
- **Automation Tools**: GitHub allows for building continuous integration, deployment, and
  testing (CI/CD/CT) pipelines, enabling automatic testing, building, and deployment of software projects,
  directly from GitHub repositories and without the need for third-party platforms.
- **Web Hosting**: GitHub provides free web hosting for static websites stored in GitHub repositories,
  making it easier to publish documentation and other project-related content.
- **Integration**: GitHub can be readily integrated with various development tools and services,
  enhancing its utility in different stages of software development.

[^github-stats]: [GitHub (2023). Octoverse: The state of open source and rise of AI in 2023.](https://github.blog/2023-11-08-the-state-of-open-source-and-ai/)

## Repository Setup

As one of the first steps in starting a new software project,
setting up a GitHub repository is a crucial part of the development process;
it lays the foundation for the project's structure and workflows,
and sets the general tone for the entire development lifecycle.
The role of the repository extends far beyond just code hosting;
it often acts as the central headquarters for the project,
where the team members meet to lay out the roadmap,
contribute code, review each other's work, discuss issues and new ideas,
maintain the project, and plan for the future.
The repository also serves as the main storefront and the public face of the project,
where users can learn about the software and track its progress,
provide feedback, and contribute to its development.
Therefore, having a robust and professional GitHub repository is
one of the key requirements for a successful software project,
influencing its development and maintainability,
affecting its visibility and accessibility to potential contributors and users,
and ultimately, determining its overall adoption, growth, and longevity.

Considering the integral and multifaceted role of the GitHub repository in software projects,
setting up a professional and robust repository involves numerous steps,
and requires a broad range of knowledge and expertise,
not only on GitHub and its various features, configurations, and options,
but also on every aspect of software development and maintenance,
and a variety of other subjects, such as graphic design, user experience, security,
community and project management, and marketing.
Large and well-established organizations often have dedicated teams for each of these aspects,
who can work together to set up and maintain a professional repository for their projects.
However, for smaller teams or individual developers,
who may not have the necessary resources or expertise to perform these tasks,
this can be a daunting and time-consuming process,
involving a steep learning curve and a significant amount of effort and resources.

While several tools and resources are available
to help developers with some of the involved tasks in isolation,
to the best of our knowledge, there is currently no comprehensive solution
that can automate and streamline the entire process.
Therefore, developers still need to have a broad understanding of the various aspects involved,
to know which tools to use and how to configure them correctly,
and spend a significant amount of time and effort to find the right combination of tools and services,
only to be able to cover a small subset of the requirements.

The following is a list of some of the most important aspects that must be considered
when setting up a GitHub repository for a software project:

- [**Accessibility**]{.primary-color}: For a project to be successful,
  it must first be easily discoverable by its target audience.
  This is especially important for independent projects that do not have the backing of a large organization,
  where the repository acts as the first point of contact for potential users and collaborators.
  Developers can increase the visibility of their projects by adding an expressive description
  and a list of related [keywords](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/classifying-your-repository-with-topics)
  (aka topics) to the repository, which are used by GitHub to categorize the project,
  and help users better find it through various
  [search](https://docs.github.com/en/search-github/searching-on-github/searching-for-repositories)
  and [filtering](https://docs.github.com/en/search-github/searching-on-github/searching-topics) options.
- [**Appearance**]{.primary-color}: The appearance of the repository is another important factor
  that can influence the first impression of potential users and collaborators.
  Next to the repository's description and keywords,
  its main [README file](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes),
  which is automatically displayed on the repository's homepage,
  is usually the first thing that users notice when they visit the repository.
  Acting as the front page of the repository,
  it is thus crucial to have an informative, engaging, and visually appealing README
  that captures the attention of visitors and provides them with a clear overview of the project.
  Ideally, a well-structured README should also include dynamic information,
  such as various statistics and status indicators that are automatically updated
  to reflect the current state of the project.
  However, GitHub requires READMEs to be written in
  [GitHub Flavored Markdown](https://github.github.com/gfm/),
  and performs additional post-processing and sanitization after rendering the contents to HTML,
  due to security concerns.
  This means that only a [limited subset of HTML features](https://docs.github.com/en/get-started/writing-on-github)
  are supported, with no support for CSS or JavaScript,
  which makes creating visually appealing and dynamic READMEs
  a non-trivial and challenging task for many developers.
  Another often neglected aspect is
  [adding a custom Open Graph image](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/customizing-your-repositorys-social-media-preview)
  to the repository, to improve its appearance on platforms with [Open Graph](https://ogp.me/) support,
  such as social media and search engines.
- [**Structure**]{.primary-color}: The directory structure of the repository defines the layout
  and the overall organization of the project; it is an important factor that can have a significant impact
  on the development process and maintainability of the project.
  A well-structured repository should have a clear directory structure,
  with a logical separation between different components of the project,
  and a consistent and standardized naming scheme for files and directories.
  This makes it easier for developers to navigate the repository,
  locate the relevant files, and understand the overall structure of the project.
  In addition, GitHub and many other tools and services that are commonly used in the project development
  process rely on the repository's structure to locate and identify various components of the project.
  This requires developers to follow a specific directory structure and naming scheme
  when setting up their repositories, so that these tools can locate the relevant files and directories
  needed for their operation.
  Moreover, the repository structure is one of the first things that users notice when visiting the repository,
  and thus plays a vital role in establishing the project's credibility and professionalism.
- [**Security**]{.primary-color}: Security is a crucial aspect of software development,
  and should be considered at every stage of the development process.
  This is especially important for open-source projects,
  where the source code is publicly available and can be accessed by anyone.
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
- [**License**]{.primary-color}: The license of a software project defines the terms and conditions
  under which the software can be used, modified, and distributed.
  It is an important aspect of software development, as it determines the legal status of the project,
  and can have a significant impact on its adoption and growth.
  A suitable license protects the rights of the creator while encouraging use and contribution from others.
  Therefore, it is crucial for developers to carefully choose a license that best suits their needs,
  and correctly [add it to the repository](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/licensing-a-repository#applying-a-license-to-a-repository-with-a-license-file)
  so that GitHub can automatically detect and display it on the repository's homepage,
  making it clear to users and collaborators
  under which terms they can use and contribute to the project.
- [**Maintenance**]{.primary-color}: Maintaining a software project is an ongoing process,
  which requires developers to regularly update the code and fix any issues that may arise.
  It is crucial to have a well-defined maintenance process in place,
  to ensure that the project is maintained in an effective and organized manner.
  An integral part of the development and maintenance process is the issue tracking system,
  where users and developers can report bugs, and request new features and other changes
  in the software and other components of the project.
  Professional repositories have a well-defined issue tracking system in place,
  with structured issue forms that guide contributors in providing the necessary details
  in a consistent standardized format.
  Equally important is a comprehensive labeling system to categorize and organize issues and pull requests.
  This makes it easier for maintainers to prioritize and manage issues,
  helps collaborators to find issues that they can contribute to,
  and facilitates efficient searching and tracking of the software's problems and progress by users.
  [GitHub Issues](https://docs.github.com/en/issues/tracking-your-work-with-issues/about-issues)
  is a built-in feature that is available for all GitHub repositories,
  and can be [configured](https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/configuring-issue-templates-for-your-repository)
  to provide a comprehensive issue tracking system for the project,
  with well-structured [issue forms](https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/syntax-for-issue-forms)
  that can be customized according to the needs of the project.
  Developers can also define a set of [labels](https://docs.github.com/en/issues/using-labels-and-milestones-to-track-work/managing-labels)
  for their GitHub repository, to categorize issues, pull requests, and discussions.
  Moreover, to further streamline the maintenance process,
  each issue form can be configured to automatically add a set of labels to the issue,
  along with a pre-defined set of assignees responsible for handling the issue.
- [**Support**]{.primary-color}: Maintaining a healthy and sustainable project
  involves more than just code management;
  providing support for users and contributors is another important aspect
  of software development, especially for open-source projects.
  It is crucial for developers to provide a clear and accessible way
  for the community to ask questions and discuss various topics related to the project, share their ideas,
  and participate in the decision-making process that shapes the future of the project.
  This can be achieved by adding a [GitHub Discussions](https://docs.github.com/en/discussions/collaborating-with-your-community-using-discussions/about-discussions)
  section to the repository, which provides a forum for community engagement and collaboration,
  fostering an environment where ideas, challenges, and solutions can be shared openly.
  It can be configured to organize discussions into various sections and categories,
  and add well-thought-out templates to each category to
  maintain a consistent and organized environment,
  and guide users on how to effectively participate in the discussions.
- [**Community**]{.primary-color}: Building a strong and vibrant community is an essential part
  of every project, as it fosters collaboration and innovation,
  and helps ensure the long-term sustainability of the project.
  To help build and maintain a healthy and collaborative environment for their open-source projects,
  GitHub allows developers to add a set of predefined [community health files](https://docs.github.com/en/communities/setting-up-your-project-for-healthy-contributions/creating-a-default-community-health-file)
  to their repositories.
  When properly configured, links to these files are automatically displayed on the repository's homepage
  and various other related pages in the repository, making them easily accessible to the community,
  and ensuring that they are aware of the project's policies and guidelines. These files include:
  - [Code of Conduct](https://docs.github.com/en/communities/setting-up-your-project-for-healthy-contributions/adding-a-code-of-conduct-to-your-project):
    Defining standards for how to engage in the community,
    expected behavior, and the consequences of violating these standards.
    It is an important aspect of community management, as it helps establish a safe and welcoming environment
    for all community members, and ensures that everyone is treated with respect and dignity.
  - [Contributing Guidelines](https://docs.github.com/en/communities/setting-up-your-project-for-healthy-contributions/setting-guidelines-for-repository-contributors):
    Providing clear instructions and guidelines for how to contribute to the project,
    from opening issues for reporting bugs and requesting new features or changes,
    to implementing the code and submitting pull requests.
    This helps ensure that contributions are made in a consistent manner
    and are compatible with the project's workflow,
    thus saving time and effort for both the contributors and the maintainers.
  - [Security Policy](https://docs.github.com/en/code-security/getting-started/adding-a-security-policy-to-your-repository):
    Detailing the security disclosure policy of the project for users and security researchers/auditors,
    providing instructions on how to securely report security vulnerabilities in the project,
    clarifying the exact steps that are taken to handle and resolve the issue,
    and the expected response time.
  - [Support Resources](https://docs.github.com/en/communities/setting-up-your-project-for-healthy-contributions/adding-support-resources-to-your-project):
    Providing information and resources on how to get help with the project,
    such as asking questions about the software,
    requesting clarifications and further information on various aspects of the project,
    reporting potential bugs and issues, and requesting new features or changes.
    This makes it easier for users to find the relevant resources,
    and helps reduce the number of duplicate issues and questions.
  - [Governance Model](https://docs.github.com/en/communities/setting-up-your-project-for-healthy-contributions/creating-a-default-community-health-file#supported-file-types):
    Defining the governance model of the project, including the roles and responsibilities of the maintainers,
    the decision-making process, and the criteria for becoming a maintainer.
    This helps establish a clear and transparent governance model for the project,
    and provides a framework for the community to participate in the decision-making process.
- [**Funding**]{.primary-color}: Securing funding enables developers
  to dedicate more time and resources to their projects,
  and helps ensure the long-term sustainability of the project.
  This is especially an important challenge for independent open-source projects,
  where developers often rely on donations from users and sponsors to fund their work.
  GitHub allows projects to include [funding options](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/displaying-a-sponsor-button-in-your-repository)
  directly on their repository homepage, to increase their visibility and open avenues for financial support.
  Funding options can be configured for various platforms,
  including [GitHub Sponsors](https://docs.github.com/en/sponsors/getting-started-with-github-sponsors/about-github-sponsors),
  several pre-defined external platforms such as [Tidelift](https://tidelift.com/) and [Patreon](https://www.patreon.com/),
  and any other platform of choice.

## Development Workflow

:::{admonition} 🚧 Under Construction 🚧
:class: danger

This subsection is currently under construction.
:::

In addition, a well-structured repository should also have a clear and consistent workflow,
  and a well-defined process for reviewing and merging contributions.
  This helps streamline the development process,
  and makes it easier for new contributors to get started with the project.

- **Continuous Integration and Deployment**: Continuous integration and deployment (CI/CD) pipelines
  automate the process of building, testing, and deploying software,
  enabling developers to quickly and efficiently release new versions of their projects.
- [**Workflow**]{.primary-color}: The development workflow defines the exact process
  by which changes are made to the project, from the initial idea to the final implementation.
  It is crucial for developers to have comprehensive and well-defined workflows in place,
  to ensure that changes are made in a consistent and organized manner.
- **Branching Model**: The branching model of the repository must be designed
    to support the development workflow of the project.
    For example, the repository may follow a [Gitflow](https://nvie.com/posts/a-successful-git-branching-model/)
    branching model, where the `master` branch is used for stable releases,
    and the `develop` branch is used for development.
    Alternatively, it may follow a [GitHub Flow](https://guides.github.com/introduction/flow/)
    branching model, where the `master` branch is used for development,
    and releases are tagged from the `master` branch.

## Packaging and Distribution

For software to be usable by others,
it must first be [packaged](https://packaging.python.org/en/latest/overview/) in a standardized format
and distributed on an online software repository (aka package index),
which provides a centralized location for publishing and sharing packages,
so that users can find, download, and install it on their systems.
There are two major software repositories for Python packages:
- [Python Package Index (PyPI)](https://pypi.org/): The official software repository for Python,
  run by the [Python Software Foundation (PSF)](https://www.python.org/psf-landing/).
- [Anaconda.org](https://anaconda.org/): A language-agnostic platform
  with support for multiple programming languages, which makes it a popular choice
  for publishing Python packages with non-Python dependencies,
  as is often the case for scientific software.

Each of these platforms has its own package management system,
which is the software that users use to download and install packages from the repository:
- [pip](https://pip.pypa.io/en/stable/): The official package manager for Python,
  maintained by the [Python Packaging Authority (PyPA)](https://www.pypa.io/en/latest/),
  and the recommended tool for downloading, installing, and managing packages from PyPI.
- [conda](https://docs.conda.io/en/latest/)
  (and its more performant twin, [mamba](https://mamba.readthedocs.io/en/latest/)):
  Cross-platform package managers for Python and other programming languages,
  used to download, install, and manage packages from Anaconda.org.

The packaging and distribution process involves several steps:
1. The source code must first be structured into one or several
   [import packages](https://packaging.python.org/en/latest/glossary/#term-Import-Package),
   to ensure that it can be seamlessly imported and used by other Python projects.
   This requires developers to follow a specific directory structure and naming scheme,
   so that the package and its components can be correctly recognized
   by the package manager and the Python interpreter.

   For example, a typical Python application containing a single top-level import package
   has a hierarchical directory structure; the top-level directory must at least contain
   a special file called `__init__.py`, which is used to mark the directory as a package,
   and can be used to define a namespace and execute package initialization code.
   The name of this directory defines the import name of the package,
   and must adhere to the [naming conventions](https://www.python.org/dev/peps/pep-0008/#package-and-module-names)
   defined in PEP 8. All the source code of the package must be placed inside this directory,
   organized into subpackages and modules, which can be further nested to any depth.
2. A variety of instructions, requirements, and metadata must be provided
   in several configuration files, each with its own syntax and standardized format,
   to ensure that the package can be correctly built, recognized and installed by the package manager.
   These include:
   - [**Build System Specifications**]{.primary-color}: Instructions for the package manager
     on how to build and install the package from source, such as the build backend to use
     (e.g., [setuptools](https://setuptools.pypa.io),
     [hatch](https://hatch.pypa.io),
     [flit](https://flit.pypa.io),
     [poetry](https://python-poetry.org),
     [pdm](https://pdm-project.org)),
     additional build dependencies, and the commands to run.
     These must adhere to a standardized format defined in
     [PEP 517](https://www.python.org/dev/peps/pep-0517/) and
     [PEP 518](https://www.python.org/dev/peps/pep-0518/).
   - [**Build Backend Configurations**]{.primary-color}: Specific configurations
     for the selected build backend, such as the location of the source code,
     files to include/exclude, and how to handle different aspects of the build process.
     The exact format and syntax of these configurations depend on the selected build backend.
   - [**Name**]{.primary-color}: The name of the package on the online repository,
     used by the package manager to uniquely identify and locate the package.
     The package name must follow the [PyPA specifications](https://packaging.python.org/en/latest/specifications/name-normalization/)
     introduced in [PEP 503](https://peps.python.org/pep-0503/#normalized-names)
     and [PEP 508](https://peps.python.org/pep-0508/#names).
   - [**Version**]{.primary-color}: The version identifier of the package, used by the package manager
     to identify and install the correct version of the package.
     It must be a valid public version identifier according to the
     [PyPA specifications](https://packaging.python.org/en/latest/specifications/version-specifiers/#version-specifiers)
     first introduced in [PEP 440](https://www.python.org/dev/peps/pep-0440/),
     and must be incremented for every new release of the package,
     following [specific rules](https://packaging.python.org/en/latest/specifications/version-specifiers/#version-ordering-across-different-metadata-versions).
   - [**Python Version**]{.primary-color}: The minimum Python version required by the package,
     used by the package manager to ensure that the package is compatible with the user's Python interpreter.
     It must be a valid version specifier according to the
     [PyPA specifications](https://packaging.python.org/en/latest/specifications/version-specifiers/#id4),
     and must be incremented whenever the package drops support for older Python versions.
   - [**Dependencies**]{.primary-color}: The required and optional dependencies of the package
     (i.e., other software that the package depends on to function correctly),
     which are automatically installed by the package manager along with the package.
     These must be specified in a standardized format defined in
     [PEP 508](https://www.python.org/dev/peps/pep-0508/),
     and must be kept up to date and synchronized with the dependencies used in the source code.
   - [**Entry Points**]{.primary-color}: The entry points of the package,
     such as console scripts, GUI scripts, and other callable objects,
     which are automatically registered by the package manager and made available to the user.
     These must follow the [PyPA specifications](https://packaging.python.org/en/latest/specifications/entry-points/),
     and must refer to actual objects (e.g., functions) defined in the source code.

   In addition, several other metadata must be provided so that the online package index
   can correctly categorize and display the package, facilitating its discovery by users,
   and providing them with a clear overview of the project.
   These include:
   - [**Description**]{.primary-color}: A short description of the package,
     which is displayed on the package index and used by the package manager
     to provide a brief overview of the project.
   - [**Keywords**]{.primary-color}: A list of keywords describing the package,
     which are used by the package index to categorize the package,
     and help users find it through various search and filtering options.
   - [**License**]{.primary-color}: The license of the package,
     so that users can know under which terms they can use the project.
   - [**Authors and Maintainers**]{.primary-color}: Names and emails of the
     authors and maintainers of the package,
     so that users can know who is responsible for the project and how to contact them.
   - [**Project URLs**]{.primary-color}: A list of URLs related to the project,
     such as the project's homepage, documentation, source code, issue tracker, and changelog,
     which are displayed on the package index and used by the package manager
     to provide users with additional information and resources for the project.
   - [**Classifiers**]{.primary-color}: A list of [Trove classifiers](https://pypi.org/classifiers/)
     as defined in [PEP 301](https://peps.python.org/pep-0301/#distutils-trove-classification),
     to describe each release of the package (e.g., development status, supported Python versions and operating systems,
     project topics, intended audience, natural language, license, etc.).
     These standardized classifiers are used by the package index to categorize the package,
     and help users find it through various search and filtering options.
   - [**README**]{.primary-color}: A README file similar to the repository's README,
     containing a detailed and up-to-date description of the package,
     which is displayed on the package index to provide users with a clear overview of the project.
     As the first thing that users notice when viewing the project on the package index,
     it is crucial to have an informative, engaging, and visually appealing README
     that captures the attention of visitors and provides them with all the necessary information
     and resources for the project.
     Both PyPI and Anaconda.org support markup languages such as Markdown and reStructuredText
     for defining the contents of the README file.
     However, like GitHub, they impose several restrictions on the supported features,
     and perform additional post-processing and sanitization after rendering the contents to HTML.
     For example, PyPI uses the [Readme Renderer](https://github.com/pypa/readme_renderer) library
     to render the README file, which only supports a limited subset of HTML
     [tags](https://github.com/pypa/readme_renderer/blob/9c2eb81301bc230f2795cf7e6dc2c23f5815ea41/readme_renderer/clean.py#L20-L31)
     and [attributes](https://github.com/pypa/readme_renderer/blob/9c2eb81301bc230f2795cf7e6dc2c23f5815ea41/readme_renderer/clean.py#L33-L65).
     Since these do not completely overlap with the features supported by GitHub,
     a separate [PyPI-friendly README](https://packaging.python.org/en/latest/guides/making-a-pypi-friendly-readme/)
     must be provided for PyPI, to ensure that the contents are correctly rendered on the package index.
3. The import package(s) must be transformed into
   [distribution packages](https://packaging.python.org/en/latest/glossary/#term-Distribution-Package),
   which are versioned archives containing the import packages and other required files and resources.
   Distribution packages are the files that are actually uploaded to the online package index,
   to be downloaded and installed for the end-users via the package manager.
   There are two major distribution formats for Python packages:
   - [**Source Distributions**](https://packaging.python.org/en/latest/glossary/#term-Source-Distribution-or-sdist):
     Source distributions (aka sdist) are `tar.gz` archive files providing the source code of the package,
     along with the required configuration files, metadata, and resources
     that are needed for generating various built distributions.
   - [**Built Distributions**](https://packaging.python.org/en/latest/glossary/#term-Built-Distribution):
     Built distributions are [binary archives](https://packaging.python.org/en/latest/specifications/binary-distribution-format/)
     containing files and metadata that only need to be moved to the correct location on the target system,
     to be installed.
     Currently, PyPI/pip uses the [Wheel](https://packaging.python.org/en/latest/glossary/#term-Wheel) format
     (originally introduced in [PEP 427](https://www.python.org/dev/peps/pep-0427/),
     replacing the older [Egg](https://packaging.python.org/en/latest/glossary/#term-Egg) format),
     while Anaconda/conda uses the
     [`.conda` format](https://docs.conda.io/projects/conda/en/latest/user-guide/concepts/packages.html#conda-file-format)
     superseding the older `.tar.bz2` format.
     These can be either platform-independent or platform-specific,
     depending on whether the package is pure Python or contains compiled extensions
     (cf. [pure-Python wheels](https://packaging.python.org/en/latest/guides/distributing-packages-using-setuptools/#pure-python-wheels) for pip,
     and [Noarch Packages](https://docs.conda.io/projects/conda/en/latest/user-guide/concepts/packages.html#noarch-packages) for conda).

   PyPA [recommends](https://packaging.python.org/en/latest/tutorials/packaging-projects/#generating-distribution-archives)
   always uploading a source distribution to PyPI,
   along with one or more built distributions for each supported platform.
   These can be generated using the [build](https://github.com/pypa/build)
   (for source distributions and pure-Python wheels)
   and [cibuildwheel](https://github.com/pypa/cibuildwheel) (for platform-specific wheels)
   packages provided by PyPA.
   Similarly, conda built distributions can be generated using the
   [conda-build](https://github.com/conda/conda-build) package provided by the [conda community](https://conda.org/).
4. The distribution packages must be uploaded to the online package index,
   so that users can find, download, and install them on their systems.
   - For PyPI, this requires developers to create an account on the platform,
     generate an API token for authentication,
     and use the [twine](https://github.com/pypa/twine/) library to upload the packages.
     Alternatively, [trusted publishing](https://docs.pypi.org/trusted-publishers/)
     ([OpenID Connect](https://openid.net/developers/how-connect-works/) standard) can be used
     in conjunction with the [PyPI publish GitHub Action](https://github.com/pypa/gh-action-pypi-publish)
     to publish packages directly from GitHub Actions, without the need for an API token.
   - Similarly, for Anaconda.org, developers must [create an account](https://docs.anaconda.com/free/anacondaorg/user-guide/work-with-accounts/)
     on the platform and use the [anaconda-client](https://github.com/Anaconda-Platform/anaconda-client) library
     to [upload the package](https://docs.anaconda.com/free/anacondaorg/user-guide/packages/conda-packages/#uploading-conda-packages)
     to their Anaconda.org repository/channel.
     However, distributing packages through personal repositories/channels is not recommended,
     as it requires users to manually add the repository/channel to their conda configuration,
     and does not provide any guarantees on the availability and reliability of the package.
     Instead, developers are encouraged to use the [conda-forge](https://conda-forge.org/)
     community repository, which provides a curated collection of high-quality packages
     that are automatically built and tested on a variety of platforms.
     Conda-forge has its own process for [contributing packages](https://conda-forge.org/docs/maintainer/adding_pkgs.html),
     which involves submitting a [conda-build recipe](https://docs.conda.io/projects/conda-build/en/stable/concepts/recipe.html)
     to the [staged-recipes repository](https://github.com/conda-forge/staged-recipes) on GitHub,
     where it is reviewed and tested by the community before being merged into the repository.
     Once merged, the package is automatically built and uploaded to the conda-forge channel,
     and made available to the users.

Correctly performing all these steps requires developers to have a comprehensive understanding
of the packaging and distribution process in the Python ecosystem,
and the various tools and best practices involved.
Since PyPI and Anaconda.org are independent platforms with their own package management systems,
developers must also be familiar with the specific requirements and nuances of each platform.
For example, most configurations and metadata for PyPI/pip must be provided
in a declarative fashion using the [TOML](https://toml.io) format in a file named
[`pyproject.toml`](https://packaging.python.org/en/latest/specifications/pyproject-toml/),
while Anaconda/conda uses the [YAML](https://yaml.org/) format to define metadata in a file named
[`meta.yaml`](https://docs.conda.io/projects/conda-build/en/stable/resources/define-metadata.html),
and requires [build scripts](https://docs.conda.io/projects/conda-build/en/stable/resources/build-scripts.html)
to be defined separately for Linux/macOS and Windows in `build.sh` and `bld.bat` files, respectively.
Moreover, due to the rapidly evolving standards in the Python ecosystem,
developers must constantly keep up to date with the latest changes
to ensure that their workflows are compatible with the current guidelines and best practices.
For example, the `pyproject.toml` file was first introduced
in 2016 in [PEP 518](https://www.python.org/dev/peps/pep-0518/),
and only established as a standard in 2021,
after the acceptance and implementation of
[PEP 621](https://www.python.org/dev/peps/pep-0621/) and
[PEP 660](https://www.python.org/dev/peps/pep-0660/),
to replace the older `setup.py` and
[`setup.cfg`](https://setuptools.pypa.io/en/latest/userguide/declarative_config.html) files.
In addition, since many of the packaging and distribution steps must be repeated for every release,
developers must maintain a detailed overview of the whole process and all the places
where each piece of information is used, and update them accordingly whenever necessary.
All these make the packaging and distribution process a time-consuming and error-prone task,
hampering the development process and slowing down the release cycle of the project.
Therefore, there is a need for a comprehensive solution that can automate and streamline
the entire packaging and distribution process, from start to finish,
to save time and effort for the developers, and ensure that the process is carried out correctly.


For the TOML file format,
see [Learn TOML in Y Minutes](https://learnxinyminutes.com/docs/toml/), or check out the
full specification at [toml.io](https://toml.io/en/v1.0.0).

## Quality Assurance and Testing


Code quality assurance and testing are crucial aspects of every software development process,
ensuring that the code is correct, functional, secure, robust,
reliable, maintainable, and sustainable {cite}`CompSciError`.
It is highly recommended to use test-driven development methodologies and perform frequent testing
from the beginning of the development cycle,
thus preventing the accumulation of errors into complex problems {cite}`10SimpleRulesOnWritingCleanAndReliableSciSoft`.
Thus, unit tests must be written parallel to code implementation,
verifying the accuracy of individual code components in isolation.
They can also be used in regression testing, which is crucial for ensuring that features remain functional
after each modification.
To ensure testing effectiveness, test coverage metrics must be monitored to identify code components
and software functionalities that are not covered
by the available test cases.
To improve reproducibility and increase trust in the software,
users must also be able to run the tests on their machines to assess the functionality and performance
of their local installation {cite}`10MetricsForSciSoftware`.
To facilitate this, all tests and corresponding data should be
organized into a software package, called test suite, and distributed along instructions on how to run it
and information about the testing methodology.

In addition to testing, static code analysis tools such as linters and type checkers
must also be used to check for violations and potential issues in the code.
These tools help with refactoring as well, improving code quality, performance,
and maintainability.
Moreover, to facilitate readability, which is a key factor in collaboration
and peer review, code formatting tools must be used to
establish a consistent coding style according to best practices {cite}`BestPracticesForSciComp`.
Importantly, to ensure that these practices are consistently performed,
they must be automated in the project's development workflow.
This is a challenging task that often prevents adequate code quality assurance and testing {cite}`StairwayToHeaven`,
specially in open-source research software projects {cite}`TestingResearchSoftwareSurvey`
as they lack management support and skills in
modern software engineering and testing methodologies {cite}`HowScientistsDevAndUseSciSoft, ProblemsOfEndUserDevs`.
Consequently, while more than half of scientists' programming time is spent on debugging code,
only primitive methods are used that are slow, ineffective, and prone to errors {cite}`SurveySEPracticesInScience2, SurveySEPracticesInScience`.
As code quality assurance and testing practices are usually neglected,
open-source software may contain inapparent issues that do not interrupt the execution of the program,
but result in incorrect outputs that compromise scientific findings \cite{CompSciError, SoftwareChasm}.
Such errors have caused numerous
retractions {cite}`NightmareRetraction, RetractionChang, RetractionMa, RetractionChang2, RetractionJAmCollCardiol, RetractionMeasuresOfCladeConfidence, RetractionsEffectOfAProgram`,
corrections {cite}`CorrectionHypertension`,
and comments {cite}`CommentOnError, CommentOnError2, CommentOnError3, CommentOnError4, CommentOnError5, ClusterFailureFMRI`,
even in high-profile publications.
Therefore, there is a current need for promoting and facilitating standard code analysis, formatting,
and testing practices in research software engineering \cite{TestingResearchSoftwareSurvey, ApproxTowerInCompSci, SoftEngForCompSci}.
Accordingly, PyPackIT offers a fully automated quality assurance and testing infrastructure
for the entire development life-cycle, fulfilling all requirements, including coverage monitoring,
documentation, and test-suite distribution.



These encompass a wide range of activities and practices, from formatting and static code analysis routines,
to various dynamic testing methods, such as unit testing, integration testing, and end-to-end testing:

- [**Formatting**]{.primary-color}: The Python interpreter imposes little to no restrictions
  on the formatting of the source code, such as naming conventions,
  annotations, indentation, line length, whitespace, and other layout and styling aspects.
  This can lead to vastly different formatting styles between developers,
  preventing them from easily following, reviewing, and maintaining each other's code.
  Therefore, it is important for developers to follow a consistent code style,
  especially in open-source collaborative projects, where the code is publicly available
  and the long-term sustainability of the project depends on the contributions from the community.
  Code formatting in Python has been greatly simplified by the introduction of
  a standardized style guide in the [Python Enhancement Proposal (PEP) 8](https://peps.python.org/pep-0008/),
  and the availability of powerful automated code formatting tools, such as
  [Black](https://github.com/psf/black) and [YAPF](https://github.com/google/yapf).
- [**Linting**]{.primary-color}: Static code analysis, also known as linting,
  is the process of analyzing the source code without actually executing it.
  It is usually the first line of defense in ensuring code quality,
  used to detect security vulnerabilities, syntax errors, suspicious constructs, and potential bugs;
  enforce styling rules; identify unused variables and imports, and perform various other checks.
  The Python ecosystem offers several powerful linting tools, such as
  [Pylint](https://github.com/pylint-dev/pylint), [Flake8](https://github.com/PyCQA/flake8),
  and [Bandit](https://github.com/PyCQA/bandit).
  More recently, [Ruff](https://github.com/astral-sh/ruff) has emerged as a rapidly growing
  and promising alternative, offering up to 100x performance improvement over existing tools.
  Written in Rust, Ruff not only introduces its own set of unique features,
  but also implements most functionalities of other linters and code formatters; as of version 0.1.7,
  Ruff can be used as a drop-in replacement for Flake8, Isort, and Black,
  while full parity with Pylint and Bandit is expected in the near future.
  More importantly, Ruff is able to automatically fix a number of issues it detects,
  in contrast to other linters that only report the issues and require manual intervention.
- [**Type Checking**]{.primary-color}: While Python is a dynamically typed language,
  it supports optional type annotations, as introduced in [PEP 484](https://www.python.org/dev/peps/pep-0484/).
  These can be extremely useful for documenting the code, and improving its readability and maintainability,
  especially in larger projects.
  More importantly, they can be used by type checking tools, such as [Mypy](https://github.com/python/mypy),
  which perform static code analysis to detect type-related errors in the code that may otherwise go unnoticed.
- [**Testing**]{.primary-color}: As one of the most important aspects of software development,
  dynamic testing refers to the process of executing the code with a given set of test cases
  to validate its functionality and correctness.
  As the complexity of software projects increases,
  it becomes increasingly difficult to ensure that the software behaves as expected in all possible scenarios,
  and that changes do not introduce new bugs or break existing functionalities.
  Therefore, it is crucial to have a comprehensive test suite in place,
  to ensure that the code is thoroughly tested and validated before being released.
  [Pytest](https://github.com/pytest-dev/pytest) is one of the most well-known testing frameworks
  for Python projects, allowing developers to write various types of tests for their software,
  including unit tests, integration tests, end-to-end tests, and functional tests.
  These can then be incorporated in the development workflows of the project,
  to ensure the integrity and functionality of the code at every stage of the development process.

While the Python ecosystem offers a comprehensive set of powerful tools to help developers
carry out these tasks, successfully integrating them into the development process
can be challenging and time-consuming, especially in the current rapidly evolving landscape:
Developers must maintain a broad and up-to-date overview
of the various tools and best practices involved,
to select the right set of tools for their project.
These tools usually offer a wide range of configuration options, which must be carefully set
to ensure that they are compatible with the project's workflow.
Integrating multiple tools, each with its own configuration and usage nuances,
into a single coherent workflow can be complex.
Ensuring that these tools work seamlessly together,
and with the project's existing infrastructure, requires significant setup and maintenance effort.
Additionally, balancing the strictness of rules
against the practicality of day-to-day development is a nuanced task.
More importantly, enforcing coding standards and testing practices
across all contributors can be challenging in collaborative projects.
It requires clear guidelines and often the implementation of automated checks
that are integrated into the development workflow,
such as pre-commit hooks or continuous integration pipelines.

## Documentation

One of the main determining factors of software quality and success is documentation {cite}`WhatMakesCompSoftSuccessful`.
It must provide clear information on how to install and execute the software,
how each part works, and how to use them correctly,
thus ensuring that the capabilities and limitations of the software are understood
and exploited in the intended way by its users.
This is especially important for open-source software,
where knowledge about the project is continuously lost
due to high developer turnover rates {cite}`RecommendOnResearchSoftware`.
Moreover, as the software evolves, it is crucial to document
all important changes in each new release compared to its earlier version.
This information must be published along each release,
allowing users to evaluate the update impact on their projects.
Additionally, it must be recorded chronologically in a so-called [changelog](https://keepachangelog.com),
providing an overview of the software evolution to new users and contributors.
As building a community is crucial for research software success,
equally important as user documentation is providing new collaborators
with project information including contribution guidelines, governance model,
and code of conduct.

Producing and maintaining high-quality documentation requires significant time, effort, and skills.
In addition to writing large amounts of content, developers typically need to design,
develop, and deploy a website to present the documentation in an accessible,
coherent, and user-friendly format.
This is a non-trivial task, requiring a broad knowledge of web development concepts and tools,
including HTML, CSS, and JavaScript, as well as web hosting services and practices.
Moreover, the documentation website must always reflect the latest state of the project,
requiring developers to periodically update and maintain it after each change.
To facilitate software documentation,
several tools and practices have been developed {cite}`TenSimpleRulesForDocumentingSciSoft`.
For example, it is recommended to embed the documentation of code components next to their source code,
as specially annotated comments called docstrings.
The developers can then use a static site generator like \href{https://www.sphinx-doc.org}{Sphinx}
to generate a website that includes the library's API documentation,
automatically extracted from these comments.
While such tools can greatly simplify the process,
developers still need to invest a lot of time and effort to find, learn, set up, and configure them.
Consequently, open-source software is typically not well-documented {cite}`AnalyzingGitHubRepoOfPapers`.
This is one of the most common barriers to using available options {cite}`HowScientistsReallyUseComputers, HowScientistsDevSciSoftExternalRepl`,
a typical cause of software misuse leading to faulty results {cite}`CompSciError`,
and one of the main reasons why developers refrain from publishing their software {cite}`BetterSoftwareBetterResearch`.
Therefore, PyPackIT puts great emphasis on documentation,
providing infrastructure and automated solutions that enable projects to maintain
high-quality documentation with minimal effort.

## Maintenance

Modern software can often remain useful and operational for decades {cite}`SoftEngForCompSci`.
Thus, considering the amounts of time and effort required to develop high-quality software,
it is important to sustain the available options. This requires active maintenance:
The project must continuously receive feedback from its community
to fix existing issues, improve functionalities, and add missing features.
Maintaining software dependencies is another important aspect {cite}`FortyYearsOfSoftwareReuse`:
To facilitate usability, software libraries must be compatible with diverse computer environments,
requiring it to remain functional with future dependency versions {cite}`EmpComparisonOfDepNetEvolution`.
However, most projects are unaware of their outdated dependencies
and do not update them regularly {cite}`DoDevsUpdateDeps`, leading to incompatibilities, bugs,
and other issues in the software {cite}`MeasuringDepFreshness, ThouShaltNotDepend, OnImpactOfSecVulnInDepNet`.
Another main barrier is technical debt {cite}`ManagingTechnicalDebt`:
Neglecting software engineering best practices during the development considerably increases the workload
of performing new tasks, causing each new modification
to further increase the software entropy and create new technical debt,
making maintenance increasingly harder.
Consequently, the extra time and effort required for maintenance is one of the main reasons
for not publicly releasing software {cite}`BetterSoftwareBetterResearch, PublishYourCode`,
which is often abandoned as an unsustainable prototype, not usable in future projects {cite}`PublishYourCode`.
To prevent these issues, quality assurance and maintenance tasks should be automated
and enforced from the beginning of the project {cite}`SoftEngForCompSci`.
{{ ccc.name }} achieves this by several mechanisms, including its automated pull-based development model
that promotes collaboration and feedback, CI/CD pipelines that enforce software engineering best practices
throughout the development process, and Continuous Maintenance (CM) {cite}`ContinuousMaintenance`,
Refactoring (CR) {cite}`ContRefact`, and Testing (CT) {cite}`ContinuousSoftEng`
pipelines (abbreviated as CM/CR/CT) that periodically perform various automated tasks,
such as updating dependencies and development tools,
to maintain the health of the software and its development environment.

## Configuration Management

Software projects usually contain multiple data files
declaring metadata and settings for different project components.
The requirement for each tool to have its own configuration file
in a specific format and location complicates maintenance and organization.
Additionally, redundancy arises as some data is reused within and across projects,
hindering the rapid and reliable modification of configurations {cite}`BestPracticesForSciComp`.
Manual adjustments via interactive interfaces further complicate configuration tracking and replicability,
making consistent production and management of software projects a challenge {cite}`DevOpsInSciSysDev`.
To solve such issues, DevOps practices such as Infrastructure-as-Code (IaC)
and Continuous Configuration Automation (CCA) have been developed
to enable dynamic configuration management of software infrastructures
using machine-readable definition files {cite}`InfrastructureAsCode`.
{{ ccc.name }} implements a similar mechanism to facilitate the definition, customization,
synchronization, and maintenance of all project metadata and settings.
It provides a user-friendly control center that renders the entire project infrastructure
and development environment dynamic, enabling automatic project management and configuration.
