%define pver p3
%define ntp_user ntp
%define ntp_group ntp

Summary:        Synchronizes system time using the Network Time Protocol (NTP)
Name:           ntp
Version:        4.2.6%{pver}
Release:        %mkrel 4
License:        BSD-Style
Group:          System/Servers
URL:            http://www.ntp.org/
Source0:        http://www.eecis.udel.edu/~ntp/ntp_spool/ntp4/%{name}-%{version}.tar.gz
Source99:       http://www.eecis.udel.edu/~ntp/ntp_spool/ntp4/%{name}-%{version}.tar.gz.md5
Source1:        ntp.conf
Source2:        ntp.keys
Source3:        ntpd.init
Source4:        ntpstat-0.2.tar.bz2
Source7:        ntpd.sysconfig
Source8:        usr.sbin.ntpd.apparmor
Patch1: ntp-4.2.6p1-sleep.patch
Patch2: ntp-4.2.6p1-droproot.patch
Patch3: ntp-4.2.6p1-bcast.patch
Patch4: ntp-4.2.6p1-cmsgalign.patch
Patch5: ntp-4.2.6p1-linkfastmath.patch
Patch6: ntp-4.2.6p2-tentative.patch
Patch7: ntp-4.2.6p1-retcode.patch
Patch8: ntp-4.2.6p1-rtnetlink.patch
Patch9: ntp-4.2.6p2-html2man.patch
Patch10: ntp-4.2.6p2-htmldoc.patch
Patch11: ntp-4.2.6p1-nano.patch
Patch12: ntp-4.2.4p7-getprecision.patch
Patch13: ntp-4.2.6p1-logdefault.patch
Patch14: ntp-4.2.6p2-mlock.patch
Patch15: ntp-4.2.6p2-multiopts.patch
Patch16: ntp-4.2.6p3-no_checkChangeLog.diff
Patch50: ntpstat-0.2-clksrc.patch
Patch51: ntpstat-0.2-multipacket.patch
Patch52: ntpstat-0.2-sysvars.patch
Patch53: ntpstat-0.2-maxerror.patch
Patch300: ntp-4.2.4p5-format_not_a_string_literal_and_no_format_arguments.diff
Patch301: ntp-automake-1.13.patch
Requires(post):  rpm-helper
Requires(postun):  rpm-helper
Requires(pre):  rpm-helper
Requires(preun): rpm-helper
Requires:       ntp-client
Conflicts:      apparmor-profiles < 2.1-1.961.5mdv2008.0
BuildRequires:  autoconf2.5
BuildRequires:  automake
BuildRequires:  openssl-devel
BuildRequires:  ncurses-devel
BuildRequires:  elfutils-devel
BuildRequires:  libcap-devel
BuildRequires:  libedit-devel
BuildRequires:  net-snmp-devel
# for html2man
BuildRequires:  perl-HTML-Parser

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
%patch9 -p1 -b .html2man
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

%patch300 -p1 -b .format_not_a_string_literal_and_no_format_arguments
%patch301 -p1 -b .am113~

#%%{__aclocal} -I m4 -I libopts/m4
#%%{__autoconf}
#%%{__automake} --foreign
autoreconf -fis

