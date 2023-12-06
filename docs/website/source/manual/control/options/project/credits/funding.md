# Funding Options
GitHub allows you to add a *Sponsor* button together with a *Sponsor this project* section
to the main page of your repository, to increase the visibility of funding options
for your open-source project. Clicking on the *Sponsor* button opens the *Sponsor this project* section,
where a list of links to your specified funding platforms is displayed to the user.
GitHub lets you specify up to four sponsored GitHub accounts (one of which can be a GitHub organization),
up to four custom URLs,
plus one name (either username, package name, or project name, depending on the platform)
per supported external funding platform (see below).
For more information, see the [About GitHub Sponsors](https://docs.github.com/en/sponsors/getting-started-with-github-sponsors/about-github-sponsors)
and [Displaying a sponsor button in your repository](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/displaying-a-sponsor-button-in-your-repository)
pages in the [GitHub Sponsors Docs](https://docs.github.com/en/sponsors/receiving-sponsorships-through-github-sponsors).


## Setting
All configurations are set under the `funding` key in the `project/credits.yaml` file.
If the file/key is not present (default), this option will be disabled.
If set, the value of the `funding` key must be an object with any number of
the supported key-value pairs (one for each type of platform) described below:

:github: ***string*** *or* ***array of strings***, ***optional***

    [GitHub Sponsors](https://github.com/sponsors) account(s);
    either a single GitHub username (as a string),
    or an array of up to four GitHub usernames of
    [sponsored personal accounts](https://docs.github.com/en/sponsors/receiving-sponsorships-through-github-sponsors/setting-up-github-sponsors-for-your-personal-account)
    and/or [sponsored organization accounts](https://docs.github.com/en/sponsors/receiving-sponsorships-through-github-sponsors/setting-up-github-sponsors-for-your-organization).

    ::::{dropdown} Examples
    :margin: 3

    - Single username:

    :::{code-block} yaml
    :caption: 🗂 `.project/credits.yaml`
    funding:
       github: ${‎{ owner.username }}
    :::

    - Multiple usernames:

    :::{code-block} yaml
    :caption: 🗂 `.project/credits.yaml`
    funding:
       github:
          - ${‎{ owner.username }}
          - RepoDynamicsBot
    :::

    ::::

:community_bridge: ***string***, ***optional***

    Name of your accounr/project on the
    [LFX Mentorship (CommunityBridge)](https://lfx.linuxfoundation.org/tools/mentorship)
    platform.

    ::::{dropdown} Example
    :margin: 3

    :::{code-block} yaml
    :caption: 🗂 `.project/credits.yaml`
    funding:
       community_bridge: my_lfx_account_name
    :::

    ::::

:issuehunt: ***string***, ***optional***

    Your [IssueHunt](https://issuehunt.io/) username.

    ::::{dropdown} Example
    :margin: 3

    :::{code-block} yaml
    :caption: 🗂 `.project/credits.yaml`
    funding:
       issuehunt: my_issuehunt_username
    :::

    ::::

:ko_fi: ***string***, ***optional***

    Your [Ko-fi](https://ko-fi.com/) username.

    ::::{dropdown} Example
    :margin: 3

    :::{code-block} yaml
    :caption: 🗂 `.project/credits.yaml`
    funding:
       ko_fi: my_kofi_username
    :::

    ::::

:liberapay: ***string***, ***optional***

    Your [Liberapay](https://liberapay.com/) username.

    ::::{dropdown} Example
    :margin: 3

    :::{code-block} yaml
    :caption: 🗂 `.project/credits.yaml`
    funding:
       liberapay: my_liberapay_username
    :::

    ::::

:open_collective: ***string***, ***optional***

    Your [Open Collective](https://opencollective.com/) username.

    ::::{dropdown} Example
    :margin: 3

    :::{code-block} yaml
    :caption: 🗂 `.project/credits.yaml`
    funding:
       open_collective: my_opencollective_username
    :::

    ::::

:otechie: ***string***, ***optional***

    Your [Otechie](https://otechie.com/) username.

    ::::{dropdown} Example
    :margin: 3

    :::{code-block} yaml
    :caption: 🗂 `.project/credits.yaml`
    funding:
       otechie: my_otechie_username
    :::

    ::::

:patreon: ***string***, ***optional***

    Your [Patreon](https://www.patreon.com/) username.

    ::::{dropdown} Example
    :margin: 3

    :::{code-block} yaml
    :caption: 🗂 `.project/credits.yaml`
    funding:
       patreon: my_patreon_username
    :::

    ::::

:tidelift: ***string***, ***optional***

    Your package address set in your [Tidelift](https://tidelift.com/) account.
    The package address must have the format `pypi/<PACKAGE-NAME>`,
    where `<PACKAGE-NAME>` is the name of your package on PyPI.

    ::::{dropdown} Example
    :margin: 3

    :::{code-block} yaml
    :caption: 🗂 `.project/credits.yaml`
    funding:
       tidelift: pypi/${‎{ package.name }}
    :::

    ::::

:custom: ***string*** *or* ***array of strings***, ***optional***

    Custom funding platform(s);
    either a single URL (as a string),
    or an array of up to four URLs to custom funding platforms.

    ::::{dropdown} Examples
    :margin: 3

    - Single URL:

    :::{code-block} yaml
    :caption: 🗂 `.project/credits.yaml`
    funding:
       custom: https://custom-url.com/my-project
    :::

    - Multiple URLs:

    :::{code-block} yaml
    :caption: 🗂 `.project/credits.yaml`
    funding:
       custom:
          - https://custom-url.com/my-project
          - https://other-url.com/my-project
    :::

    ::::


## Usage

GitHub looks for a YAML file at `.github/FUNDING.yml` in the default branch of the repository;
If it exists and has the correct format, GitHub will display the
*Sponsor* button and *Sponsor this project* section on the repository's main page,
and will use the information in the file to populate the *Sponsor this project* section,
otherwise, the *Sponsor* button and *Sponsor this project* section will not be displayed.
{{ name }} automatically generates the `.github/FUNDING.yml` file when the `funding` key is set,
and will update/remove the file when the `funding` key is updated/removed.
