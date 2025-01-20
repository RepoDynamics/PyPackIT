# Packaging and Distribution


Since PyPI and Anaconda.org are independent platforms with their own package management systems,
developers must also be familiar with the specific requirements and nuances of each platform.


while Anaconda/conda uses the [YAML](https://yaml.org/) format to define metadata in a file named
[`meta.yaml`](https://docs.conda.io/projects/conda-build/en/stable/resources/define-metadata.html),
and requires [build scripts](https://docs.conda.io/projects/conda-build/en/stable/resources/build-scripts.html)
to be defined separately for Linux/macOS and Windows in `build.sh` and `bld.bat` files, respectively.


while Anaconda/conda uses the
  [`.conda` format](https://docs.conda.io/projects/conda/en/latest/user-guide/concepts/packages.html#conda-file-format)
  superseding the older `.tar.bz2` format.
Similarly, conda built distributions can be generated using the
[conda-build](https://github.com/conda/conda-build) package provided by the [conda community](https://conda.org/).

and [Noarch Packages](https://docs.conda.io/projects/conda/en/latest/user-guide/concepts/packages.html#noarch-packages) for conda)

  
Similarly, for Anaconda.org, developers must [create an account](https://docs.anaconda.com/free/anacondaorg/user-guide/work-with-accounts/)
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