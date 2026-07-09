%global debug_package %{nil}

# main @ 2026-07-08: "Fix decimal config validation for temperature thresholds (#192)"
%global commit          4ca85b3a8157951ddaf2496917de65fd542e7952
%global shortcommit     %(c=%{commit}; echo ${c:0:7})
%global snapshotdate    20260708

Name:           fw-fanctrl
# Post-release snapshot of main (v1.1.0 + #195, #177, #192)
Version:        1.1.0^%{snapshotdate}git%{shortcommit}
Release:        %autorelease
Summary:        Framework FanControl Software

License:        BSD-3-Clause
BuildArch:      noarch
URL:            https://github.com/TamtamHero/%{name}
Source0:        %{url}/archive/%{commit}/%{name}-%{commit}.tar.gz

BuildRequires:  systemd-rpm-macros
BuildRequires:  python3-devel
BuildRequires:  python3-pip
BuildRequires:  python3dist(setuptools)
BuildRequires:  python3dist(wheel)
# for the upstream test suite (tests/ added in #192)
BuildRequires:  python3dist(pytest)
BuildRequires:  python3dist(jsonschema)
Requires:       python3
Requires:       %{_bindir}/framework_tool

Patch0:         138-no-build.patch
Patch1:         199-critical-temperature.patch

Source1:        99-fw-fanctrl.rules

%description
fw-fanctrl is a Python service that controls fan speed on Framework
laptops using configurable temperature strategies. It runs
as a systemd service and supports runtime strategy switching.

%prep
%autosetup -n %{name}-%{commit} -p1

%build
%pyproject_wheel

%install
./install.sh --no-sudo \
    --ignore-tool framework_tool \
    --no-pip-install \
    --no-pip-build \
    --no-post-install \
    -d %{buildroot} \
    --effective-installation-dir /usr/bin
%pyproject_install

rm -f %{buildroot}%{_sysconfdir}/%{name}/config.schema.json

install -D -m 0644 %{SOURCE1} %{buildroot}%{_udevrulesdir}/99-fw-fanctrl.rules

%check
%pytest

%post
%systemd_post %{name}.service %{name}-suspend.service
%udev_rules_update

%preun
%systemd_preun %{name}.service %{name}-suspend.service
%udev_rules_update

%postun
%systemd_postun_with_restart %{name}.service
%udev_rules_update

%files
%license LICENSE
%doc README.md
%{_bindir}/%{name}
%{python3_sitelib}/fw_fanctrl*
%{_unitdir}/%{name}.service
%{_unitdir}/%{name}-suspend.service
%config(noreplace) %{_sysconfdir}/%{name}/config.json
%{_udevrulesdir}/99-fw-fanctrl.rules

%changelog
%autochangelog
