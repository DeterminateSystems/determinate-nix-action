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

Determinate is the best way to use Nix on macOS, WSL, and Linux.
It is an end-to-end toolchain for using Nix, from installation to collaboration to deployment.

Based on the [Determinate Nix Installer](https://github.com/DeterminateSystems/nix-installer) and its corresponding [Nix Installer Action](https://github.com/DeterminateSystems/nix-installer-action), responsible for over tens of thousands of Nix installs daily.

> [!NOTE] > **Why a different action?**
>
> We created a new action to synchronize version tags to Determinate Nix releases.
> GitHub Actions are tagged with the specific version, like `v3.5.2`, with a moving `v3` tag for the major version.
> We needed a fresh tag namespace since nix-installer-action already has a `v3` tag.

## 🫶 Platform support

- ⚡ **Accelerated KVM** on open source projects and larger runners. See [GitHub's announcement](https://github.blog/changelog/2023-02-23-hardware-accelerated-android-virtualization-on-actions-windows-and-linux-larger-hosted-runners/) for more info.
- 🐧 Linux, x86_64, aarch64, and i686
- 🍏 macOS, x86_64 and aarch64
- 🪟 WSL2, x86_64 and aarch64
- 🐋 Containers, ARC, and Act
- 🐙 GitHub Enterprise Server
- 💁 GitHub Hosted, self-hosted, and long running Actions Runners

## ️🔧 Usage

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

## 📌 Version Pinning: Lock It Down!

### Why Pin Your Action?

Unlike `DeterminateSystems/nix-installer-action`, we fully support explicit version pinning for maximum consistency.
This action is **automatically tagged** for every Determinate Nix release, giving you complete control over your CI environment:

📍 Pinning to `DeterminateSystems/determinate-nix-action@<!-- version -->` guarantees:

- Same `nix-installer-action` revision every time
- Consistent Determinate Nix <!-- version --> installation
- Reproducible CI workflows, even years later

✨ Using `@main` instead? You'll:

- Always get the latest Determinate Nix release
- Occasionally participate in phased rollouts (helping us test new releases!)

> [!IMPORTANT]
> Set up Dependabot to stay current with Determinate Nix releases without sacrificing stability.

### 🤖 Automate Updates with Dependabot

Keep your GitHub actions fresh without manual work! Create `.github/dependabot.yml` with:

```yaml
version: 2
updates:
  - package-ecosystem: "github-actions"
    directory: "/"
    schedule:
      interval: "weekly"
```

## ️⚙️ Configuration

<!-- table -->

## 🛟 Need Help? We're Here For You!

We're committed to making your experience with Determinate Nix as smooth as possible. If you encounter any issues or have questions, here's how to reach us:

- 🐛 **Found a bug?** [Open an issue](https://github.com/DeterminateSystems/determinate-nix-action/issues/new) on GitHub
- 💬 **Want to chat?** Join our [Discord community](https://determinate.systems/discord) for quick help and discussions
- 📧 **Need direct support?** Email us at [support@determinate.systems](mailto:support@determinate.systems)

🤝 **Looking for enterprise support?** We offer dedicated support contracts and shared Slack channels for organizations requiring priority assistance. [Contact us](mailto:support@determinate.systems) to learn more.
