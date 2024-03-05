#! /usr/bin/env python3

from i3ipc import Connection
sway = Connection()

# Kill all windows
if __name__ == "__main__":
    for c in sway.get_tree().leaves():
        sway.command('[con_id="{}"] kill'.format(c.id))

