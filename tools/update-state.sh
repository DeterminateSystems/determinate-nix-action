#!/bin/sh

set -eux

DETERMINATE_NIX_TAG=$1
REPO="DeterminateSystems/nix-installer-action"

default_branch() {
    gh api "repos/$REPO" \
        | jq -r '.default_branch'
}

get_latest_revision() {
    gh api "repos/$REPO/commits/$(default_branch)" \
        | jq -r '.sha'
}

checkout_tag() {
    gh release list \
        --repo actions/checkout \
        --exclude-drafts \
        --exclude-pre-releases \
        --jq 'map(select(.isLatest)) | first | .tagName' \
        --json isLatest,tagName
}

main() {
    revision=$(get_latest_revision)
    checkout_tag=$(checkout_tag)

    jq -n '$ARGS.named' \
        --arg nix_installer_action_revision "$revision" \
        --arg "determinate_nix_tag" "$DETERMINATE_NIX_TAG" \
        --arg "checkout_action_tag" "$checkout_tag" \
        | cat > tools/state.json
}

main
