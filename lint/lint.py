from pylint import lint
from pathlib import Path


def lint_file(options=[], lint_log_file=""):
    if len(options) > 0:
        file_name = options[len(options) - 1]
        print(f"Linting: {file_name}")
        if lint_log_file != "":
            Path("./logs").mkdir(parents=True, exist_ok=True)
            with open(lint_log_file, "w"):
                pass
            options = [
                "--msg-template='{msg_id}:{line:3d},{column}: {obj}: {msg}'"
            ] + options
            options = [f"--output-format=json:{lint_log_file}"] + options
        lint.Run(options, do_exit=False)


# Lint options
options = [["--disable=C0103", "--disable=R0913", "src/components/application.py"],
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
            "src/utils/logger.py"]]

for option in options:
    # Split by /, get the file name from the path,
    # then split by . and get file name without extension
    file_name = option[len(option) - 1].split("/")[2].split(".")[0]
    lint_file(option, f"logs/{file_name}.json")
