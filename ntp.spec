%define pver p5
%define ntp_user ntp
%define ntp_group ntp

Summary:        Synchronizes system time using the Network Time Protocol (NTP)
Name:           ntp
Version:        4.2.6%{pver}
Release:        3
License:        BSD-Style
Group:          System/Servers
URL:            http://www.ntp.org/
Source0:        http://www.eecis.udel.edu/~ntp/ntp_spool/ntp4/ntp-4.2/%{name}-%{version}.tar.gz
Source99:       http://www.eecis.udel.edu/~ntp/ntp_spool/ntp4/ntp-4.2/%{name}-%{version}.tar.gz.md5
Source1:        ntp.conf
Source2:        ntp.keys
Source4:        ntpstat-0.2.tar.bz2
Source7:        ntpd.sysconfig
Source11:       50-ntpd.list
Source12:       ntpd.service
Source13:       ntpdate.service
Source14:       ntp-wait.service
Source15:       ntpdate.wrapper
Source16:       ntpdate.sysconfig
Patch1:		ntp-4.2.6p1-sleep.patch
Patch2:		ntp-4.2.6p4-droproot.patch
Patch3:		ntp-4.2.6p1-bcast.patch
Patch4:		ntp-4.2.6p1-cmsgalign.patch
Patch5:		ntp-4.2.6p1-linkfastmath.patch
Patch6:		ntp-4.2.6p2-tentative.patch
Patch7:		ntp-4.2.6p1-retcode.patch
Patch8:		ntp-4.2.6p4-rtnetlink.patch
Patch10:	ntp-4.2.6p4-htmldoc.patch
Patch11:	ntp-4.2.6p1-nano.patch
Patch12:	ntp-4.2.4p7-getprecision.patch
Patch13:	ntp-4.2.6p1-logdefault.patch
Patch14:	ntp-4.2.6p4-mlock.patch
Patch15:	ntp-4.2.6p2-multiopts.patch
Patch16:	ntp-4.2.6p3-no_checkChangeLog.diff
Patch50:	ntpstat-0.2-clksrc.patch
Patch51:	ntpstat-0.2-multipacket.patch
Patch52:	ntpstat-0.2-sysvars.patch
Patch53:	ntpstat-0.2-maxerror.patch
Patch54:	ntpstat-0.2-errorbit.patch
Patch300:	ntp-4.2.4p5-format_not_a_string_literal_and_no_format_arguments.diff
Patch301:	ntp-4.2.6p5-automake-1.13.patch
Requires(post):  rpm-helper
Requires(preun): rpm-helper
Requires:	ntp-client
BuildRequires:	ncurses-devel
BuildRequires:	elfutils-devel
BuildRequires:	net-snmp-devel
BuildRequires:	cap-devel
BuildRequires:	pkgconfig(libedit)
BuildRequires:	pkgconfig(ncurses)
BuildRequires:	pkgconfig(openssl)
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

%prep

%setup -q -n ntp-%{version} -a4
%patch1 -p1 -b .sleep
%patch2 -p1 -b .droproot
%patch3 -p0 -b .bcast
%patch4 -p1 -b .cmsgalign
%ifarch ia64
%patch5 -p1 -b .linkfastmath
%endif
%patch6 -p0 -b .tentative
%patch7 -p1 -b .retcode
%patch8 -p1 -b .rtnetlink
%patch10 -p1 -b .htmldoc
%patch11 -p1 -b .nano
%patch12 -p1 -b .getprecision
%patch13 -p1 -b .logdefault
%patch14 -p1 -b .mlock
%patch15 -p1 -b .multiopts
%patch16 -p0 -b .no_checkChangeLog

# set default path to sntp KoD database
sed -i 's|/var/db/ntp-kod|%{_localstatedir}/lib/ntp/sntp-kod|' sntp/*.{1,c}

# ntpstat patches
%patch50 -p1 -b .clksrc
%patch51 -p1 -b .multipacket
%patch52 -p1 -b .sysvars
%patch53 -p1 -b .maxerror
%patch54 -p1 -b .errorbit

%patch300 -p1 -b .format_not_a_string_literal_and_no_format_arguments
%patch301 -p1 -b .automake-1_13

%build
autoreconf -fis
%serverbuild

%configure2_5x \
    --with-crypto=openssl \
    --enable-linuxcaps \
    --with-ntpsnmpd

%make CFLAGS="%{optflags}"
%{__make} -C ntpstat-0.2 CFLAGS="%{optflags}"

# generate manpages from HTML docs
pushd html
../scripts/html2man
# remove adjacent blank lines
sed -i 's/^[\t\ ]*$//;/./,/^$/!d' man/man*/*.[58]
popd

