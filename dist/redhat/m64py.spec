%define name m64py
%define version 0.1.0
%define unmangled_version 0.1.0
%define release 1

Summary: M64Py - A frontend for Mupen64Plus
Name: %{name}
Version: %{version}
Release: %{release}
Source0: %{name}-%{unmangled_version}.tar.gz
License: GNU GPLv3
Group: Games/Emulator
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Prefix: %{_prefix}
BuildArch: noarch
Vendor: Milan Nikolic <gen2brain@gmail.com>
Url: http://m64py.sourceforge.net
Requires: PyQt4 SDL

%description
M64Py is a Qt4 front-end (GUI) for Mupen64Plus 2.0, a cross-platform plugin-based Nintendo 64 emulator.

%prep
%setup -n %{name}-%{unmangled_version}

%build
python setup.py build

%install
python setup.py install -O1 --root=$RPM_BUILD_ROOT --record=INSTALLED_FILES

%clean
rm -rf $RPM_BUILD_ROOT

%files -f INSTALLED_FILES
%defattr(-,root,root)
