%define rver            4.2.4p2
%define ntp_user        ntp
%define ntp_group       ntp

Name:           ntp
Version:        4.2.4
Release:        %mkrel 7
Summary:        Synchronizes system time using the Network Time Protocol (NTP)
License:        BSD-Style
Group:          System/Servers
Source0:        http://www.eecis.udel.edu/~ntp/ntp_spool/ntp4/%{name}-%{rver}.tar.gz
Source99:       http://www.eecis.udel.edu/~ntp/ntp_spool/ntp4/%{name}-%{rver}.tar.gz.md5        
Source1:        ntp.conf
Source2:        ntp.keys
Source3:        ntpd.init
Source4:        ntpstat-0.2.tar.bz2
Source7:        ntpd.sysconfig
Patch1:         ntp-4.1.1-biarch-utmp.patch
Patch2:         ntp-4.2.0-ntpdate_quiet.diff
Patch4:         ntp-4.2.4-md5.patch
Patch6:         ntp-4.2.4-lib64.patch
# http://qa.mandriva.com/show_bug.cgi?id=14333
# https://ntp.isc.org/bugs/show_bug.cgi?id=251
# http://ntp.bkbits.net:8080/ntp-stable/cset@3fe3631eWOmqU87rpGQrj82kAK8NoQ?nav=index.html|ChangeSet@-2w
Patch7:         ntp-4.2.0-droproot.patch
# Fedora patches
# This is similar to Patch7
Patch102:       ntp-4.2.4-droproot.patch
Patch103:       ntp-stable-4.2.0a-20040616-groups.patch
Patch104:       ntp-4.1.1c-rc3-authkey.patch
Patch107:       ntp-4.2.0-sbinpath.patch
Patch108:       ntp-4.2.4-html2man.patch
# Adjustments to manpage generation (not from Fedora)
Patch109:       ntp-4.2.4-html2man-adjusts.patch
Patch110:       ntp-4.2.4-loopback.patch
Patch111:       ntp-stable-4.2.0a-20050816-keyfile.patch
Patch112:       ntp-4.2.4-sprintf.patch
URL:            http://www.ntp.org/
Requires(post):  rpm-helper
Requires(postun):  rpm-helper
Requires(pre):  rpm-helper
Requires(preun): rpm-helper
Requires:       ntp-client
BuildRequires:  autoconf2.5
BuildRequires:  automake1.7
BuildRequires:  openssl-static-devel
BuildRequires:  ncurses-devel
BuildRequires:  elfutils-devel
BuildRequires:  libcap-devel
# for html2man
BuildRequires:  perl-HTML-Parser
Buildroot:      %{_tmppath}/%{name}-%{version}-%{release}-buildroot

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

