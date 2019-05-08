# Fedora 27 and newer, no need to build the debug package
%if 0%{?fedora} >= 27 || 0%{?rhel} >= 8
%global debug_package %{nil}
%endif

%global with_python3 1


# Use our interpreter for brp-python-bytecompile script
%global __python %{__pyvenv_root}/bin/python3



Name: ansible
Summary: SSH-based configuration management, deployment, and task execution system
Version: 2.7.1
Release: 1%{?dist}

Group: Development/Libraries
License: GPLv3+
Source0: https://releases.ansible.com/ansible/%{name}-%{version}.tar.gz

# Patch to utilize a newer jinja2 package on epel6
# Non-upstreamable as it creates a dependency on a specific version of jinja.
# This is desirable for us as we have packages for that version but not for
# upstream as they don't know what their customers are running.
Patch100: ansible-newer-jinja.patch

Url: http://ansible.com
BuildArch: x86_64

# This is needed to update the old ansible-fireball package that is no 
# longer needed. Note that you should also remove ansible-node-fireball manually
# Where you still have it installed. 
#
Provides: ansible-fireball = %{version}-%{release}
Obsoletes: ansible-fireball < 1.2.4


BuildRequires: python3-devel
BuildRequires: python3-setuptools
Requires: sshpass



%description
Ansible is a radically simple model-driven configuration management,
multi-node deployment, and remote task execution system. Ansible works
over SSH and does not require any software or daemons to be installed
on remote nodes. Extension modules can be written in any language and
are transferred to managed machines automatically.



%prep
%setup -q


%build
%pyvenv_create
%{__pyvenvpip3} install --upgrade pip
%pyvenv_build


