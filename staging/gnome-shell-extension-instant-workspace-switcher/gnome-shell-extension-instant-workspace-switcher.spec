%global extuuid        instantworkspaceswitcher@amalantony.net
%global extdir         %{_datadir}/gnome-shell/extensions/%{extuuid}
%global debug_package  %{nil}

# renovate: datasource=github-releases depName=amalantony/gnome-shell-extension-instant-workspace-switcher
%global commit      875e22f799d23df754084f3d708dddb595c27900
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global gitrel      .git%{shortcommit}

Name:        gnome-shell-extension-instant-workspace-switcher
Version:     0.0.0
Release:     5%{gitrel}%{?dist}
Summary:     Disables the workspace switch animation

Group:       User Interface/Desktops
License:     GPL-2.0-only
URL:         https://github.com/amalantony/gnome-shell-extension-instant-workspace-switcher
Source0:     %{url}/archive/%{commit}.tar.gz    
BuildArch:   noarch

Requires:    gnome-shell >= 45~rc

%description
Disables the workspace switch animation while preserving all other animations.

%prep
%autosetup -n gnome-shell-extension-instant-workspace-switcher-%{commit} -N

%build
ls -lah

%install
mkdir -p %{buildroot}%{extdir}

%{__cp} -rf %{extuuid}/* %{buildroot}%{extdir}
    
# Cleanup crap.
%{__rm} -fr %{buildroot}%{extdir}/{LICENSE*,README*}

%files
%doc README.md
%license LICENSE
%{extdir}

%changelog
%autochangelog
