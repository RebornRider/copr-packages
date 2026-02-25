%global extuuid        quake-terminal@diegodario88.github.io
%global extdir         %{_datadir}/gnome-shell/extensions/%{extuuid}
%global gschemadir     %{_datadir}/glib-2.0/schemas
%global gschemafile    org.gnome.shell.extensions.quake-terminal.gschema.xml
%global debug_package  %{nil}

# renovate: datasource=github-releases depName=diegodario88/quake-terminal
%global commit      bea075af5062cea7c0edb746ebea3ce077ed1a7d
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global gitrel      .git%{shortcommit}

Name:        gnome-shell-extension-quake-terminal
Version:     1.0.4
Release:     10%{gitrel}%{?dist}
Summary:     Quickly launch a terminal in Quake mode using a keyboard shortcut

Group:       User Interface/Desktops
License:     GPL-3.0-only
URL:         https://github.com/diegodario88/quake-terminal
Source0:     %{url}/archive/%{commit}.tar.gz
BuildArch:   noarch

BuildRequires:  make
BuildRequires:  %{_bindir}/glib-compile-schemas
BuildRequires:  gnome-shell >= 45~rc
Requires:    gnome-shell >= 45~rc

%description
Quickly launch a terminal in Quake mode using a keyboard shortcut

%prep
%autosetup -n quake-terminal-%{commit} -N

%build
make compile 

%install
make pack

mkdir -p %{buildroot}%{extdir}
unzip -q %{extuuid}.shell-extension.zip -d %{buildroot}%{extdir}/

mkdir -p %{buildroot}%{gschemadir}
%{__mv} -f %{buildroot}%{extdir}/schemas/%{gschemafile} -t %{buildroot}%{gschemadir}/
    
# Cleanup crap.
%{__rm} -fr %{buildroot}%{extdir}/{LICENSE*,README*,schemas}

%files
%doc README.md
%license LICENSE
%{extdir}
%{gschemadir}/%{gschemafile}

%changelog
%autochangelog
