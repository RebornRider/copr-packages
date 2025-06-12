%global extuuid        fw-fanctrl-revived@willow.sh
%global extdir         %{_datadir}/gnome-shell/extensions/%{extuuid}
%global gschemadir     %{_datadir}/glib-2.0/schemas
%global gschemafile    org.gnome.shell.extensions.fw-fanctrl-revived.gschema.xml
%global debug_package  %{nil}

# renovate: datasource=github-releases depName=ghostdevv/fw-fanctrl-revived-gnome-shell-extension
%global commit      555bab46a5c0643171668fca0a73cb8d98cb70cb
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global gitrel      .git%{shortcommit}

Name:        gnome-shell-extension-fw-fanctrl-revived
Version:     0.0.0
Release:     1%{gitrel}%{?dist}
Summary:     A Gnome extension that controls your framework laptop fan profile

Group:       User Interface/Desktops
License:     MIT
URL:         https://github.com/ghostdevv/fw-fanctrl-revived-gnome-shell-extension
Source0:     https://github.com/RebornRider/copr-packages/releases/download/source-artefacts/gnome-shell-extension-fw-fanctrl-revived-%{shortcommit}.zip    
BuildArch:   noarch

Requires:    gnome-shell >= 45~rc

%description
A Gnome extension that provides a convenient way to 
control your framework laptop fan profile when using fw-fanctrl

%prep
%autosetup -n gnome-shell-extension-fw-fanctrl-revived -N

%build
ls -lah

%install
mkdir -p %{buildroot}%{extdir}
cp -r "$(dirname "$dir")" %{buildroot}%{extdir}/

mkdir -p %{buildroot}%{gschemadir}
%{__mv} -f schemas/%{gschemafile} -t %{buildroot}%{gschemadir}/

# Cleanup crap.
%{__rm} -fr %{buildroot}%{extdir}/{LICENSE*,README*,schemas} 

%files
%doc README.md
%license LICENSE
%{extdir}
%{gschemadir}/%{gschemafile}

%changelog
%autochangelog