%install
%pyvenv_create
%{__pyvenvpip3} install --upgrade pip
%pyvenv_install
mkdir -p $RPM_BUILD_ROOT/etc/ansible/
mkdir -p $RPM_BUILD_ROOT/etc/ansible/roles/
cp examples/hosts $RPM_BUILD_ROOT/etc/ansible/
cp examples/ansible.cfg $RPM_BUILD_ROOT/etc/ansible/
mkdir -p $RPM_BUILD_ROOT/%{_mandir}/man1
cp -v docs/man/man1/*.1 $RPM_BUILD_ROOT/%{_mandir}/man1/
mkdir -p $RPM_BUILD_ROOT/usr/bin

# Now let us create the symlinks for the executable(s)
for i in %{__pyvenv_root}/bin/ansible* ; do
	ln -s /opt/venvs/%{name}/bin/$(basename $i) $RPM_BUILD_ROOT%{_bindir}/$(basename $i)
done

%files
%config(noreplace) %{_sysconfdir}/ansible/
%doc README.rst PKG-INFO COPYING changelogs/CHANGELOG-v2.7.rst
%doc %{_mandir}/man1/ansible*
/opt/venvs/%{name}/*
%{_bindir}/ansible*

%changelog
* Mon Oct 29 2018 Kevin Fenzi <kevin@scrye.com> - 2.7.1-1
- Update to 2.7.1 and modified for virtualenv

* Thu Oct 04 2018 Kevin Fenzi <kevin@scrye.com> - 2.7.0-1
- Update to 2.7.0

* Fri Sep 28 2018 Kevin Fenzi <kevin@scrye.com> - 2.6.5-1
- Update to 2.6.5.

* Fri Sep 07 2018 Kevin Fenzi <kevin@scrye.com> - 2.6.4-1
- Update to 2.6.4.

* Thu Aug 16 2018 Kevin Fenzi <kevin@scrye.com> - 2.6.3-1
- Upgrade to 2.6.3.

* Sat Jul 28 2018 Kevin Fenzi <kevin@scrye.com> - 2.6.2-1
- Update to 2.6.2. Fixes bug #1609486

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jul 05 2018 Kevin Fenzi <kevin@scrye.com> - 2.6.1-1
- Update to 2.6.1. Fixes bug #1598602
- Fixes CVE-2018-10874 and CVE-2018-10875

* Mon Jul 02 2018 Miro Hrončok <mhroncok@redhat.com> - 2.6.0-2
- Rebuilt for Python 3.7

* Thu Jun 28 2018 Kevin Fenzi <kevin@scrye.com> - 2.6.0-1
- Update to 2.6.0. Fixes bug #1596424

* Tue Jun 26 2018 Miro Hrončok <mhroncok@redhat.com> - 2.5.5-5
- Rebuilt for Python 3.7

* Mon Jun 25 2018 Toshio Kuratomi <toshio@fedoraproject.org> - - 2.5.5-4
- Upstream patch to build docs with older jinja2 (Fedora 27)
- Build changes to build only rst docs for modules and plugins when a distro
  doesn't have modern enough packages to build the documentation. (EPEL7)

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 2.5.5-3
- Rebuilt for Python 3.7

* Fri Jun 15 2018 Kevin Fenzi <kevin@scrye.com> - 2.5.5-2
- Stop building docs on F27 as python-jinja2 is too old there.

* Thu Jun 14 2018 Kevin Fenzi <kevin@scrye.com> - 2.5.5-1
- Update to 2.5.5. Fixes bug #1580530 and #1584927
- Fixes 1588855,1590200 (fedora) and 1588855,1590199 (epel)
  CVE-2018-10855 (security bug with no_log handling)

* Thu May 31 2018 Kevin Fenzi <kevin@scrye.com> - 2.5.4-1
- Update to 2.5.4. Fixes bug #1584927

* Thu May 17 2018 Kevin Fenzi <kevin@scrye.com> - 2.5.3-1
- Update to 2.5.3. Fixes bug #1579577 and #1574221

* Thu Apr 26 2018 Kevin Fenzi <kevin@scrye.com> - 2.5.2-1
- Update to 2.5.2 with bugfixes.

* Wed Apr 18 2018 Kevin Fenzi <kevin@scrye.com> - 2.5.1-1
- Update to 2.5.1 with bugfixes. Fixes: #1569270 #1569153 #1566004 #1566001

* Tue Mar 27 2018 Kevin Fenzi <kevin@scrye.com> - 2.5.0-2
- Some additional python3 fixes. Thanks churchyard!

* Sat Mar 24 2018 Kevin Fenzi <kevin@scrye.com> - 2.5.0-1
- Update to 2.5.0. Fixes bug #1559852
- Spec changes/improvements with tests, docs, and conditionals.

* Fri Mar 16 2018 Miro Hrončok <mhroncok@redhat.com> - 2.4.3.0-3
- Don't build and ship Python 2 bits on EL > 7 and Fedora > 29

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jan 31 2018 Kevin Fenzi <kevin@scrye.com> - 2.4.3.0-1
- Update to 2.4.3. See https://github.com/ansible/ansible/blob/stable-2.4/CHANGELOG.md for full changes.

* Mon Jan 08 2018 Troy Dawson <tdawson@redhat.com> - 2.4.2.0-2
- Update conditional

* Wed Nov 29 2017 Kevin Fenzi <kevin@scrye.com> - 2.4.2.0-1
- Update to 2.4.2. See https://github.com/ansible/ansible/blob/stable-2.4/CHANGELOG.md for full changes.

* Mon Oct 30 2017 Kevin Fenzi kevin@scrye.com - 2.4.1.0-2
- Add PR to conditionalize docs building. Thanks tibbs!
- Fix up el6 patches

* Thu Oct 26 2017 Kevin Fenzi <kevin@scrye.com> - 2.4.1.0-1
- Update to 2.4.1

* Thu Oct 12 2017 Toshio Kuratomi <toshio@fedoraproject.org> - - 2.4.0.0-3
- Fix Python3 subpackage to symlink to the python3 versions of the scripts
  instead of the python2 version

* Mon Sep 25 2017 Kevin Fenzi <kevin@scrye.com> - 2.4.0.0-2
- Rebase rhel6 jinja2 patch.
- Conditionalize jmespath to work around amazon linux issues. Fixes bug #1494640

* Tue Sep 19 2017 Kevin Fenzi <kevin@scrye.com> - 2.4.0.0-1
- Update to 2.4.0. 

* Tue Aug 08 2017 Kevin Fenzi <kevin@scrye.com> - 2.3.2.0-1
- Update to 2.3.2. Fixes bugs #1471017 #1461116 #1465586

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu Jun 01 2017 Kevin Fenzi <kevin@scrye.com> - 2.3.1.0-1
- Update to 2.3.1.0.

* Wed Apr 19 2017 James Hogarth <james.hogarth@gmail.com> - 2.3.0.0-3
- Update backported patch to the one actually merged upstream

* Wed Apr 19 2017 James Hogarth <james.hogarth@gmail.com> - 2.3.0.0-2
- Backport hotfix to fix ansible-galaxy regression https://github.com/ansible/ansible/issues/22572

* Wed Apr 12 2017 Toshio Kuratomi <toshio@fedoraproject.org> - 2.3.0.0-1
- Update to 2.3.0
- Remove upstreamed patches
- Remove controlpersist socket path path as a custom solution was included
  upstream
- Run the unittests from the upstream tarball now instead of having to download
  separately
- Build a documentation subpackage

* Tue Mar 28 2017 Kevin Fenzi <kevin@scrye.com> - 2.2.2.0-3
- Deal with RHEL7 pytest vs python-pytest.
- Rebase epel6 newer jinja patch.
- Conditionalize exclude for RHEL6 rpm.

* Tue Mar 28 2017 Kevin Fenzi <kevin@scrye.com> - 2.2.2.0-2
- Conditionalize python3 files for epel builds.

* Tue Mar 28 2017 Toshio Kuratomi <toshio@fedoraproject.org> - - 2.2.2.0-1
- 2.2.2.0 final
- Add new patch to fix unittests

* Mon Mar 27 2017 Toshio Kuratomi <toshio@fedoraproject.org> - - 2.2.2.0-0.4.rc1
- Add python-crypto and python3-crypto as explicit requirements

* Mon Mar 27 2017 Toshio Kuratomi <toshio@fedoraproject.org> - - 2.2.2.0-0.3.rc1
- Add a symlink for ansible executables to be accessed via python major version
  (ie: ansible-3) in addition to python-major-minor (ansible-3.6)

* Wed Mar  8 2017 Toshio Kuratomi <toshio@fedoraproject.org> - - 2.2.2.0-0.2.rc1
- Add a python3 ansible package.  Note that upstream doesn't intend for the library
  to be used by third parties so this is really just for the executables.  It's not
  strictly required that the executables be built for both python2 and python3 but
  we do need to get testing of the python3 version to know if it's stable enough to
  go into the next Fedora.  We also want the python2 version available in case a user
  has to get something done and the python3 version is too buggy.
- Fix Ansible cli scripts to handle appended python version

* Wed Feb 22 2017 Kevin Fenzi <kevin@scrye.com> - 2.2.2.0-0.1.rc1
- Update to 2.2.2.0 rc1. Fixes bug #1421485

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Jan 16 2017 Kevin Fenzi <kevin@scrye.com> - 2.2.1.0-1
- Update to 2.2.1.
- Fixes: CVE-2016-9587 CVE-2016-8647 CVE-2016-9587 CVE-2016-8647
- Fixes bug #1405110

* Wed Nov 09 2016 Kevin Fenzi <kevin@scrye.com> - 2.2.0.0-3
- Update unit tests that will skip docker related tests if docker isn't available.
- Drop docker BuildRequires. Fixes bug #1392918

* Fri Nov  4 2016 Toshio Kuratomi <toshio@fedoraproject.org> - - 2.2.0.0-3
- Fix for dnf group install

* Tue Nov 01 2016 Kevin Fenzi <kevin@scrye.com> - 2.2.0.0-2
- Fix some BuildRequires to work on all branches.

* Tue Nov 01 2016 Kevin Fenzi <kevin@scrye.com> - 2.2.0.0-1
- Update to 2.2.0. Fixes #1390564 #1388531 #1387621 #1381538 #1388113 #1390646 #1388038 #1390650
- Fixes for CVE-2016-8628 CVE-2016-8614 CVE-2016-8628 CVE-2016-8614

* Thu Sep 29 2016 Kevin Fenzi <kevin@scrye.com> - 2.1.2.0-1
- Update to 2.1.2

* Thu Jul 28 2016 Kevin Fenzi <kevin@scrye.com> - 2.1.1.0-1
- Update to 2.1.1

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.0.0-3
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Wed Jun 15 2016 Matt Domsch <matt@domsch.com> - 2.1.0.0-2
- Force python 2.6 on EL6

* Wed May 25 2016 Kevin Fenzi <kevin@scrye.com> - 2.1.0.0-1
- Update to 2.1.0.0.
- Fixes: 1334097 1337474 1332233 1336266

* Tue Apr 19 2016 Kevin Fenzi <kevin@scrye.com> - 2.0.2.0-1
- Update to 2.0.2.0. https://github.com/ansible/ansible/blob/stable-2.0/CHANGELOG.md
- Fixes CVE-2016-3096
- Fix for failed to resolve remote temporary directory issue. bug #1328359

* Thu Feb 25 2016 Toshio Kuratomi <toshio@fedoraproject.org> - 2.0.1.0-2
- Patch control_path to be not hit path length limitations (RH BZ #1311729)
- Version the test tarball

* Thu Feb 25 2016 Toshio Kuratomi <toshio@fedoraproject.org> - 2.0.1.0-1
- Update to upstream bugfix for 2.0.x release series.

* Thu Feb  4 2016 Toshio Kuratomi <toshio@fedoraproject.org> - - 2.0.0.2-3
- Utilize the python-jinja26 package on EPEL6

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jan 14 2016 Toshio Kuratomi <toshio@fedoraproject.org> - - 2.0.0.2-1
- Ansible 2.0.0.2 release from upstream.  (Minor bugfix to one callback plugin
  API).

* Tue Jan 12 2016 Toshio Kuratomi <toshio@fedoraproject.org> - 2.0.0.1-1
- Ansible 2.0.0.1 from upstream.  Rewrite with many bugfixes, rewritten code,
  and new features. See the upstream changelog for details:
  https://github.com/ansible/ansible/blob/devel/CHANGELOG.md

* Wed Oct 14 2015 Adam Williamson <awilliam@redhat.com> - 1.9.4-2
- backport upstream fix for GH #2043 (crash when pulling Docker images)

* Fri Oct 09 2015 Kevin Fenzi <kevin@scrye.com> 1.9.4-1
- Update to 1.9.4

* Sun Oct 04 2015 Kevin Fenzi <kevin@scrye.com> 1.9.3-3
- Backport dnf module from head. Fixes bug #1267018

* Tue Sep  8 2015 Toshio Kuratomi <toshio@fedoraproject.org> - 1.9.3-2
- Pull in patch for yum module that fixes state=latest issue

* Thu Sep 03 2015 Kevin Fenzi <kevin@scrye.com> 1.9.3-1
- Update to 1.9.3
- Patch dnf as package manager. Fixes bug #1258080
- Fixes bug #1251392 (in 1.9.3 release)
- Add requires for sshpass package. Fixes bug #1258799

* Thu Jun 25 2015 Kevin Fenzi <kevin@scrye.com> 1.9.2-1
- Update to 1.9.2

* Tue Jun 16 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed May 27 2015 Toshio Kuratomi <toshio@fedoraproject.org> - 1.9.1-2
- Fix for dnf

* Tue Apr 28 2015 Kevin Fenzi <kevin@scrye.com> 1.9.1-1
- Update to 1.9.1

* Wed Mar 25 2015 Kevin Fenzi <kevin@scrye.com> 1.9.0.1-2
- Drop upstreamed epel6 patches. 

* Wed Mar 25 2015 Kevin Fenzi <kevin@scrye.com> 1.9.0.1-1
- Update to 1.9.0.1

* Wed Mar 25 2015 Kevin Fenzi <kevin@scrye.com> 1.9.0-1
- Update to 1.9.0

* Thu Feb 19 2015 Kevin Fenzi <kevin@scrye.com> 1.8.4-1
- Update to 1.8.4

* Tue Feb 17 2015 Kevin Fenzi <kevin@scrye.com> 1.8.3-1
- Update to 1.8.3

* Sun Jan 11 2015 Toshio Kuratomi <toshio@fedoraproject.org> - 1.8.2-3
- Work around a bug in python2.6 by using simplejson (applies in EPEL6)

* Wed Dec 17 2014 Michael Scherer <misc@zarb.org> 1.8.2-2
- precreate /etc/ansible/roles and /usr/share/ansible_plugins

* Sun Dec 07 2014 Kevin Fenzi <kevin@scrye.com> 1.8.2-1
- Update to 1.8.2

* Thu Nov 27 2014 Kevin Fenzi <kevin@scrye.com> 1.8.1-1
- Update to 1.8.1

* Tue Nov 25 2014 Kevin Fenzi <kevin@scrye.com> 1.8-2
- Rebase el6 patch

* Tue Nov 25 2014 Kevin Fenzi <kevin@scrye.com> 1.8-1
- Update to 1.8

* Thu Oct  9 2014 Toshio Kuratomi <toshio@fedoraproject.org> - 1.7.2-2
- Add /usr/bin/ansible to the rhel6 newer pycrypto patch

* Wed Sep 24 2014 Kevin Fenzi <kevin@scrye.com> 1.7.2-1
- Update to 1.7.2

* Thu Aug 14 2014 Kevin Fenzi <kevin@scrye.com> 1.7.1-1
- Update to 1.7.1

* Wed Aug 06 2014 Kevin Fenzi <kevin@scrye.com> 1.7-1
- Update to 1.7

* Fri Jul 25 2014 Kevin Fenzi <kevin@scrye.com> 1.6.10-1
- Update to 1.6.10

* Thu Jul 24 2014 Kevin Fenzi <kevin@scrye.com> 1.6.9-1
- Update to 1.6.9 with more shell quoting fixes.

* Tue Jul 22 2014 Kevin Fenzi <kevin@scrye.com> 1.6.8-1
- Update to 1.6.8 with fixes for shell quoting from previous release. 
- Fixes bugs #1122060 #1122061 #1122062

* Mon Jul 21 2014 Kevin Fenzi <kevin@scrye.com> 1.6.7-1
- Update to 1.6.7
- Fixes CVE-2014-4966 and CVE-2014-4967

* Tue Jul 01 2014 Kevin Fenzi <kevin@scrye.com> 1.6.6-1
- Update to 1.6.6

* Wed Jun 25 2014 Kevin Fenzi <kevin@scrye.com> 1.6.5-1
- Update to 1.6.5

* Wed Jun 25 2014 Kevin Fenzi <kevin@scrye.com> 1.6.4-1
- Update to 1.6.4

* Mon Jun 09 2014 Kevin Fenzi <kevin@scrye.com> 1.6.3-1
- Update to 1.6.3

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri May 23 2014 Kevin Fenzi <kevin@scrye.com> 1.6.2-1
- Update to 1.6.2 release

* Wed May  7 2014 Toshio Kuratomi <toshio@fedoraproject.org> - 1.6.1-1
- Bugfix 1.6.1 release

* Mon May  5 2014 Toshio Kuratomi <toshio@fedoraproject.org> - 1.6-1
- Update to 1.6
- Drop accelerate fix, merged upstream
- Refresh RHEL6 pycrypto patch.  It was half-merged upstream.

* Fri Apr 18 2014 Kevin Fenzi <kevin@scrye.com> 1.5.5-1
- Update to 1.5.5

* Mon Apr  7 2014 Toshio Kuratomi <toshio@fedoraproject.org> - 1.5.4-2
- Fix setuptools requirement to apply to rhel=6, not rhel<6

* Wed Apr  2 2014 Toshio Kuratomi <toshio@fedoraproject.org> - 1.5.4-1
- Update to 1.5.4
- Add upstream patch to fix accelerator mode
- Merge fedora and el6 spec files

* Fri Mar 14 2014 Kevin Fenzi <kevin@scrye.com> 1.5.3-2
- Update to NEW 1.5.3 upstream release.
- Add missing dependency on python-setuptools (el6 build)

* Thu Mar 13 2014 Kevin Fenzi <kevin@scrye.com> 1.5.3-1
- Update to 1.5.3
- Fix ansible-vault for newer python-crypto dependency (el6 build)

* Tue Mar 11 2014 Kevin Fenzi <kevin@scrye.com> 1.5.2-2
- Update to redone 1.5.2 release

* Tue Mar 11 2014 Kevin Fenzi <kevin@scrye.com> 1.5.2-1
- Update to 1.5.2

* Mon Mar 10 2014 Kevin Fenzi <kevin@scrye.com> 1.5.1-1
- Update to 1.5.1

* Fri Feb 28 2014 Kevin Fenzi <kevin@scrye.com> 1.5-1
- Update to 1.5

* Wed Feb 12 2014 Kevin Fenzi <kevin@scrye.com> 1.4.5-1
- Update to 1.4.5

* Sat Dec 28 2013 Kevin Fenzi <kevin@scrye.com> 1.4.3-1
- Update to 1.4.3 with ansible galaxy commands.
- Adds python-httplib2 to requires

* Wed Nov 27 2013 Kevin Fenzi <kevin@scrye.com> 1.4.1-1
- Update to upstream 1.4.1 bugfix release

* Thu Nov 21 2013 Kevin Fenzi <kevin@scrye.com> 1.4-1
- Update to 1.4

* Tue Oct 29 2013 Kevin Fenzi <kevin@scrye.com> 1.3.4-1
- Update to 1.3.4

* Tue Oct 08 2013 Kevin Fenzi <kevin@scrye.com> 1.3.3-1
- Update to 1.3.3

* Thu Sep 19 2013 Kevin Fenzi <kevin@scrye.com> 1.3.2-1
- Update to 1.3.2 with minor upstream fixes

* Mon Sep 16 2013 Kevin Fenzi <kevin@scrye.com> 1.3.1-1
- Update to 1.3.1

* Sat Sep 14 2013 Kevin Fenzi <kevin@scrye.com> 1.3.0-2
- Merge upstream spec changes to support EPEL5
- (Still needs python26-keyczar and deps added to EPEL)

* Thu Sep 12 2013 Kevin Fenzi <kevin@scrye.com> 1.3.0-1
- Update to 1.3.0
- Drop node-fireball subpackage entirely.
- Obsolete/provide fireball subpackage. 
- Add Requires python-keyczar on main package for accelerated mode.

* Wed Aug 21 2013 Kevin Fenzi <kevin@scrye.com> 1.2.3-2
- Update to 1.2.3
- Fixes CVE-2013-4260 and CVE-2013-4259

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sat Jul 06 2013 Kevin Fenzi <kevin@scrye.com> 1.2.2-1
- Update to 1.2.2 with minor fixes

* Fri Jul 05 2013 Kevin Fenzi <kevin@scrye.com> 1.2.1-2
- Update to newer upstream re-release to fix a syntax error

* Thu Jul 04 2013 Kevin Fenzi <kevin@scrye.com> 1.2.1-1
- Update to 1.2.1
- Fixes CVE-2013-2233

* Mon Jun 10 2013 Kevin Fenzi <kevin@scrye.com> 1.2-1
- Update to 1.2

* Tue Apr 02 2013 Kevin Fenzi <kevin@scrye.com> 1.1-1
- Update to 1.1

* Mon Mar 18 2013 Kevin Fenzi <kevin@scrye.com> 1.0-1
- Update to 1.0

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Nov 30 2012 Michael DeHaan <michael.dehaan@gmail.com> - 0.9-0
- Release 0.9

* Fri Oct 19 2012 Michael DeHaan <michael.dehaan@gmail.com> - 0.8-0
- Release of 0.8

* Thu Aug 9 2012 Michael DeHaan <michael.dehaan@gmail.com> - 0.7-0
- Release of 0.7

* Mon Aug 6 2012 Michael DeHaan <michael.dehaan@gmail.com> - 0.6-0
- Release of 0.6

* Wed Jul 4 2012 Michael DeHaan <michael.dehaan@gmail.com> - 0.5-0
- Release of 0.5

* Wed May 23 2012 Michael DeHaan <michael.dehaan@gmail.com> - 0.4-0
- Release of 0.4

* Mon Apr 23 2012 Michael DeHaan <michael.dehaan@gmail.com> - 0.3-1
- Release of 0.3

* Tue Apr  3 2012 John Eckersberg <jeckersb@redhat.com> - 0.0.2-1
- Release of 0.0.2

* Sat Mar 10 2012  <tbielawa@redhat.com> - 0.0.1-1
- Release of 0.0.1
