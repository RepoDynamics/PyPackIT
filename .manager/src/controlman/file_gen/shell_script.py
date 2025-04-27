from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Literal


def create_script(
    name: str,
    data: dict,
    global_functions: dict | None = None
) -> str:
    lines = [
        f"#!{data["shebang"].removeprefix("#!")}",
        "set -euo pipefail",
        *create_cleanup_function(data.get("function", {})),
    ]
    functions = {
        func_name: func_data for func_name, func_data in (global_functions or {}).items()
        if func_name in data.get("import", [])
    } | data.get("function", {})
    for func_name, func_data in sorted(functions.items()):
        lines.extend(create_function(func_name, func_data))
    lines.extend(
        [
            '_LOGFILE_TMP="$(mktemp)"',  # Create a temporary log file
            'exec > >(tee -a "$_LOGFILE_TMP") 2>&1',  # Redirect stdout and stderr into the log file
            log_endpoint(name, typ="script", stage="entry"),
            'trap __cleanup__ EXIT',  # Call cleanup function on exit
        ]
    )
    parameters = data.get("parameter")
    if parameters:
        lines.extend(
            [
                'if [ "$#" -gt 0 ]; then',
                indent(log(f"Script called with arguments: $@", "info"), 1),
                *indent(create_argparse(parameters, local=True), 1),
                "else",
                indent(log("Script called with no arguments. Read environment variables.", "info"), 1),
                *indent(create_env_var_parse(parameters), 1),
                "fi",
                '[[ "$DEBUG" == true ]] && set -x',
                *create_validation_block(parameters, local=True),
            ]
        )
    lines.extend(
        [
            *sanitize_code([section["content"] for section in data.get("body", [])]),
            *create_output(data.get("return")),
            log_endpoint(name, typ="script", stage="exit"),
        ]
    )
    return "\n".join(lines)


def create_env_var_parse(parameters: dict):
    lines = []
    for param_name, param_data in sorted(parameters.items()):
        var_name = param_name_to_var_name(param_name, local=False)
        param_type = param_data["type"]
        if param_type == "array":
            array_lines = [
                f'if [ "${{{var_name}+defined}}" ]; then',
                indent(log(f"Parse '{pram_name}' into array: '${var_name}'", "info"), 1),
                indent(f'IFS="{param_data["array_delimiter"]}" read -r -a _tmp_array <<< "${var_name}"', 1),
                indent(f'{var_name}=("${{_tmp_array[@]}}")', 1),
                indent(f'for _item in "${{{var_name}[@]}}"; do', 1),
                indent(log_arg_read(param_name, "_item"), 2),
                indent("done", 1),
                indent(f'unset _item', 1),
                indent(f'unset _tmp_array', 1),
                "fi",
            ]
            lines.extend(array_lines)
        else:
            lines.append(f'[ "${{{var_name}+defined}}" ] && {log_arg_read(param_name, var_name)}')
    return lines


def create_cleanup_function(functions: dict) -> list[str]:
    """Generate a cleanup function to be called on script exit.

    Parameters
    ----------
    functions
        Dictionary containing function names and their data.

    Returns
    -------
    Shell command (as a list of lines) to define the cleanup function.
    """
    func = functions.get("__cleanup__", {})
    func.setdefault("body", [])
    if isinstance(func["body"], str):
        func["body"] = func["body"].splitlines()
    log_cleanup_lines = [
        'if [ -n "${LOGFILE-}" ]; then',
        indent(log("Write logs to file '$LOGFILE'", "info"), 1),
        indent('mkdir -p "$(dirname "$LOGFILE")"', 1),
        indent('cat "$_LOGFILE_TMP" >> "$LOGFILE"', 1),
        indent('rm -f "$_LOGFILE_TMP"', 1),
        "fi",
    ]
    func["body"].extend(log_cleanup_lines)
    return create_function("__cleanup__", func)


def create_function(
    name: str,
    data: dict
) -> list[str]:
    parameters = data.get("parameter")
    body_lines = [
        log_endpoint(name, typ="function", stage="entry"),
        *create_argparse(parameters, local=True),
        *create_validation_block(parameters, local=True),
        *sanitize_code(data["body"]),
        *create_output(data.get("return")),
        log_endpoint(name, typ="function", stage="exit"),
    ]
    return [f"{name}() {{", *indent(body_lines, 1), "}"]


