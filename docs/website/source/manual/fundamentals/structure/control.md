# Control Center Directory

The meta directory is the main control center of your repository,
where all configurations, metadata, and settings
for your GitHub repository (and its corresponding git repository),
package, website, development pipeline, and other tools are stored in one place.
When you apply a change to the repository's `meta` content and push it to the remote repository,
{{pp_meta.name}} will automatically apply the corresponding changes to entire repository and its content,
so that the repository is always in a consistent state with its `meta` content.
This is the main mechanism that {{pp_meta.name}} uses to manage your repository and project,
so you must never modify any configuration directly, but always through the `meta` content.

This directory is named `.meta` by default, and is located at the root of the repository.
You can change the name and location of your repository's `meta` directory,
but it must have a specific substructure, meaning that {{pp_meta.name}} will look for
specific files and directories in specific locations inside the `meta` directory
to read the corresponding configurations and data from.
