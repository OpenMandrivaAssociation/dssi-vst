%define name            dssi-vst
%define version         0.9
%define release         %mkrel 1

Name:           %{name}
Summary:        DSSI and LADSPA plugin wrapper for VST plugins
Version:        %{version}
Release:        %{release}
Source0:        http://code.breakfastquay.com/attachments/download/2/%{name}-%{version}.tar.bz2
Patch0:         %{name}-0.8-cstdio.patch
URL:            http://breakfastquay.com/dssi-vst/
ExclusiveArch:  %{ix86} x86_64

License:        GPLv2
Group:          Sound
BuildRequires:  liblo-devel
BuildRequires:  libstdc++-devel
BuildRequires:  alsa-lib-devel
BuildRequires:  dssi-devel
BuildRequires:  ladspa-devel
BuildRequires:  libjack-devel

Requires:       dssi

# From Fedora: The -wine subpackage will only be built on ix86
%ifarch %{ix86}
BuildRequires: wine-devel
%endif

# Both packages depend on each other
Requires:      %{name}-wine = %{version}-%{release}

%description
dssi-vst enables any compliant DSSI or LADSPA host to use VST instruments
and effects as plugins. They will recognize VSTs placed in the user's

myhome/plugins/win32-vst

Note:
x86_64 users also need the dssi-vst-wine package from the i586 contrib
repository.

'VST is a trademark of Steinberg Media Technologies GmbH'

However, this library does not use VST headers, and is absolutely free.

#=====================================
# From Fedora: The -wine subpackage will only be built on i586
%ifarch %{ix86}
%package wine
Summary:       VST plugins wrapper
Group:         System/Libraries
Requires:      %{name} = %{version}-%{release}

%description wine
This package provides two 32bit executables necessary for using dssi-vst
even on 64bit platforms.
dssi-vst enables any compliant DSSI or LADSPA host to use VST instruments
and effects as plugins. They will recognize VSTs placed in the user's

myhome/plugins/win32-vst

'VST is a trademark of Steinberg Media Technologies GmbH'

However, this library does not use VST headers, and is absolutely free.


%files wine
%defattr(-,root,root,-)
%dir %{_libdir}/dssi/
%dir %{_libdir}/dssi/%{name}/
%{_libdir}/dssi/%{name}/%{name}-scanner*
%{_libdir}/dssi/%{name}/%{name}-server*

%endif

#=====================================

%prep
%setup -q -n %{name}
%patch0 -p1

%build

%ifarch %{ix86}
#build all targets only on i586
%make CXXFLAGS="-O3 -fPIC -Ivestige"

%if %mdkversion > 200900
# correct executable filenames if wineg++ >= 4.3
mv dssi-vst-server.exe dssi-vst-server
mv dssi-vst-scanner.exe dssi-vst-scanner
%endif

%else
# From Fedora: On x86_64, build non-wine parts only:
make \
     dssi-vst.so vsthost dssi-vst_gui \
    CXXFLAGS="-O3 -fPIC -Ivestige"
%endif

%install
rm -rf %{buildroot}
%ifarch %{ix86}
make  DSSIDIR=%{buildroot}%{_libdir}/dssi   \
    LADSPADIR=%{buildroot}%{_libdir}/ladspa \
       BINDIR=%{buildroot}%{_bindir}        \
    install
rm -f %{buildroot}%{_libdir}/ladspa/*
%else
mkdir -p %{buildroot}%{_libdir}/dssi/%{name} \
         %{buildroot}%{_bindir}              \
         %{buildroot}%{_libdir}/ladspa
install -pm 755 vsthost %{buildroot}%{_bindir}
install -pm 755 %{name}.so %{buildroot}%{_libdir}/dssi/
install -pm 755 %{name}_gui %{buildroot}%{_libdir}/dssi/%{name}/
%endif
ln -s ../dssi/%{name}.so %{buildroot}%{_libdir}/ladspa

install -d -m 755 %{buildroot}%{_sysconfdir}/profile.d

#prepare VST_PATH definition in user profile 
cat > %{buildroot}%{_sysconfdir}/profile.d/%{name}.csh << EOF
# Set VST_PATH for csh
if ( \${?VST_PATH} ) then
   exit
endif
setenv VST_PATH \$HOME/plugins/win32-vst
EOF

cat > %{buildroot}%{_sysconfdir}/profile.d/%{name}.sh << EOF
# Set VST_PATH for Bash shell
if [ -n "\$VST_PATH" ]; then
   export VST_PATH="\$HOME/plugins/win32-vst"
fi
EOF

# add 32bit dssi path on x86_64 systems to find wine executables

%ifarch %{ix86}
%else
cat  > %{buildroot}%{_sysconfdir}/profile.d/%{name}.csh << EOF
setenv DSSI_PATH \$DSSI_PATH:/usr/lib/dssi
EOF
cat  > %{buildroot}%{_sysconfdir}/profile.d/%{name}.sh << EOF
export DSSI_PATH="\$DSSI_PATH:/usr/lib/dssi"
EOF
%endif


%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc README
%{_bindir}/*
%{_libdir}/dssi/%{name}.so
%{_libdir}/dssi/%{name}/
%{_libdir}/ladspa/%{name}.so
%config(noreplace) %attr(644,root,root) %{_sysconfdir}/profile.d/dssi-vst.sh
%config(noreplace) %attr(644,root,root) %{_sysconfdir}/profile.d/dssi-vst.csh

