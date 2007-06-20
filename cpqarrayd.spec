%define name	cpqarrayd
%define version	2.2
%define release %mkrel 6

Summary:	Monitors SmartArray controllers and notifies via SNMP and syslog
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		System/Servers
URL:		http://www.strocamp.net/opensource/
Source0:	http://www.strocamp.net/opensource/compaq/downloads/%{name}-%{version}.tar.bz2
Patch0:		cpqarrayd-2.2-debian.diff
Requires(post): rpm-helper
Requires(preun): rpm-helper
Requires:	net-snmp
BuildRequires:	net-snmp-devel
BuildRequires:	libopenssl-devel
# This is a hack to force the use of kernel-source rather than
# kernel-source-stripped. Should be replaced by something more elegant
# once kernel provides are saner. -AdamW 2007/06
BuildRequires:	kernel-source-latest
BuildRequires:	libtool
BuildRequires:	autoconf >= 2.50
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
Cpqarrayd monitors SmartArray controllers for you and notifies by sending SNMP
traps and via syslog.

%prep

%setup -q
%patch -p1

%build
rm -rf .deps
rm -f configure
libtoolize --force --copy; aclocal; autoheader; automake --add-missing --copy --foreign; autoconf

%configure \
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
%doc AUTHORS ChangeLog INSTALL NEWS README
%attr(0755,root,root) %{_initrddir}/cpqarrayd
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/sysconfig/cpqarrayd
%{_sbindir}/cpqarrayd
%{_mandir}/man1/cpqarrayd.1*

