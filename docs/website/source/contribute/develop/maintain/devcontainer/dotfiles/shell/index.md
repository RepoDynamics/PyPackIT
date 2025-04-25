# Shell Configuration

Shells are commonly configured via startup/shutdown configuration files {cite}`effective-shell-configuring`.
These are an essential component of Unix-like operating systems,
acting as the foundation for controlling shell behavior, environment variables,
command aliases, prompt appearance, function definitions, and more.
Shell configuration files are scripts sourced automatically by the shell to customize user environments.
For developers and system administrators, a deep understanding of how these files operate and how they interact
is crucial for creating reliable, portable, and maintainable environments.

Each shell has its own set of configuration files.
Usually, each configuration file has two variants:
a global configuration file located at a fixed (installation-specific) location and loaded for all users,
as well as a user-specific version stored in each user's home directory and loaded only for that user.
Which exact configuration files are loaded and the order in which they are executed
can vary depending on the shell invocation type
and the value of specific environment variables at invocation time.
This can lead to confusion, especially when switching between different shells
or when using terminal emulators that may invoke shells in unexpected ways.

This guide is focused on `bash` and [Zsh](https://www.zsh.org/), two of the most common interactive shells.
It explores the differences between shell types, the specific configuration files involved,
the order in which they're executed, and how to use them effectively.


## Shell Invocation Types

Shell configuration behavior depends on the type of shell sessions. There are two axes:

- **Login vs. Non-login**
- **Interactive vs. Non-interactive**

| Type                  | Description                                                       |
|-----------------------|-------------------------------------------------------------------|
| **Login**             | Initiated by logging in via `tty`, `ssh`, or using `bash -l`      |
| **Non-login**         | Invoked by terminal emulators (e.g., `gnome-terminal`, `iTerm`)   |
| **Interactive**       | Connected to a user terminal and reads user input                 |
| **Non-interactive**   | Used for scripting or automation (e.g., cron jobs, CI pipelines)  |

A shell session can therefore be login and interactive, login and non-interactive,
non-login and interactive, or non-login and non-interactive.
Most shells a user interacts with are **non-login interactive** shells.
This is the case for most Linux terminals and the
integrated terminal inside a devcontainer in VS Code [^devcontainer-userEnvProbe].
Typically, users only encounter a login shell if they log in remotely (e.g., through ssh)
or from a TTY (not a GUI).
An exception is terminals opened on a macOS, which are login shells by default.

You can get the invocation type of a shell session by running the following commands
in that shell:

:::::{tab-set}

::::{tab-item} Interactivity (sh)
:::{code-block} bash
case $- in
  *i*) echo "Interactive" ;;
  *)   echo "Non-interactive" ;;
esac
:::
::::

::::{tab-item} Interactivity (bash/zsh)
:::{code-block} bash
[[ $- == *i* ]] && echo "Interactive" || echo "Non-interactive"
:::
::::

::::{tab-item} Interactivity (zsh)
:::{code-block} bash
[[ -o interactive ]] && echo "Interactive" || echo "Non-interactive"
:::
::::

::::{tab-item} Login (bash)
:::{code-block} bash
[[ "${0:0:1}" == "-" ]] && echo "Login" || echo "Non-login"
:::
or
:::{code-block} bash
shopt -q login_shell && echo "Login" || echo "Non-login"
:::
::::

::::{tab-item} Login (zsh)
:::{code-block} bash
[[ -o login ]] && echo "Login shell" || echo "Non-login shell"
:::
::::

:::::

