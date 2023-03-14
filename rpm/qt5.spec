Name: opt-qt5
Version: 5.15.8
Release: 1%{?dist}
Summary: Qt5 meta package
License: GPLv3
URL: https://getfedora.org/
Source0: %{name}-%{version}.tar.bz2
BuildArch: noarch

Requires: opt-qt5-qdbusviewer
Requires: opt-qt5-qt3d
Requires: opt-qt5-qtbase
Requires: opt-qt5-qtbase-gui
Requires: opt-qt5-qtbase-mysql
Requires: opt-qt5-qtbase-postgresql
Requires: opt-qt5-qtconnectivity
Requires: opt-qt5-qtdeclarative
Requires: opt-qt5-qtdoc
Requires: opt-qt5-qtgraphicaleffects
Requires: opt-qt5-qtimageformats
Requires: opt-qt5-qtlocation
Requires: opt-qt5-qtmultimedia
Requires: opt-qt5-qtquickcontrols
Requires: opt-qt5-qtquickcontrols2
Requires: opt-qt5-qtscript
Requires: opt-qt5-qtsensors
Requires: opt-qt5-qtserialport
Requires: opt-qt5-qtsvg
Requires: opt-qt5-qttools
Requires: opt-qt5-qtwayland
Requires: opt-qt5-qtwebchannel
## qtwebengine is not available on all archs, omit for now
## else, need to make qt5 arch'd and deps conditional (on arch)
#Requires: qt5-qtwebengine
Requires: opt-qt5-qtwebsockets
Requires: opt-qt5-qtx11extras
Requires: opt-qt5-qtxmlpatterns

%description
%{summary}.

%package devel
Summary: Qt5 meta devel package
Requires: opt-qt5-rpm-macros
Requires: opt-qt5-qttools-static
Requires: opt-qt5-qtdeclarative-static
Requires: opt-qt5-qtbase-static
Requires: opt-qt5-designer
Requires: opt-qt5-qdoc
Requires: opt-qt5-qhelpgenerator
Requires: opt-qt5-linguist
Requires: opt-qt5-qt3d-devel
Requires: opt-qt5-qtbase-devel
Requires: opt-qt5-qtconnectivity-devel
Requires: opt-qt5-qtdeclarative-devel
Requires: opt-qt5-qtlocation-devel
Requires: opt-qt5-qtmultimedia-devel
Requires: opt-qt5-qtscript-devel
Requires: opt-qt5-qtsensors-devel
Requires: opt-qt5-qtserialport-devel
Requires: opt-qt5-qtsvg-devel
Requires: opt-qt5-qttools-devel
Requires: opt-qt5-qtwayland-devel
Requires: opt-qt5-qtwebchannel-devel
#Requires: qt5-qtwebengine-devel
Requires: opt-qt5-qtwebsockets-devel
Requires: opt-qt5-qtx11extras-devel
Requires: opt-qt5-qtxmlpatterns-devel

%description devel
%{summary}.

%package rpm-macros
Summary: RPM macros for building Qt5 and KDE Frameworks 5 packages
Conflicts: opt-qt5-qtbase-devel < 5.6.0-0.23
Requires: cmake >= 3
Requires: gcc-c++
%description rpm-macros
%{summary}.

%package srpm-macros
Summary: RPM macros for source Qt5 packages
%description srpm-macros
%{summary}.

%prep
%setup -q

%install
install -Dpm644 macros.qt5 %{buildroot}%{_rpmconfigdir}/macros.d/macros.qt5
install -Dpm644 macros.qt5-srpm %{buildroot}%{_rpmconfigdir}/macros.d/macros.qt5-srpm

# substitute custom flags, and the path to binaries: binaries referenced from
# macros should not change if an application is built with a different prefix.
# %_libdir is left as /usr/%{_lib} (e.g.) so that the resulting macros are
# architecture independent, and don't hardcode /usr/lib or /usr/lib64.
sed -i \
  -e "s|@@QT5_CFLAGS@@|%{?qt5_cflags}|g" \
  -e "s|@@QT5_CXXFLAGS@@|%{?qt5_cxxflags}|g" \
  -e "s|@@QT5_RPM_LD_FLAGS@@|%{?qt5_rpm_ld_flags}|g" \
  -e "s|@@QT5_RPM_OPT_FLAGS@@|%{?qt5_rpm_opt_flags}|g" \
  -e "s|@@QMAKE@@|%{_prefix}/%%{_lib}/qt5/bin/qmake|g" \
  -e "s|@@QMAKE_QT5_WRAPPER@@|%{_bindir}/qmake-qt5.sh|g" \
  %{buildroot}%{_rpmconfigdir}/macros.d/macros.qt5