def create_output(returns: list[dict]) -> list[str]:
    """Generate a snippet to return values from a function or script.

    Depending on the number of returns and their types,
    it uses different methods to format the output:
    - **Single scalar value**: `echo` is used to print the value to stdout.
      The caller can read the value from stdout like this:
      `return_value=$(my_function)`
    - **Single array value**: `printf` is used to print each element of the array
      to stdout, separated by a null character (`\\0`).
      The caller can read the value like this:
      - Read into an array (e.g. when number of elements is unknown):
        ```bash
        # Call `my_function` and read the output into an array called `return_values`
        mapfile -d '' -t return_values < <(my_function)
        # Access elements of the array by index
        echo "${return_values[0]}"  # First element
        ```
      - Read into separate variables (when number of elements is known):
        ```bash
        # Call `my_function` and read the output into two variables `return_value1` and `return_value2`
        IFS= read -r -d '' return_value1 return_value2 < <(my_function)
        ```
    - **Multiple scalar values**: Same as single array value.
    - **Multiple values with mixed types**: Top-level return values
      can be read identically to the single array value.
      Additionally, each array return value is printed with a sub-separator (`\\x1F`)
      and can be further processed by the caller:
      ```bash
      # Assuming `my_function` returns a scalar and an array:
      IFS= read -r -d '' scalar_value array_value < <(my_function)
      # Now parse array_value into an array
      mapfile -d $'\\x1F' -t array1 < <(printf '%s' "$array_value")

    Parameters
    ----------
    returns
        List of dictionaries containing return information.
    """
    def output_array(var_label: str, var_name: str, separator) -> list[str]:
        return [
            f'for elem in "${{{var_name}[@]}}"; do',
            indent(log_arg_write(var_label, var_name), 1),
            indent(f'''printf '%s{separator}' "$elem"''', 1),
            "done",
        ]

    top_separator = "\\0"
    sub_separator = "\\x1F"

    num_returns = len(returns or [])
    if num_returns == 0:
        return []
    if num_returns == 1:
        var = returns[0]
        var_type = var["type"]
        var_name = var["variable"]
        var_label = var["name"]
        if var_type != "array":
            # Single scalar return
            return [log_arg_write(var_label, var_name), f'echo "${{{var_name}}}"']
        # Single array return
        return output_array(var_label, var_name, top_separator)
    # Multiple returns
    lines = []
    for ret in returns:
        var_type = ret["type"]
        var_name = ret["variable"]
        var_label = ret["name"]
        if var_type == "array":
            lines.extend(
                [*output_array(var_label, var_name, sub_separator), f"printf '{top_separator}'"]
            )
        else:
            lines.append(log_arg_write(var_label, var_name))
            lines.append(f'''printf '%s{top_separator}' "${{{var_name}}}"''')
    return lines


def create_argparse(
    parameters: dict,
    local: bool,
) -> list[str]:
    """Generate a snippet to parse command-line arguments.

    Parameters
    ----------
    parameters
        Dictionary containing parameter information.
    local
        Whether the variables are local or global.

    Returns
    -------
    Shell snippet (as a list of lines) to parse command-line arguments.
    """
    if not parameters:
        return []
    def_lines = []
    argparse_lines = [
        f"while [[ $# -gt 0 ]]; do",
        indent("case $1 in", 1),
    ]
    for param_name, param_data in sorted(parameters.items()):
        var_name = param_name_to_var_name(param_name, local)
        param_type = param_data["type"]
        param_default = param_data.get("default")
        if param_type == "boolean":
            initial_value = '""'
            argparse_cmd = f"{var_name}=true; {log_arg_read(param_name, var_name)}"
        elif param_type == "string":
            initial_value = '""'
            argparse_cmd = f'{var_name}="$1"; {log_arg_read(param_name, var_name)}; shift'
        elif param_type == "array":
            initial_value = "()"
            argparse_cmd = f'while [[ $# -gt 0 && ! "$1" =~ ^-- ]]; do {var_name}+=("$1"); {log_arg_read(param_name, "1")}; shift; done'
        else:
            raise ValueError(f"Unsupported parameter type: {param_type}")
        def_lines.append(f"{"local " if local else ""}{var_name}={initial_value}")
        argparse_lines.append(
            indent(f"--{param_name}) shift; {argparse_cmd};;", 2)
        )
    argparse_lines.extend(
        [
            indent(f"--*) {log(f'Unknown option: "$1"', 'critical')};;", 2),
            indent(f"*) {log(f'Unexpected argument: "$1"', 'critical')};;", 2),
        ]
    )
    argparse_lines.extend([indent("esac", 1), "done"])
    lines = def_lines + argparse_lines
    return lines


