#
# ~/.bashrc
#

# If not running interactively, don't do anything
[[ $- != *i* ]] && return

# Bash aliases file
if [[ -f "$HOME/.bash_aliases" ]]; then
    . "$HOME/.bash_aliases"
fi

# Prompt
enable_powerline=false
if [[ "$enable_powerline" == true ]]; then
    powerline-daemon -q
    POWERLINE_BASH_CONTINUATION=1
    POWERLINE_BASH_SELECT=1
    . /usr/share/powerline/bindings/bash/powerline.sh
else
    set_prompt \
        enable_color=yes \
        prefix=trans,hostname \
        path=full \
        main_color=104
fi

# Path
export PATH="$PATH:$HOME/.local/bin"

# Support Ctrl+x Ctrl-e in bash
export EDITOR=nvim

# Suppress pycache
export PYTHONDONTWRITEBYTECODE=true

