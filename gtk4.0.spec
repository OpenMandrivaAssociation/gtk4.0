%bcond_with bootstrap
%if %{with bootstrap}
# Disable gstreamer to avoid a circular build dependency between gtk4 and gst-plugins-bad. Enable it after bootstraping.
%bcond_with gstreamer
%else
%bcond_without gstreamer
%endif
%bcond_with gtkdoc
%bcond_with tests

# required version of various libraries
%global glib2_version 2.65.0
%global pango_version 1.49.0
%global atk_version 2.15.1
%global cairo_version 1.14.0
%global gdk_pixbuf_version 2.30.0
%global wayland_protocols_version 1.20
%global wayland_version 1.14.91


%define pkgname			gtk
%define api			4
%define api_version		4.0
%define binary_version		4.0.0
%define lib_major		1
%define libname			%mklibname %{pkgname} %{api} %{lib_major}
%define girname			%mklibname gtk-gir %{api_version}
%define develname		%mklibname -d %{pkgname} %{api_version}

%define url_ver	%(echo %{version}|cut -d. -f1,2)

# "fix" underlinking:
%define _disable_ld_no_undefined 1

Name:		%{pkgname}%{api_version}
Version:	4.14.1
Release:	1
Summary:        GTK graphical user interface library
License:	LGPLv2+
Group:		System/Libraries
URL:		https://www.gtk.org
Source0:	https://download.gnome.org/sources/%{pkgname}/%{url_ver}/%{pkgname}-%{version}.tar.xz

# Backported from upstream

# Fedora patches

# OpenMandriva patches

# FIXME this patch is not entirely correct, but should be good enough.
# Certainly better than failing to even compile...
Patch1:		gtk-4.10.1-ffmpeg-6.0.patch

Requires:	common-licenses

BuildRequires: autoconf-archive
BuildRequires: cups-devel
BuildRequires: gettext-devel
BuildRequires: git
BuildRequires: gtk-doc
BuildRequires: meson
BuildRequires: pkgconfig(atk) >= %{atk_version}
BuildRequires: pkgconfig(atk-bridge-2.0)
BuildRequires: pkgconfig(avahi-gobject)
BuildRequires: pkgconfig(cairo) >= %{cairo_version}
BuildRequires: pkgconfig(cairo-gobject) >= %{cairo_version}
BuildRequires: pkgconfig(colord)
BuildRequires: pkgconfig(egl)
BuildRequires: pkgconfig(epoxy)
BuildRequires: pkgconfig(gdk-pixbuf-2.0) >= %{gdk_pixbuf_version}
BuildRequires: pkgconfig(glib-2.0) >= %{glib2_version}
BuildRequires: pkgconfig(gobject-introspection-1.0)
BuildRequires: pkgconfig(graphene-gobject-1.0)
%if %{with gstreamer}
BuildRequires: pkgconfig(gstreamer-player-1.0)
%endif
BuildRequires: pkgconfig(gi-docgen)
BuildRequires: pkgconfig(iso-codes)
BuildRequires: pkgconfig(json-glib-1.0)
BuildRequires: pkgconfig(libavcodec)
BuildRequires: pkgconfig(librsvg-2.0)
BuildRequires: pkgconfig(libjpeg)
BuildRequires: pkgconfig(libpng)
BuildRequires: pkgconfig(libtiff-4)
BuildRequires: pkgconfig(pango) >= %{pango_version}
BuildRequires: pkgconfig(pangocairo)
%if !  %{with bootstrap}
BuildRequires: pkgconfig(sysprof-6)
BuildRequires: pkgconfig(sysprof-capture-4)
BuildRequires: pkgconfig(rest-0.7)
%endif
BuildRequires: pkgconfig(tracker-sparql-3.0)
BuildRequires: pkgconfig(vulkan)
BuildRequires: pkgconfig(wayland-client) >= %{wayland_version}
BuildRequires: pkgconfig(wayland-cursor) >= %{wayland_version}
BuildRequires: pkgconfig(wayland-egl) >= %{wayland_version}
BuildRequires: pkgconfig(wayland-protocols) >= %{wayland_protocols_version}
BuildRequires: pkgconfig(xcomposite)
BuildRequires: pkgconfig(xcursor)
BuildRequires: pkgconfig(xdamage)
BuildRequires: pkgconfig(xfixes)
BuildRequires: pkgconfig(xi)
BuildRequires: pkgconfig(xinerama)
BuildRequires: pkgconfig(xkbcommon)
BuildRequires: pkgconfig(xrandr)
BuildRequires: pkgconfig(xrender)
BuildRequires: python3dist(pygobject)
BuildRequires: python3dist(docutils)
BuildRequires: %{_lib}harfbuzz-gir-devel
BuildRequires: sassc
BuildRequires: glslc

BuildRequires: vulkan-headers

%rename gtk+4.0

%if %{with tests}
BuildRequires:	x11-server-xvfb
%endif