def create_validation_block(parameters: dict, local: bool) -> list[str]:
    lines = []
    for param_name, param_data in sorted((parameters or {}).items()):
        lines.extend(
            validate_variable(
                var_name=param_name_to_var_name(param_name, local=local),
                var_type=param_data["type"],
                default=param_data.get("default"),
                validations=param_data.get("validation", {}),
            )
        )
    return lines


def validate_variable(
    var_name: str,
    var_type: Literal["string", "array", "boolean"],
    default: str | list[str] | None,
    validations: dict | None,
) -> list[str]:
    """Generate validation checks for a variable.

    Parameters
    ----------
    var_name
        Name of the variable to validate.
    var_type
        Type of the variable.
        Options are "string", "array", or "boolean".
    default
        Default value to set if the variable is empty.
        If None, the variable is considered required.
    validations
        Dictionary of validation checks to apply.
        Supported validations are:
        - "enum": Check if the variable is one of the allowed values.
        - "path_existence": Check if the variable points to a valid path.
        - "custom": Custom validation function.

    Returns
    -------
    Shell command (as a list of lines) to validate the variable.
    """
    if var_type == "boolean":
        return []
    validator_names = {"enum", "path_existence"}
    validations = validations or {}
    out = [
        validate_missing_arg(
            var_name=var_name,
            var_type=var_type,
            default=default,
        )
    ]
    has_non_custom_validations = any(validator_name in validations for validator_name in validator_names)
    in_for_loop = has_non_custom_validations and var_type == "array"
    if in_for_loop:
        out.append(f'for elem in "${{{var_name}[@]}}"; do')
    for validation_name, validation_data in validations.items():
        if validation_name == "enum":
            validation_lines = validation_enum(var_name=var_name, enum=validation_data)
        elif validation_name == "path_existence":
            validation_lines = validate_path_existence(var_name=var_name, **validation_data)
        else:
            raise ValueError(f"Unsupported validation type: {validation_name}")
        out.extend(indent(validation_lines, indent=1 if in_for_loop else 0))
    if in_for_loop:
        out.append("done")
    custom = validations.get("custom")
    if custom:
        out.extend(custom)
    return out


def validate_missing_arg(
    var_name: str,
    var_type: Literal["string", "array"],
    default: str | list[str] | None,
) -> str:
    """Generate a validation check for missing arguments.

    The generated function first checks whether the variable is empty.
    If so, it sets the variable to its default value (if provided) and prints a message.
    If the variable does not have a default value,
    it prints an error message and returns an exit code of 1.

    Parameters
    ----------
    var_name
        Name of the variable to check.
    var_type
        Type of the variable.
        Options are "string" or "array".
    default
        Default value to set if the variable is empty.
        If None, the variable is considered required.

    Returns
    -------
    Shell command (as a list of lines) to validate the variable.
    """
    def info_default_set(default_value: str) -> str:
        return log(f"Argument '--{var_name}' set to default value '{default_value}'.", "info")

    err_missing_arg = log(f"Missing required argument '{var_name}'.", "critical")
    if var_type == "string":
        check = f'[ -z "${{{var_name}-}}" ]'  # True if var_name is not set or empty
        action = err_missing_arg if default is None else f'{info_default_set(default)}; {var_name}="{default}"'
    elif var_type == "array":
        check = f'{{ [ "${{{var_name}+isset}}" != "isset" ] || [ ${{#{var_name}[@]}} -eq 0 ] }}'
        if default is None:
            action = err_missing_arg
        else:
            default_str = f"({" ".join(f'"{elem}"' for elem in default)})"
            action = f'{info_default_set(default_str)}; {var_name}={default_str}'
    return f'{check} && {{ {action}; }}'


