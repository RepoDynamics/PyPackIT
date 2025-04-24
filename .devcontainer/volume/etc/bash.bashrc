# System-wide .bashrc file for interactive non-login bash shells.

# To enable the settings / commands in this file for login shells as well,
# this file has to be sourced in /etc/profile.


# If not running interactively, don't do anything
case $- in
    *i*) ;;
      *) return;;
esac


# Source scripts
# ==============

if [ -f /etc/shellrc ]; then
    . /etc/shellrc
fi

if [ -f /etc/bash/bash_env ]; then
    . /etc/bash/bash_env
fi

if [ -f /etc/bash/bash_theme ]; then
    . /etc/bash/bash_theme
fi


# Activate pixi
eval "$(pixi completion -s bash)"


# Variables
# =========

# History Configuration
# ---------------------

# Commands to exclude from history
HISTIGNORE="pwd:exit:clear"
# Exclude duplicates, and commands starting with a space; erase older duplicates
HISTCONTROL=erasedups:ignoredups:ignorespace
# Maximum number of commands to remember in the current session's history.
HISTSIZE=1000
# Maximum number of lines contained in the history file.
HISTFILESIZE=5000
# Format for timestamps in history output
HISTTIMEFORMAT='%F %T '
# Save history after each command and reload new entries from other sessions
PROMPT_COMMAND="history -a; history -n"


# Shell Options
# =============

# Append to history file instead of overwriting
shopt -s histappend

# check the window size after each command and, if necessary,
# update the values of LINES and COLUMNS.
shopt -s checkwinsize

# append to the history file, don't overwrite it
shopt -s histappend

# If set, the pattern "**" used in a pathname expansion context will
# match all files and zero or more directories and subdirectories.
#shopt -s globstar


# enable bash completion in interactive shells
if ! shopt -oq posix; then
  if [ -f /usr/share/bash-completion/bash_completion ]; then
    . /usr/share/bash-completion/bash_completion
  elif [ -f /etc/bash_completion ]; then
    . /etc/bash_completion
  fi
fi


# sudo hint
if [ ! -e "$HOME/.sudo_as_admin_successful" ] && [ ! -e "$HOME/.hushlogin" ] ; then
    case " $(groups) " in *\ admin\ *|*\ sudo\ *)
    if [ -x /usr/bin/sudo ]; then
	cat <<-EOF
	To run a command as administrator (user "root"), use "sudo <command>".
	See "man sudo_root" for details.

	EOF
    fi
    esac
fi


# if the command-not-found package is installed, use it
if [ -x /usr/lib/command-not-found -o -x /usr/share/command-not-found/command-not-found ]; then
	function command_not_found_handle {
	        # check because c-n-f could've been removed in the meantime
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


# Check if lesspipe exists and is executable, then initialize it
# to enable smarter previews in non-text input files (e.g. archives, PDFs, etc.).
[ -x /usr/bin/lesspipe ] && eval "$(SHELL=/bin/sh lesspipe)"


# Customize GCC diagnostic colors (errors, warnings, etc.)
export GCC_COLORS='error=01;31:warning=01;35:note=01;36:caret=01;32:locus=01:quote=01'
