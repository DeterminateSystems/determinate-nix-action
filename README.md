<p align="center">
  <a href="https://determinate.systems" target="_blank"><img src="https://raw.githubusercontent.com/determinatesystems/.github/main/.github/banner.jpg"></a>
</p>
<p align="center">
  &nbsp;<a href="https://determinate.systems/discord" target="_blank"><img alt="Discord" src="https://img.shields.io/discord/1116012109709463613?style=for-the-badge&logo=discord&logoColor=%23ffffff&label=Discord&labelColor=%234253e8&color=%23e4e2e2"></a>&nbsp;
  &nbsp;<a href="https://bsky.app/profile/determinate.systems" target="_blank"><img alt="Bluesky" src="https://img.shields.io/badge/Bluesky-0772D8?style=for-the-badge&logo=bluesky&logoColor=%23ffffff"></a>&nbsp;
  &nbsp;<a href="https://hachyderm.io/@determinatesystems" target="_blank"><img alt="Mastodon" src="https://img.shields.io/badge/Mastodon-6468fa?style=for-the-badge&logo=mastodon&logoColor=%23ffffff"></a>&nbsp;
  &nbsp;<a href="https://twitter.com/DeterminateSys" target="_blank"><img alt="Twitter" src="https://img.shields.io/badge/Twitter-303030?style=for-the-badge&logo=x&logoColor=%23ffffff"></a>&nbsp;
  &nbsp;<a href="https://www.linkedin.com/company/determinate-systems" target="_blank"><img alt="LinkedIn" src="https://img.shields.io/badge/LinkedIn-1667be?style=for-the-badge&logo=linkedin&logoColor=%23ffffff"></a>&nbsp;
</p>

# ️❄️ Determinate Nix Action

[Determinate] is the best way to use Nix on macOS, WSL, and Linux.
It is an end-to-end toolchain for using Nix, from installation to collaboration to deployment.

Based on the [Determinate Nix Installer][nix-installer] and its corresponding [Nix Installer Action][nix-installer-action], responsible for over tens of thousands of Nix installs daily.

> [!NOTE]
>
> **Why a different Action?**
>
> We created a new Action to synchronize version tags to [Determinate Nix][det-nix] releases.
> GitHub Actions are tagged with the specific version, like `v3.5.2`, with a moving `v3` tag for the major version.
> We needed a fresh tag namespace since `nix-installer-action` already has a `v3` tag.

## 🫶 Platform support

