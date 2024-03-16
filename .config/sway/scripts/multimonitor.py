#! /usr/bin/env python3

import sys
import types
from i3ipc import Connection
sway = Connection()

def current_container():
    return sway.get_tree().find_focused()

def current_workspace():
    return sway.get_tree().find_focused().workspace()

def current_output():
    for op in sway.get_outputs():
        if op.focused:
            return op

def next_output():
    outputs = sway.get_outputs()
    current_index = [op.focused for op in outputs].index(True)
    next_index = (current_index + 1) % len(outputs)
    return outputs[next_index]
    
def prev_output():
    outputs = sway.get_outputs()
    current_index = [op.focused for op in outputs].index(True)
    prev_index = (current_index - 1) % len(outputs)
    return outputs[prev_index]

def workspaces_on_output(op):
    workspaces = []
    for ws in sway.get_workspaces():
        if ws.output == op.name:
            workspaces.append(ws)
    return workspaces

def current_workspace_on_output(op):
    workspaces = workspaces_on_output(op)
    current_index = [ws.visible for ws in workspaces].index(True)
    return workspaces[current_index]

def next_workspace_on_output(op):
    workspaces = workspaces_on_output(op)
    current_index = [ws.visible for ws in workspaces].index(True)
    next_index = (current_index + 1) % len(workspaces)
    return workspaces[next_index]

def prev_workspace_on_output(op):
    workspaces = workspaces_on_output(op)
    current_index = [ws.visible for ws in workspaces].index(True)
    prev_index = (current_index - 1) % len(workspaces)
    return workspaces[prev_index]

def output_of_workspace(ws):
    for op in sway.get_outputs():
        if op.name == ws.ipc_data['output']:
            return op

def new_workspace(op):
    # Get the next unused workspace number on this output.
    # The "next" number is the smallest unused workspace number after the smallest used workspace number on this output.
    used_nums_on_output = [ws.num for ws in sway.get_workspaces() if ws.output == op.name]
    n = min(used_nums_on_output)
    while n in used_nums_on_output:
        n += 1
    ws = types.SimpleNamespace()
    ws.num = n
    ws.name = str(n)
    return ws

def workspace_is_empty(ws):
    for con in sway.get_tree().workspaces():
        if con.name == ws.name and con.leaves():
            return False
    return True

def focus_container(c):
    sway.command('[con_id="{}"] focus'.format(c.id))

def focus_workspace(ws):
    sway.command('workspace number {}'.format(ws.num))

def focus_output(op):
    focus_workspace(current_workspace_on_output(op))

def move_container_to_workspace(c, ws):
    sway.command('[con_id="{}"] move container to workspace number {}'.format(c.id, ws.num))

def move_workspace_to_output(ws, op):
    # No way to do this on an empty workspace without focusing on it.
    initial_ws = current_workspace()
    sway.command('workspace "{}", move workspace to output {}'.format(ws.name, op.name))
    focus_workspace(initial_ws)

def move_workspace_to_output_and_focus(ws, op):
    sway.command('workspace "{}", move workspace to output {}'.format(ws.name, op.name))

def move_container_to_output(c, op):
    move_container_to_workspace(c, current_workspace_on_output(op))

def move_focused_container_to_workspace(ws):
    move_container_to_workspace(current_container(), ws)

def move_focused_workspace_to_output(op):
    move_workspace_to_output(current_workspace(), op)

def move_focused_container_to_output(op):
    move_container_to_output(current_container(), op)

def cycle_outputs_next():
    outputs = sway.get_outputs()
    new_assignments = {}
    starting_ws = current_workspace()
    for i in range(len(outputs)):
        next_op = outputs[(i + 1) % len(outputs)]
        new_assignments[next_op] = workspaces_on_output(outputs[i])
    for op, workspaces in new_assignments.items():
        for ws in workspaces:
            move_workspace_to_output_and_focus(ws, op)
    focus_workspace(starting_ws)

def cycle_outputs_prev():
    outputs = sway.get_outputs()
    new_assignments = {}
    starting_ws = current_workspace()
    for i in range(len(outputs)):
        prev_op = outputs[(i - 1) % len(outputs)]
        new_assignments[prev_op] = workspaces_on_output(outputs[i])
    for op, workspaces in new_assignments.items():
        for ws in workspaces:
            move_workspace_to_output(ws, op)
    focus_workspace(starting_ws)

def handle(arg):
    match arg:
        case "focus_next_output":
            focus_output(next_output())

        case "focus_prev_output":
            focus_output(prev_output())

        case "focus_next_workspace":
            focus_workspace(next_workspace_on_output(current_output()))

        case "focus_prev_workspace":
            focus_workspace(prev_workspace_on_output(current_output()))

        case "focus_new_workspace":
            op = current_output()
            ws = new_workspace(op)
            move_workspace_to_output_and_focus(ws, op)

        case "move_container_to_new_workspace":
            c = current_container()
            op = current_output()
            ws = new_workspace(op)
            move_workspace_to_output_and_focus(ws, op)
            move_container_to_workspace(c, ws)
            focus_container(c)

        case "move_container_to_next_output":
            c = current_container()
            op = next_output()
            move_container_to_output(c, op)
            focus_container(c)

        case "move_container_to_prev_output":
            c = current_container()
            op = prev_output()
            move_container_to_output(c, op)
            focus_container(c)

        case "move_workspace_to_next_output":
            ws = current_workspace()
            op = next_output()
            move_workspace_to_output(ws, op)
            focus_workspace(ws)

        case "move_workspace_to_prev_output":
            ws = current_workspace()
            op = prev_output()
            move_workspace_to_output(ws, op)
            focus_workspace(ws)

        case "cycle_outputs_next":
            ws = current_workspace()
            cycle_outputs_next()
            focus_workspace(ws)

        case "cycle_outputs_prev":
            ws = current_workspace()
            cycle_outputs_prev()
            focus_workspace(ws)

if __name__ == "__main__":
    args = sys.argv[1:]
    if len(args) != 1:
        raise RuntimeError("Expect one arg")
    handle(args[0])

