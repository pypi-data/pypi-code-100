# This file is part of tdmclient-ty.
# Copyright 2021 ECOLE POLYTECHNIQUE FEDERALE DE LAUSANNE,
# Miniature Mobile Robots group, Switzerland
# Author: Yves Piguet
#
# SPDX-License-Identifier: BSD-3-Clause

from thonny import get_workbench, get_shell
from tdmclient import ClientAsync, aw
from tdmclient.atranspiler import ATranspiler, TranspilerError
from tdmclient.module_thymio import ModuleThymio
from tdmclient.module_clock import ModuleClock

import tkinter
import sys

client = None
node = None

def connect():
    global client, node
    if client is None:
        client = ClientAsync()
        node = aw(client.wait_for_node())
        aw(node.lock())
        get_workbench().after(100, process_incoming_messages)  # schedule after 100 ms

def disconnect():
    global client, node
    if client is not None:
        aw(node.unlock())
        node = None
        client = None

def process_incoming_messages():
    if client is not None:
        client.process_waiting_messages()
        get_workbench().after(100, process_incoming_messages)  # reschedule after 100 ms

def get_source_code():
    editor = get_workbench().get_editor_notebook().get_current_editor()
    code_view = editor.get_code_view()
    source_code = str(code_view.get_content_as_bytes(), "utf-8")
    return source_code

def print_to_shell(str, stderr=False):
    text = get_shell().text
    text._insert_text_directly(str, ("io", "stderr") if stderr else ("io",))
    text.see("end")

def print_error(str):
    get_shell().print_error(str)

def print_transpiled_code():
    # get source code
    program = get_source_code()

    # transpile from Python to Aseba
    transpiler = ATranspiler()
    modules = {
        "thymio": ModuleThymio(transpiler),
        "clock": ModuleClock(transpiler),
    }
    transpiler.modules = {**transpiler.modules, **modules}
    transpiler.set_preamble("""from thymio import *
""")
    transpiler.set_source(program)
    try:
        transpiler.transpile()
    except TranspilerError as error:
        print_error(f"\n{error.message}\n")
        return
    program = transpiler.get_output()

    # display in the shell
    print_to_shell("\n" + program)

print_statements = None
exit_received = False
has_started_printing = False  # to print LF before anything else

def on_event_received(node, event_name, event_data):
    global has_started_printing, exit_received
    if event_name == "_exit":
        exit_received = event_data[0]
        stop()
    elif event_name == "_print":
        print_id = event_data[0]
        print_format, print_num_args = print_statements[print_id]
        print_args = tuple(event_data[1 : 1 + print_num_args])
        print_str = print_format % print_args
        if not has_started_printing:
            print_to_shell("\n")
            has_started_printing = True
        print_to_shell(print_str + "\n")
    else:
        if not has_started_printing:
            print_to_shell("\n")
            has_started_printing = True
        print_to_shell(event_name + "".join(["," + str(d) for d in event_data]) + "\n")

def run():
    # get source code
    program = get_source_code()

    # transpile from Python to Aseba
    transpiler = ATranspiler()
    modules = {
        "thymio": ModuleThymio(transpiler),
        "clock": ModuleClock(transpiler),
    }
    transpiler.modules = {**transpiler.modules, **modules}
    transpiler.set_preamble("""from thymio import *
""")
    transpiler.set_source(program)
    try:
        transpiler.transpile()
    except TranspilerError as error:
        print_error(f"\n{error.message}\n")
        return
    program = transpiler.get_output()

    events = []

    global print_statements
    print_statements = transpiler.print_format_strings
    if len(print_statements) > 0:
        events.append(("_print", 1 + transpiler.print_max_num_args))
    if transpiler.has_exit_event:
        events.append(("_exit", 1))
    for event_name in transpiler.events_in:
        events.append((event_name, transpiler.events_in[event_name]))
    for event_name in transpiler.events_out:
        events.append((event_name, transpiler.events_out[event_name]))

    global has_started_printing, exit_received
    has_started_printing = False
    exit_received = False

    # make sure we're connected
    connect()

    # run
    async def prog():
        nonlocal events
        if len(events) > 0:
            events = await node.filter_out_vm_events(events)
            await node.register_events(events)
        error = await node.compile(program)
        if error is not None:
            print_error(f"Compilation error: {error['error_msg']}\n")
        else:
            client.clear_events_received_listeners()
            if len(events) > 0:
                client.add_event_received_listener(on_event_received)
                await node.watch(events=True)
            error = await node.run()
            if error is not None:
                print_error(f"Run error {error['error_code']}\n")
        error = await node.set_scratchpad(program)
        if error is not None:
            pass  # ignore

    client.run_async_program(prog)

def stop():
    async def prog():
        error = await node.stop()
        if error is not None:
            print_error(f"Stop error {error['error_code']}\n")

    connect()
    client.run_async_program(prog)

def load_plugin():
    get_workbench().add_command(command_id="run_th",
                                menu_name="tools",
                                command_label="Run on Thymio",
                                default_sequence="<Control-Shift-R>",
                                handler=run)
    get_workbench().add_command(command_id="transpile_th",
                                menu_name="tools",
                                command_label="Transpile Program",
                                handler=print_transpiled_code)
    get_workbench().add_command(command_id="stop_th",
                                menu_name="tools",
                                command_label="Stop Thymio",
                                default_sequence="<Control-Shift-space>",
                                handler=stop)
    get_workbench().add_command(command_id="unlock_th",
                                menu_name="tools",
                                command_label="Unlock Thymio",
                                handler=disconnect)
