%undefine _auto_set_build_flags
# Undefining _auto_set_build_flags does not appear to work. Instead define
# the duild flags to nil.
%global build_cflags %{nil}
%global build_ldflags %{nil}

Name:     avd-fw
Version:  0.2
Release:  %autorelease -b 101
Summary:  Firmware for Apple/Asahi AVD video decoder V4L2 driver
License:  MIT
URL:      https://github.com/AsahiLinux/avd-fw
Source:   https://github.com/AsahiLinux/avd-fw/releases/download/v%{version}/avd-fw-v%{version}.tar.xz

Patch1:   0001-build-factor-out-objcopy_cmd.patch
Patch2:   0002-build-use-int-as-type-for-pad-value.patch
Patch3:   0003-compat-Provide-the-config-at-the-end-of-the-firmware.patch

BuildRequires:  meson >= 1.3.0
BuildRequires:  arm-none-eabi-gcc-cs
BuildRequires:  arm-none-eabi-binutils-cs

BuildArch:      noarch

%global debug_package %{nil}

%description
Firmware for Apple/Asahi AVD video decoder V4L2 driver while the driver
is only in the downstream kernel and the firmware can't yet submitted to
linux-firmware.

%prep
%autosetup -p1 -n %{name}-v%{version}

%build
%meson \
  --cross-file=./arm-none-eabi-gcc.ini \
  -Dvideo-codecs=all \
  %{nil}
%meson_build

%install
%meson_install

%files
%{_prefix}/lib/firmware/apple

%changelog
%autochangelog
