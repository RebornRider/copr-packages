%global real_name framework-laptop

%global debug_package %{nil}

%global commit      6164bc3dec24b6bb2806eedd269df6a170bcc930
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global gitrel      .git%{shortcommit}

Name:           %{real_name}-kmod-common
Version:        %autorelease
Release:        2%{gitrel}%{?dist}
Summary:        Kernel module to expose more Framework Laptop stuff
License:        GPL-2.0-only
URL:            https://github.com/DHowett/framework-laptop-kmod
BuildArch:      noarch

Source:         %{url}/archive/%{commit}/%{real_name}-kmod-%{shortcommit}.tar.gz

Requires:       %{real_name}-kmod = %{?epoch:%{epoch}:}%{version}
Provides:       %{real_name}-kmod-common = %{?epoch:%{epoch}:}%{version}

%description
A kernel module that exposes the Framework Laptop (13, 16)'s
battery charge limit and LEDs to userspace.

%prep
%autosetup -p1 -n %{real_name}-kmod-%{commit}

%files
%license LICENSE
%doc README.md

%changelog
%autochangelog