%package client
Summary:        The ntpdate client for setting system time from NTP servers
Group:          System/Servers
Conflicts:      ntp < 4.2.0-3mdk

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
%setup -q -n ntp-%{rver} -a4
%patch1 -p1 -b .biarch-utmp
#%patch2 -p1 -b .ntpdate_quiet
%patch4 -p1 -b .md5
%patch6 -p1 -b .lib64
%patch102 -p1 -b .droproot
%patch103 -p1 -b .groups
%patch104 -p1 -b .authkey
%patch107 -p1 -b .sbinpath
%patch108 -p1 -b .html2man
%patch109 -p1 -b .adjusts
%patch110 -p1 -b .loopback
%patch111 -p1 -b .keyfile
%patch112 -p1 -b .sprintf
%{__aclocal} -I m4 -I libopts/m4
%{__autoconf}
%{__automake} --foreign
%{__perl} -pi -e 's/\r$//g' html/{drivers/*.html,scripts/*}

%build
%serverbuild
%{configure2_5x} \
    --with-crypto=openssl \
    --enable-linuxcaps

%make CFLAGS="$RPM_OPT_FLAGS"
%{__make} -C ntpstat-0.2 CFLAGS="$RPM_OPT_FLATS"

# generate manpages from HTML docs
pushd html && ../scripts/html2man && popd


%install
%{__rm} -rf %{buildroot}

%{__mkdir_p} %{buildroot}%{_mandir}/man1
%{__mkdir_p} %{buildroot}%{_mandir}/man5
%{__mkdir_p} %{buildroot}%{_mandir}/man8

%{makeinstall} bindir=%{buildroot}%{_sbindir}

%{__install} -m644 %{SOURCE1} -D %{buildroot}%{_sysconfdir}/ntp.conf
%{__install} -m640 %{SOURCE2} -D %{buildroot}%{_sysconfdir}/ntp/keys
%{__install} -m755 %{SOURCE3} -D %{buildroot}%{_initrddir}/ntpd
%{__install} -m644 %{SOURCE7} -D %{buildroot}%{_sysconfdir}/sysconfig/ntpd

/bin/touch %{buildroot}%{_sysconfdir}/ntp/step-tickers

%{__install} -m755 ntpstat-0.2/ntpstat %{buildroot}%{_sbindir}/
%{__install} -m644 ntpstat-0.2/ntpstat.1 %{buildroot}%{_mandir}/man1/
%{__install} -m644 html/man/man5/*.5 %{buildroot}%{_mandir}/man5/
%{__install} -m644 html/man/man8/*.8 %{buildroot}%{_mandir}/man8/

# biggest file in the main package, when uncompressed
bzip2 -9 ChangeLog*
# cleanup HTML docs directory for %doc
%{__rm} -rf html/man
# cleanup patched HTML files
%{__rm} -f html/ntpdate.html.droproot
# for %doc
%{__cp} sntp/README README.sntp
%{__cp} sntp/COPYRIGHT COPYRIGHT.sntp

%pre
%_pre_useradd %{ntp_user} %{_sysconfdir}/ntp /bin/false

%post
# ntpd needs to be able to write to the ntp directory
# as well as into the drift file, but not step-tickers
# first installs already have the correct permissions
if [ "$1" = "2" ]; then
        %{__chown} %{ntp_user}:%{ntp_group} %{_sysconfdir}/ntp
        [ -f %{_sysconfdir}/ntp/drift ] && \
                %{__chown} %{ntp_user}:%{ntp_group} %{_sysconfdir}/ntp/drift || :
        %{__chown} root:%{ntp_group} %{_sysconfdir}/ntp/keys
        %{__chmod} 0640 %{_sysconfdir}/ntp/keys
fi
%_post_service ntpd
/bin/touch %{_sysconfdir}/ntp/step-tickers

%preun
%_preun_service ntpd

%postun
%_postun_userdel %{ntp_user}

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(0644,root,root,0755)
%doc COPYRIGHT NEWS TODO README* ChangeLog.bz2 conf README.sntp COPYRIGHT.sntp
%defattr(-,root,root)
%{_initrddir}/ntpd
%config(noreplace) %{_sysconfdir}/ntp.conf
%config(noreplace) %{_sysconfdir}/sysconfig/ntpd
%attr(-,%{ntp_user},%{ntp_group})%dir %{_sysconfdir}/ntp
%attr(0640,root,%{ntp_group})%config(noreplace) %{_sysconfdir}/ntp/keys
%ghost %config(noreplace) %{_sysconfdir}/ntp/step-tickers
%{_sbindir}/ntp-keygen
%{_sbindir}/ntp-wait
%{_sbindir}/ntpd
%{_sbindir}/ntpdc
%{_sbindir}/ntpq
%{_sbindir}/ntpstat
%{_sbindir}/ntptime
%{_sbindir}/ntptrace
%{_sbindir}/sntp
%{_sbindir}/tickadj
# prevent man1 pages from hiding the more complete html2man generated man8 ones
%exclude %{_mandir}/man1/ntpd.1*
%exclude %{_mandir}/man1/ntpdc.1*
%exclude %{_mandir}/man1/ntpdsim.1*
%exclude %{_mandir}/man1/ntp-keygen.1*
%exclude %{_mandir}/man1/ntpq.1*
%{_mandir}/man1/ntpstat.1*
%{_mandir}/man1/sntp.1*
%{_mandir}/man8/ntpd.8*
%{_mandir}/man8/ntpdc.8*
%{_mandir}/man8/ntpq.8*
%{_mandir}/man8/ntptime.8*
%{_mandir}/man8/ntptrace.8*
%{_mandir}/man8/ntp-keygen.8*
%{_mandir}/man8/tickadj.8*
%{_mandir}/man5/ntp.conf.5*
%{_mandir}/man5/ntp_acc.5*
%{_mandir}/man5/ntp_auth.5*
%{_mandir}/man5/ntp_clock.5*
%{_mandir}/man5/ntp_misc.5*
%{_mandir}/man5/ntp_mon.5*
%{_mandir}/man5/ntp_auto.5*

%files client
%defattr(-,root,root)
%doc COPYRIGHT ChangeLog.bz2 README
%{_sbindir}/ntpdate
%{_mandir}/man8/ntpdate.8*

%files doc
%defattr(0644,root,root,0755)
%doc COPYRIGHT html/
