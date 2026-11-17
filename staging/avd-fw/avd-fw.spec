# meson's exported Fedora CFLAGS break this freestanding Cortex-M3 build
%global build_cflags %{nil}
%global build_ldflags %{nil}

Name:     avd-fw
Version:  0.2
Release:  92%{?dist}
Summary:  Firmware for the Apple Silicon AVD (video decode) V4L2 driver

License:  MIT
URL:      https://github.com/AsahiLinux/avd-fw
Source:   %{url}/releases/download/v%{version}/avd-fw-v%{version}.tar.xz

BuildRequires:  meson >= 1.4.0
BuildRequires:  arm-none-eabi-gcc-cs
BuildRequires:  arm-none-eabi-binutils-cs

BuildArch:      noarch

%description
Trampoline firmware for the Cortex-M3 core inside Apple Silicon's AVD
(Apple Video Decoder) block, consumed by the drivers/media/platform/apple/avd
V4L2 driver (CONFIG_VIDEO_APPLE_AVD). It's a from-scratch reimplementation,
not Apple's own firmware, so it isn't in linux-firmware yet and ships here
instead - see https://github.com/AsahiLinux/fairydust-rpm for the kernel
this firmware pairs with.

Installs into %{_prefix}/lib/firmware/updates/apple, which the kernel's
firmware loader searches before the plain %{_prefix}/lib/firmware/ tree, so
this package can override/precede anything a future linux-firmware upload
ships under the same names.

%prep
%autosetup -n avd-fw-v%{version}

%build
%meson \
  --libdir=lib \
  -Dfirmwaredir=firmware/updates \
  --cross-file=./arm-none-eabi-gcc.ini \
  -Dvideo-codecs=all \
  %{nil}
%meson_build

%install
%meson_install

%files
%{_prefix}/lib/firmware/updates/apple

%changelog
* Mon Nov 16 2026 Lachlan Marie <lchlnm@pm.me> - 0.2-2
- Build from meson dist release tarball

* Mon Nov 16 2026 Lachlan Marie <lchlnm@pm.me> - 0.2-1
- Update to 0.2

* Sat Oct 03 2026 Lachlan Marie <lchlnm@pm.me> - 0.1-2
- Drop no-op build flag and debuginfo overrides

* Wed Sep 02 2026 Lachlan Marie <lchlnm@pm.me> - 0.1-1
- Initial packaging, based on jannau/avd-fw-spec.