%if 0%{?metapackage}
mkdir -p %{buildroot}%{_docdir}/qt5
mkdir -p %{buildroot}%{_docdir}/qt5-devel
echo "- Qt5 meta package" > %{buildroot}%{_docdir}/qt5/README
echo "- Qt5 devel meta package" > %{buildroot}%{_docdir}/qt5-devel/README

%files
%{_docdir}/qt5/README

%files devel
%{_docdir}/qt5-devel/README
%endif

%files rpm-macros
%{_rpmconfigdir}/macros.d/macros.qt5

%files srpm-macros
%{_rpmconfigdir}/macros.d/macros.qt5-srpm


%changelog
* Thu Jan 05 2023 Jan Grulich <jgrulich@redhat.com> - 5.15.8-1
- 5.15.8

* Mon Oct 31 2022 Jan Grulich <jgrulich@redhat.com> - 5.15.7-1
- 5.15.7

* Tue Sep 20 2022 Jan Grulich <jgrulich@redhat.com> - 5.15.6-1
- 5.15.6

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 5.15.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jul 13 2022 Jan Grulich <jgrulich@redhat.com> - 5.15.5-1
- 5.15.5

* Mon May 16 2022 Jan Grulich <jgrulich@redhat.com> - 5.15.4-1
- 5.15.4

* Fri Mar 04 2022 Jan Grulich <jgrulich@redhat.com> - 5.15.3-1
- 5.15.3

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 5.15.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 5.15.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 5.15.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Fri Nov 20 08:56:04 CET 2020 Jan Grulich <jgrulich@redhat.com> - 5.15.2-1
- 5.15.2

* Thu Sep 10 2020 Jan Grulich <jgrulich@redhat.com> - 5.15.1-1
- 5.15.1

* Wed Aug 19 2020 Troy Dawson <tdawson@redhat.com> - 5.14.2-5
- fix rpm-macros for RHEL builds

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 5.14.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Apr 06 2020 Rex Dieter <rdieter@fedoraproject.org> - 5.14.2-3
- drop qt5,qt5-devel metapackages f32+

* Mon Apr 06 2020 Rex Dieter <rdieter@fedoraproject.org> - 5.14.2-2
- qt5-devel: drop R: qt5-qtenginio-devel

