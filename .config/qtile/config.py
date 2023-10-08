# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os
import subprocess
import re

from libqtile import bar, layout, widget, hook
from libqtile.config import Click, Drag, Group, Key, KeyChord, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal
from libqtile.log_utils import logger

from powerline.bindings.qtile.widget import PowerlineTextBox

mod = "mod4"

#####################
##    FUNCTIONS    ##
#####################

##
# Check if the group contains a matching window.
##
def group_contains_window(group, match):
    for w in group.windows:
        if w.match(match):
            return True
    return False

##
# Check if the group contains no windows.
##
def group_is_empty(group):
    return len(group.windows) == 0

##
# Focus on the next empty group.
#
# If `move_current_window` is true, the currently-focused window
# will be moved to the new group.
##
def to_next_empty_group(qtile, move_current_window=False):
    for group in qtile.groups:
        if group_is_empty(group):
            if move_current_window:
                qtile.current_window.togroup(group.name)
            qtile.current_screen.set_group(group)
            return

##
# Find an existing window, or open it if it doesn't exist.
#
# If there is an existing window matching `name`, switch to whatever group it's in.
# Otherwise, launch the program. If `empty_group` is True, the program will be
# launched in the next available empty group, if one exists.
##
def focus_or_open(qtile, name, empty_group=False, match=None):
    for group in qtile.groups:
        if group_contains_window(group, match or Match(wm_class=name)):
            qtile.current_screen.set_group(group)
            return
    if empty_group:
        to_next_empty_group(qtile)
    qtile.cmd_spawn(name)

##
# Focus on the next screen.
##
def to_next_screen(qtile, move_current_window=False):
    next_screen_index = (qtile.screens.index(qtile.current_screen) + 1) % len(qtile.screens)
    if move_current_window:
        qtile.current_window.togroup(qtile.screens[next_screen_index].group.name)
    qtile.focus_screen(next_screen_index)

##
# Rotate groups on the screens.
##
def rotate_screens(qtile, skip_empty=False):
    screens = qtile.screens
    if skip_empty:
        screens = [screen for screen in screens if not group_is_empty(screen.group)]
    groups = [screen.group for screen in screens]
    groups = groups[1:] + groups[:1]
    for i in range(len(groups)):
        screens[i].set_group(groups[i])


keys = [

    # Move the focus.
    Key([mod], "Left", lazy.layout.left()),
    Key([mod], "Right", lazy.layout.right()),
    Key([mod], "Down", lazy.layout.down()),
    Key([mod], "Up", lazy.layout.up()),
    Key([mod], "h", lazy.layout.left()),
    Key([mod], "l", lazy.layout.right()),
    Key([mod], "j", lazy.layout.down()),
    Key([mod], "k", lazy.layout.up()),
    Key([mod], "n", lazy.layout.next()),
    Key([mod], "m", lazy.layout.previous()),
    Key([mod], "i", lazy.function(to_next_screen)), 

    # Switch groups.
    Key([mod], "Tab", lazy.screen.next_group(skip_empty=True, skip_managed=True)),
    Key([mod, "shift"], "Tab", lazy.function(rotate_screens)),
    Key([mod], "g", lazy.function(to_next_empty_group)),
    Key([mod, "shift"], "g", lazy.function(to_next_empty_group, move_current_window=True)),

    # Shuffle windows.
    Key([mod, "shift"], "Left", lazy.layout.shuffle_left()),
    Key([mod, "shift"], "Right", lazy.layout.shuffle_right()),
    Key([mod, "shift"], "Down", lazy.layout.shuffle_down()),
    Key([mod, "shift"], "Up", lazy.layout.shuffle_up()),
    Key([mod, "shift"], "i", lazy.function(to_next_screen, move_current_window=True)), 

    # Kill a window.
    Key([mod], "c", lazy.window.kill()),

	# Flip window nodes (works in BSP layout).
	Key([mod, "control"], "Left", lazy.layout.flip_left()),
	Key([mod, "control"], "Right", lazy.layout.flip_right()),
	Key([mod, "control"], "Down", lazy.layout.flip_down()),
	Key([mod, "control"], "Up", lazy.layout.flip_up()),
	Key([mod, "control"], "t", lazy.layout.toggle_split()),

    # Grow windows.
    # mod1 is left alt.
    Key([mod, "mod1"], "Left", lazy.layout.grow_left()),
    Key([mod, "mod1"], "Right", lazy.layout.grow_right()),
    Key([mod, "mod1"], "Down", lazy.layout.grow_down()),
    Key([mod, "mod1"], "Up", lazy.layout.grow_up()),
	Key([mod, "mod1"], "n", lazy.layout.normalize()),

    # Spawn programs.
    Key([mod], "Return", lazy.spawn("alacritty")),
    KeyChord([mod], "o", [
        Key([mod], "o", lazy.spawn("rofi -show drun -theme " + os.path.expanduser("~/.config/rofi/theme.rasi"))),
        Key([], "f", lazy.spawn("thunar")),
        Key([], "b", lazy.spawn("firefox")),
        Key([], "g", lazy.spawn("glava")),
        Key([], "l", lazy.spawn("xset dpms force off")),
        Key([], "s", lazy.function(focus_or_open, "steam", empty_group=True)),
        Key([], "y", lazy.function(focus_or_open, "youtubemusic", empty_group=True)),
        Key([], "d", lazy.function(focus_or_open, "discord", empty_group=True)),
        Key([], "t", lazy.function(focus_or_open, "todoist", empty_group=True)),
        Key([], "m", lazy.function(focus_or_open, "minecraft-launcher",
            empty_group=True,
            match=Match(title=re.compile("Minecraft")))),
    ]),
    
    # System controls.
    Key([mod, "control"], "r", lazy.reload_config()),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),

    # Sound controls.
    Key([], "XF86AudioRaiseVolume", lazy.spawn("pamixer --increase 5")),
    Key([], "XF86AudioLowerVolume", lazy.spawn("pamixer --decrease 5")),
    Key([], "XF86AudioMute", lazy.spawn("pamixer --toggle-mute")),
    Key([], "XF86AudioMicMute", lazy.spawn("pactl set-source-mute @DEFAULT_SOURCE@ toggle")),
]