def validate_enum(
    var_name: str,
    enum: list[str],
) -> list[str]:
    """Generate a validation check for enum values.

    Generate a shell command to verify that a variable's value is one of the allowed
    values in the enum list. If the value is not in the enum, an error message is printed
    to stderr and the script exits with code 1.

    Parameters
    ----------
    var_name
        Name of the variable to check.
    enum
        List of allowed values for the variable.

    Returns
    -------
    Shell command (as a list of lines) to validate the variable's value.
    """
    enum_str = "|".join(f'"{elem}"' for elem in [*enum, ""])
    return [
        f'case "${var_name}" in',
        indent(f"{enum_str});;", 1),
        indent(f"*) {log(f"Invalid value for argument '--{var_name}': '${var_name}'", 'critical')};;", 1),
        "esac",
    ]


def validate_path_existence(
    var_name: str,
    must_exist: bool,
    path_type: Literal["dir", "exec", "file", "symlink"] | None = None,
) -> list[str]:
    """Generate a validation check for path existence.

    Generate a shell command to verify that a path stored in a variable
    exists or does not exist, depending on the `must_exist` parameter.
    Additionally, the type of the path (e.g., directory, file) can be
    validated using the `path_type` parameter.

    Parameters
    ----------
    var_name
        Name of the variable holding the path to check.
    must_exist
        If True, the path must exist.
        If False, the path must not exist.
    path_type
        Type of the path to check.
        Options are:
        - "dir": Check if the path is a directory.
        - "exec": Check if the path is an executable file.
        - "file": Check if the path is a regular file.
        - "symlink": Check if the path is a symbolic link.
        - None (default): Do not check the type.

    Returns
    -------
    Shell command (as a list of lines) to validate the path existence.
    If the condition is not met, the generated command will print an error message
    to stderr and return exit code 1.

    Examples
    --------
    >>> validate_path_existence(var_name="my_dir", must_exist=True, path_type="dir")
    ['[ ! -d "$my_dir" ] && { echo "⛔ Directory argument to parameter \'my_dir\' not found: \'$my_dir\'" >&2; return 1; }']
    """
    operator = {
        None: "e",
        "dir": "d",
        "exec": "x",
        "file": "f",
        "symlink": "L",
    }
    name = {
        None: "Path",
        "dir": "Directory",
        "exec": "Executable",
        "file": "File",
        "symlink": "Symbolic link",
    }
    condition = "not found" if must_exist else "already exists"
    err_msg = f"{name[path_type]} argument to parameter '{var_name}' {condition}: '${var_name}'"
    cmd = f'[ -n ${{{var_name}-}} ] && [ {"! " if must_exist else ""}-{operator[path_type]} "${var_name}" ] && {{ {log(err_msg, "critical")}; }}'
    return cmd


def log_endpoint(
    name: str,
    typ: Literal["function", "script"],
    stage: Literal["entry", "exit"],
) -> str:
    """Generate a shell command to log function/script entry or exit.

    Parameters
    ----------
    name
        Name of the function/script.
    typ
        "function" or "script".
    stage
        Stage of the function.
        Options are "entry" or "exit".

    Returns
    -------
    Shell command to log the function entry or exit.

    Examples
    --------
    >>> log_endpoint("my_function", "entry")
    'echo "Entering my_function" >&2'
    >>> log_endpoint("my_function", "exit")
    'echo "Exiting my_function" >&2'
    """
    emoji = {
        "entry": "↪️",
        "exit": "↩️",
    }
    return log(f"{emoji[stage]} {typ.capitalize()} {stage}: {name}")


def log_arg_read(
    param_name: str,
    var_name: str,
) -> str:
    """Generate a shell command to log argument reading.

    Parameters
    ----------
    param_name
        Name of the parameter.
    var_name
        Name of the variable.

    Returns
    -------
    Shell command to log the argument reading.

    Examples
    --------
    >>> log_arg_read("my_param", "my_var")
    'echo "📩 Read argument \'my_param\': \'$my_var\'" >&2'
    """
    return log(f"""📩 Read argument '{param_name}': '"${var_name}"'""")