* Sat Apr 04 2020 Rex Dieter <rdieter@fedoraproject.org> - 5.14.2-1
- 5.14.2
- drop qt5-qtwebkit from metapackage (hasn't been a core qt5 pkg for awhile)

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 5.13.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Dec 09 2019 Jan Grulich <jgrulich@redhat.com> - 5.13.2-1
- 5.13.2

* Tue Sep 24 2019 Jan Grulich <jgrulich@redhat.com> - 5.12.5-1
- 5.12.5

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 5.12.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Jun 11 2019 Jan Grulich <jgrulich@redhat.com> - 5.12.4-1
- 5.12.4

* Tue Jun 04 2019 Jan Grulich <jgrulich@redhat.com> - 5.12.3-1
- 5.12.3

* Thu Feb 14 2019 Rex Dieter <rdieter@fedoraproject.org> - 5.12.1-1
- 5.12.1

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 5.11.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Dec 07 2018 Rex Dieter <rdieter@fedoraproject.org> - 5.11.3-1
- 5.11.3

* Fri Sep 21 2018 Jan Grulich <jgrulich@redhat.com> - 5.11.2-1
- 5.11.2

* Tue Aug 21 2018 Owen Taylor <otaylor@redhat.com> - 5.11.1-4
- rpm-macros: always refer to binaries in their installed location, even if %%_libdir
  and %%_bindir are redefined.

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 5.11.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Jun 29 2018 Rex Dieter <rdieter@fedoraproject.org> - 5.11.1-2
- %%_qt5_prefix=%%_prefix (was %%_libdir/qt5}

* Tue Jun 19 2018 Rex Dieter <rdieter@fedoraproject.org> - 5.11.1-1
- 5.11.1

* Sat Jun 02 2018 Rex Dieter <rdieter@fedoraproject.org> - 5.11.0-2
- rpm-macros: do not define _qt5_archdatadir, _qt5_bindir in terms of _qt5_prefix anymore

* Sat May 26 2018 Rex Dieter <rdieter@fedoraproject.org> - 5.11.0-1
- 5.11.0

* Wed Mar 07 2018 Rex Dieter <rdieter@fedoraproject.org> - 5.10.1-1
- 5.10.1
- rpm-macros: Requires: gcc-c++

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 5.10.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jan 24 2018 Rex Dieter <rdieter@fedoraproject.org> - 5.10.0-4
- macros.qt5: fix path to qmake-qt5.sh wrapper

* Wed Jan 24 2018 Rex Dieter <rdieter@fedoraproject.org> - 5.10.0-3
- use noarch-friendly paths for qmake-qt5.sh wrapper

* Wed Jan 24 2018 Rex Dieter <rdieter@fedoraproject.org> - 5.10.0-2
- provide qmake-qt5.sh wrapper and new macro: %%opt_qmake_qt5_wrapper

* Wed Jan 03 2018 Rex Dieter <rdieter@fedoraproject.org> 5.10.0-1
- 5.10.0

* Wed Jan 03 2018 Rex Dieter <rdieter@fedoraproject.org> 5.9.3-1
- 5.9.3

* Tue Oct 10 2017 Rex Dieter <rdieter@fedoraproject.org> - 5.9.2-1
- 5.9.2

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 5.9.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Jul 19 2017 Rex Dieter <rdieter@fedoraproject.org> - 5.9.1-1
- 5.9.1

* Thu Jun 01 2017 Rex Dieter <rdieter@fedoraproject.org> - 5.9.0-2
- drop -fno-delete-null-pointer-checks hack/workaround

* Sat Apr 15 2017 Helio Chissini de Castro <helio@kde.org> - 5.9.0-1
- Up to match upcoming 5.9.0

* Fri Mar 31 2017 Rex Dieter <rdieter@fedoraproject.org> - 5.8.0-3
- rebuild

* Fri Jan 27 2017 Helio Chissini de Castro <helio@kde.org> - 5.8.0-1
- Tie to new upstream release

* Mon Jan 02 2017 Rex Dieter <rdieter@math.unl.edu> - 5.7.1-2
- drop Requires: qt5-gstreamer qt5-qtacountsservice qt5-qtconfiguration (not from qtproject.org)

* Wed Nov 09 2016 Helio Chissini de Castro <helio@kde.org> - 5.7.1-1
- Prepare for new release

* Tue Sep 27 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.7.0-10
- s/%%rhel/%%epel/ , cmake3 is only available in epel

* Wed Sep 14 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.7.0-9
- install the right macros.qt5-srpm file

* Wed Sep 14 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.7.0-8
- introduce -srpm-macros (initially defines %%qt5_qtwebengine_arches)
- -devel: drop Requires: qt5-qtwebengine-devel (since not all archs are supported)

* Sat Jul 23 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.7.0-7
- drop Requires: qt5-qtwebengine (not available on all archs)

* Tue Jul 12 2016 Helio Chissini de Castro <helio@kde.org> - 5.7.0-6
- Fix macros with invalid substitutions.

* Wed Jul 06 2016 Helio Chissini de Castro <helio@kde.org> - 5.7.0-5
- Fix typo. Thanks to Diego Herrera.
- Add macro qt5_includedir as more logical than headerdir. Old one still available

* Mon Jul 04 2016 Helio Chissini de Castro <helio@kde.org> - 5.7.0-4
- Clang is not default anymore. End of experimentation phase

* Wed Jun 15 2016 Helio Chissini de Castro <helio@kde.org> - 5.7.0-3
- Move package to be qt5 and create meta packages
- Add new macro for qml dir

* Mon Jun 13 2016 Helio Chissini de Castro <helio@kde.org> - 5.7.0-2
- Test repositories using clang by default


* Thu Jun 09 2016 Helio Chissini de Castro <helio@kde.org> - 5.7.0-1
- Decouple macros from main qtbase package




