#!/bin/sh

# Allow "useless" cat
# shellcheck disable=SC2002

set -eux

REPO="DeterminateSystems/nix-installer-action"
FILEPATH="action.yml"

get_action_as_json() (
    rev=$1

    curl -s -L "https://raw.githubusercontent.com/$REPO/$rev/$FILEPATH" \
        | yq
)

main() {

    echo "::group::{./tools/state.json}"
    cat ./tools/state.json
    echo "::endgroup::"


    nix_installer_action_revision=$(cat ./tools/state.json | jq -r .nix_installer_action_revision)
    determinate_nix_tag=$(cat ./tools/state.json | jq -r .determinate_nix_tag)
    checkout_action_tag=$(cat ./tools/state.json | jq -r .checkout_action_tag)

    get_action_as_json "$nix_installer_action_revision" > upstream.json

    echo "::group::{./upstream.json}"
    cat ./upstream.json
    echo "::endgroup::"

    python3 -- ./tools/generate.py \
        "$determinate_nix_tag" \
        "$nix_installer_action_revision" \
        "$checkout_action_tag" \
        ./upstream.json \
        ./action.yml \
        ./tools/README.template.md \
        ./README.md

    rm ./upstream.json
}

main
