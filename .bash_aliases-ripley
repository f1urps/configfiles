
###################
##    ALIASES    ##
###################

# Remap well-known commands
alias df='df -h'
alias vim='nvim'
alias ls='eza --color=always'
alias cmatrix='cmatrix -C blue'

# Shortcuts
alias rl='source ~/.bashrc'
alias bt='bluetoothctl power on; while ! bluetoothctl connect 00:16:94:3A:AD:81; do echo "Retrying in 1 second..."; sleep 1; done'
alias btoff='bluetoothctl power off'
alias clock='tty-clock -tBscC 6'
alias fixmonitors='xrandr --output DP-2 --output HDMI-0 --left-of DP-2'
alias fixmonitors3='xrandr --output DP-2 --output HDMI-0 --left-of DP-2 --output DP-5 --same-as DP-2 --scale-from 1920x1080'
alias git-dotfiles='git --git-dir=$HOME/.dotfiles-git-bare-repo --work-tree=$HOME'

# Pacman
alias pacman_install='pacman -S'
alias pacman_upgrade_all='pacman -Syu'
alias pacman_remove='pacman -Rnsu'
alias pacman_list_orphans='pacman -Qqdt'
alias pacman_list_explicit='pacman -Qqet'
alias pacman_package_info='pacman -Qii'

# Scripts
alias countdown="$HOME/scripts/countdown.sh"
alias ytmd="$HOME/scripts/ytmd/ytmd.py"
alias tags="$HOME/scripts/ytmd/tags.py"

# SSH to Godel
alias godel1='ssh -t root@godel "tmux new-session -A -s S1"'
alias godel2='ssh -t root@godel "tmux new-session -A -s S2"'
alias godel3='ssh -t root@godel "tmux new-session -A -s S3"'
alias godel=godel1


###################
##   FUNCTIONS   ##
###################

function wait {
    cmd="$@"
    read -p "[press enter to run '$cmd']" && eval "$cmd"
}

# Terminal screensavers
ss(){
    rand=$(($RANDOM % 6))
    case $rand in
        0) pipes;;
        1) cmatrix;;
        2) cbonsai -Sw 1;;
        3) asciiquarium;;
        4) rain;;
        5) clock;;
        *) ;;
    esac
}


##
# Commands to toggle the PROMPT_PATH_STYLE setting,
# which controls how the current path is displayed in the prompt.
#
#   none:  Only the basename of $PWD is displayed, with no path.
#   full:  Full path is displayed (relative to ~ or workspace root)
#   short: Full path is displayed, but directory names are shortened to one character.
##
alias pps_none="export PROMPT_PATH_STYLE=none"
alias pps_full="export PROMPT_PATH_STYLE=full"
alias pps_short="export PROMPT_PATH_STYLE=short"

