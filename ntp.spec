%define pver p18
%define ntp_user ntp
%define ntp_group ntp

Summary:        Synchronizes system time using the Network Time Protocol (NTP)
Name:           ntp
Version:        4.2.8%{pver}
Release:        1
License:        BSD-Style
Group:          System/Servers
URL:            https://www.ntp.org/
Source0:        http://www.eecis.udel.edu/~ntp/ntp_spool/ntp4/ntp-4.2/%{name}-%{version}.tar.gz
Source99:       http://www.eecis.udel.edu/~ntp/ntp_spool/ntp4/ntp-4.2/%{name}-%{version}.tar.gz.md5
Source1:        ntp.conf
Source2:        ntp.keys
# https://github.com/mlichvar/ntpstat/tags
Source4:        https://github.com/mlichvar/ntpstat/archive/refs/tags/0.6.tar.gz
Source7:        ntpd.sysconfig
Source11:       50-ntpd.list
Source12:       ntpd.service
Source13:       ntpdate.service
Source14:       ntp-wait.service
Source15:       ntpdate.wrapper
Source16:       ntpdate.sysconfig
Source17:	ntpdate.8
Patch0:		ntp-4.2.8-fix-pthread_detach-check.patch
#Patch1:		ntp-4.2.6p1-sleep.patch
#Patch2:		ntp-4.2.6p4-droproot.patch
#Patch3:		ntp-4.2.6p1-bcast.patch
#Patch14:	ntp-4.2.6p4-mlock.patch
BuildRequires:	rpm-helper
Requires(post):  rpm-helper
Requires(post):	 ntp-config
Requires(preun): rpm-helper
Requires:	ntp-client
BuildRequires:	ncurses-devel
BuildRequires:	elfutils-devel
BuildRequires:	lm_sensors-devel
BuildRequires:	net-snmp-devel
BuildRequires:	cap-devel
BuildRequires:	wrap-devel
BuildRequires:	pkgconfig(libedit)
BuildRequires:	pkgconfig(ncurses)
BuildRequires:	pkgconfig(openssl)
BuildRequires:	pkgconfig(libevent)
BuildRequires:	pkgconfig(libevent_pthreads)
# for html2man
BuildRequires:	perl-HTML-Parser

%description
The Network Time Protocol (NTP) is used to synchronize a computer's time
with another reference time source.  The ntp package contains utilities
and daemons which will synchronize your computer's time to Coordinated
Universal Time (UTC) via the NTP protocol and NTP servers.  Ntp includes
ntpdate (a program for retrieving the date and time from remote machines
via a network) and ntpd (a daemon which continuously adjusts system time).

Install the ntp package if you need tools for keeping your system's
time synchronized via the NTP protocol.

Note: Primary, original, big, HTML documentation, is in the package ntp-doc.

%package	client
Summary:	The ntpdate client for setting system time from NTP servers
Group:		System/Servers
Requires(post):	rpm-helper 
Requires(preun):	rpm-helper 
Requires:	%{name}-config

%description client
The Network Time Protocol (NTP) is used to synchronize a computer's time
with another reference time source.  The ntp package contains utilities
and daemons which will synchronize your computer's time to Coordinated
Universal Time (UTC) via the NTP protocol and NTP servers.  Ntp includes
ntpdate (a program for retrieving the date and time from remote machines
via a network) and ntpd (a daemon which continuously adjusts system time).

ntpdate is a simple NTP client which allows a system's clock to be set
to match the time obtained by communicating with one or more servers.

ntpdate is optional (but recommended) if you're running an NTP server,
because initially setting the system clock to an almost-correct time
will help the NTP server synchronize faster.

The ntpdate client by itself is useful for occasionally setting the time on
machines that are not on the net full-time, such as laptops.

%package doc
Summary:        Complete HTML documentation for ntp
Group:          System/Servers
BuildArch:	noarch

%description doc
This is the original, complete, documentation for NTP, in HTML format.
Manpages documentation comes with the binary package(s).

The Network Time Protocol (NTP) is used to synchronize a computer's time
with another reference time source.  The ntp package contains utilities
and daemons which will synchronize your computer's time to Coordinated
Universal Time (UTC) via the NTP protocol and NTP servers.  Ntp includes
ntpdate (a program for retrieving the date and time from remote machines
via a network) and ntpd (a daemon which continuously adjusts system time).

%package	config
Summary:        Complete config for ntp
Group:          System/Servers
BuildArch:	noarch

%description config
Config files for %{name}

The Network Time Protocol (NTP) is used to synchronize a computer's time
with another reference time source.  The ntp package contains utilities
and daemons which will synchronize your computer's time to Coordinated
Universal Time (UTC) via the NTP protocol and NTP servers.  Ntp includes
ntpdate (a program for retrieving the date and time from remote machines
via a network) and ntpd (a daemon which continuously adjusts system time).

%prep

%setup -q -n ntp-%{version} -a4

%autopatch -p1

