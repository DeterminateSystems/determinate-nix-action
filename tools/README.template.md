# Determinate Nix Action

Determinate is the best way to use Nix on macOS, WSL, and Linux.
It is an end-to-end toolchain for using Nix, from installation to collaboration to deployment.

Based on the [Determinate Nix Installer](https://github.com/DeterminateSystems/nix-installer) and its corresponding [Nix Installer Action](https://github.com/DeterminateSystems/nix-installer-action), responsible for over tens of thousands of Nix installs daily.

## Supports

- ✅ **Accelerated KVM** on open source projects and larger runners. See [GitHub's announcement](https://github.blog/changelog/2023-02-23-hardware-accelerated-android-virtualization-on-actions-windows-and-linux-larger-hosted-runners/) for more info.
- ✅ Linux, x86_64, aarch64, and i686
- ✅ macOS, x86_64 and aarch64
- ✅ WSL2, x86_64 and aarch64
- ✅ Containers, ARC, and Act
- ✅ GitHub Enterprise Server
- ✅ GitHub Hosted, self-hosted, and long running Actions Runners

## Usage

```yaml
on:
  pull_request:
  push:
    branches: [main]

jobs:
  lints:
    name: Build
    runs-on: ubuntu-latest
    permissions:
      id-token: "write"
      contents: "read"
    steps:
      - uses: actions/checkout@<!-- checkout_action_tag -->
      - uses: DeterminateSystems/determinate-nix-action@main # or <!-- version --> to pin to a release
      - run: nix build .
```

## Pinning

This action is tagged automatically for every Determinate Nix release.
Pinning to `DeterminateSystems/determinate-nix-action@<!-- version -->` will always resolve to the same `DeterminateSystems/nix-installer-action` revision and will always install Determinate Nix <!-- version -->.

This is different from `DeterminateSystems/nix-installer-action`, which does not support explicit pinning.

If your action does not pin to a specific tag and uses `DeterminateSystems/determinate-nix-action@main` your workflows will follow the latest Determinate Nix release, and occasionally participate in phased Determinate Nix releases.

> [!IMPORTANT]  
> Make sure to setup Dependabot to stay up to date with Determinate Nix releases.

### Setting up Dependabot

Automatically keep your GitHub actions up to date with Dependabot.
Create a file in your repository at `.github/dependabot.yml` with the following contents:

```yaml
version: 2
updates:
  - package-ecosystem: "github-actions"
    directory: "/"
    schedule:
      interval: "weekly"
```

## Configuration

<!-- table -->

## Need help?

- Open an issue,
- Join our Discord: https://determinate.systems/discord,
- Contact us over email: [support@determinate.systems](mailto:support@determinate.systems),

Support contracts and shared slack rooms are available.