%if %{with gtkdoc}
BuildRequires:	gtk-doc >= 1.99
BuildRequires:	sgml-tools
BuildRequires:	texinfo
%endif

# gw tests will fail without this
BuildRequires:	fonts-ttf-dejavu

%if ! %{with bootstrap}
Recommends:	xdg-user-dirs-gtk
%endif
Recommends:	%mklibname gvfs 0

Requires:	%{libname} = %{version}
Provides:	%{pkgname}%{api} = %{version}-%{release}

%description
GTK is a multi-platform toolkit for creating graphical user
interfaces. Offering a complete set of widgets, GTK is suitable for
projects ranging from small one-off tools to complete application
suites.
 
This package contains version 4 of GTK.

#--------------------------------------------------------------------

%package -n %{libname}
Summary:	%{summary}
Group:		%{group}
Provides:	%mklibname %{pkgname}%{api} = %{version}-%{release}
Provides:	%mklibname %{name} = %{version}-%{release}
Requires:	gtk4.0 = %{version}-%{release}
Obsoletes:	%{mklibname gtk+4.0 %{api} %{lib_major} } <= %{version}-%{release} 
Provides:	%{mklibname gtk+4.0 %{api} %{lib_major} } = %{version}-%{release}

# standard icons
Requires:	adwaita-icon-theme
# required for icon theme apis to work
Requires:	hicolor-icon-theme

Requires(posttrans):	gtk4.0
#Requires(posttrans):	%mklibname GLX_mesa0

%description -n %{libname}
This package contains the library needed to run programs dynamically
linked with gtk.

#--------------------------------------------------------------------

%package -n %{girname}
Summary:	GObject introspection interface library for %{name}
Group:		System/Libraries
Requires:	%{libname} = %{version}-%{release}

%description -n %{girname}
GObject introspection interface library for %{name}.

#--------------------------------------------------------------------

%package -n %{develname}
Summary:	Development files for GTK
Group:		Development/GNOME and GTK+
Provides:	%{pkgname}%{api}-devel = %{version}-%{release}
Provides:	%mklibname %{pkgname}%{api}-devel = %{version}-%{release}
Provides:	%mklibname %{pkgname}%{api_version}-devel = %{version}-%{release}
Provides:	%mklibname %{pkgname}-x11-%{api_version}-devel = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}
Provides:	gtk4-devel = %{version}-%{release}
Requires:	%{libname} = %{version}
Requires:	%{girname} = %{version}
Requires:	pkgconfig(gdk-pixbuf-2.0)
Requires:	pkgconfig(atk)
Requires:	pkgconfig(pango)
# Not needed but used as sanity workaround after harfuzz gir splitting.
Requires:       %{_lib}harfbuzz-gir-devel

%description -n %{develname}
This package contains the libraries and header files that are needed
for writing applications with version 4 of the GTK widget toolkit.

#--------------------------------------------------------------------

%prep
%autosetup -p1 -n gtk-%{version}

# subprojects caused an issue with gtk-doc
#            https://gitlab.gnome.org/GNOME/gtk/-/issues/3219
rm -rf subprojects

%build
%meson \
        -Dx11-backend=true \
        -Dwayland-backend=true \
        -Dbroadway-backend=true \
        -Dvulkan=enabled \
        -Dmedia-ffmpeg=enabled \
%if %{with gstreamer}        
        -Dmedia-gstreamer=enabled \
%else        
        -Dmedia-gstreamer=disabled \
%endif        
%if %{with bootstrap}
	-Dsysprof=disabled \
%else
        -Dsysprof=enabled \
%endif
        -Dcolord=enabled \
        -Dcloudproviders=disabled \
        -Dgtk_doc=false \
        -Dman-pages=true \
        -Dtracker=enabled \
        -Dbuild-testsuite=false \
        -Dbuild-tests=false

%meson_build

%install
%meson_install

%find_lang gtk40 --all-name

mkdir -p $RPM_BUILD_ROOT%{_libdir}/gtk-%{api_version}/modules

