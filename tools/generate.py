#!/usr/bin/env python3

import json
from pprint import pprint
import sys


def eprintln(line):
    print(line, file=sys.stderr)


def make_inputs_table(inputs):
    headers = ["Parameter", "Description", "Required", "Default"]
    rows = []
    for input_name, input_options in inputs.items():
        required = input_options.get("required", False)
        default = input_options.get("default")

        if isinstance(default, bool):
            default_str = f"`{str(default).lower()}`"
        elif default is not None:
            default_str = f"`{default}`"
        else:
            default_str = ""

        rows.append(
            [
                f"`{input_name}`",
                input_options["description"],
                "📍" if required else "",
                default_str,
            ]
        )

    # The following is just tedious markdown formatting junk so we didn't need a dep,
    # if it seems wack just rewrite it lol
    all_rows = [headers] + rows
    col_widths = [max(len(str(cell)) for cell in col) for col in zip(*all_rows)]

    def format_row(row):
        return (
            "| "
            + " | ".join(str(cell).ljust(width) for cell, width in zip(row, col_widths))
            + " |"
        )

    lines = [
        format_row(headers),
        "|" + "|".join("-" * (w + 2) for w in col_widths) + "|",
    ]
    for row in rows:
        lines.append(format_row(row))

    return "\n".join(lines)


keep_inputs = [
    "extra-conf",
    "github-server-url",
    "github-token",
    "trust-runner-user",
    "summarize",
    # Advanced run-time environment options
    "force-no-systemd",
    "init",
    "kvm",
    "planner",
    "proxy",
    "reinstall",
    # Determinate Nix Installer testing, swap-out options
    "source-binary",
    "source-branch",
    "source-pr",
    "source-revision",
    "source-tag",
    "source-url",
    # debugging
    "backtrace",
    "diagnostic-endpoint",
    "log-directives",
    "logger",
    "_internal-strict-mode",
]

discard_inputs = [
    "determinate",
    "extra-args",
    "flakehub",
    "job-status",
    "local-root",
    "mac-case-sensitive",
    "mac-encrypt",
    "mac-root-disk",
    "mac-volume-label",
    "modify-profile",
    "nix-build-group-id",
    "nix-build-group-name",
    "nix-build-user-base",
    "nix-build-user-count",
    "nix-build-user-prefix",
    "nix-installer-branch",
    "nix-installer-pr",
    "nix-installer-revision",
    "nix-installer-tag",
    "nix-installer-url",
    "nix-package-url",
    "ssl-cert-file",
    "start-daemon",
]

result = {
    "name": "Install Determinate Nix",
    "description": "Install Determinate Nix. See: https://docs.determinate.systems",
    "branding": {
        "icon": "box",
        "color": "rainbow",
    },
    "inputs": {},
    "runs": {
        "using": "composite",
        "steps": [],
    },
}

readme_table_marker = "<!-- table -->"
readme_checkout_action_tag_marker = "<!-- checkout_action_tag -->"
readme_version_marker = "<!-- version -->"

faults = []

# these are in reverse order lol
output_readme = sys.argv.pop()
readme_template = sys.argv.pop()
output_action = sys.argv.pop()
source_file = sys.argv.pop()
checkout_action_tag = sys.argv.pop()
nix_installer_revision = sys.argv.pop()
nix_installer_tag = sys.argv.pop()

# these are printed in argument order
eprintln(f"Determinate Nix Installer binary tag: {nix_installer_tag}")
eprintln(f"Nix Installer Action revision: {nix_installer_revision}")
eprintln(f"Checkout Action tag: {checkout_action_tag}")
eprintln(f"Source action json doc: {source_file}")
eprintln(f"Target action.yml: {output_action}")
eprintln(f"Readme template file: {readme_template}")
eprintln(f"Target readme: {output_readme}")


with open(source_file) as fp:
    source = json.load(fp)

del source["name"]
del source["description"]
del source["branding"]
del source["runs"]

nix_install_step = {
    "uses": f"DeterminateSystems/nix-installer-action@{nix_installer_revision}",
    "with": {},
}

# Move kept inputs into the resulting action document
for input_name in keep_inputs:
    try:
        input = source["inputs"][input_name]
        del source["inputs"][input_name]

        result["inputs"][input_name] = input
        nix_install_step["with"][input_name] = f"${{{{ inputs.{input_name} }}}}"
    except KeyError:
        faults.append(f"Input action is missing this 'keep_inputs' input: {input_name}")

# Turn on Determinate Nix
nix_install_step["with"]["determinate"] = True

result["runs"]["steps"].append(nix_install_step)

# Delete inputs we specifically do not want to support without a specific and known use case
for input_name in discard_inputs:
    try:
        del source["inputs"][input_name]
    except KeyError as e:
        pprint(e)
        faults.append(
            f"Input action is missing this 'discarded_inputs' input: {input_name}"
        )

# Kvetch if there are remaining inputs we're not aware of
if source["inputs"] != {}:
    faults.append(
        f"Input action has inputs that were not accounted for in either keep_inputs, discarded_inputs: {', '.join(source['inputs'].keys())}"
    )
else:
    del source["inputs"]

# Kvetch if the source document has ANY remaining properties (like outputs!) that we don't already handle
if source != {}:
    faults.append(
        f"The source action was not completely obliterated by the translation, so this script needs updating. Remains: {json.dumps(source)}"
    )

# Set the default source-tag to the currently released tag
result["inputs"]["source-tag"]["default"] = nix_installer_tag

# Generate a README from the inputs
table = make_inputs_table(result["inputs"])

print("Resulting action:")
print(json.dumps(result, indent=4))
print("")
print("Readme table:")
print(table)

eprintln(f"Reading the README template from {readme_template}")
with open(readme_template) as fp:
    template = fp.read()

    if readme_table_marker not in template:
        faults.append(
            f"Replacement template marker `{readme_table_marker}` is not present in {readme_template}."
        )
    if readme_version_marker not in template:
        faults.append(
            f"Replacement template marker `{readme_version_marker}` is not present in {readme_template}."
        )

    if readme_checkout_action_tag_marker not in template:
        faults.append(
            f"Replacement template marker `{readme_checkout_action_tag_marker}` is not present in {readme_template}."
        )
        readme_checkout_action_tag_marker

if len(faults) > 0:
    eprintln("Faults preventing saves:")
    for fault in faults:
        eprintln(f"* {fault}")
    raise SystemExit

eprintln(f"Writing out the action.yml to {output_action}")
with open(output_action, "w") as fp:
    json.dump(result, indent=4, fp=fp)

eprintln(f"Writing out the README.md to {output_readme}")
with open(output_readme, "w") as fp:
    fp.write(
        template.replace(readme_table_marker, table)
        .replace(readme_version_marker, nix_installer_tag)
        .replace(readme_checkout_action_tag_marker, checkout_action_tag)
    )
