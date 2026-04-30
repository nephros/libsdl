%undefine __cmake_in_source_build
%bcond_with tests
%bcond_with examples

# cmake of SDL requires static libs to exist
%define keepstatic 1

Summary: Simple DirectMedia Layer 3
Name: SDL3
Version: 3.4.4
Release: 1
Source: %{name}-%{version}.tar.gz
URL: http://www.libsdl.org/
License: zlib
BuildRequires: cmake
BuildRequires: pkgconfig(wayland-egl)
BuildRequires: pkgconfig(wayland-client)
BuildRequires: pkgconfig(wayland-cursor)
BuildRequires: pkgconfig(wayland-egl)
BuildRequires: pkgconfig(wayland-protocols)
BuildRequires: pkgconfig(wayland-scanner)
BuildRequires: pkgconfig(egl)
#BuildRequires: pkgconfig(glesv1_cm)
BuildRequires: pkgconfig(glesv2)
BuildRequires: pkgconfig(xkbcommon)
BuildRequires: pkgconfig(libpulse-simple)
# added for SDL3:
BuildRequires: pkgconfig(dbus-1)
BuildRequires: pkgconfig(libudev)
BuildRequires: pkgconfig(libusb)
# do we want these?
# KMS/DRM driver needs libdrm and libgbm
BuildRequires: pkgconfig(gbm)
BuildRequires: pkgconfig(libdrm)
# experimental/future?
#BuildRequires: pkgconfig(libpipewire-0.3)
# vulkan?
BuildRequires: pkgconfig(vulkan)

# Optional:
BuildRequires: pkgconfig(alsa)
BuildRequires: pkgconfig(libavcodec)
BuildRequires: pkgconfig(libavformat)
BuildRequires: pkgconfig(libavutil)
BuildRequires: pkgconfig(libswscale)

BuildRequires: pkgconfig(liburing-ffi)

# Maliit IME integration (TODO)
%if 0%{?sailfishos_version} >= 40600
BuildRequires: pkgconfig(maliit-glib)
%endif
# Sailfish sensors API (TODO)
#Buildrequires: pkgconfig(sensors-glib)
# Camera and other droidmedia things
BuildRequires: pkgconfig(droidmedia)
# detecting Sailfish via /etc/os-release variables
BuildRequires: config(sailfish-version-variant)

# We don't strictly *need* Vulkan
# As it may pull useless things like amdgpu, lets suggest, not recommend it:
Suggests: vulkan-drivers

Patch0:  0000-cmake-respect-no-color.patch
Patch1:  0000-define-sdl-platform-sailfishos.patch

Patch10:  0010-sailfishos-platform-readme.patch
Patch11:  0011-sailfishos-report-phone-or-tablet.patch
Patch12:  0012-sailfishos-sailjail-sandbox.patch
Patch13:  0013-sailfishos-lipstick-open-url.patch
Patch14:  0014-sailfishos-lipstick-progressbar.patch
Patch15:  0015-sailfishos-pulse-set-media-role.patch
Patch16:  0016-sailfishos-no-gtk-quit.patch
Patch17:  0017-sailfish-extra-xdg-folders.patch
# this probably needs a socket connection which we have in SDL_net.
# Patch17:  0017-sailfish-sensorfw-impl.patch
# Patch18:  0018-sailfish-droidmedia-camera-impl.patch
# Patch19:  0019-sailfish-handle-display-bounds.patch

Patch20: 0020-sailfishos-force-always-fullscreen.patch
Patch21: 0021-sailfish-wl-the-enemy-gate-is-always-down.patch

# that's the big one!
#Patch50: 0050-sailfishos-bring-back-wl_shell-support.patch

%description
This is the Simple DirectMedia Layer, a generic API that provides low
level access to audio, keyboard, mouse, and display framebuffer across
multiple platforms.

%package devel
Summary: Simple DirectMedia Layer 3 - Development libraries
Requires: %{name} = %{version}
Provides: cmake(SDL3)
Provides: cmake(SDL3::SDL3-shared)
Provides: cmake(SDL3::Headers)

