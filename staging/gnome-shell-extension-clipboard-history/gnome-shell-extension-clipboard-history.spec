%global extuuid        clipboard-history@alexsaveau.dev
%global extdir         %{_datadir}/gnome-shell/extensions/%{extuuid}
%global gschemadir     %{_datadir}/glib-2.0/schemas
%global gschemafile    org.gnome.shell.extensions.clipboard-indicator.gschema.xml
%global debug_package  %{nil}

# renovate: datasource=github-releases depName=SUPERCILEX/gnome-clipboard-history
%global commit      450694983c5b6b03bbe80a449ce3dc4450ca7b95
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global gitrel      .git%{shortcommit}

Name:        gnome-shell-extension-gnome-clipboard-history
Version:     0.0.0
Release:     5%{gitrel}%{?dist}
Summary:     a clipboard manager for GNOME

Group:       User Interface/Desktops
License:     MIT
URL:         https://github.com/SUPERCILEX/gnome-clipboard-history
Source0:     %{url}/archive/%{commit}.tar.gz
BuildArch:   noarch

BuildRequires:  make
BuildRequires:  gettext
BuildRequires:  %{_bindir}/glib-compile-schemas
Requires:    gnome-shell >= 45~rc

%description
Gnome Clipboard History is a clipboard manager

%prep
%autosetup -n gnome-clipboard-history-%{commit} -N

%build
make all 

%install
make bundle

mkdir -p %{buildroot}%{extdir}
unzip -q bundle.zip -d %{buildroot}%{extdir}/

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
