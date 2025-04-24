# Dotfiles

Many applications allow users to customize their behavior through configuration files.
These are mostly plain text files that define user-specific settings and preferences
in a format recognized by the corresponding application (e.g., JSON, YAML, Bash).
They are commonly reffered to as "dotfiles"
because their filenames usually begin with a dot (`.`).
This is Unix convention to hide files from default directory listings,
helping prevent accidental modifications or deletions.
This convention has persisted, and today "dotfiles" denotes configuration files
intended for system or application initialization rather than ordinary data or documents.

Applications expect their dotfiles in specific locations in the filesystem.
Some applications use hardcoded locations,
while others allow for customizing locations---usually
by setting environment variables
(cf. [XDG Base Directory Specification](https://wiki.archlinux.org/title/XDG_Base_Directory#Support)).
Usually, each configuration file has two variants:
a global configuration file located at a fixed (installation-specific) location and loaded for all users,
as well as a user-specific version stored in each user's home directory and loaded only for that user.
This allows setting global defaults for all users
while still allowing individual users to override and/or extend them.


## Dotfiles in Devcontainers

On a system shared by different users---such as a devcontainer---it
is good practice to only set configurations in global dotfiles,
allowing each user to override and/or extend them using their own dotfiles.
Therefore, while a devcontainer commonly predefines
a single non-root user for everyone using it,
configuration files should not be placed in that user's home directory.
This allows each user to readily [add their own dotfiles](#add-dotfiles-repo)
in the container user's home directory after connecting to the container,
without the risk of unintentionally overwriting global configurations.