%description devel
This is the Simple DirectMedia Layer, a generic API that provides low
level access to audio, keyboard, mouse, and display framebuffer across
multiple platforms.

This is the libraries, include files and other resources you can use
to develop SDL applications.

%package static
Summary: Simple DirectMedia Layer 3 - Static libraries
# Needed to keep CMake happy
Requires: %{name}-devel = %{version}
Provides: cmake(SDL3::SDL3-static)

%description static
This is the Simple DirectMedia Layer, a generic API that provides low
level access to audio, keyboard, mouse, and display framebuffer across
multiple platforms.

This is the static libraries for SDL3.
applications.

%if %{with tests}
%package testlib
Summary: Simple DirectMedia Layer 3 - Testing libraries
# Needed to keep CMake happy
Requires: %{name}-devel = %{version}
Provides: cmake(SDL3::SDL3_test)

%description testlib
This is the Simple DirectMedia Layer, a generic API that provides low
level access to audio, keyboard, mouse, and display framebuffer across
multiple platforms.

This is the testing libraries for SDL3.
%endif

%if %{with examples}
%package examples
Summary: Simple DirectMedia Layer 3 - Example Programs
Requires: %{name} = %{version}

%description examples
This is the Simple DirectMedia Layer, a generic API that provides low
level access to audio, keyboard, mouse, and display framebuffer across
multiple platforms.

In here are a collection of standalone SDL application examples. Unless
otherwise stated, they should work on all supported platforms out of the box.
%endif


%if %{with tests}
%package tests
Summary: Simple DirectMedia Layer 3 - Test Programs
Requires: %{name} = %{version}

%description tests
This is the Simple DirectMedia Layer, a generic API that provides low
level access to audio, keyboard, mouse, and display framebuffer across
multiple platforms.

In here are a collection of SDL test programs.
%endif

# add missing macros in case we want to use cmake_build/install
%if 0%{?sailfishos_version} < 40600
%if 0%{?sailfishos_version} <= 40000
%define cmake_build %__cmake --build "."
%define cmake_install %make_install
%else
%define cmake_build %__cmake --build "." -j8 --verbose
%define cmake_install DESTDIR=%buildroot %__cmake --install .
%endif
%endif

%prep
%autosetup -p1 -n %{name}-%{version}/%{name}

%build
# disable color output in cmake, it looks garbled on OBS:
export CLICOLOR=0
# SDL_*_SHARED=OFF -> link to libs rather than dlopen.
%cmake \
  -DLIB_SUFFIX="" \
  -DPULSEAUDIO=ON \
  -DSDL_RPATH=OFF \
  -DSDL_STATIC=ON \
  -DSDL_SHARED=ON \
  -DSDL_RENDER_VULKAN=ON \
  -DSDL_RENDER_GPU=ON \
%if %{with examples}
  -DSDL_EXAMPLES=ON \
  -DSDL_INSTALL_EXAMPLES=ON \
%endif
%if %{with tests}
  -DSDL_TEST_LIBRARY=ON \
  -DSDL_TESTS=ON \
  -DSDL_INSTALL_TESTS=ON \
%endif
  -DSDL_WAYLAND_WL_SHELL=ON \
  -DSDL_DIALOG=OFF \
  -DSDL_TRAY=OFF \
  -DSDL_OPENVR=OFF \
  -DSDL_HIDAPI=OFF \
  -DSDL_VIRTUAL_JOYSTICK=ON \
  %{nil}


%cmake_build

%install
%cmake_install
rm -f %{buildroot}%{_datadir}/licenses/%{name}/LICENSE.txt

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%license LICENSE.txt
%{_libdir}/lib*.so.*

