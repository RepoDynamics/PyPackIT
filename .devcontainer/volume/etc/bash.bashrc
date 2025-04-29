case $- in
  *i*) ;;
    *) return;;
esac
. "/etc/global_shellrc"
. "/etc/bash/bash_theme"
HISTIGNORE="pwd:exit:clear"
HISTCONTROL=erasedups:ignoredups:ignorespace
HISTSIZE=1000
HISTFILESIZE=5000
HISTTIMEFORMAT='%F %T '
PROMPT_COMMAND="history -a; history -n"
shopt -s histappend
shopt -s checkwinsize
shopt -s histappend
if ! shopt -oq posix; then
    if [ -f /usr/share/bash-completion/bash_completion ]; then
        . /usr/share/bash-completion/bash_completion
    elif [ -f /etc/bash_completion ]; then
        . /etc/bash_completion
    fi
fi
if [ ! -e "$HOME/.sudo_as_admin_successful" ] && [ ! -e "$HOME/.hushlogin" ] && command -v sudo >/dev/null 2>&1; then
    case " $(groups) " in
        *\ admin\ *|*\ sudo\ *)
            printf '%s\n\n' \
                'To run a command as administrator (user "root"), use "sudo <command>".' \
                'See "man sudo_root" for details.'
            ;;
    esac
fi
if [ -x /usr/lib/command-not-found -o -x /usr/share/command-not-found/command-not-found ]; then
  function command_not_found_handle {
                if [ -x /usr/lib/command-not-found ]; then
      /usr/lib/command-not-found -- "$1"
                  return $?
                elif [ -x /usr/share/command-not-found/command-not-found ]; then
      /usr/share/command-not-found/command-not-found -- "$1"
                  return $?
    else
      printf "%s: command not found\n" "$1" >&2
      return 127
    fi
  }
fi
[ -x /usr/bin/lesspipe ] && eval "$(SHELL=/bin/sh lesspipe)"
export GCC_COLORS='error=01;31:warning=01;35:note=01;36:caret=01;32:locus=01:quote=01'
eval "$(pixi completion -s bash)"
