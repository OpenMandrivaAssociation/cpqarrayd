Summary:	Monitors SmartArray controllers and notifies via SNMP and syslog
Name:		cpqarrayd
Version:	2.3
Release:	%mkrel 11
License:	GPL
Group:		System/Servers
URL:		http://www.strocamp.net/opensource/
Source0:	http://www.strocamp.net/opensource/compaq/downloads/%{name}-%{version}.tar.bz2
Patch0:		cpqarrayd-2.3.no_ida.patch
Patch1:		cpqarrayd-2.3-message-overrun.patch
Patch2:		cpqarrayd-2.3-fix-str-fmt.patch
Requires(post): rpm-helper
Requires(preun): rpm-helper
Requires:	net-snmp
BuildRequires:	net-snmp-devel
BuildRequires:	openssl-devel
BuildRequires:	kernel-source
BuildRequires:	libtool
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
This tool can run on a linux based intel box with a smart array controller from
Compaq. It reports status changes in the disks both to the syslog and to a snmp
trap host. The default is to only log to the syslog. You can specify traphosts
with the -t parameter at the commandline. Multiple traphosts are allowed. It
checks for valid input, but any errors are non-fatal, in fact the traphost is
just ignored. To ensure correct opereration compile it for the same kernel that
runs on the machine where you want to use this. At least make sure that the
version of the SmartArray driver is the same. Strange things can happen
otherwise.

%prep

%setup -q
%patch0 -p1 -b .no_ida
%patch1 -p1 -b .message-overrun
%patch2 -p0

chmod 644 AUTHORS ChangeLog NEWS README

%build
rm -rf .deps
rm -f configure
#libtoolize --force --copy; aclocal; autoheader; automake --add-missing --copy --foreign; autoconf
autoreconf -fiv

%configure2_5x \
    --with-kernel=/usr/src/linux

%make

%install
rm -rf %{buildroot}

install -d %{buildroot}%{_initrddir}
install -d %{buildroot}%{_sysconfdir}/sysconfig

%makeinstall

perl -i -p -e 's:\@installroot\@:%{prefix}:;' scripts/cpqarrayd

install -m0755 scripts/cpqarrayd %{buildroot}%{_initrddir}
install scripts/cpqarrayd.sysconfig %{buildroot}%{_sysconfdir}/sysconfig/cpqarrayd

%post
%_post_service cpqarrayd

%preun
%_preun_service cpqarrayd

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc AUTHORS ChangeLog NEWS README
%attr(0755,root,root) %{_initrddir}/cpqarrayd
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/sysconfig/cpqarrayd
%{_sbindir}/cpqarrayd
%{_mandir}/man1/cpqarrayd.1*


%changelog
* Tue May 03 2011 Oden Eriksson <oeriksson@mandriva.com> 2.3-9mdv2011.0
+ Revision: 663406
- mass rebuild

* Sun Mar 14 2010 Oden Eriksson <oeriksson@mandriva.com> 2.3-8mdv2011.0
+ Revision: 518991
- rebuild

* Fri Oct 16 2009 Oden Eriksson <oeriksson@mandriva.com> 2.3-7mdv2010.0
+ Revision: 457882
- sync with cpqarrayd-2.3-12.fc12.src.rpm
- rediffed cpqarrayd-2.3-fix-str-fmt.patch
- rebuilt against new net-snmp libs

* Sun Aug 09 2009 Oden Eriksson <oeriksson@mandriva.com> 2.3-5mdv2010.0
+ Revision: 413269
- rebuild

* Sun Mar 08 2009 Emmanuel Andry <eandry@mandriva.org> 2.3-4mdv2009.1
+ Revision: 352714
- diff p0 to fix string format not literal
- use autoreconf and configure2_5x

  + Antoine Ginies <aginies@mandriva.com>
    - rebuild

* Thu Sep 11 2008 Oden Eriksson <oeriksson@mandriva.com> 2.3-3mdv2009.0
+ Revision: 283799
- fix #41350 (cpqarrayd: useless description, documentation files only readable for root)

* Mon Jun 16 2008 Thierry Vignaud <tv@mandriva.org> 2.3-2mdv2009.0
+ Revision: 220511
- rebuild
- kill re-definition of %%buildroot on Pixel's request

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

* Sat Dec 15 2007 Emmanuel Andry <eandry@mandriva.org> 2.3-1mdv2008.1
+ Revision: 120400
- New version
- drop patch0 (applied upstream)

* Wed Aug 08 2007 Oden Eriksson <oeriksson@mandriva.com> 2.2-7mdv2008.0
+ Revision: 60199
- rebuilt against new net-snmp libs

* Wed Jun 20 2007 Adam Williamson <awilliamson@mandriva.org> 2.2-6mdv2008.0
+ Revision: 41942
- even uglier
- try it a different way
- buildconflicts kernel-source-stripped to fix build
- update autoconf buildrequire; rebuild for 2008


* Sat Jul 29 2006 Oden Eriksson <oeriksson@mandriva.com> 2.2-5mdv2007.0
- rebuild
- use %%mkrel
- fix url and deps

* Wed Jan 04 2006 Oden Eriksson <oeriksson@mandriva.com> 2.2-4mdk
- rebuilt against new net-snmp with new major (10)

* Wed Dec 21 2005 Oden Eriksson <oeriksson@mandriva.com> 2.2-3mdk
- rebuilt against net-snmp that has new major (9)

* Mon Nov 14 2005 Oden Eriksson <oeriksson@mandriva.com> 2.2-2mdk
- rebuilt against openssl-0.9.8a

* Mon Oct 24 2005 Oden Eriksson <oeriksson@mandriva.com> 2.2-1mdk
- 2.2
- added rediffed P0 from debian

* Tue May 24 2005 Christiaan Welvaart <cjw@daneel.dyndns.org> 2.0-4mdk
- add BuildRequires: kernel-source libopenssl-devel

* Tue May 10 2005 Oden Eriksson <oeriksson@mandriva.com> 2.0-3mdk
- rpmlint fixes

* Tue May 10 2005 Oden Eriksson <oeriksson@mandriva.com> 2.0-2mdk
- added P0 from debian to make it compile on x86_64

* Tue Jul 13 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 2.0-1mdk
- initial mandrake package, used parts from the provided spec file

