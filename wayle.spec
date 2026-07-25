### Cargo vendor source for wayle
#   From within the source tree run:
#   cargo vendor
#   copy output from terminal
#   replace contents of .cargo/config.toml with cat as seen in the prep section
#   compress and rename vendor directory as seen in Source1 below
#   tar -cJvf wayle-0.7.0-vendor.tar.xz vendor
#   place archive alongside original source archive

%global debug_package %{nil}
%define desktop_entry_filename com.wayle.settings.desktop

Name:		wayle
Version:	0.7.0
Release:	1
Source0:	https://github.com/wayle-rs/wayle/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
Source1:	%{name}-%{version}-vendor.tar.xz
Summary:	A configurable desktop shell for Wayland compositors
License:	Apache-2.0 AND BSD-2-Clause AND BSD-3-Clause AND CC0-1.0 AND CDLA-Permissive-2.0 AND ISC AND MIT AND OpenSSL AND Unicode-3.0 AND Zlib
URL:      https://wayle.app/
Group:		Graphical desktop/Other

BuildRequires:	rust-packaging
BuildRequires:  pkgconfig(cairo)
BuildRequires:	pkgconfig(fftw3)
BuildRequires:	pkgconfig(gdk-pixbuf-2.0)
BuildRequires:	pkgconfig(gtk4)
BuildRequires:	pkgconfig(gtk4-layer-shell-0)
BuildRequires:	pkgconfig(gtksourceview-5)
BuildRequires:	pkgconfig(libpipewire-0.3)
BuildRequires:	pkgconfig(libpulse)
BuildRequires:	pkgconfig(pango)
BuildRequires:	pkgconfig(udev)
BuildRequires:	pkgconfig(xkbcommon)

Requires:	networkmanager
Requires:	bluez
Requires:	power-profiles-daemon
Requires:	upower
Requires:	wireplumber

%description
A configurable desktop shell for Wayland compositors.

%prep
%autosetup -p1
tar -zxf %{SOURCE1}
mkdir -p .cargo
cat >> .cargo/config.toml << EOF
[source.crates-io]
replace-with = "vendored-sources"

[source.vendored-sources]
directory = "vendor"
EOF

%build
cargo build --frozen --release

%install
install -Dm755 target/release/%{name} %{buildroot}%{_bindir}/%{name}
install -Dm755 target/release/%{name}-settings %{buildroot}%{_bindir}/%{name}-settings

install -dm755 %{buildroot}%{_datadir}/%{name}/icons
cp -r resources/icons/hicolor %{buildroot}%{_datadir}/%{name}/icons

target/release/%{name} completions bash > %{name}.bash
target/release/%{name} completions zsh > _%{name}
target/release/%{name} completions fish > %{name}.fish

install -Dm644 %{name}.bash %{buildroot}%{_datadir}/bash-completion/completions/%{name}
install -Dm644 _%{name} %{buildroot}%{_datadir}/zsh/site-functions/_%{name}
install -Dm644 %{name}.fish %{buildroot}%{_datadir}/fish/vendor_completions.d/%{name}.fish

install -Dm644 resources/%{name}.service %{buildroot}%{_userunitdir}/%{name}.service
install -Dm644 resources/%{desktop_entry_filename} %{buildroot}%{_datadir}/applications/%{desktop_entry_filename}
install -Dm644 resources/%{name}-settings.svg %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/%{name}-settings.svg

%files
%license LICENSE
%doc README.md docs/config docs/guide
%{_bindir}/%{name}
%{_bindir}/%{name}-settings
%{_datadir}/%{name}/
%{_datadir}/bash-completion/completions/%{name}
%{_datadir}/zsh/site-functions/_%{name}
%{_datadir}/fish/vendor_completions.d/%{name}.fish
%{_userunitdir}/%{name}.service
%{_datadir}/applications/%{desktop_entry_filename}
%{_iconsdir}/hicolor/scalable/apps/%{name}-settings.svg