[^devcontainer-userEnvProbe]: The `userEnvProbe` property in [`devcontainer.json`](https://containers.dev/implementors/json_reference/#general-properties) appears to be setting shell invoctation type, but it does not affect the shell type in the VS Code terminal (cf. https://github.com/microsoft/vscode-remote-release/issues/3593). However, the behavior seems to be configurable via the `terminal.integrated.profiles`
option in VS Code settings (cf. [stackoverflow](https://stackoverflow.com/a/72034200/14923024)).


## Bash

Bash recognizes two main configuration files: `profile` and `bashrc`
{cite}`bash-docs-dotfiles, bash-dotfiles-linux-doc-project, bash-dotfiles-christollefson, zsh-bash-dotfiles-lumber-room`.
Each file can have a global and a user-specific version.
The global `profile` file is always expected at `/etc/profile`,
while the location where Bash searches for the global `bashrc` file is installation-specific;
`/etc/bash.bashrc` on Debian, `/etc/bash/bashrc` on Alpine,
and `/etc/bashrc` on Red Hat and macOS.
(cf. [here](https://github.com/devcontainers/features/blob/8895eb3d161d28ada3a8de761a83135e811cae3d/src/common-utils/main.sh#L479-L489)).

User-specific configuration files are only expected
in the user's home directory (i.e., at `~/`).
All user-specific files must start with a dot in their name
(e.g., `bashrc` becomes `.bashrc`).
Moreover, the `.profile` file may also be named `.bash_profile` or `.bash_login`;
Bash first checks for `.bash_profile`, then `.bash_login`, and finally `.profile`
and uses the first one it finds.

The order of execution of all startup files for each shell type is as follows:

- **Non-Login Non-Interactive**: `BASH_ENV`
- **Non-Login Interactive**: `bashrc` → `.bashrc`
- **Login (Interactive or Non-Interactive)**: `profile` → (`.bash_profile` or `.bash_login` or `.profile`)

As can be seen, Bash does not try to load any configuration files
when the shell is non-interactive.
Instead, it looks for the environment variable `BASH_ENV`,
and if set, expands its value and uses that as the path to
a file to read and execute.

Moreover, Bash does not offer a configuration file
that is only sourced by interactive shells or by login shells.
Therefore, it is common practices to add a condition in the `profile` file
that sources the `bashrc` file if the shell is interactive:

```sh
if case $- in *i*) true ;; *) false ;; esac && [ -f /etc/bash.bashrc ]; then
    . /etc/bash.bashrc
fi
```

## Zsh

Zsh recognizes five configuration files: `zshenv`, `zprofile`, `zshrc`, `zlogin`, and `zlogout`
{cite}`zsh-docs-dotfiles, zsh-archwiki, zsh-dotfiles-freecodecap, zsh-bash-dotfiles-lumber-room`.
Each file can have a global and a user-specific version.
The location where Zsh searches for global files is installation-specific;
on most Linux distributions it is the `/etc/zsh/` directory,
whereas on Red Hat distributions and macOS
they are expected directly under the `/etc/` directory
(cf. [here](https://github.com/devcontainers/features/blob/8895eb3d161d28ada3a8de761a83135e811cae3d/src/common-utils/main.sh#L510-L514)).

User-specific configuration files are expected in a directory
whose path is defined in the `ZDOTDIR` environment variable.
If `ZDOTDIR` is not set, the default is the user's home directory
(i.e., the `HOME` environment variable).
Moreover, all user-specific files must start with a dot in their name
(e.g., `zshenv` becomes `.zshenv`).

The only file that is always loaded is `zshenv`.
Subsequent behavior is defined by the shell invocation type
as well as the following environment variables:
- `RCS`: If unset (set by default), no other configuration file is loaded.
- `GLOBAL_RCS`: If unset (set by default), no other global configuration file is loaded
  (but user-specific files are loaded).

The above variables can also be set/unset by later configuration files
to change the loading behavior of subsequent files. Assuming both are set,
the order of execution for all startup files for each shell type is as follows:

1. `zshenv`
2. `.zshenv`
3. `zprofile` (login)
4. `.zprofile` (login)
5. `zshrc` (interactive)
6. `zshrc` (interactive)
7. `zlogin` (login)
8. `.zlogin` (login)

This results in the following executation orders for each shell type:

- **Non-Login Non-Interactive**: `zshenv` → `.zshenv`
- **Non-Login Interactive**:     `zshenv` → `.zshenv` → `zshrc` → `.zshrc`
- **Login Non-Interactive**:     `zshenv` → `.zshenv` → `zprofile` → `.zprofile`
- **Login Interactive**:         `zshenv` → `.zshenv` → `zprofile` → `.zprofile` → `zshrc` → `.zshrc` → `zlogin` → `.zlogin`

Moreover, when a login shell exits, the files `.zlogout` and then `zlogout` are sourced
(notice the reversed global/user order compared to startup files).

Therefore, each file must contain only the code
that is relevant for its specific invocation type:
- `zshenv`: Must be kept as small as possible, only containing configurations
  that are needed for all shell types, such as environment variables
  and specific function definitions and aliases that are always needed.
  It should not contain commands that produce output or assume the shell is attached to a TTY.
- `zprofile`: Must contain additional configurations that are only needed for login shells,
  such as additional PATH settings.
  In most cases, it only contains a single line to source the `profile` file.
- `zshrc`: Must contain configurations that are only needed for interactive shells,
  such as prompt and theme settings, command history, and interactive functions.

:::{admonition} Precompiling Configuration Files
:class: tip

Any of these files may be pre-compiled with the [`zcompile`](https://zsh.sourceforge.io/Doc/Release/Shell-Builtin-Commands.html#Shell-Builtin-Commands) builtin command.
If a compiled file exists (named for the original file plus the .zwc extension)
and it is newer than the original file, the compiled file will be used instead.
:::


## Best Practices

### Unifying Login and Non-login Behavior

To avoid duplicated logic between `~/.bash_profile` and `~/.bashrc`, explicitly source `~/.bashrc` from the login file:

```bash
# ~/.bash_profile
if [ -f ~/.bashrc ]; then
  . ~/.bashrc
fi
```

This ensures that login shells benefit from the same aliases, functions, and environment variables as non-login shells.

### Avoid Polluting Non-interactive Environments

Many scripts and CI tools invoke shells in non-interactive mode. Adding interactive-specific behavior (e.g., setting `PS1`, printing messages) to these environments can break automation. Guard such logic:

```bash
case $- in
  *i*) ;;
  *) return;;
esac
```

### Modularize Your Configuration

Instead of placing all logic in a monolithic `~/.bashrc` or `~/.zshrc`, split configuration into maintainable files:

```bash
# ~/.bashrc
for file in ~/.config/shell/rc.d/*.sh; do
  [ -r "$file" ] && . "$file"
done
```

```
~/.config/shell/rc.d/
├── env.sh
├── aliases.sh
├── functions.sh
└── prompt.sh
```

This allows for cleaner version control, testing, and reusability across machines.

### Supporting Non-interactive Scripts

If scripts need a consistent environment, avoid sourcing full interactive configs. Instead, create a minimal `env.sh`:

```bash
# ~/.config/shell/env.sh
export PATH="$HOME/bin:$PATH"
export EDITOR=nvim
```

Then, in scripts:

```sh
#!/bin/sh
. "$HOME/.config/shell/env.sh"
```

### Shell Debugging

To trace configuration loading:

```bash
bash --login -x
zsh -x
```

Or use embedded debug statements:

```bash
echo "Sourcing ~/.bashrc" >> ~/shell.log
```

### Version Control with Dotfile Managers

Use tools like [chezmoi](https://www.chezmoi.io/), [yadm](https://yadm.io/), or bare Git repos to manage your dotfiles. Always include a local override:

```bash
# ~/.bashrc
[ -f ~/.bashrc.local ] && . ~/.bashrc.local
```

This keeps secrets or machine-specific changes out of version control.

## Summary

- Shell behavior depends on whether it's login, non-login, interactive, or non-interactive.
- Bash and Zsh load different sets of configuration files depending on context.
- Always guard interactive-only logic with checks.
- Modularize configuration files for clarity and maintainability.
- Avoid sourcing full configs in scripts—use minimal setups instead.