- ⚡ **Accelerated KVM** on open source projects and larger runners. See [GitHub's announcement](https://github.blog/changelog/2023-02-23-hardware-accelerated-android-virtualization-on-actions-windows-and-linux-larger-hosted-runners/) for more info.
- 🐧 Linux, x86_64, aarch64, and i686
- 🍏 macOS, x86_64 and aarch64
- 🪟 WSL2, x86_64 and aarch64
- 🐋 Containers, ARC, and Act
- 🐙 GitHub Enterprise Server
- 💁 GitHub Hosted, self-hosted, and long running Actions Runners

## ️🔧 Usage

Here's an example Actions workflow configuration that uses `determinate-nix-action`:

```yaml
on:
  pull_request:
  push:
    branches: [main]

jobs:
  build-pkg:
    name: Build Nix package
    runs-on: ubuntu-latest
    permissions:
      id-token: write
      contents: read
    steps:
      - uses: actions/checkout@v6.0.1
      - uses: DeterminateSystems/determinate-nix-action@main # or v3.15.2 to pin to a release
      - run: nix build .
```

> [!IMPORTANT]
> If you use [FlakeHub], you need to add a `permissions` block like the one in the example above or else Determinate Nix can't authenticate with FlakeHub or [FlakeHub Cache][cache].

## 📌 Version pinning: lock it down!

### Why pin your Action?

Unlike `DeterminateSystems/nix-installer-action`, we fully support explicit version pinning for maximum consistency.
This Action is **automatically tagged** for every Determinate Nix release, giving you complete control over your CI environment:

📍 Pinning to `DeterminateSystems/determinate-nix-action@v3.15.2` guarantees:

- Same `nix-installer-action` revision every time
- Consistent Determinate Nix v3.15.2 installation
- Reproducible CI workflows, even years later

✨ Using `@main` instead? You'll:

- Always get the latest Determinate Nix release
- Occasionally participate in phased rollouts (helping us test new releases!)

> [!IMPORTANT]
> Set up [Dependabot] to stay current with Determinate Nix releases without sacrificing stability.

### 🤖 Automate updates with Dependabot

Keep your GitHub Actions fresh without manual work! Create `.github/dependabot.yml` with:

```yaml
version: 2
updates:
  - package-ecosystem: github-actions
    directory: /
    schedule:
      interval: weekly
```

## ️⚙️ Configuration

| Parameter               | Description                                                                                                                                                                                                                                                                    | Required | Default                    |
|-------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------|----------------------------|
| `extra-conf`            | Extra configuration lines for `/etc/nix/nix.conf` (includes `access-tokens` with `secrets.GITHUB_TOKEN` automatically if `github-token` is set)                                                                                                                                |          |                            |
| `github-server-url`     | The URL for the GitHub server, to use with the `github-token` token. Defaults to the current GitHub server, supporting GitHub Enterprise Server automatically. Only change this value if the provided `github-token` is for a different GitHub server than the current server. |          | `${{ github.server_url }}` |
| `github-token`          | A GitHub token for making authenticated requests (which have a higher rate-limit quota than unauthenticated requests)                                                                                                                                                          |          | `${{ github.token }}`      |
| `trust-runner-user`     | Whether to make the runner user trusted by the Nix daemon                                                                                                                                                                                                                      |          | `true`                     |
| `summarize`             | Whether to add a build summary and timeline chart to the GitHub job summary                                                                                                                                                                                                    |          | `true`                     |
| `force-no-systemd`      | Force using other methods than systemd to launch the daemon. This setting is automatically enabled when necessary.                                                                                                                                                             |          | `false`                    |
| `init`                  | The init system to configure, requires `planner: linux-multi` (allowing the choice between `none` or `systemd`)                                                                                                                                                                |          |                            |
| `kvm`                   | Automatically configure the GitHub Actions Runner for NixOS test supports, if the host supports it.                                                                                                                                                                            |          | `true`                     |
| `planner`               | A planner to use                                                                                                                                                                                                                                                               |          |                            |
| `proxy`                 | The proxy to use (if any), valid proxy bases are `https://$URL`, `http://$URL` and `socks5://$URL`                                                                                                                                                                             |          |                            |
| `reinstall`             | Force a reinstall if an existing installation is detected (consider backing up `/nix/store`)                                                                                                                                                                                   |          | `false`                    |
| `source-binary`         | Run a version of the nix-installer binary from somewhere already on disk. Conflicts with all other `source-*` options. Intended only for testing this Action.                                                                                                                  |          |                            |
| `source-branch`         | The branch of `nix-installer` to use (conflicts with `source-tag`, `source-revision`, `source-pr`)                                                                                                                                                                             |          |                            |
| `source-pr`             | The PR of `nix-installer` to use (conflicts with `source-tag`, `source-revision`, `source-branch`)                                                                                                                                                                             |          |                            |
| `source-revision`       | The revision of `nix-installer` to use (conflicts with `source-tag`, `source-branch`, `source-pr`)                                                                                                                                                                             |          |                            |
| `source-tag`            | The tag of `nix-installer` to use (conflicts with `source-revision`, `source-branch`, `source-pr`)                                                                                                                                                                             |          | `v3.15.2`                  |
| `source-url`            | A URL pointing to a `nix-installer` executable                                                                                                                                                                                                                                 |          |                            |
| `backtrace`             | The setting for `RUST_BACKTRACE` (see https://doc.rust-lang.org/std/backtrace/index.html#environment-variables)                                                                                                                                                                |          |                            |
| `diagnostic-endpoint`   | Diagnostic endpoint url where the installer sends data to. To disable set this to an empty string.                                                                                                                                                                             |          | `-`                        |
| `log-directives`        | A list of Tracing directives, comma separated, `-`s replaced with `_` (eg. `nix_installer=trace`, see https://docs.rs/tracing-subscriber/latest/tracing_subscriber/filter/struct.EnvFilter.html#directives)                                                                    |          |                            |
| `logger`                | The logger to use for install (eg. `pretty`, `json`, `full`, `compact`)                                                                                                                                                                                                        |          |                            |
| `_internal-strict-mode` | Whether to fail when any errors are thrown. Used only to test the Action; do not set this in your own workflows.                                                                                                                                                               |          | `false`                    |

## 🛟 Need help? We're here for you!

We're committed to making your experience with Determinate Nix as smooth as possible. If you encounter any issues or have questions, here's how to reach us:

- 🐛 **Found a bug?** [Open an issue](https://github.com/DeterminateSystems/determinate-nix-action/issues/new) on GitHub
- 💬 **Want to chat?** Join our [Discord community](https://determinate.systems/discord) for quick help and discussions
- 📧 **Need direct support?** Email us at [support@determinate.systems](mailto:support@determinate.systems)

🤝 **Looking for enterprise support?** We offer dedicated support contracts and shared Slack channels for organizations requiring priority assistance. [Contact us](mailto:support@determinate.systems) to learn more.

[cache]: https://flakehub.com/cache
[dependabot]: https://github.com/dependabot
[det-nix]: https://docs.determinate.systems/determinate-nix
[determinate]: https://docs.determinate.systems
[flakehub]: https//flakehub.com
[nix-installer]: https://github.com/DeterminateSystems/nix-installer
[nix-installer-action]: https://github.com/DeterminateSystems/nix-installer-action
