%global debug_package %{nil}

Name:    atuin
Version: 18.6.1
Release: %autorelease
Summary: Magical shell history
# Main package is BSD-3-Clause, remaining licenses are from statically linked dependencies
License: MIT AND ((Apache-2.0 OR MIT) AND BSD-3-Clause) AND (0BSD OR MIT OR Apache-2.0) AND (Apache-2.0) AND (Apache-2.0 / MIT) AND (Apache-2.0 AND ISC) AND (Apache-2.0 OR BSL-1.0) AND (Apache-2.0 OR BSL-1.0 OR MIT) AND (Apache-2.0 OR ISC OR MIT) AND (Apache-2.0 WITH LLVM-exception OR Apache-2.0 OR MIT) AND (BSD-2-Clause OR Apache-2.0 OR MIT) AND (BSD-3-Clause) AND (ISC) AND (MIT AND BSD-3-Clause) AND (MIT OR Apache-2.0) AND (MIT OR Apache-2.0 OR CC0-1.0) AND (MIT OR Apache-2.0 OR Zlib) AND (MPL-2.0) AND (Unicode-3.0) AND (Unlicense OR MIT) AND (Zlib) AND (Zlib OR Apache-2.0 OR MIT) AND 

URL:     https://github.com/atuinsh/%{name}
Source0: https://github.com/atuinsh/%{name}/archive/refs/tags/v%{version}.tar.gz

BuildRequires: cargo
BuildRequires: rust

%description
Atuin replaces your existing shell history with a SQLite database, 
and records additional context for your commands.

%prep
%autosetup -n %{name}-%{version}

%build
export RUSTFLAGS="%{build_rustflags}"
cargo build --release --locked

for shell in 'bash' 'fish' 'zsh'; do
  target/release/%{name} gen-completions -s "$shell" -o ./
done

# Generate license documentation
cargo tree --workspace --edges no-build,no-dev,no-proc-macro --no-dedupe --prefix none --format '{l}' | sort -u > LICENSE.summary
cargo tree --workspace --edges no-build,no-dev,no-proc-macro --no-dedupe --prefix none --format '{l}: {p}' | sort -u > LICENSE.dependencies


%install
install -Dpm 0755 target/release/%{name} -t %{buildroot}%{_bindir}/

# Shell completions
install -Dpm 0644 %{name}.bash -t %{buildroot}/%{bash_completions_dir}
install -Dpm 0644 _%{name} -t %{buildroot}/%{zsh_completions_dir}
install -Dpm 0644 %{name}.fish -t %{buildroot}/%{fish_completions_dir}

%files
%license LICENSE LICENSE.summary LICENSE.dependencies
%doc README.md
%{_bindir}/%{name}
%{bash_completions_dir}/%{name}.bash
%{zsh_completions_dir}/_%{name}
%{fish_completions_dir}/%{name}.fish

%changelog
%autochangelog
