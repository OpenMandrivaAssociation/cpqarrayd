Summary:	Monitors SmartArray controllers and notifies via SNMP and syslog
Name:		cpqarrayd
Version:	2.3
Release:	21
License:	GPL
Group:		System/Servers
URL:		https://www.strocamp.net/opensource/
Source0:	http://www.strocamp.net/opensource/compaq/downloads/%{name}-%{version}.tar.bz2
Patch0:		cpqarrayd-2.3.no_ida.patch
Patch1:		cpqarrayd-2.3-message-overrun.patch
Patch2:		cpqarrayd-2.3-fix-str-fmt.patch
Patch3:		cpqarrayd-2.3-automake-1.13.patch

BuildRequires:	kernel-source
BuildRequires:	libtool
BuildRequires:	net-snmp-devel
BuildRequires:	pkgconfig(openssl)
Requires:	net-snmp
Requires(post,preun):	rpm-helper

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
%autopatch -p1
chmod 644 AUTHORS ChangeLog NEWS README

%build
rm -rf .deps
rm -f configure
autoreconf -fiv

%configure2_5x \
	--with-kernel=/usr/src/linux

%make

%install
install -d %{buildroot}%{_initrddir}
install -d %{buildroot}%{_sysconfdir}/sysconfig

%makeinstall

sed -i -e 's:\@installroot\@:%{prefix}:;' scripts/cpqarrayd

install -m0755 scripts/cpqarrayd %{buildroot}%{_initrddir}
install scripts/cpqarrayd.sysconfig %{buildroot}%{_sysconfdir}/sysconfig/cpqarrayd

%post
%_post_service cpqarrayd

%preun
%_preun_service cpqarrayd

%files
%doc AUTHORS ChangeLog NEWS README
%attr(0755,root,root) %{_initrddir}/cpqarrayd
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/sysconfig/cpqarrayd
%{_sbindir}/cpqarrayd
%{_mandir}/man1/cpqarrayd.1*

