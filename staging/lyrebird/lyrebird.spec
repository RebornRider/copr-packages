%global forgeurl https://gitlab.torproject.org/tpo/anti-censorship/pluggable-transports/lyrebird
%global commit fc105a03c0e0acc2479301c361c012ffed359c43
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global source_date_epoch_from_changelog 0
%global debug_package %{nil}
# Required: %%gobuild exports GO111MODULE from this macro. Without it the macro
# falls back to GO111MODULE=off, forcing GOPATH mode and breaking dependency
# resolution for this module-based build.
%global gomodulesmode GO111MODULE=on
%forgemeta

Name:           lyrebird
Version:        0.8.1
Release:        %autorelease -b 1 -s git%{shortcommit}
Summary:        Tor pluggable transport
# LICENSE is BSD-2-Clause (Tor/Yawning Angel) AND BSD-3-Clause (Go Authors);
# LICENSE-GPL3.txt covers bundled GPLv3 code.
License:        BSD-2-Clause AND BSD-3-Clause AND GPL-3.0-or-later
URL:            %{forgeurl}
Source0:        %{forgesource}
# go.mod declares "go 1.22.0"; bump if you specifically need a newer toolchain.
BuildRequires:  golang-bin >= 1.22
BuildRequires:  go-rpm-macros
BuildRequires:  git-core

%description
Lyrebird is the Tor Project's maintained fork of obfs4proxy, providing a
pluggable transport for Tor. It supports multiple obfuscation protocols:
obfs2/3/4, the Meek client, the ScrambleSuit client, Snowflake, and the
WebTunnel client.

%prep
%forgeautosetup

%build
# Network-enabled Copr build: enable internet access in the project settings.
# "direct" is required to resolve the utls "replace" fork hosted on the Tor
# GitLab, which proxy.golang.org will not serve.
export GOPROXY="https://proxy.golang.org,direct"
export LDFLAGS="$LDFLAGS -X main.lyrebirdVersion=%{version}"
%gobuild -o %{name} ./cmd/%{name}

%install
install -Dpm 0755 -t %{buildroot}%{_bindir} %{name}
install -Dpm 0644 -t %{buildroot}%{_mandir}/man1 doc/%{name}.1
install -Dpm 0644 -t %{buildroot}%{_pkgdocdir} README.md ChangeLog doc/obfs4-spec.txt

%files
%license LICENSE LICENSE-GPL3.txt
%doc %{_pkgdocdir}
%{_bindir}/%{name}
%{_mandir}/man1/%{name}.1*

%changelog
%autochangelog
