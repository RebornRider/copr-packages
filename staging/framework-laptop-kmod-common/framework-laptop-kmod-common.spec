%global real_name framework-laptop

%global debug_package %{nil}

Name:           %{real_name}-kmod-common
Version:        %autorelease
Release:        1%{?dist}
Summary:        Kernel module to expose more Framework Laptop stuff
License:        GPL-2.0-only
URL:            https://github.com/DHowett/framework-laptop-kmod
BuildArch:      noarch

Source:         %{url}/archive/refs/heads/main.tar.gz

Requires:       %{real_name}-kmod = %{?epoch:%{epoch}:}%{version}
Provides:       %{real_name}-kmod-common = %{?epoch:%{epoch}:}%{version}

%description
A kernel module that exposes the Framework Laptop (13, 16)'s 
battery charge limit and LEDs to userspace.
 
%prep
%autosetup -p1 -n %{real_name}-kmod-main

%files
%license LICENSE
%doc README.md

%changelog
%autochangelog
