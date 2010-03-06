%define name            dssi-vst
%define version         0.8
%define release         %mkrel 1

%define major 0
%define libname %mklibname %{name} %{major}

Name:           %{name}
Summary:        DSSI and LADSPA plugin wrapper for VST plugins
Version:        %{version}
Release:        %{release}
Source0:        http://downloads.sourceforge.net/project/dssi/dssi-vst/0.8/%{name}-%{version}.tar.gz
Source1:        dssi-vst-loader
Patch0:         %{name}-0.8-cstdio.patch
URL:            http://breakfastquay.com/dssi-vst/

License:        GPLv2
Group:          Sound
BuildRequires:  libwine-devel >= 1.1
BuildRequires:  liblo-devel >= 0.26
BuildRequires:  libstdc++-devel
BuildRequires:  alsa-lib-devel >= 1.0
BuildRequires:  dssi-devel
BuildRequires:  ladspa-devel
BuildRequires:  libjack-devel

Requires:       %{libname} >= %{version}

%description
dssi-vst enables any compliant DSSI or LADSPA host to use VST instruments
and effects as plugins. They will recognize VSTs placed in the user's

myhome/plugins/win32-vst

'VST is a trademark of Steinberg Media Technologies GmbH'

However, this library does not use VST headers, and is absolutely free.

#=====================================
%package -n %{libname}
Summary:    permits using windows VST audio plugins as DSSI plugins
License:    GPL
Group:      System/Libraries
Requires:   wine >= 1.1,libwine1 >= 1.1
Provides:   lib%{name} = %{version}

%description -n %{libname}
This library can be used by programs to run windows VST audio plugins 
under linux as LADSPA or DSSI plugins.
'VST is a trademark of Steinberg Media Technologies GmbH'

However, this library does not use VST headers, and is absolutely free.

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/dssi/*
%{_libdir}/ladspa/%{name}.so

#=====================================

%prep
%setup -q -n %{name}-%{version}
%patch0 -p1

%build
make \
    DSSIDIR=%{_libdir}/dssi \
    BINDIR=%{_bindir} \
    LADSPADIR=%{_libdir}/ladspa \
    CXXFLAGS=-I./vestige 

# correct executable filenames if wineg++ >= 4.3
%if %mdkversion > 200900
mv dssi-vst-server.exe dssi-vst-server
mv dssi-vst-scanner.exe dssi-vst-scanner
%endif

%install
rm -rf %{buildroot}
make install \
    DESTDIR=%{buildroot} \
    DSSIDIR=%{buildroot}%{_libdir}/dssi \
    LADSPADIR=%{buildroot}%{_libdir}/ladspa \
    BINDIR=%{buildroot}%{_bindir} \

%__strip %{buildroot}%{_libdir}/dssi/%{name}/*.so
%__strip %{buildroot}%{_libdir}/dssi/%{name}/dssi-vst_gui
%__strip %{buildroot}%{_libdir}/dssi/%{name}.so
%__strip %{buildroot}%{_libdir}/ladspa/%{name}.so

install -d %buildroot/%{_bindir}/
install -m 755 runvst.sh %buildroot/%{_libdir}/dssi/%{name}/runvst.sh
install -m 755 %{SOURCE1} %buildroot/%{_bindir}/dssi-vst-loader

chmod 755 %buildroot%{_bindir}/dssi-vst-loader

install -d -m 755 %{buildroot}%{_sysconfdir}/profile.d

#prepare VST_PATH definition in user profile 
cat > %{buildroot}%{_sysconfdir}/profile.d/%{name}.csh << EOF
# Set VST_PATH for csh
if ( \${?VST_PATH} ) then
   exit
endif
setenv VST_PATH $HOME/plugins/win32-vst
EOF

cat > %{buildroot}%{_sysconfdir}/profile.d/%{name}.sh << EOF
# Set VST_PATH for Bash shell
if [ -n "\$VST_PATH" ]; then
   export VST_PATH="$HOME/plugins/win32-vst"
fi
EOF

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,0755)
%doc README
%{_bindir}/*
%config(noreplace) %attr(755,root,root) %{_sysconfdir}/profile.d/dssi-vst.sh
%config(noreplace) %attr(755,root,root) %{_sysconfdir}/profile.d/dssi-vst.csh