%files devel
%{_libdir}/lib*.so
%{_includedir}/*/*.h
%{_libdir}/pkgconfig/*
%{_libdir}/cmake/%{name}/SDL3Config*.cmake
%if %{without tests}
%exclude %{_libdir}/cmake/%{name}/SDL3testTargets-relwithdebinfo.cmake
%exclude %{_libdir}/cmake/%{name}/SDL3testTargets.cmake
%exclude %{_libdir}/lib*_test.a
%endif
%{_libdir}/cmake/%{name}/SDL3headersTargets.cmake
%{_libdir}/cmake/%{name}/SDL3sharedTargets*.cmake

%files static
%{_libdir}/lib*3.a
%{_libdir}/cmake/%{name}/SDL3staticTargets*.cmake

%if %{with tests}
%files testlib
%{_libdir}/lib*_test.a
%{_libdir}/cmake/%{name}/SDL3testTargets*.cmake
%endif

%if %{with examples}
%files examples
%dir %{_libexecdir}/installed-examples/SDL3
%{_libexecdir}/installed-examples/SDL3/*
%endif

%if %{with tests}
%files tests
%dir %{_libexecdir}/installed-tests/SDL3
%{_libexecdir}/installed-tests/SDL3/*
%dir %{_datadir}/installed-tests/SDL3
%{_datadir}/installed-tests/SDL3/*
%endif

%changelog
* Thu Feb 15 2024 Matti Lehtimäki <matti.lehtimaki@jolla.com> - 2.30.0+git2
- [sdl] Replace revert patch with proper upstream fix. JB#61492
* Wed Feb  7 2024 Matti Lehtimäki <matti.lehtimaki@jolla.com> - 2.30.0+git1
- [sdl] Update to version 2.30.0. JB#61492
* Mon Jun 26 2023 Matti Lehtimäki <matti.lehtimaki@jolla.com> - 2.28.0+git1
- [sdl] Update to version 2.28.0. JB#60520
* Tue Aug 30 2022 Matti Lehtimäki <matti.lehtimaki@jolla.com> - 2.24.0+git1
- [sdl] Update to version 2.24.0. JB#58606
* Fri Dec  3 2021 Matti Lehtimäki <matti.lehtimaki@jolla.com> - 2.0.18+git1
- [sdl] Update to version 2.0.18. JB#56588
* Fri Aug 27 2021 Matti Lehtimäki <matti.lehtimaki@jolla.com> - 2.0.16+git1
- [sdl] Update to version 2.0.16. JB#54674
* Wed Jun  9 2021 Matti Lehtimäki <matti.lehtimaki@jolla.com> - 2.0.14+git2
- [sdl] Fix creating EGLSurface in Wayland. JB#54613
- [sdl] Implement GetDisplayDPI for Wayland. JB#54613
* Thu Jan 14 2021 Matti Lehtimäki <matti.lehtimaki@jolla.com> - 2.0.14+git1
- [sdl] Update to 2.0.14 release. JB#52619
* Mon May 11 2020 Matti Lehtimäki <matti.lehtimaki@jolla.com> - 2.0.12+git1
- [sdl] Update to 2.0.12 release. JB#49887
* Fri May  3 2019 Matti Lehtimäki <matti.lehtimaki@jolla.com> - 2.0.9+git3
- [sdl] Add upstream patch to not force X11 in EGL. Contributes to JB#37662
* Fri Mar 29 2019 Matti Lehtimäki <matti.lehtimaki@jolla.com> - 2.0.9+git2
- [sdl] Update libsdl to 2.0.9. Fixes MER#1920
* Wed Aug 22 2018 Matti Kosola <matti.kosola@jollamobile.com> - 2.0.3-nemo4
- [sdl] Fix "unresponsible application" issue. Contributes MER#1934
* Thu Nov 24 2016 pvuorela <pekka.vuorela@jolla.com> - 2.0.3-nemo3
- [sdl] Set orientation and window flags via SDL hints. Fixes JB#27386
* Mon Apr 21 2014 Thomas Perl <m@thp.io> - 2.0.3-nemo2
- [nemo] Add RPM changes entries from old branch
- [nemo] Rebased RPM packaging on upstream 2.0.3 tag
* Fri Apr 18 2014 Thomas Perl <thomas.perl@jolla.com> - 2.0.3-nemo1
- [nemo] New upstream release 2.0.3
- [nemo] SDL 2.0.3 RPM packaging
- [nemo] Wayland: Resize windows with 0x0 requested size to screen size
* Mon Dec 30 2013 Thomas Perl <thomas.perl@jolla.com> - 2.0.1-nemo2
- [nemo] Add RPM packaging
