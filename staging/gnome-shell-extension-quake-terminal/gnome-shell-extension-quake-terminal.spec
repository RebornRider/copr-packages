%global extuuid        quake-terminal@diegodario88.github.io
%global extdir         %{_datadir}/gnome-shell/extensions/%{extuuid}
%global gschemadir     %{_datadir}/glib-2.0/schemas

# renovate: datasource=github-releases depName=diegodario88/quake-terminal
%global commit      c94b35f0bd00d3bd88aca7f8b7efac763bd18735
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global gitrel      .git%{shortcommit}

Name:        gnome-shell-extension-quake-terminal
Version:     0.0.0
Release:     2%{gitrel}%{?dist}
Summary:     Quickly launch a terminal in Quake mode using a keyboard shortcut

Group:       User Interface/Desktops
License:     GPLv3
URL:         https://github.com/diegodario88/quake-terminal
Source0:     %{url}/archive/%{commit}.tar.gz
BuildArch:   noarch

BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  make
BuildRequires:  %{_bindir}/glib-compile-schemas
BuildRequires:  gnome-shell >= 45~rc
Requires:    gnome-shell >= 45~rc
Requires:    glib2

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
%{__mv} -f %{buildroot}%{extdir}/schemas/org.gnome.shell.extensions.quake-terminal.gschema.xml %{buildroot}%{gschemadir}/org.gnome.shell.extensions.quake-terminal.gschema.xml
    
# Cleanup crap.
%{__rm} -fr %{buildroot}%{extdir}/{LICENSE*,README*,schemas}

%files
%doc README.md
%license LICENSE
%{extdir}
%{gschemadir}/org.gnome.shell.extensions.quake-terminal.gschema.xml

%changelog
%autochangelog
