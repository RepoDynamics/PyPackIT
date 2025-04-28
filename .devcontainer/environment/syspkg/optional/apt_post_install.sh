# Setup Fish
# - https://github.com/devcontainers/images/blob/0f13a9b8a31b9c81be78abfc404cc00748e946bb/src/universal/.devcontainer/Dockerfile#L85-L88
FISH_PROMPT="function fish_prompt\n    set_color green\n    echo -n (whoami)\n    set_color normal\n    echo -n \":\"\n    set_color blue\n    echo -n (pwd)\n    set_color normal\n    echo -n \"> \"\nend\n";
printf "$FISH_PROMPT" >> /etc/fish/functions/fish_prompt.fish;
printf "if type code-insiders > /dev/null 2>&1; and not type code > /dev/null 2>&1\n  alias code=code-insiders\nend" >> /etc/fish/conf.d/code_alias.fish;
