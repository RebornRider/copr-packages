%global debug_package %{nil}

Name:    dysk
Version: 2.10.1
Release: %autorelease
Summary: A linux utility listing your filesystems
# Main package is BSD-3-Clause, remaining licenses are from statically linked dependencies
License: MIT AND (Apache-2.0 OR BSL-1.0)AND (Apache-2.0 OR MIT)AND (Apache-2.0 WITH LLVM-exception OR Apache-2.0 OR MIT)AND (MIT OR Apache-2.0)AND (Unlicense OR MIT)

URL:     https://github.com/Canop/%{name}
Source0: https://github.com/Canop/%{name}/archive/refs/tags/v%{version}.tar.gz

BuildRequires: cargo
BuildRequires: rust

%description
A linux utility listing your filesystems.

%prep
%autosetup -n %{name}-%{version}

%build
export RUSTFLAGS="%{build_rustflags}"
cargo build --release --locked

# Generate license documentation
cargo tree --workspace --edges no-build,no-dev,no-proc-macro --no-dedupe --prefix none --format '{l}' | sort -u > LICENSE.summary
cargo tree --workspace --edges no-build,no-dev,no-proc-macro --no-dedupe --prefix none --format '{l}: {p}' | sort -u > LICENSE.dependencies


%install
install -Dpm 0755 target/release/%{name} -t %{buildroot}%{_bindir}/

out_dir=$(find target -type f -name %{name}.bash -exec dirname {} \;)

# Shell completions
install -Dpm 0644 "$out_dir"/%{name}.bash -t %{buildroot}/%{bash_completions_dir}
install -Dpm 0644 "$out_dir"/_%{name} -t %{buildroot}/%{zsh_completions_dir}
install -Dpm 0644 "$out_dir"/%{name}.fish -t %{buildroot}/%{fish_completions_dir}

# man page
install -Dpm 0644 "$out_dir"/%{name}.1 -t %{buildroot}%{_mandir}/man1/

%files
%license LICENSE LICENSE.summary LICENSE.dependencies
%{_bindir}/%{name}
%{_mandir}/man1/%{name}.1*
%{bash_completions_dir}/%{name}.bash
%{zsh_completions_dir}/_%{name}
%{fish_completions_dir}/%{name}.fish

%changelog
%autochangelog