# Adwaita is the default theme but it's not installed and neither was
# Raleigh before it as far as I can tell.
# Most of this is compiled into GTK binaries but it causes the theme not to be
# "seen" by theme choosers - e.g. gnome-tweak-tool, so you cannot switch from
# e.g. oxygen-gtk (the Mageia default) to Adwaita (the upstream default) without
# these files in place or a fix to gnome-tweak-tool and other theme choosers to
# hard-code Adwaita.
# See https://bugzilla.gnome.org/show_bug.cgi?id=733420
#mkdir -p %{buildroot}%{_datadir}/themes/Adwaita/gtk-4.0
#cp -a gtk/theme/Adwaita/gtk{,-dark}.css %{buildroot}%{_datadir}/themes/Adwaita/gtk-4.0

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/*.desktop
%if %{with tests}
XDISPLAY=$(i=1; while [ -f /tmp/.X$i-lock ]; do i=$(($i+1)); done; echo $i)
%{_bindir}/Xvfb :$XDISPLAY &
export DISPLAY=:$XDISPLAY
make check
kill $(cat /tmp/.X$XDISPLAY-lock) ||:
%endif

%files -f gtk40.lang
%doc README.md
%{_bindir}/gtk4-query-settings
%{_bindir}/gtk4-launch
%{_bindir}/gtk4-update-icon-cache
%{_bindir}/gtk4-broadwayd
%{_bindir}/gtk4-rendernode-tool
%{_datadir}/glib-2.0/schemas/org.gtk.gtk4.Settings.ColorChooser.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gtk.gtk4.Settings.Debug.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gtk.gtk4.Settings.EmojiChooser.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gtk.gtk4.Settings.FileChooser.gschema.xml
%{_datadir}/gtk-%{api_version}/emoji/*.gresource
%{_mandir}/man1/gtk4-launch.1*
%{_mandir}/man1/gtk4-update-icon-cache.1*
%{_mandir}/man1/gtk4-broadwayd.1*
%{_mandir}/man1/gtk4-rendernode-tool.1.*

%files -n %{libname}
%doc README.md
%dir %{_libdir}/gtk-%{api_version}
%dir %{_libdir}/gtk-%{api_version}/modules
%dir %{_libdir}/gtk-%{api_version}/%{binary_version}
%dir %{_libdir}/gtk-%{api_version}/%{binary_version}/printbackends
%{_libdir}/gtk-%{api_version}/%{binary_version}/printbackends/*.so
%{_libdir}/libgtk-4.so.%{lib_major}.*
%{_libdir}/libgtk-4.so.%{lib_major}
%{_libdir}/gtk-%{api_version}/%{binary_version}/media/libmedia-ffmpeg.so
%if %{with gstreamer}
%{_libdir}/gtk-%{api_version}/%{binary_version}/media/libmedia-gstreamer.so
%endif

%files -n %{girname}
%{_libdir}/girepository-1.0/Gdk-%{api_version}.typelib
%{_libdir}/girepository-1.0/GdkX11-%{api_version}.typelib
%{_libdir}/girepository-1.0/GdkWayland-%{api_version}.typelib
%{_libdir}/girepository-1.0/Gsk-%{api_version}.typelib
%{_libdir}/girepository-1.0/Gtk-%{api_version}.typelib

%files -n %{develname}
%doc docs/*.txt AUTHORS NEWS README.md
%{_includedir}/*
%{_libdir}/pkgconfig/*
%{_bindir}/gtk4-builder-tool
%{_bindir}/gtk4-demo
%{_bindir}/gtk4-demo-application
%{_bindir}/gtk4-encode-symbolic-svg
%{_bindir}/gtk4-icon-browser
%{_bindir}/gtk4-node-editor
%{_bindir}/gtk4-print-editor
%{_bindir}/gtk4-widget-factory
%{_libdir}/libgtk-%{api}.so
%{_datadir}/applications/org.gtk.Demo4.desktop
%{_datadir}/applications/org.gtk.IconBrowser4.desktop
%{_datadir}/applications/org.gtk.gtk4.NodeEditor.desktop
%{_datadir}/applications/org.gtk.PrintEditor4.desktop
%{_datadir}/applications/org.gtk.WidgetFactory4.desktop
%{_datadir}/icons/hicolor/*/apps/org.gtk.Demo4*.svg
%{_datadir}/icons/hicolor/*/apps/org.gtk.IconBrowser4*.svg
%{_datadir}/icons/hicolor/*/apps/org.gtk.gtk4.NodeEditor*.svg
%{_datadir}/icons/hicolor/*/apps/org.gtk.PrintEditor4*.svg
%{_datadir}/icons/hicolor/*/apps/org.gtk.WidgetFactory4*.svg
%{_datadir}/gettext/
%{_datadir}/gir-1.0
%{_datadir}/glib-2.0/schemas/org.gtk.Demo4.gschema.xml
%dir %{_datadir}/gtk-4.0
%{_datadir}/gtk-4.0/gtk4builder.rng
%{_datadir}/gtk-4.0/valgrind/
%{_datadir}/metainfo/org.gtk.Demo4.appdata.xml
%{_datadir}/metainfo/org.gtk.IconBrowser4.appdata.xml
%{_datadir}/metainfo/org.gtk.gtk4.NodeEditor.appdata.xml
%{_datadir}/metainfo/org.gtk.PrintEditor4.appdata.xml
%{_datadir}/metainfo/org.gtk.WidgetFactory4.appdata.xml
%{_mandir}/man1/gtk4-builder-tool.1*
%{_mandir}/man1/gtk4-demo.1*
%{_mandir}/man1/gtk4-demo-application.1*
%{_mandir}/man1/gtk4-encode-symbolic-svg.1*
%{_mandir}/man1/gtk4-icon-browser.1*
%{_mandir}/man1/gtk4-node-editor.1.*
%{_mandir}/man1/gtk4-query-settings.1*
%{_mandir}/man1/gtk4-widget-factory.1*