##
# Call this from .bashrc to set the prompt.
#
# Example:
#   set_prompt \
#     enable_color=yes \
#     prefix=rainbow,cloud,hostname \
#     path=full
#
# `prefix` controls what elements are placed before the workspace name and path.
#  Available prefix elements: rainbow, wobniar, cloud, hostname
#  Elements can be in any order, for example:
#   cloud,rainbow
#   rainbow,cloud
#   cloud,cloud,hostname,cloud,cloud
#
# `path` controls how the current path is displayed in the prompt.
#   none:  Only the basename of $PWD is displayed, with no path.
#   full:  Full path is displayed (relative to ~ or workspace root)
#   short: Full path is displayed, but directory names are shortened to one character.
##
function set_prompt {
  local enable_color="$(eval "$@"; echo $enable_color)"
  local prefix="$(eval "$@"; echo $prefix)"
  local path="$(eval "$@"; echo $path)"
  local main_color="$(eval "$@"; echo $main_color)"

  local main_color_code="\[\e[${main_color}m\]"
  local main_color_code_bold="\[\e[1;${main_color}m\]"
  local trans='\[\e[104m\] \[\e[105m\] \[\e[47m\] \[\e[105m\] \[\e[104m\] '
  local rainbow='\[\e[31;41m\] \[\e[m\]\[\e[33;43m\] \[\e[m\]\[\e[32;42m\] \[\e[m\]\[\e[36;46m\] \[\e[m\]\[\e[34;44m\] \[\e[m\]'
  local wobniar='\[\e[34;44m\] \[\e[m\]\[\e[36;46m\] \[\e[m\]\[\e[32;42m\] \[\e[m\]\[\e[33;43m\] \[\e[m\]\[\e[31;41m\] \[\e[m\]'
  local cloud="$main_color_code☁ \[\e[m\]"
  local heart="$main_color_code\e[95m\]❤\[\e[m\]"
  local hostname="$main_color_code_bold\H \[\e[m\]"
  local user="$main_color_code_bold\u \[\e[m\]"
  local root="$main_color_code_bold\e[31m\][ROOT] \[\e[m\]"

  local prefix_list=$(echo "$prefix" | tr "," "\n")
  local prefixstr
  local s
  for s in $prefix_list; do
    case "$s" in
      "trans")
        prefixstr="$prefixstr$trans";;
      "rainbow")
        prefixstr="$prefixstr$rainbow";;
      "wobniar")
        prefixstr="$prefixstr$wobniar";;
      "cloud")
        prefixstr="$prefixstr$cloud";;
      "heart")
        prefixstr="$prefixstr$heart";;
      "hostname")
        prefixstr="$prefixstr$hostname";;
      "user")
        prefixstr="$prefixstr$user";;
      "root")
        prefixstr="$prefixstr$root";;
    esac
  done

  export PROMPT_PATH_STYLE="$path"

  if [[ "$enable_color" == "true" || "$enable_color" == "yes" ]]; then
    PS1="$prefixstr\[\e[0;36m\] \$(_prompt_dirname)\[\e[1;36m\]\$(_prompt_basename)\[\e[m\]\$ "
  else
    PS1="\$(_prompt_dirname)\$(_prompt_basename)\$"
  fi
}

# Dirname of current directory, formatted for use in the prompt.
# This function is called every time the prompt is rendered.
function _prompt_dirname {
  local d="$(dirs)"
  local dirname
  if [[ "$PROMPT_PATH_STYLE" = "none" ]]; then
    return
  elif [[ "$PROMPT_PATH_STYLE" = "short" ]]; then
    d=$(echo "/$d" | sed -r 's|/(.)[^/]*|/\1|g')
    d="${d:1}"
  fi
  dirname="$(dirname "$d")"
  if [ -n "$d" ]; then
    if ! [[ "$dirname" = "." || "$d" = "/" || "$d" = "~" ]]; then
      if [[ "$dirname" = "/" ]]; then
        echo "$dirname"
      else
        echo "$dirname/"
      fi
    fi
  fi
}

# Basename of the current directory, formatted for use in the prompt.
# This function is called every time the prompt is rendered.
function _prompt_basename {
  local d="$(dirs)"
  local basename="$(basename "$d")"
  if [ -n "$d" ]; then
    if ! [ "$basename" = "." ]; then
      echo "$basename"
    fi
  fi
}

##
# Output a grid of colored text, containing every
# combination of foreground & background colors.
##
function colors {
  local i
  local j
  local k
  local s
  local n
  let k=0
  while [[ $k -lt 16 ]]; do
    n=$k
    if [[ $(expr length $n) = 1 ]]; then
      n=" $n"
    fi
    s="$s\$(tput setaf $k)$n"
    let k=k+1
  done
  eval "echo \"$s\""
  let i=0
  while [[ $i -lt 16 ]]; do
    n=$i
    if [[ $(expr length $n) = 1 ]]; then
      n=" $n"
    fi
    s="\$(tput setab 0)\$(tput setaf $i)$n"
    let j=1
    while [[ $j -lt 16 ]]; do
      s="$s\$(tput setab $j)$n"
      let j=j+1
    done
    s="$s\$(tput setab 0)"
    eval "echo \"$s\""
    let i=i+1
  done
}

