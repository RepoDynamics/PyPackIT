While the [Devcontainer specification](https://containers.dev/implementors/spec/)
technically allows for
[connecting to multiple containers](https://code.visualstudio.com/remote/advancedcontainers/connect-multiple-containers) simultaneously,
[Devcontainer Features](https://containers.dev/implementors/features/) are
[only loaded for the first connected container](https://github.com/microsoft/vscode-remote-release/issues/8744).


Terminals opened inside VSCODE in the container are non-login interactive shells.
The `userEnvProbe` property in [`devcontainer.json`](https://containers.dev/implementors/json_reference/#general-properties)
appears to be setting shell type, but it does not affect the shell type in the VS Code terminal.

Interactivity test (bash/zsh): `[[ $- == *i* ]] && echo "Interactive" || echo "Non-interactive"`
Interactivity test (zsh): `[[ -o interactive ]] && echo "Interactive" || echo "Non-interactive"`

Login test (bash): `[[ "${0:0:1}" == "-" ]] && echo "Login" || echo "Non-login"` or `shopt -q login_shell && echo "Login" || echo "Non-login"`
Login test (zsh): `[[ -o login ]] && echo "Login shell" || echo "Non-login shell"`