# set default path to sntp KoD database
sed -i 's|/var/db/ntp-kod|%{_localstatedir}/lib/ntp/sntp-kod|' sntp/*.{man.in,c}

%build
autoreconf -fis
%serverbuild

%configure \
    --with-crypto=openssl \
    --enable-linuxcaps \
    --with-ntpsnmpd

%make CFLAGS="%{optflags}"
%{__make} -C ntpstat-0.6 CFLAGS="%{optflags}"

%install
install -d -m 755 %{buildroot}%{_mandir}/man1
install -d -m 755 %{buildroot}%{_mandir}/man5
install -d -m 755 %{buildroot}%{_mandir}/man8

%makeinstall_std bindir=%{_sbindir}

install -d -m 755 %{buildroot}%{_sysconfdir}
install -m 644 %{SOURCE1} %{buildroot}%{_sysconfdir}/ntp.conf

install -d -m 755 %{buildroot}%{_sysconfdir}/ntp
install -m 640 %{SOURCE2} %{buildroot}%{_sysconfdir}/ntp/keys

install -d -m 755 %{buildroot}%{_sysconfdir}/sysconfig
install -m 644 %{SOURCE7} %{buildroot}%{_sysconfdir}/sysconfig/ntpd
install -m 644 %{SOURCE16} %{buildroot}%{_sysconfdir}/sysconfig/ntpdate

install -m 755 %{SOURCE15} %{buildroot}%{_sbindir}/ntpdate-wrapper

/bin/touch %{buildroot}%{_sysconfdir}/ntp/step-tickers
install -d -m 755 %{buildroot}/var/lib/ntp

install -m755 ntpstat-0.6/ntpstat %{buildroot}%{_sbindir}/
install -m644 ntpstat-0.6/ntpstat.1 %{buildroot}%{_mandir}/man1/
install -m644 %{SOURCE17} %{buildroot}%{_mandir}/man8/

# cleanup patched HTML files
%{__rm} -f html/ntpdate.html.droproot
# for %doc
%{__cp} sntp/COPYRIGHT COPYRIGHT.sntp


install -D -p -m 644 %{SOURCE11} %{buildroot}%{_prefix}/lib/systemd/ntp-units.d/50-ntpd.list
install -D -p -m 644 %{SOURCE12} %{buildroot}%{_unitdir}/ntpd.service
install -D -p -m 644 %{SOURCE13} %{buildroot}%{_unitdir}/ntpdate.service
install -D -p -m 644 %{SOURCE14} %{buildroot}%{_unitdir}/ntp-wait.service

%pre
%_pre_useradd %{ntp_user} %{_sysconfdir}/ntp /bin/false

%pre client
%_pre_useradd %{ntp_user} %{_sysconfdir}/ntp /bin/false

%pre config
%_pre_useradd %{ntp_user} %{_sysconfdir}/ntp /bin/false

%post
%_post_service ntpd
/bin/touch %{_sysconfdir}/ntp/step-tickers

%post client
%_post_service ntpdate

%preun
%_preun_service ntpd

%preun client
%_preun_service ntpdate

%postun
%_postun_userdel %{ntp_user}

%postun	client
%_postun_userdel %{ntp_user}

%files
%{_sbindir}/ntpd
%{_sbindir}/ntpdc
%{_sbindir}/ntp-keygen
%{_sbindir}/ntpq
%{_sbindir}/ntpsnmpd
%{_sbindir}/ntpstat
%{_sbindir}/ntptime
%{_sbindir}/ntptrace
%{_sbindir}/ntp-wait
%{_sbindir}/sntp
%{_sbindir}/tickadj
%{_sbindir}/calc_tickadj
%{_sbindir}/update-leap
%{_mandir}/man1/ntpsnmpd.1*
%{_mandir}/man1/ntpstat.1*
%{_mandir}/man1/sntp.1*
%{_mandir}/man1/calc_tickadj.1.*
%{_mandir}/man1/ntp-keygen.1.*
%{_mandir}/man1/ntp-wait.1.*
%{_mandir}/man1/ntpd.1.*
%{_mandir}/man1/ntpdc.1.*
%{_mandir}/man1/ntpq.1.*
%{_mandir}/man1/ntptrace.1.*
%{_mandir}/man1/update-leap.1.*
%{_mandir}/man5/ntp.conf.5.*
%{_mandir}/man5/ntp.keys.5.*

%{_prefix}/lib/systemd/ntp-units.d/50-ntpd.list
%{_unitdir}/ntp-wait.service
%{_unitdir}/ntpd.service
%{_datadir}/%name

%files client
%doc COPYRIGHT ChangeLog README
%{_sbindir}/ntpdate
%{_sbindir}/ntpdate-wrapper
%{_unitdir}/ntpdate.service
%{_mandir}/man8/ntpdate.8.*
%config(noreplace) %{_sysconfdir}/sysconfig/ntpdate

%files config
%doc COPYRIGHT NEWS TODO README* ChangeLog conf COPYRIGHT.sntp
%config(noreplace) %{_sysconfdir}/ntp.conf
%config(noreplace) %{_sysconfdir}/sysconfig/ntpd
%dir %{_sysconfdir}/ntp
%attr(0640,root,%{ntp_group})%config(noreplace) %{_sysconfdir}/ntp/keys
%config(noreplace) %{_sysconfdir}/ntp/step-tickers
%attr(-,%{ntp_user},%{ntp_group}) /var/lib/ntp

%files doc
%doc COPYRIGHT html/
%{_docdir}/%name
%{_docdir}/sntp
