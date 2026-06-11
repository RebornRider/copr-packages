%global real_name framework-laptop

%global debug_package %{nil}

%global commit      6164bc3dec24b6bb2806eedd269df6a170bcc930
%global shortcommit %(c=%{commit}; echo ${c:0:7})

Name:           %{real_name}-kmod-common
# Upstream has no version tags; stay at 1 (previously published version) so
# upgrades keep working without an Epoch.
Version:        1
Release:        %autorelease -b 4 -s git%{shortcommit}
Summary:        Kernel module to expose more Framework Laptop stuff
License:        GPL-2.0-only
URL:            https://github.com/DHowett/framework-laptop-kmod
BuildArch:      noarch

Source:         %{url}/archive/%{commit}/%{real_name}-kmod-%{shortcommit}.tar.gz

Requires:       %{real_name}-kmod = %{?epoch:%{epoch}:}%{version}

%description
A kernel module that exposes the Framework Laptop (13, 16)'s
battery charge limit and LEDs to userspace.

%prep
%autosetup -p1 -n %{real_name}-kmod-%{commit}

%build
# Docs-only subpackage; nothing to compile.

%install
# Files shipped come from %%prep; no install steps required.

%files
%license LICENSE
%doc README.md

%changelog
%autochangelog
