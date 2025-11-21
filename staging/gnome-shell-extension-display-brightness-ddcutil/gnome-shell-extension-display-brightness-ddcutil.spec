%global extuuid        display-brightness-ddcutil@themightydeity.github.com
%global extdir         %{_datadir}/gnome-shell/extensions/%{extuuid}
%global gschemadir     %{_datadir}/glib-2.0/schemas
%global gschemafile    org.gnome.shell.extensions.display-brightness-ddcutil.gschema.xml
%global debug_package  %{nil}

# renovate: datasource=github-releases depName=daitj/gnome-display-brightness-ddcutil
%global commit      13f5bbd75e550fe6802ad633b893f9a763242292
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global gitrel      .git%{shortcommit}

Name:        gnome-shell-extension-gnome-display-brightness-ddcutil
Version:     58.0.0
Release:     1%{gitrel}%{?dist}
Summary:     Display brightness slider for gnome shell using ddcutil backend

Group:       User Interface/Desktops
License:     GPL-3.0-only
URL:         https://github.com/daitj/gnome-display-brightness-ddcutil
Source0:     %{url}/archive/%{commit}.tar.gz
BuildArch:   noarch

BuildRequires:  make
BuildRequires:  gettext
BuildRequires:  %{_bindir}/glib-compile-schemas
BuildRequires:  gnome-shell >= 45~rc
Requires:    gnome-shell >= 45~rc

%description
Display brightness slider for gnome shell using ddcutil backend

%prep
%autosetup -n gnome-display-brightness-ddcutil-%{commit} -N

%build
make build 

%install
mkdir -p %{buildroot}%{extdir}
unzip -q dist/%{extuuid}.shell-extension.zip -d %{buildroot}%{extdir}/

mkdir -p %{buildroot}%{gschemadir}
%{__mv} -f %{buildroot}%{extdir}/schemas/%{gschemafile} -t %{buildroot}%{gschemadir}/
    
# Cleanup crap.
%{__rm} -fr %{buildroot}%{extdir}/{LICENSE*,README*,schemas,locale}

%files
%doc README.md
%license LICENSE
%{extdir}
%{gschemadir}/%{gschemafile}

%changelog
%autochangelog