groups = [
    Group("1"),
    Group("2"),
    Group("3"),
    Group("4"),
    Group("5"),
    Group("6"),
    Group("7"),
    Group("8"),
    Group("9"),
]

for group in groups:
    char = group.name[0]
    keys.extend([
        # mod+N switches to group N.
        Key([mod], char, lazy.group[group.name].toscreen(),
            desc="Switch to group {}".format(group.name)),

        # mod+shift+N switches to group N, and also moves the focused window.
        Key([mod, "shift"], char, lazy.window.togroup(group.name, switch_group=True),
            desc="Switch to & move focused window to group {}".format(group.name)),
    ])


layouts = [
    layout.Bsp(
        border_focus="#3d72c4",
        border_normal="#394252",
        border_width=3,
        margin=8,
        border_on_single=False,
        margin_on_single=False,
        fair=False,
        wrap_clients=True,
        grow_amount=1,
    ),
]

# Bar/widget settings.
bar_width               = 48
bar_border_width        = [0, 0, 0, 0]
bar_margin              = [0, 0, 0, 0]
bar_border_color        = ["295080", "000000", "000000", "000000"]
bar_background_color    = ["#243754", "#10152e"]
bar_highlight_color     = ["#3d72c4", "#10152e"]
bar_foreground_color    = "#c2e4ff"

# Default values for widgets.
widget_defaults = dict(
    font="JetBrains Mono",
    fontsize=24,
    padding=6,
    background=bar_background_color,
    foreground=bar_foreground_color,
)
extension_defaults = widget_defaults.copy()

##
# Return text for dropbox widget.
##
def dropbox_widget_text():
    cmd = "dropbox-cli status 2>/dev/null | grep Syncing"
    try:
        output = subprocess.check_output(cmd, shell=True, text=True)
        output = output.replace("\n", "")
    except subprocess.CalledProcessError:
        output = ""
    return "Syncing..." if output else "✓" 

##
# Return text for pacman widget.
##
def pacman_widget_text():
    cmd = os.path.expanduser('~/.config/qtile/scripts/days_since_last_pacman_update.sh')
    try:
        output = subprocess.check_output(cmd, shell=True, text=True)
        return output.replace("\n", "")
    except subprocess.CalledProcessError:
        return "?"