def log_arg_write(
    param_name: str,
    var_name: str,
) -> str:
    """Generate a shell command to log argument writing.

    Parameters
    ----------
    param_name
        Name of the parameter.
    var_name
        Name of the variable.

    Returns
    -------
    Shell command to log the argument writing.

    Examples
    --------
    >>> log_arg_read("my_param", "my_var")
    'echo "📤 Write output \'my_param\': \'$my_var\'" >&2'
    """
    return log(f"""📤 Write output '{param_name}': '"${var_name}"'""")


def log(
    msg: str,
    level: Literal["info", "warn", "error", "critical"] | None = None,
    code: int = 1,
    indent_level: int = 0,
) -> str:
    """Generate a shell command to log a message to stderr and optionally exit.

    Parameters
    ----------
    msg
        The message to log.
    level
        The severity level of the message.
        Options are "info", "warn", "error", or "critical".
        For "error", the script will return the specified code.
        For "critical", the script will exit with the specified code.
        If None, no emoji is added to the message.
    code
        The exit code to return if the level is "critical".
    indent
        Indentation level to add to the command.
        The total number of spaces will be `indent` * 2.

    Examples
    --------
    >>> log("This is an info message.", level="info")
    'echo "ℹ️ This is an info message." >&2'
    >>> log("This is an error message.", level="error")
    'echo "❌ This is an error message." >&2; return 1'
    >>> log("This is a critical error message.", level="critical", code=123)
    'echo "⛔ This is a critical error message." >&2; exit 123'
    """
    emoji = {
        "info": "ℹ️",
        "warn": "⚠️",
        "error": "❌",
        "critical": "⛔",
    }
    echo = f"""echo "{f"{emoji[level]} " if level else ""}{msg}" >&2"""
    full_cmd = echo if level not in ("error", "critical") else f"{echo}; {"return" if level == "error" else "exit"} {code}"
    return indent(full_cmd, indent_level)


def param_name_to_var_name(
    param_name: str,
    local: bool,
) -> str:
    """Convert a parameter name to a variable name.

    This function replaces hyphens with underscores.
    The variable name is then converted to uppercase
    if `local` is False.

    Parameters
    ----------
    param_name
        The parameter name to convert.
    local
        Whether the variable is local.

    Returns
    -------
    The converted variable name.
    """
    var_name = param_name.replace("-", "_")
    return var_name if local else var_name.upper()


def sanitize_code(
    code: str | list[str],
    remove_comments: bool = True,
    remove_empty_lines: bool = True,
    remove_trailing_whitespace: bool = True,
    indent_level: int = 0,
) -> list[str]:
    """Sanitize shell code.

    Parameters
    ----------
    code
        The shell code to sanitize.
        Can be a string or a list of strings (lines).
    remove_comments
        Remove comments from the code.
    remove_empty_lines
        Remove empty lines from the code.
    remove_trailing_whitespace
        Remove trailing whitespace from each line.
    indent_level
        Indentation level to add to each line.
        The total number of spaces will be `indent` * 2.

    Returns
    -------
    List of sanitized lines of shell code.
    """
    if isinstance(code, str):
        code = code.splitlines()
    sanitized_code = []
    for line in (code or []):
        if remove_comments and line.lstrip().startswith("#"):
            continue
        if remove_empty_lines and not line.strip():
            continue
        if remove_trailing_whitespace:
            line = line.rstrip()
        if indent_level:
            line = f"{" " * indent_level * 2}{line}"
        sanitized_code.append(line)
    return sanitized_code


def indent(code: str | list[str], level: int = 0) -> str | list[str]:
    """Indent shell code.

    Parameters
    ----------
    code
        The shell code to indent.
        Can be a string or a list of strings (lines).
    level
        Indentation level to add to each line.
        The total number of spaces will be `indent` * 2.

    Returns
    -------
    Indented shell code as the same type as the input.
    """
    if not level:
        return code
    input_is_str = isinstance(code, str)
    if input_is_str:
        code = code.splitlines()
    code_indented = [f"{' ' * level * 2}{line}" for line in code]
    return "\n".join(code_indented) if input_is_str else code_indented
