#!/usr/bin/env bash
set -euo pipefail

mise_version="${RENOVATE_MISE_VERSION:-2026.5.8}"
mise_sha256="${RENOVATE_MISE_SHA256:-19e56db5286f7fae879f13c43a6f2aa9bf80a959b3bfb71eff8ee001fe2532d6}"
platform="linux-x64"

if [[ "$(uname -s)" != "Linux" || "$(uname -m)" != "x86_64" ]]; then
  echo "Unsupported Renovate mise lock platform: $(uname -s)-$(uname -m)" >&2
  exit 1
fi

cache_root="${RENOVATE_MISE_CACHE_DIR:-${TMPDIR:-/tmp}/renovate-mise}"
install_root="${cache_root}/v${mise_version}-${platform}"
mise_bin="${install_root}/mise/bin/mise"

if [[ ! -x "${mise_bin}" ]]; then
  archive="${cache_root}/mise-v${mise_version}-${platform}.tar.gz"
  mkdir -p "${cache_root}"
  curl -fsSL \
    -o "${archive}" \
    "https://github.com/jdx/mise/releases/download/v${mise_version}/mise-v${mise_version}-${platform}.tar.gz"
  echo "${mise_sha256}  ${archive}" | sha256sum -c -
  rm -rf "${install_root}"
  mkdir -p "${install_root}"
  tar -xzf "${archive}" -C "${install_root}"
fi

"${mise_bin}" trust --yes mise.toml
"${mise_bin}" lock --platform "${platform}"