mv html/man .
# biggest file in the main package, when uncompressed
bzip2 -9 ChangeLog*

%install
install -d -m 755 %{buildroot}%{_mandir}/man1
install -d -m 755 %{buildroot}%{_mandir}/man5
install -d -m 755 %{buildroot}%{_mandir}/man8

%makeinstall bindir=%{buildroot}%{_sbindir}

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

install -m755 ntpstat-0.2/ntpstat %{buildroot}%{_sbindir}/
install -m644 ntpstat-0.2/ntpstat.1 %{buildroot}%{_mandir}/man1/
install -m644 man/man5/*.5 %{buildroot}%{_mandir}/man5/
install -m644 man/man8/*.8 %{buildroot}%{_mandir}/man8/

# cleanup patched HTML files
%{__rm} -f html/ntpdate.html.droproot
# for %doc
%{__cp} sntp/COPYRIGHT COPYRIGHT.sntp

# prevent man1 pages from hiding the more complete html2man generated man8 ones
rm -f %{buildroot}%{_mandir}/man1/ntpd.1*
rm -f %{buildroot}%{_mandir}/man1/ntpdc.1*
rm -f %{buildroot}%{_mandir}/man1/ntp-keygen.1*
rm -f %{buildroot}%{_mandir}/man1/ntpq.1*

install -D -p -m 644 %{SOURCE11} %{buildroot}%{_prefix}/lib/systemd/ntp-units.d/50-ntpd.list
install -D -p -m 644 %{SOURCE12} %{buildroot}%{_unitdir}/ntpd.service
install -D -p -m 644 %{SOURCE13} %{buildroot}%{_unitdir}/ntpdate.service
install -D -p -m 644 %{SOURCE14} %{buildroot}%{_unitdir}/ntp-wait.service

%pre
%_pre_useradd %{ntp_user} %{_sysconfdir}/ntp /bin/false

%post
%_post_service ntpd
/bin/touch %{_sysconfdir}/ntp/step-tickers

%preun
%_preun_service ntpd

%postun
%_postun_userdel %{ntp_user}

%files
%doc COPYRIGHT NEWS TODO README* ChangeLog.bz2 conf COPYRIGHT.sntp
%config(noreplace) %{_sysconfdir}/ntp.conf
%config(noreplace) %{_sysconfdir}/sysconfig/ntpd
%dir %{_sysconfdir}/ntp
%attr(0640,root,%{ntp_group})%config(noreplace) %{_sysconfdir}/ntp/keys
%config(noreplace) %{_sysconfdir}/ntp/step-tickers
%attr(-,%{ntp_user},%{ntp_group}) /var/lib/ntp
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
%{_mandir}/man1/ntpsnmpd.1*
%{_mandir}/man1/ntpstat.1*
%{_mandir}/man1/sntp.1*
%{_mandir}/man5/ntp_acc.5*
%{_mandir}/man5/ntp_auth.5*
%{_mandir}/man5/ntp_clock.5*
%{_mandir}/man5/ntp.conf.5*
%{_mandir}/man5/ntp_decode.5*
%{_mandir}/man5/ntp_misc.5*
%{_mandir}/man5/ntp_mon.5*
%{_mandir}/man8/ntpd.8*
%{_mandir}/man8/ntpdc.8*
%{_mandir}/man8/ntp-keygen.8*
%{_mandir}/man8/ntpq.8*
%{_mandir}/man8/ntptime.8*
%{_mandir}/man8/ntptrace.8*
%{_mandir}/man8/ntp-wait.8*
%{_mandir}/man8/tickadj.8*
%{_prefix}/lib/systemd/ntp-units.d/50-ntpd.list
%{_unitdir}/ntp-wait.service
%{_unitdir}/ntpd.service

%files client
%doc COPYRIGHT ChangeLog.bz2 README
%{_sbindir}/ntpdate
%{_sbindir}/ntpdate-wrapper
%{_mandir}/man8/ntpdate.8*
%{_unitdir}/ntpdate.service
%config(noreplace) %{_sysconfdir}/sysconfig/ntpdate

%files doc
%doc COPYRIGHT html/
