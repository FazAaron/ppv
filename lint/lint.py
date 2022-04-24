from pylint import lint


def lint_file(options=[]):
    if len(options) > 0:
        file_name = options[len(options) - 1]
        print(f"Linting: {file_name}")
        options = ["--disable=E0401"] + options
        options = [
            "--msg-template='{msg_id}:{line:3d},{column}: {obj}: {msg}'"
        ] + options
        lint.Run(options, do_exit=False)


# Lint options
options = [["--disable=C0103",
            "--disable=R0913",
            "src/components/application.py"],
           ["src/components/interface.py"],
           ["--disable=R0903", "src/components/link.py"],
           ["--disable=C0103",
            "--disable=R0913",
            "--disable=R0201",
            "--disable=R0904",
            "src/components/network.py"],
           ["--disable=C0103",
            "--disable=W0223",
            "--disable=R0201",
            "src/components/node.py"],
           ["--disable=R0903", "src/components/packet.py"],
           ["src/components/routing_table.py"],
           ["--disable=R0914",
            "--disable=C0103",
            "--disable=R1710",
            "--disable=R0912",
            "src/utils/graph.py"],
           ["--disable=R1732",
            "--disable=R0903",
            "src/utils/logger.py"],
           ["src/utils/regex_checker.py"],
           ["--disable=R0903",
            "src/event_handlers/simulation.py"],
           ["--disable=R0903",
            "src/graphic_handlers/main_window.py"],
           ["--disable=R0903",
            "src/graphic_handlers/object_canvas.py"],
           ["--disable=R0903",
            "src/graphic_handlers/object_frame.py"],
           ["--disable=R0903",
            "src/graphic_handlers/statistics_frame.py"]]

for option in options:
    lint_file(option)
