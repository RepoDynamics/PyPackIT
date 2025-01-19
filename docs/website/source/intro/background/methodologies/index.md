(bg-methodologies)=
# Software Development Methodologies

Software development methodologies are structured frameworks 
that guide the planning, execution, and delivery of software projects. 
These methodologies define best practices, processes, and principles 
to ensure the development of high-quality software 
that meets user requirements and business objectives. 
Over the decades, software development methodologies have evolved 
to adapt to technological advancements and growing project complexities, 
transitioning from rigid, linear models to more flexible and adaptive approaches.

The earliest methodologies, such as the Waterfall Model, 
followed a strict sequence of phases, 
which worked well for predictable and well-defined projects. 
However, as software systems became more complex 
and user requirements more dynamic, 
these models showed significant limitations. 
This led to the emergence of iterative and incremental models, 
Agile methodologies, and modern cloud-native practices, 
which emphasize collaboration, flexibility, and rapid delivery.

Software development methodologies can be broadly categorized into 
**Traditional Methodologies**, **Agile Methodologies**, and **Cloud-Native Practices**. 
Each category incorporates unique concepts and practices 
designed to address specific project challenges and environments.


(bg-traditional-methodologies)=
## Traditional Methodologies

Traditional software development methodologies are structured, 
phase-driven approaches that focus on meticulous planning, 
comprehensive documentation, and sequential execution of development phases. 
These methodologies, including the Waterfall Model, 
V-Model, Spiral Model, and Incremental Models, 
were designed to handle projects 
with well-defined requirements and predictable outcomes. 
They typically divide the development lifecycle 
into discrete stages such as requirement analysis, 
design, implementation, testing, deployment, and maintenance.

While these models excel at managing projects 
where requirements are stable and clearly understood from the outset, 
they often struggle with flexibility. 
Any changes in requirements during development 
can lead to significant delays and increased costs 
because revisiting earlier phases is challenging. 
Additionally, users and stakeholders often 
do not see a working version of the product until the later stages, 
making it difficult to incorporate feedback effectively.

Traditional methodologies are particularly suited for industries 
where compliance, safety, and extensive documentation are paramount—such as 
aerospace, healthcare, and manufacturing. 
However, in fast-paced and dynamic environments 
where adaptability and rapid delivery are essential, 
these approaches can result in slower time-to-market and reduced customer satisfaction.

As software systems became more complex and market demands shifted 
toward more dynamic and user-driven development cycles, 
the shortcomings of traditional methodologies 
highlighted the need for more adaptive and iterative approaches, 
ultimately leading to the development of Agile methodologies {cite}`BalancingAgilityAndDiscipline`.


(bg-agile)=
## Agile Software Development

