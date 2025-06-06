%global debug_package %{nil}
%global bin_name framework_tool

Name:    framework-system
Version: 0.4.3
Release: %autorelease -e 1
Summary: Rust tool to interact with the Framework Computer systems
# Main package is BSD-3-Clause, remaining licenses are from statically linked dependencies
License: BSD-3-Clause AND (Apache-2.0 OR BSL-1.0) AND (Apache-2.0 OR MIT) AND (MIT) AND (MPL-2.0) AND (Unlicense OR MIT)

URL:     https://github.com/FrameworkComputer/%{name}
Source:  https://github.com/FrameworkComputer/%{name}/archive/refs/tags/v%{version}.tar.gz

BuildRequires: cargo
BuildRequires: rust
BuildRequires: pkgconfig(libudev)
Requires: udev

%description
Rust tool to interact with the Framework Computer systems

%prep
%autosetup -n %{name}-%{version}

%build
export RUSTFLAGS="%{build_rustflags}"
cargo build --release --locked -p framework_tool

# Generate license documentation
cargo tree --workspace --edges no-build,no-dev,no-proc-macro --no-dedupe --prefix none --format '{l}' | sort -u > LICENSE.summary
cargo tree --workspace --edges no-build,no-dev,no-proc-macro --no-dedupe --prefix none --format '{l}: {p}' | sort -u > LICENSE.dependencies

%install
install -Dpm 0755 target/release/%{bin_name} -t %{buildroot}%{_bindir}/

# Shell completions
install -Dpm 0644 completions/bash/%{bin_name} -t %{buildroot}/%{bash_completions_dir}
install -Dpm 0644 completions/zsh/_%{bin_name} -t %{buildroot}/%{zsh_completions_dir}

%files
%license LICENSE.md LICENSE.summary LICENSE.dependencies
%doc README.md
%{_bindir}/%{bin_name}
%{bash_completions_dir}/%{bin_name}
%{zsh_completions_dir}/_%{bin_name}

%changelog
%autochangelog