# Widgets that appear on the right side of the bar, and are shared between all screens.
right_widgets = [

    # CMUS widget
    widget.Cmus(
        background=bar_highlight_color,
        play_color="#00eeff",
    ),

    # Memory and CPU graphs
    # Memory graph
    widget.TextBox(background=bar_highlight_color, text="M:"),
    widget.MemoryGraph(
        type            = "box",
        border_width    = 1,
        samples         = 50,
        width           = 50,
        background      = bar_highlight_color,
        border_color    = bar_foreground_color, 
        graph_color     = bar_foreground_color,
    ),

    # CPU graph
    widget.TextBox(background=bar_highlight_color, text="C:"),
    widget.CPUGraph(
        type            = "box",
        border_width    = 1,
        samples         = 50,
        width           = 50,
        background      = bar_highlight_color,
        border_color    = bar_foreground_color, 
        graph_color     = bar_foreground_color,
    ),


    # Dropbox widget
    widget.Image(
        background=bar_highlight_color,
        filename=os.path.expanduser("~/.config/qtile/icons/dropbox.png"),
    ),
    widget.GenPollText(
        background          = bar_highlight_color,
        func                = dropbox_widget_text,
        update_interval     = 1,
    ),

    # Pacman widget
    widget.Image(
        background=bar_highlight_color,
        filename=os.path.expanduser("~/.config/qtile/icons/pacman.png"),
    ),
    widget.GenPollText(
        background          = bar_highlight_color,
        func                = pacman_widget_text,
        update_interval     = 10,
    ),

    # Volume widget
    widget.Image(
        background=bar_highlight_color,
        filename=os.path.expanduser("~/.config/qtile/icons/volume.png"),
        margin_x=-4,
    ),
    widget.Volume(background=bar_highlight_color),

    # Clock widget
    widget.Sep(background=bar_highlight_color),
    widget.Clock(
        format="%m/%d/%Y %I:%M %p",
        background=bar_highlight_color,
    ),
]

screens = [

    Screen(bottom=bar.Bar([
                widget.CurrentScreen(
                    active_text = '🟢',
                    inactive_text = '⭕',
                ),
                widget.GroupBox(
                    highlight_method            = "line",
                    hide_unused                 = True,
                    use_mouse_wheel             = False,
                    active                      = bar_highlight_color[0],
                    block_highlight_text_color  = bar_foreground_color,
                    highlight_color             = bar_highlight_color,
                    other_current_screen_border = bar_background_color[0],
                    other_screen_border         = bar_background_color[0],
                    this_current_screen_border  = bar_highlight_color[0],
                    this_screen_border          = bar_highlight_color[0],
                ),
                widget.Spacer(length=bar.STRETCH),
            ] + right_widgets,
            bar_width,
            border_width=bar_border_width,
            border_color=bar_border_color,
            background=bar_background_color,
            margin=bar_margin,
        ),
    ),

    Screen(bottom=bar.Bar([
                widget.CurrentScreen(
                    active_text = '🟢',
                    inactive_text = '⭕',
                ),
                widget.GroupBox(
                    highlight_method            = "line",
                    hide_unused                 = True,
                    use_mouse_wheel             = False,
                    active                      = bar_highlight_color[0],
                    block_highlight_text_color  = bar_foreground_color,
                    highlight_color             = bar_highlight_color,
                    other_current_screen_border = bar_background_color[0],
                    other_screen_border         = bar_background_color[0],
                    this_current_screen_border  = bar_highlight_color[0],
                    this_screen_border          = bar_highlight_color[0],
                ),
                widget.Spacer(length=bar.STRETCH),
            ] + right_widgets,
            bar_width,
            border_width=bar_border_width,
            border_color=bar_border_color,
            background=bar_background_color,
            margin=bar_margin,
        ),
    ),

    Screen(bottom=bar.Bar([
                widget.CurrentScreen(
                    active_text = '🟢',
                    inactive_text = '⭕',
                ),
                widget.GroupBox(
                    highlight_method            = "line",
                    hide_unused                 = True,
                    use_mouse_wheel             = False,
                    active                      = bar_highlight_color[0],
                    block_highlight_text_color  = bar_foreground_color,
                    highlight_color             = bar_highlight_color,
                    other_current_screen_border = bar_background_color[0],
                    other_screen_border         = bar_background_color[0],
                    this_current_screen_border  = bar_highlight_color[0],
                    this_screen_border          = bar_highlight_color[0],
                ),
                widget.Spacer(length=bar.STRETCH),
            ] + right_widgets,
            bar_width,
            border_width=bar_border_width,
            border_color=bar_border_color,
            background=bar_background_color,
            margin=bar_margin,
        ),
    ),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = False
bring_front_click = True
cursor_warp = False
floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
    ]
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = False

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"

# Autorun script when qtile starts
@hook.subscribe.startup
def autostart():
    autostart_script = os.path.expanduser('~/.config/qtile/scripts/autostart.sh')
    subprocess.call([autostart_script])

