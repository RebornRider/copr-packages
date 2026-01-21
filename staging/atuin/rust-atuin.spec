%global debug_package %{nil}

%ifarch x86_64
%define         build_target x86_64-unknown-linux-gnu
%else
%define         build_target aarch64-unknown-linux-gnu
%endif

Name:           atuin
Version:        18.11.0
Release:        %autorelease -e 4
Summary:        Magical shell history

License:        MIT
URL:            https://github.com/atuinsh/atuin
Source:         %{url}/archive/refs/tags/v%{version}.tar.gz

BuildRequires:  rust
BuildRequires:  cargo

%description
Atuin - magical shell history. 

%prep
%autosetup -n ./%{name}-%{version}

%build
export RUSTFLAGS="%{build_rustflags}"
cargo build "-j$(nproc)" --profile dist --target %build_target

cargo tree --workspace --edges no-build,no-dev,no-proc-macro --no-dedupe --prefix none --format '{l}' | sort -u > LICENSE.summary
cargo tree --workspace --edges no-build,no-dev,no-proc-macro --no-dedupe --prefix none --format '{l}: {p}' | sort -u > LICENSE.dependencies

# generate completions
./target/%{build_target}/dist/%{name} gen-completions -s bash -o .
./target/%{build_target}/dist/%{name} gen-completions -s zsh -o .
./target/%{build_target}/dist/%{name} gen-completions -s fish -o .

%install
install -Dpm 0755 ./target/%{build_target}/dist/%{name} -t %{buildroot}%{_bindir}/

# install shell completions
install -Dpm0644 %{name}.bash \
    %{buildroot}/%{bash_completions_dir}/%{name}.bash
install -Dpm0644 %{name}.fish \
    %{buildroot}/%{fish_completions_dir}/%{name}.fish
install -Dpm0644 _%{name} \
    %{buildroot}/%{zsh_completions_dir}/_%{name}

%files
%license LICENSE LICENSE.dependencies
%doc README.md
%{_bindir}/%{name}
%{bash_completions_dir}/%{name}.bash
%{zsh_completions_dir}/_%{name}
%{fish_completions_dir}/%{name}.fish

%changelog
%autochangelog