Agile software development emerged in the early 2000s 
as a response to the rigid and inflexible nature of 
traditional software development models {cite}`AgileSoftDevBook`. 
The formal introduction of Agile came with 
the publication of the [Agile Manifesto](https://agilemanifesto.org/) in 2001, 
which outlined core values and principles focused on adaptive planning, 
early and continuous delivery, and close collaboration with customers. 
Agile methods emphasize iterative development, 
where requirements and solutions evolve through the 
collaborative effort of self-organizing and cross-functional teams {cite}`AgileSoftDevEcosystems`.

The primary motivation behind Agile was to 
create a development process that could quickly adapt 
to changing customer needs and market demands. 
Traditional methodologies often struggled with incorporating late-stage changes, 
whereas Agile promotes flexibility and responsiveness. 
Agile frameworks like Scrum, Kanban, Extreme Programming (XP), 
and Lean Development were developed to support these principles 
by encouraging iterative work cycles, continuous feedback, 
and incremental product improvements {cite}`AgileSoftDevMethodAndPractices`.

Agile has gained widespread popularity due to its success 
in delivering high-quality, user-centric software efficiently. 
By breaking projects into smaller, manageable increments, 
Agile allows teams to produce functional components early and frequently. 
This approach ensures that user feedback is continuously integrated, 
resulting in products that better meet customer needs and expectations {cite}`AgileSoftDev`.

One of the key advantages of Agile is its ability to reduce risk 
and improve product quality through continuous testing, integration, and delivery. 
Agile's collaborative environment fosters communication between developers, 
stakeholders, and customers, leading to more innovative solutions 
and faster adaptation to market changes. 
Its focus on incremental progress and continuous improvement 
makes Agile particularly effective in dynamic industries 
where requirements are constantly evolving.


(bg-cloud-native)=
## Cloud-Native Practices

Cloud-native practices represent a modern approach 
to building and deploying applications that leverage 
cloud computing technologies for scalability, resilience, and agility. 
This approach involves designing applications as modular services, 
automating infrastructure management, and enabling continuous delivery pipelines. 
Cloud-native development is built around scalability, flexibility, and fault tolerance, 
leveraging on-demand infrastructure provided by cloud service providers.

Cloud-native applications are optimized for cloud environments 
by utilizing containers, microservices, serverless architectures, and declarative APIs. 
These practices enable organizations to respond quickly to market demands, 
scale efficiently, and deploy changes rapidly with minimal risk. 
By embracing automation, cloud-native practices eliminate manual processes, 
reduce errors, and streamline deployment workflows.


(bg-continuous)=
### Continuous Software Engineering

Continuous software engineering practices 
enable projects to keep up with the fast-paced nature of Agile methods through automation
{cite}`ContSoftEngineering, ContinuousSoftEng`.
Most common are **Continuous Integration** (CI) {cite}`ExtremeProgExplained, CIBlogPost, EffectsOfCIOnSoftDev`,
**Continuous Delivery** (CDE) {cite}`DevDepSecCloudApp, CDReliableSoftReleaseBook, CDHugeBenefits`,
and **Continuous Deployment** (CD) {cite}`DeploymentProductionLine, CDatFacebook, CDatFBandOANDA`,
which build on top of each other (collectively called CI/CD)
to create a seamless, automated pipeline from development to production {cite}`CICDSystematicReview`.
CI involves automatically building and testing code changes as they are committed, 
ensuring early detection of bugs and integration issues. 
CD automates the deployment of code to staging or production environments, 
enabling faster and more reliable releases.
Together, they provide numerous benefits, including decreased errors, 
more efficient bug discovery and resolution, 
and a high level of control over applied changes, 
allowing projects to produce higher quality software 
more rapidly, efficiently, and reliably
{cite}`UsageCostsAndBenefitsOfCI, QualityAndProductivityCI, ImpactOfCI, HighwaysToCD, CIImprovingSoftQualBook, ExpBenefitsOfCI, UncoveringBenefitsAndChallengesOfCI, ModelingCI, StairwayToHeaven, StudyImpactAdoptCIOnPR`.


(bg-devops)=
### DevOps

DevOps is a cultural and technical movement 
that integrates software development (Dev) and IT operations (Ops). 
It promotes close collaboration between teams to automate workflows, 
enhance efficiency, and accelerate software delivery. 
DevOps emphasizes the adoption of CI/CD pipelines, 
infrastructure automation, and proactive monitoring {cite}`WhatIsDevOps`.

By breaking down silos between development and operations, 
DevOps fosters a culture of shared responsibility for product delivery. 
Automation of build, test, and deployment processes minimizes manual intervention, 
reducing errors and deployment times. 
Additionally, real-time monitoring and incident response enable teams to identify 
and resolve issues before they impact users {cite}`DevOpsInSciSysDev, ResearchOps`.


(bg-iac)=
### Infrastructure-as-Code (IaC)

Infrastructure-as-Code (IaC) is a practice that 
involves managing and provisioning infrastructure 
through machine-readable code. 
Instead of manually configuring servers and networks, 
IaC automates infrastructure deployment 
using tools like **Terraform**, **AWS CloudFormation**, and **Pulumi**. 
This approach ensures consistent, repeatable infrastructure setups across environments.

IaC improves scalability and reduces human error 
by enabling version-controlled infrastructure configurations. 
It also facilitates disaster recovery and rollback processes 
by making infrastructure reproducible. 
Teams can provision complex environments on-demand, 
accelerating development and deployment workflows.


(bg-cca)=
### Continuous Configuration Automation

Continuous Configuration Automation (CCA)
refers to the automated management and maintenance
of configuration settings across IT infrastructure.
It ensures that systems remain consistent, compliant,
and aligned with predefined configurations while adapting to changes dynamically.
CCA tools enable version-controlled, repeatable configuration changes,
reducing manual effort and errors.
By integrating with CI/CD pipelines, CCA supports scalability
rapid deployments, and the enforcement of configuration policies in modern DevOps practices.


### Containerization

Containerization encapsulates applications and their dependencies 
into isolated, lightweight containers, 
enabling consistent performance across development, testing, and production environments. 
Tools like **Docker** simplify packaging applications, 
while orchestration platforms like **Kubernetes** automate deployment, scaling, and management.

Containers improve resource utilization, portability, and scalability. 
They allow for faster deployment cycles, easy rollback, and better fault isolation. 
By decoupling applications from underlying infrastructure, 
containerization enhances operational efficiency
and enables organizations to deploy and scale applications seamlessly.


(bg-pull-based)=
## Pull-Based Development

Pull-based development is a collaborative workflow model 
that separates development from integration {cite}`ExplorStudyPullBased, WorkPractPullBased`,
fostering collaboration among globally distributed teams.
It is a bottom-up approach that accelerates development
by enabling the community to spontaneously propose changes to the project
while core maintainers are responsible for reviewing and integrating the work
{cite}`CharacterizingProjEvolOnSocialCodingPlat`.
In a pull-based model, developers create separate branches or forks
for implementing new features, bug fixes, or improvements. 
Once the changes are complete, they submit a pull request (PR) 
to merge their branch into the main codebase. 
This triggers a thorough review and testing process 
to ensure that changes meet quality standards before integration.

A central advantage of pull-based development is 
its structured code review process and feedback loops,
which are recognized as one of the most effective and crucial
quality assessment activities for software development
{cite}`5RecommendedPracticesForCompSci, 10MetricsForSciSoftware, BestPracticesForSciComp`. 
Peer reviews not only improve code quality 
but also facilitate knowledge sharing within teams. 
By involving multiple developers in the review cycle, 
potential bugs and design flaws can be identified early, 
reducing the risk of defects reaching production. 
Automated testing and integration tools are commonly integrated with pull requests, 
ensuring continuous validation of code changes.

Pull-based workflows are well-suited to Agile and DevOps methodologies, 
complementing practices like Continuous Integration/Continuous Deployment (CI/CD). 
Automated pipelines can run unit tests, security scans, and deployment scripts 
as part of the pull request workflow. 
This automation reduces manual overhead 
and speeds up the delivery process without compromising reliability.


(bg-tdd)=
## Test-Driven Development

Test-Driven Development (TDD) is a software development methodology 
that emphasizes writing automated tests before writing the actual code. 
This approach ensures that development is guided by predefined test cases, 
promoting code quality and reducing the likelihood of defects. 
TDD follows a cyclical process, often referred to as Red-Green-Refactor:

1. **Red**: Write a test case for a new functionality, which initially fails because the code has not yet been implemented.
2. **Green**: Write the minimum amount of code needed to make the test pass.
3. **Refactor**: Improve the code structure while ensuring that the test continues to pass.

This iterative process encourages developers 
to focus on the functionality and correctness of their code, 
resulting in robust and maintainable systems.

TDD has several advantages. By writing tests first, 
developers gain clarity on the requirements and expected behavior of the system. 
The presence of comprehensive test suites facilitates early detection of bugs, 
reduces regression risks, and provides a safety net during refactoring. 
Additionally, TDD promotes modular design, as code written 
to pass specific tests tends to be simpler and more focused.

However, TDD also comes with challenges. 
Writing tests before code may initially slow down development, 
and it requires discipline and experience to write effective test cases. 
Despite these challenges, TDD is widely used in industries 
where quality and reliability are critical, 
such as healthcare, finance, and aerospace. 
When implemented effectively, TDD enhances software quality, 
streamlines debugging, and fosters a test-centric development culture.
