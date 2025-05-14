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
      - uses: actions/checkout@v4.2.1
      - uses: DeterminateSystems/determinate-nix-action@main # or v3.5.1 to pin to a release
      - run: nix build .
```

## Pinning

This action is tagged automatically for every Determinate Nix release.
Pinning to `DeterminateSystems/determinate-nix-action@v3.5.1` will always resolve to the same `DeterminateSystems/nix-installer-action` revision and will always install Determinate Nix v3.5.1.

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

| Parameter               | Description                                                                                                                                                                                                                                                                    | Required | Default                    |
|-------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------|----------------------------|
| `extra-conf`            | Extra configuration lines for `/etc/nix/nix.conf` (includes `access-tokens` with `secrets.GITHUB_TOKEN` automatically if `github-token` is set)                                                                                                                                |          |                            |
| `github-server-url`     | The URL for the GitHub server, to use with the `github-token` token. Defaults to the current GitHub server, supporting GitHub Enterprise Server automatically. Only change this value if the provided `github-token` is for a different GitHub server than the current server. |          | `${{ github.server_url }}` |
| `github-token`          | A GitHub token for making authenticated requests (which have a higher rate-limit quota than unauthenticated requests)                                                                                                                                                          |          | `${{ github.token }}`      |
| `trust-runner-user`     | Whether to make the runner user trusted by the Nix daemon                                                                                                                                                                                                                      |          | `True`                     |
| `force-no-systemd`      | Force using other methods than systemd to launch the daemon. This setting is automatically enabled when necessary.                                                                                                                                                             |          | `False`                    |
| `init`                  | The init system to configure, requires `planner: linux-multi` (allowing the choice between `none` or `systemd`)                                                                                                                                                                |          |                            |
| `kvm`                   | Automatically configure the GitHub Actions Runner for NixOS test supports, if the host supports it.                                                                                                                                                                            |          | `True`                     |
| `planner`               | A planner to use                                                                                                                                                                                                                                                               |          |                            |
| `proxy`                 | The proxy to use (if any), valid proxy bases are `https://$URL`, `http://$URL` and `socks5://$URL`                                                                                                                                                                             |          |                            |
| `reinstall`             | Force a reinstall if an existing installation is detected (consider backing up `/nix/store`)                                                                                                                                                                                   |          | `False`                    |
| `source-binary`         | Run a version of the nix-installer binary from somewhere already on disk. Conflicts with all other `source-*` options. Intended only for testing this Action.                                                                                                                  |          |                            |
| `source-branch`         | The branch of `nix-installer` to use (conflicts with `source-tag`, `source-revision`, `source-pr`)                                                                                                                                                                             |          |                            |
| `source-pr`             | The PR of `nix-installer` to use (conflicts with `source-tag`, `source-revision`, `source-branch`)                                                                                                                                                                             |          |                            |
| `source-revision`       | The revision of `nix-installer` to use (conflicts with `source-tag`, `source-branch`, `source-pr`)                                                                                                                                                                             |          |                            |
| `source-tag`            | The tag of `nix-installer` to use (conflicts with `source-revision`, `source-branch`, `source-pr`)                                                                                                                                                                             |          | `v3.5.1`                   |
| `source-url`            | A URL pointing to a `nix-installer` executable                                                                                                                                                                                                                                 |          |                            |
| `backtrace`             | The setting for `RUST_BACKTRACE` (see https://doc.rust-lang.org/std/backtrace/index.html#environment-variables)                                                                                                                                                                |          |                            |
| `diagnostic-endpoint`   | Diagnostic endpoint url where the installer sends data to. To disable set this to an empty string.                                                                                                                                                                             |          | `-`                        |
| `log-directives`        | A list of Tracing directives, comma separated, `-`s replaced with `_` (eg. `nix_installer=trace`, see https://docs.rs/tracing-subscriber/latest/tracing_subscriber/filter/struct.EnvFilter.html#directives)                                                                    |          |                            |
| `logger`                | The logger to use for install (eg. `pretty`, `json`, `full`, `compact`)                                                                                                                                                                                                        |          |                            |
| `_internal-strict-mode` | Whether to fail when any errors are thrown. Used only to test the Action; do not set this in your own workflows.                                                                                                                                                               |          | `False`                    |

## Need help?

- Open an issue,
- Join our Discord: https://determinate.systems/discord,
- Contact us over email: [support@determinate.systems](mailto:support@determinate.systems),

Support contracts and shared slack rooms are available.
