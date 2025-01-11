(bg-py)=
# Python


[Python](https://www.python.org/) is a general-purpose, multi-paradigm programming language,
created by Guido van Rossum and first released in 1991.[^python-timeline]
It has since evolved into one of the most popular programming languages in the world,
consistently ranking among the top five throughout the last decade, and topping the list since 2021,
according to the [TIOBE Index](https://www.tiobe.com/tiobe-index/).

[^python-timeline]: [G. van Rossum (2009). A Brief Timeline of Python. The History of Python](https://python-history.blogspot.com/2009/01/brief-timeline-of-python.html)

Python was designed with an emphasis on code readability and simplicity;
its high-level abstractions and straightforward syntax
have made software development accessible to a wider range of users,
while still being powerful and robust enough to support advanced applications.
Python is a dynamically typed, interpreted language, with automatic memory management,
which allows for rapid prototyping and implementation of complex concepts,
enabling users to readily develop their ideas and share them with others.

Owing to an active community of open-source developers, Python's rich ecosystem of libraries
and frameworks has grown exponentially over the years,
making it a powerful and versatile tool for a wide range of applications,
from web development, to data science, artificial intelligence, and machine learning.
Not only do large organizations like Google, NASA, and CERN use Python in many of their projects,
but it has also become the language of choice for many startups,
small businesses, and academic research groups.
For example, the majority of scientific software across various disciplines of computational sciences
are now being published as Python packages.



Over the past decade, Python has emerged as the leading programming language 
for research software development \cite{SurveySEPracticesInScience2, AnalyzingGitHubRepoOfPapers, DevOpsInSciSysDev}, 
widely adopted by major organizations such as CERN \cite{IntroducingPythonAtCERN, PythonAtCERN} and NASA \cite{PythonAtNASA}, 
and instrumental in key scientific achievements \cite{PythonScientificSuccessStories}, 
including the discovery of gravitational waves \cite{GravWaveDiscovery} and black hole imaging \cite{BlackHoleImage}. 
Python is now the most recommended language for scientific computing due to its simplicity, 
versatility, and extensive ecosystem \cite{PythonBatteriesIncluded, PythonForSciComp, PythonForSciAndEng, PythonJupyterEcosystem, SciCompWithPythonOnHPC, PythonEcosystemSciComp, WhatMakesPythonFirstChoice}, 
which provides performance-optimized libraries for array programming \cite{NumPy}, 
fundamental algorithms \cite{SciPy}, 
data analysis \cite{pandas}, machine learning \cite{PyTorch, Top5MLLibPython, ScikitLearn}, 
image processing \cite{scikitImage}, visualization \cite{Matplotlib, Mayavi}, 
interactive distributed computing \cite{IPython, Jupyter, Jupyter2}, 
parallel programming \cite{DaskAndNumba, DaskApplications}, 
and domain-specific scientific applications \cite{Astropy, SunPy, Pangeo, MDAnalysis, Biopython, NIPY}. 
Python can readily handle complex tasks such as web integration and visualization, 
which are hard to address in low-level languages \cite{PythonEcosystemSciComp}, 
while bridging the performance gap via optimized compilers \cite{Cython, Numba, Pythran}, 
GPU run-time code generators \cite{PyCUDA}, and APIs for integrating low-level languages \cite{PythonForSciComp, PythonEcosystemSciComp}. 
This adaptability enables rapid prototyping of complex applications, 
allowing researchers to quickly evaluate various scientific models and 
efficiently optimize the best solution \cite{BestPracticesForSciComp}. 
The recent advancements in parallel distributed computing with 
Python \cite{SciCompWithPythonOnHPC, ParallelDistCompUsingPython, ScientistsGuideToCloudComputing, DemystPythonPackageWithCondaEnvMod, PythonAcceleratorsForHPC} 
and Jupyter \cite{DistWorkflowsWithJupyter} has even motivated large HPC communities 
to shift toward Python \cite{SoftEngForCompSci, InteractiveSupercomputingWithJupyter}. 