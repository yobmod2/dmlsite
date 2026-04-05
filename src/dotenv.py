from __future__ import annotations

import os
import re
import sys
import warnings
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Sequence

line_re = re.compile(
    r"""
    ^
    (?:export\s+)?      # optional export
    ([\w\.]+)           # key
    (?:\s*=\s*|:\s+?)   # separator
    (                   # optional value begin
        '(?:\'|[^'])*'  #   single quoted value
        |               #   or
        "(?:\"|[^"])*"  #   double quoted value
        |               #   or
        [^#\n]+         #   unquoted value
    )?                  # value end
    (?:\s*\#.*)?        # optional comment
    $
""",
    re.VERBOSE,
)

variable_re = re.compile(
    r"""
    (\\)?               # is it escaped with a backslash?
    (\$)                # literal $
    (                   # collect braces with var for sub
        \{?             #   allow brace wrapping
        ([A-Z0-9_]+)    #   match the variable
        \}?             #   closing brace
    )                   # braces end
""",
    re.IGNORECASE | re.VERBOSE,
)


def open_dotenv(
    dotenv_dir: str | Path = "",
    filename: str = ".env",
) -> Path | None:
    """Finds .env file and checks it exists.
    If checks fail, logs a warning
    If checks succeed, returns Path"""
    if not dotenv_dir:
        frame_filename = sys._getframe().f_back.f_code.co_filename  # type: ignore
        dotenv_dir = Path(frame_filename).parent.resolve()
    elif isinstance(dotenv_dir, str | Path):
        dotenv_dir = Path(dotenv_dir)
    else:
        raise TypeError("Path to .env file should be [str | Path]")

    dotenv_path = dotenv_dir / filename
    if dotenv_path.exists():
        return dotenv_path
    else:
        warn_msg = "Not reading dotenv_dir."
        if not dotenv_dir.is_dir():
            warn_msg = warn_msg + f"No directory found at {dotenv_dir}"
        if not dotenv_path.is_file():
            warn_msg = warn_msg + f"No {filename} file found in {dotenv_dir}"
        warnings.warn(warn_msg, stacklevel=2)
        return None


def parse_dotenv(content: str) -> dict[str, str]:
    env = {}

    for line in content.splitlines():
        m1 = line_re.search(line)

        if m1:
            key, value = m1.groups()

            if value is None:
                value = ""

            # Remove leading/trailing whitespace
            value = value.strip()

            # Remove surrounding quotes
            m2 = re.match(r'^([\'"])(.*)\1$', value)

            if m2:
                quotemark, value = m2.groups()
            else:
                quotemark = None

            # Unescape all chars except $ so variables can be escaped properly
            if quotemark == '"':
                value = re.sub(r"\\([^$])", r"\1", value)

            if quotemark != "'":
                # Substitute variables in a value
                for parts in variable_re.findall(value):
                    if parts[0] == "\\":
                        # Variable is escaped, don't replace it
                        replace = "".join(parts[1:-1])
                    else:
                        # Replace it with the value from the environment
                        replace = env.get(parts[-1], os.environ.get(parts[-1], ""))

                    value = value.replace("".join(parts[0:-1]), replace)

            env[key] = value

        elif not re.search(r"^\s*(?:#.*)?$", line):  # not comment or blank
            warnings.warn(
                f"Line {line!r} doesn't match format", SyntaxWarning, stacklevel=1
            )

    return env


def get_dotenv(dotenv_path: Path) -> dict[str, str]:
    with dotenv_path.open() as f:
        env_dict = parse_dotenv(f.read())
    return env_dict


def set_dotenv(env_dict: dict[str, str], *, override=False) -> None:
    for k, v in env_dict.items():
        if override:
            os.environ[k] = v
        else:
            os.environ.setdefault(k, v)


def read_dotenv(
    dotenv_dir: str | Path = "",
    *,
    filename: str = ".env",
    set_env=True,
    override=False,
    return_dict=False,
) -> dict[str, str] | None:
    """
    Read a .env file and add it into os.environ and/or return it as a dict.

    If not given a path to a dotenv_dir path or filename,
    defaults to searching for .env in current and parent directories

    :override: True if values in .env should override system variables.
    :return_dict: True to return .env contents as a python dict[str|str]
    """
    dotenv_file = open_dotenv(dotenv_dir, filename=filename)
    if dotenv_file is not None:
        env_dict = get_dotenv(dotenv_file)
        if set_env:
            set_dotenv(env_dict, override=override)
        if return_dict:
            return env_dict
    else:
        return None


def print_dotenv(
    dotenv_dir: str | Path = "", *, filename: str = ".env", turn_on: bool = True
) -> None:
    """helper function to print .env contents for debugging.
    Uses read_dotenv(set_env=False) so does not add .env content to ENV_VARS"""
    if turn_on:
        env_read = read_dotenv(
            dotenv_dir, filename=filename, return_dict=True, set_env=False
        )
        if env_read:
            for k, v in env_read.items():
                print(f"{k.upper()} = {v}")
        else:
            print(".env file was empty or not found")


def print_sys_env(var: str | Sequence[str] | set[str] = "") -> None:
    """helper function to check current system environment VARS"""
    if var:
        if isinstance(var, str):
            var = [var]
        for v in var:
            v = v.upper()
            try:
                print(f"{v} = {os.environ[v]}")
            except KeyError as e:
                print(repr(e), "Key not found in ENVIRONMENT_VARS")
    else:
        print(os.environ)


if __name__ == "__main__":
    # read_dotenv(
    #     dotenv_dir="",  # will try to find dotenv_dir itself
    #     filename="dev.env",
    #     override=False,  # will not override already present ENV_VARS
    #     return_dict=True,
    # )
    # print_sys_env({"test_var_str", "SHELL"})  # print specific env_var already in system
    # print_dotenv(filename="dmlsite.env", turn_on=True)
    pass
