%global reponame    framework-ec

%global debug_package   %{nil}

# renovate: datasource=github-releases depName=DHowett/framework-ec
%global commit      54c140399bbc3e6a3dce6c9f842727c4128367be
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global commit_date 20221204
%global gitrel      .%{commit_date}.git%{shortcommit}

Name:           fw-ectool
Version:        v0.3.3
Release:        4%{gitrel}%{?dist}
Summary:        A tool for interacting with the embedded controller on a Framework laptop

License:        BSD-3-Clause
URL:            https://github.com/DHowett/framework-ec
Source0:        https://github.com/DHowett/framework-ec/archive/%{commit}/%{reponame}-%{shortcommit}.tar.gz
Source1:        fw-ectool.sh

BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  arm-none-eabi-gcc-cs
BuildRequires:  libftdi-devel

%description
A tool for interacting with the embedded controller on a Framework laptop.

%prep
%autosetup -n %{reponame}-%{commit}

%build
make utils

%install
install -Dm755 build/bds/util/ectool %{buildroot}%{_bindir}/ectool
install -m755 %SOURCE1 %{buildroot}%{_bindir}/fw-ectool

%files
%license LICENSE
%{_bindir}/ectool
%{_bindir}/fw-ectool

%changelog
%autochangelog
