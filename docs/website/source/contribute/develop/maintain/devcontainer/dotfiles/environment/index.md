# Environment Variables

Environment variables are named strings available to all applications,
providing a simple way to share configuration settings
between multiple applications and processes in Linux.
They are used to adapt applications' behavior to the environment they are running in.
The value of an environmental variable can for example be
the location of all executable files in the file system,
the default editor that should be used, or the system locale settings.
You can see each application's manual to see what variables are used by that application.



In devcontainers, `ENV` instructions from the `Dockerfile`
are added to the `/etc/environment` file
(cf. https://github.com/microsoft/vscode-remote-release/issues/6157)



https://man7.org/linux/man-pages/man5/environment.d.5.html
https://manpages.debian.org/experimental/systemd/environment.d.5.en.html
https://wiki.archlinux.org/title/Environment_variables
https://wiki.debian.org/EnvironmentVariables
https://help.ubuntu.com/community/EnvironmentVariables
https://superuser.com/questions/664169/what-is-the-difference-between-etc-environment-and-etc-profile
https://askubuntu.com/questions/866161/setting-path-variable-in-etc-environment-vs-profile


## XDG Base Directories

https://wiki.archlinux.org/title/XDG_Base_Directory
