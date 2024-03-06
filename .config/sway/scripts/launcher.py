#! /usr/bin/env python3

import socket
from typing import Callable
from i3ipc import Connection, Event

sway = Connection()

class Program:
    def __init__(self, name:str, cmd:str, workspace:str, matcher:Callable,
            enabled:bool=True, do_relaunch:bool=False, timeout_secs:float=5,
            post_swaycmd:str=None):
        self.name           = name
        self.cmd            = cmd
        self.workspace      = workspace
        self.matcher        = matcher
        self.enabled        = enabled
        self.do_relaunch    = do_relaunch
        self.timeout_secs   = timeout_secs
        self.post_swaycmd   = post_swaycmd


def programs_to_launch():
    match socket.gethostname():

        case "ripley":
            return [
                Program(
                    name            = 'youtube_music',
                    workspace       = "9",
                    cmd             = 'google-chrome "--profile-directory=Default" ' +
                                        '"--app-id=cinhimbnkkaeohfgghhklpknlkffjgod"',
                    matcher         = match_chrome_app('cinhimbnkkaeohfgghhklpknlkffjgod'),
                ),
                Program(
                    name            = 'glava',
                    workspace       = "9",
                    cmd             = 'glava',
                    matcher         = match_by_window_props('GLava', 'GLava'),
                    post_swaycmd    = 'move up, resize set height 200px, focus next',
                ),
                Program(
                    name            = 'term_stui',
                    workspace       = "10",
                    cmd             = 'alacritty --class term_stui --command s-tui',
                    matcher         = match_by_app_id('term_stui'),
                ),
                Program(
                    name            = 'term_htop',
                    workspace       = "10",
                    cmd             = 'alacritty --class term_htop --command htop',
                    matcher         = match_by_app_id('term_htop'),
                    post_swaycmd    = 'focus',
                ),
                Program(
                    name            = 'discord',
                    workspace       = "3",
                    cmd             = 'discord',
                    matcher         = match_discord(),
                    timeout_secs    = 10,
                ),
                Program(
                    name            = 'todoist',
                    workspace       = "2",
                    cmd             = 'todoist',
                    matcher         = match_by_window_props('Todoist', 'todoist'),
                    timeout_secs    = 10,
                ),
                Program(
                    name            = 'mail',
                    workspace       = "1",
                    cmd             = 'google-chrome "--profile-directory=Default" ' +
                                        '"--app-id=fmgjjmmmlfnkbppncabfkddbjimcfncm"',
                    matcher         = match_chrome_app('fmgjjmmmlfnkbppncabfkddbjimcfncm'),
                ),
                Program(
                    name            = 'calendar',
                    workspace       = "1",
                    cmd             = 'google-chrome "--profile-directory=Default" ' +
                                        '"--app-id=kjbdgfilnfhdoflbpgamdcdgpehopbep"',
                    matcher         = match_chrome_app('kjbdgfilnfhdoflbpgamdcdgpehopbep'),
                    post_swaycmd    = 'move left, resize set width 40ppt, focus next',
                ),
            ]
            
        case "viviancox-glaptop":
            return [
                Program(
                    name            = 'youtube_music',
                    workspace       = "9",
                    cmd             = 'google-chrome "--profile-directory=Profile 1" ' +
                                        '"--app-id=cinhimbnkkaeohfgghhklpknlkffjgod"',
                    matcher         = match_by_app_id('chrome-cinhimbnkkaeohfgghhklpknlkffjgod-Profile_1'),
                ),
                Program(
                    name            = 'term_cava',
                    workspace       = "9",
                    cmd             = 'alacritty --class term_cava --command cava',
                    matcher         = match_by_app_id('term_cava'),
                    post_swaycmd    = 'move up, resize set height 200px, focus next',
                ),
                Program(
                    name            = 'term_stui',
                    workspace       = "10",
                    cmd             = 'alacritty --class term_stui --command s-tui',
                    matcher         = match_by_app_id('term_stui'),
                ),
                Program(
                    name            = 'term_htop',
                    workspace       = "10",
                    cmd             = 'alacritty --class term_htop --command htop',
                    matcher         = match_by_app_id('term_htop'),
                    post_swaycmd    = 'focus',
                ),
                Program(
                    name            = 'term_work',
                    workspace       = "4",
                    cmd             = 'alacritty --class term_work --command bash -ic "wait work"',
                    matcher         = match_by_app_id('term_work'),
                ),
                Program(
                    name            = 'empty_browser',
                    workspace       = "2",
                    cmd             = 'google-chrome --new-window',
                    matcher         = match_by_app_id('google-chrome'),
                ),
                Program(
                    name            = 'gmail',
                    workspace       = "1",
                    cmd             = 'google-chrome "--profile-directory=Profile 1" ' +
                                        '"--app-id=fmgjjmmmlfnkbppncabfkddbjimcfncm"',
                    matcher         = match_by_app_id('chrome-fmgjjmmmlfnkbppncabfkddbjimcfncm-Profile_1'),
                ),
                Program(
                    name            = 'calendar',
                    workspace       = "1",
                    cmd             = 'google-chrome "--profile-directory=Profile 1" ' +
                                        '"--app-id=kjbdgfilnfhdoflbpgamdcdgpehopbep"',
                    matcher         = match_by_app_id('chrome-kjbdgfilnfhdoflbpgamdcdgpehopbep-Profile_1'),
                    post_swaycmd    = 'move left, resize set width 25ppt, focus next',
                ),
            ]

        case _:
            raise RuntimeError("Unknown hostname.")


def match_by_app_id(app_id:str):
    def matcher(c):
        return c.app_id == app_id
    return matcher

def match_by_window_props(window_class:str, window_instance:str):
    def matcher(c):
        return (
            'window_properties' in c.ipc_data and
            'class' in c.ipc_data['window_properties'] and
            'instance' in c.ipc_data['window_properties'] and
            c.ipc_data['window_properties']['class'] == window_class and
            c.ipc_data['window_properties']['instance'] == window_instance )
    return matcher

def match_chrome_app(chrome_app_id:str):
    return match_by_window_props('Google-chrome', 'crx_' + chrome_app_id)

def match_discord():
    # Need another condition to match Discord, because the startup icon
    # has the same window properties as the main discord window.
    def matcher(c):
        return match_by_window_props('discord', 'discord') and c.geometry.height > 350
    return matcher

def sway_exec(command:str):
    sway.command('exec {}'.format(command))

def sway_move(con_id:int, workspace:str):
    sway.command('[con_id="{}"] move container to workspace {}'.format(
        con_id, workspace))

def sway_container_cmd(con_id:int, swaycmd:str):
    sway.command('[con_id="{}"] {}'.format(
        con_id, swaycmd))

def sway_already_launched(matcher:Callable, workspace:str):
    for c in sway.get_tree().leaves():
        if c.workspace().name == workspace and matcher(c):
            return True
    return False

def launch(p:Program):
    if not p.do_relaunch and sway_already_launched(p.matcher, p.workspace):
        return

    def new_window_callback(self, e):
        if e.change == 'new' and p.matcher(e.container):
            sway_move(e.container.id, p.workspace)
            if p.post_swaycmd:
                sway_container_cmd(e.container.id, p.post_swaycmd)
            sway.main_quit()

    sway.on(Event.WINDOW_NEW, new_window_callback)
    sway_exec(p.cmd)
    sway.main(timeout=p.timeout_secs)
    sway.off(new_window_callback)


def main():
    for p in programs_to_launch():
        if p.enabled:
            launch(p)

if __name__ == "__main__":
    main()