%{__perl} -pi -e 's/\r$//g' html/{drivers/*.html,scripts/*}

%build
%serverbuild

%configure2_5x \
    --with-crypto=openssl \
    --enable-linuxcaps \
    --with-ntpsnmpd

%make CFLAGS="$CFLAGS"
%{__make} -C ntpstat-0.2 CFLAGS="$CFLAGS"

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
%{__rm} -rf %{buildroot}

%{__mkdir_p} %{buildroot}%{_mandir}/man1
%{__mkdir_p} %{buildroot}%{_mandir}/man5
%{__mkdir_p} %{buildroot}%{_mandir}/man8

%makeinstall bindir=%{buildroot}%{_sbindir}

%{__install} -m644 %{SOURCE1} -D %{buildroot}%{_sysconfdir}/ntp.conf
%{__install} -m640 %{SOURCE2} -D %{buildroot}%{_sysconfdir}/ntp/keys
%{__install} -m755 %{SOURCE3} -D %{buildroot}%{_initrddir}/ntpd
%{__install} -m644 %{SOURCE7} -D %{buildroot}%{_sysconfdir}/sysconfig/ntpd

/bin/touch %{buildroot}%{_sysconfdir}/ntp/step-tickers
install -d -m 755 %{buildroot}/var/lib/ntp

%{__install} -m755 ntpstat-0.2/ntpstat %{buildroot}%{_sbindir}/
%{__install} -m644 ntpstat-0.2/ntpstat.1 %{buildroot}%{_mandir}/man1/
%{__install} -m644 man/man5/*.5 %{buildroot}%{_mandir}/man5/
%{__install} -m644 man/man8/*.8 %{buildroot}%{_mandir}/man8/

# cleanup patched HTML files
%{__rm} -f html/ntpdate.html.droproot
# for %doc
%{__cp} sntp/COPYRIGHT COPYRIGHT.sntp

# apparmor profile
mkdir -p %{buildroot}%{_sysconfdir}/apparmor.d
install -m 0644 %{SOURCE8} %{buildroot}%{_sysconfdir}/apparmor.d/usr.sbin.ntpd

# prevent man1 pages from hiding the more complete html2man generated man8 ones
rm -f %{buildroot}%{_mandir}/man1/ntpd.1*
rm -f %{buildroot}%{_mandir}/man1/ntpdc.1*
rm -f %{buildroot}%{_mandir}/man1/ntp-keygen.1*
rm -f %{buildroot}%{_mandir}/man1/ntpq.1*

%posttrans
# if we have apparmor installed, reload if it's being used
if [ -x /sbin/apparmor_parser ]; then
        /sbin/service apparmor condreload
fi

%pre
%_pre_useradd %{ntp_user} %{_sysconfdir}/ntp /bin/false

%post
%_post_service ntpd
/bin/touch %{_sysconfdir}/ntp/step-tickers

%preun
%_preun_service ntpd

%postun
%_postun_userdel %{ntp_user}

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root)
%doc COPYRIGHT NEWS TODO README* ChangeLog.bz2 conf COPYRIGHT.sntp
%{_initrddir}/ntpd
%config(noreplace) %{_sysconfdir}/ntp.conf
%config(noreplace) %{_sysconfdir}/sysconfig/ntpd
%config(noreplace) %{_sysconfdir}/apparmor.d/usr.sbin.ntpd
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

%files client
%defattr(-,root,root)
%doc COPYRIGHT ChangeLog.bz2 README
%{_sbindir}/ntpdate
%{_mandir}/man8/ntpdate.8*

%files doc
%defattr(-,root,root)
%doc COPYRIGHT html/


%changelog
* Wed May 04 2011 Oden Eriksson <oeriksson@mandriva.com> 4.2.6p3-3mdv2011.0
+ Revision: 666631
- mass rebuild

* Wed Jan 19 2011 Oden Eriksson <oeriksson@mandriva.com> 4.2.6p3-2
+ Revision: 631673
- fix #62115 (ntpd throws some errors about syntax in /var/log/messages)

* Tue Jan 04 2011 Oden Eriksson <oeriksson@mandriva.com> 4.2.6p3-1mdv2011.0
+ Revision: 628622
- 4.2.6p3
- bring back the "p" in the %%version...
- rediff/drop/add patches

* Sun Jan 02 2011 Oden Eriksson <oeriksson@mandriva.com> 4.2.6-2mdv2011.0
+ Revision: 627658
- fix the darn filelists...
- fix build (damn %%exclude removal!)
- don't force the usage of automake1.7

* Sun Oct 24 2010 Oden Eriksson <oeriksson@mandriva.com> 4.2.6-1mdv2011.0
+ Revision: 588710
- more fixes...
- fix deps
- enable ntpsnmpd
- 4.2.6p2
- sync patches with fedora
- rediffed the format string patch

* Fri Feb 26 2010 Oden Eriksson <oeriksson@mandriva.com> 4.2.4-29mdv2010.1
+ Revision: 511598
- rebuilt against openssl-0.9.8m

* Wed Dec 09 2009 Oden Eriksson <oeriksson@mandriva.com> 4.2.4-28mdv2010.1
+ Revision: 475199
- 4.2.4p8 (fixes CVE-2009-3563)

* Mon Oct 12 2009 Oden Eriksson <oeriksson@mandriva.com> 4.2.4-27mdv2010.0
+ Revision: 456718
- revert the hack to fix #50815 due to regressions

* Fri Oct 02 2009 Oden Eriksson <oeriksson@mandriva.com> 4.2.4-26mdv2010.0
+ Revision: 452749
- fix #50815 (ntp initialization being blocked by shorewall initialization)

* Wed Jun 03 2009 Oden Eriksson <oeriksson@mandriva.com> 4.2.4-25mdv2010.0
+ Revision: 382399
- bump release
- P115: fix build (gentoo)
- enable ntpdate to read configurable variables from the /etc/sysconfig/ntpd file (#51393)

* Tue May 19 2009 Oden Eriksson <oeriksson@mandriva.com> 4.2.4-23mdv2010.0
+ Revision: 377685
- fix build
- 4.2.4p7 (fixes CVE-2009-0159, CVE-2009-1252)
- nuke redundant patches

* Mon Apr 13 2009 Oden Eriksson <oeriksson@mandriva.com> 4.2.4-22mdv2009.1
+ Revision: 366819
- P115: security fix for CVE-2009-0159
- fix autopoo

* Thu Jan 08 2009 Frederik Himpe <fhimpe@mandriva.org> 4.2.4-21mdv2009.1
+ Revision: 327218
- Update to new version 4.2.4p6 (fixes CVE-2009-0021)

* Wed Dec 17 2008 Oden Eriksson <oeriksson@mandriva.com> 4.2.4-20mdv2009.1
+ Revision: 315242
- rediffed fuzzy patches
- added P114 to fix build with -Werror=format-security

* Thu Oct 16 2008 Oden Eriksson <oeriksson@mandriva.com> 4.2.4-19mdv2009.1
+ Revision: 294183
- rebuild

* Mon Aug 18 2008 Oden Eriksson <oeriksson@mandriva.com> 4.2.4-18mdv2009.0
+ Revision: 273166
- 4.2.4p5
- drop P104, it won't apply anymore
- restore the init script

* Mon Jul 07 2008 Oden Eriksson <oeriksson@mandriva.com> 4.2.4-17mdv2009.0
+ Revision: 232369
- rebuilt against new libcap

  + Pixel <pixel@mandriva.com>
    - adapt to %%_localstatedir now being /var instead of /var/lib (#22312)

* Fri May 30 2008 Oden Eriksson <oeriksson@mandriva.com> 4.2.4-16mdv2009.0
+ Revision: 213440
- added P8 to stop it from working with minor openssl version
  changes (after looking at the openssh patch)

* Fri Mar 14 2008 Gustavo De Nardin <gustavodn@mandriva.com> 4.2.4-15mdv2008.1
+ Revision: 187777
- fixed the initial sync loop running ntpdate to properly set RETVAL

* Fri Mar 14 2008 Gustavo De Nardin <gustavodn@mandriva.com> 4.2.4-14mdv2008.1
+ Revision: 187763
- made the initscript try more than once to do the initial clock sync with
  ntpdate, to account for slow systems or slow network initialization, even
  though this shouldn't happen....

* Thu Mar 06 2008 Guillaume Rousse <guillomovitch@mandriva.org> 4.2.4-13mdv2008.1
+ Revision: 180874
- FHS compliance: move drift file under %%{_localstatedir}/ntp
  drop useless file ownership change in %%post
  file section cleanup

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Fri Dec 07 2007 David Walluck <walluck@mandriva.org> 4.2.4-12mdv2008.1
+ Revision: 116373
- rebuild for new openssl

* Sat Oct 20 2007 Oden Eriksson <oeriksson@mandriva.com> 4.2.4-11mdv2008.1
+ Revision: 100563
- rebuilt against latest openssl (OpenSSL version mismatch. Built against 90805f, you have 908070)

* Tue Sep 25 2007 Oden Eriksson <oeriksson@mandriva.com> 4.2.4-10mdv2008.0
+ Revision: 92784
- 4.2.4p4
- added rediffed P113 from debian to use capabilities at runtime if found
- don't load the capabilities kernel module in the initscript

* Wed Sep 19 2007 Andreas Hasenack <andreas@mandriva.com> 4.2.4-9mdv2008.0
+ Revision: 91196
- ship apparmor profile and use it if apparmor is in effect

* Mon Jul 02 2007 David Walluck <walluck@mandriva.org> 4.2.4-8mdv2008.0
+ Revision: 46885
- 4.2.4p3

* Wed Jun 27 2007 Andreas Hasenack <andreas@mandriva.com> 4.2.4-7mdv2008.0
+ Revision: 45128
- fix serverbuild usage

* Wed Jun 27 2007 Guillaume Rousse <guillomovitch@mandriva.org> 4.2.4-6mdv2008.0
+ Revision: 44896
- drop bash completion scriplet, as already included in main bash completion script

* Thu Jun 21 2007 David Walluck <walluck@mandriva.org> 4.2.4-5mdv2008.0
+ Revision: 42153
- bump release
- rediff and apply droproot patch
- remove loopfilter patch (not needed)
- fix release
- 4.2.4p2
- fix doc perms


* Thu Mar 08 2007 Olivier Blin <oblin@mandriva.com> 4.2.4-4mdv2007.1
+ Revision: 138392
- fix syntax error in initscript

  + Gustavo De Nardin <gustavodn@mandriva.com>
    - don't default to disabled authentication, it is unsafe, specially because
      our current default configuration has multicastclient enabled; (#27079)
    - changed patch ntp-4.2.4-html2man-adjusts, adding generation and packaging
      of ntp_auto(5), for the autoconfiguration modes manpage
    - added README and COPYRIGHT for sntp to docs
    - added example configurations to docs
    - small note about ntp-doc package in ntp package description
    - renamed patch ntp-4.2.4-html2man-tickadj to ntp-4.2.4-html2man-adjusts
      - made it add references to ntp_*(5) configuration manpages from
        ntp.conf(5)
      - made the generated SEE ALSO manpages sections note about ntp-doc package
        instead of filesystem location

* Fri Jan 26 2007 Gustavo De Nardin <gustavodn@mandriva.com> 4.2.4-3mdv2007.1
+ Revision: 114164
- make proper use of pool.ntp.org in default ntp.conf
- split HTML docs into a separate package ntp-doc
- added COPYRIGHT notice to all (sub)packages documentation
- updated manpages:
  . stopped using old manpages from Redhat (ntp-4.1.2-rh-manpages.tar.bz2)
  . added patch ntp-4.2.4-html2man from Fedora ntp-4.2.4-3.fc7 to fix
    html2man manpages generation from HTML docs
  . generate manpages from the more uptodate HTML docs, with html2man
- manpages of ntpdate, ntpd, ntpdc, ntpdsim, ntpq, ntp-keygen, ntptime,
  ntptrace, moved from man1 to man8 section
- removed pointless patch ntp-4.2.2-mlockall.patch: it is applied OK to
  'configure', but then 'configure' is regenerated by %%{__autoconf} ...
- removed ntp-4.2.0-genkey3.patch: already fixed (correctly) upstream
- replaced patch ntp-4.2.4-sprintf with the one from actual Fedora package, as
  ours contained an error (call to sprintf instead of snprintf), and to keep
  them really the same, and so avoid "WTF?" situations

* Sat Jan 20 2007 Olivier Blin <oblin@mandriva.com> 4.2.4-2mdv2007.1
+ Revision: 111122
- start services providing the named system facility if any is enabled (#25935)

* Sun Jan 07 2007 David Walluck <walluck@mandriva.org> 4.2.4-1mdv2007.1
+ Revision: 105137
- new version 4.2.4
- remove Patch0, Patch5, Patch8 (no longer needed)
- remove Patch9 (merged upstream)
- replace Patch7 with Patch102 (from Fedora)
- add patches from Fedora (102-112)

* Sun Oct 01 2006 Stew Benedict <sbenedict@mandriva.com> 4.2.0-31.2mdv2007.0
- rebuild against updated openssl-static-devel (0.9.8b-2.2mdv2007)

* Fri Sep 29 2006 Stew Benedict <sbenedict@mandriva.com> 4.2.0-31.1mdv2007.0
- rebuild against updated openssl-static-devel (0.9.8b-2.1mdv2007)

* Wed Sep 20 2006 Per Øyvind Karlsen <pkarlsen@mandriva.com> 4.2.0-31mdv2007.0
- rebuild

* Fri Aug 25 2006 Per Øyvind Karlsen <pkarlsen@mandriva.com> 4.2.0-30mdv2007.0
- sync initscript with fedora's and adapt it (a more proper fix to #23673
  without causing hang when failing to reach ntp server #24508), puts back 
  dependency on ntp-client again
- add sysconfig conf file for ntpd arguments
- comment out example keys in key file
- fix macro-in-%%changelog
* Tue Feb 21 2012 abf
- The release updated by ABF

- fix non-conffile-in-etc
- bunzip2 stuff

* Wed Jul 19 2006 Emmanuel Blindauer <blindauer@mandriva.org> 4.2.0-29mdv2007.0
- Fix typo.

* Sun Jul 16 2006 Emmanuel Blindauer <blindauer@mandriva.org> 4.2.0-28mdv2007.0
- Fix init startup and drop ntpdate requirement. (#23673)

* Thu Feb 09 2006 Andreas Hasenack <andreas@mandriva.com> 4.2.0-27mdk
- fixed capability module issue (#21043)

* Mon Jan 09 2006 Olivier Blin <oblin@mandriva.com> 4.2.0-26mdk
- fix typo in initscript

* Mon Jan 09 2006 Olivier Blin <oblin@mandriva.com> 4.2.0-25mdk
- convert parallel init to LSB
- mkrel

* Mon Jan 02 2006 Olivier Blin <oblin@mandriva.com> 4.2.0-24mdk
- parallel init support

* Fri Dec 02 2005 Olivier Blin <oblin@mandriva.com> 4.2.0-23mdk
- don't require modutils, it's deprecated
  (and module tools are required by basesystem and kernel packages)

* Sun Nov 13 2005 Oden Eriksson <oeriksson@mandriva.com> 4.2.0-22mdk
- rebuilt against openssl-0.9.8a

* Thu Sep 08 2005 Warly <warly@mandriva.com> 4.2.0-21mdk
- Security update for CAN-2005-2496 (P9)

* Sat Jul 23 2005 Couriousous <couriousous@mandriva.org> 4.2.0-20mdk
- fix gcc4 patch ( #16954 )

* Fri Jul 22 2005 Guillaume Rousse <guillomovitch@mandriva.org> 4.2.0-19mdk 
- ntpdate bash-completion
- fix gcc 4 build (<couriousous@mandriva.org>)

* Mon Mar 21 2005 Andreas Hasenack <andreas@mandrakesoft.com> 4.2.0-18mdk
- check for stale subsystem lock in the init script (we now check for
  the lock file and if there are any ntpd processes running). If we still
  have problems with this, then the last option would be to make ntpd create
  a pid file and use that.
- just a safe guard: check if we need to load the capability kernel module.
  MDK has this builtin, but some user might rebuild the kernel and use it
  as a module
- Prereq -> Requires(bla)

* Thu Mar 17 2005 Andreas Hasenack <andreas@mandrakesoft.com> 4.2.0-17mdk
- argh, a typo in the init script was preventing step-tickers from ever being
  used

* Thu Mar 17 2005 Andreas Hasenack <andreas@mandrakesoft.com> 4.2.0-16mdk
- using rpm macros for user add/delete
- test for drift file existance before chowning it in %%post
- only use step-tickers if it has some content

* Mon Mar 07 2005 Andreas Hasenack <andreas@mandrakesoft.com> 4.2.0-15mdk
- added drop-root patch from http://bugzilla.ntp.org/show_bug.cgi?id=251 (#14333)
  (it's already applied in the -stable branch)
- deal with upgrades from versions before this patch was applied
- avoid multiple starts in the init script
- return appropriate error codes for start/stop/status
- ntpdate's output was messing the screen. TODO: fix ntpdate's -s option

* Sat Feb 19 2005 Christiaan Welvaart <cjw@daneel.dyndns.org> 4.2.0-14mdk
- add BuildRequires: dos2unix

* Thu Feb 17 2005 Warly <warly@mandrakesoft.com> 4.2.0-13mdk
- fix bad touch of the step-tickers file

* Wed Feb 16 2005 Warly <warly@mandrakesoft.com> 4.2.0-12mdk
- change chkconfig level from 55 to 56 to fix bug 9045

* Thu Jan 20 2005 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 4.2.0-11mdk
- rebuild for new readline
- fix summary-ended-with-dot

* Fri Oct 01 2004 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 4.2.0-10mdk
- lib64 fixes

* Tue Sep 14 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 4.2.0-9mdk
- fix S1 (#8844)

* Tue Aug 10 2004 Warly <warly@mandrakesoft.com> 4.2.0-8mdk
- Add more pool.ntp.org entry in ntpd.conf

* Wed Jul 07 2004 Frederic Crozat <fcrozat@mandrakesoft.com> 4.2.0-7mdk
- Add Conflicts to ease upgrade (Mdk bug #10208)

* Wed Jun 30 2004 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 4.2.0-6mdk
- fix buildrequires

* Mon Jun 28 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 4.2.0-5mdk
- added P3 & P4 (fedora) fix #10159 
- added P5
- fix deps

* Sun Jun 27 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 4.2.0-4mdk
- new url

* Sun Jun 27 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 4.2.0-3mdk
- broke out ntpdate as that's the only one needed if using an external 
  clock source (description stolen from debian)
- added P2 (stolen from gentoo, but tweaked some; usage "ntpdate -Q" 
  and it won't spit out "host found : ..." anymore)
- change group
- added S4 and S5 from fedora
- fix deps
- misc spec file fixes

