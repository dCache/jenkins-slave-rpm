%define _prefix	%{_usr}/lib/jenkins-swarm-slave

Summary: Jenkins Swarm slave
Vendor: dCache.org
Name: jenkins-swarm-slave
Version: 2.2
Release: 1
BuildArch: noarch
Prefix: /
Packager: dCache.org <support@dcache.org>.


License: Distributable
Group: Development/Tools/Building


Source: https://repo.jenkins-ci.org/releases/org/jenkins-ci/plugins/swarm-client/%{version}/swarm-client-%{version}.jar
Source1: jenkins-slave.service
Source2: jenkins-slave.sysconfig

Requires: java-1.8.0-openjdk-headless
Requires(pre): shadow-utils
Requires(post): systemd

BuildRoot:	%{_tmppath}/build-%{name}-%{version}
%description
Jenkins is a self-contained, open source automation server which can be used to
automate all sorts of tasks such as building, testing, and deploying software.
Jenkins can be installed through native system packages, Docker, or even run
standalone by any machine with the Java Runtime Environment installed.

This plugin enables slaves to auto-discover nearby Jenkins master and join it
automatically, thereby forming an ad-hoc cluster.

%prep
%setup -q -T -c

%build

%install
rm -rf "%{buildroot}"
mkdir -p "%{buildroot}%{_prefix}/"
mkdir -p "%{buildroot}/var/lib/jenkins"

%__install -D -m0644 "%{SOURCE0}" "%{buildroot}%{_prefix}/"
%__install -D -m0644 "%{SOURCE1}" "%{buildroot}/etc/systemd/system/%{name}.service"
%__install -D -m0644 "%{SOURCE2}" "%{buildroot}/etc/sysconfig/%{name}"

%pre
getent group jenkins >/dev/null || /usr/sbin/groupadd -r jenkins
getent passwd jenkins > /dev/null || /usr/sbin/useradd -g jenkins \
  -l -M -s /sbin/nologin -r -c "Jenkins Swarm slave" \
	-d "/var/lib/jenkins" jenkins

%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%files
%defattr(-,root,root)
%dir %{_prefix}
%{_prefix}/*.jar
/etc/systemd/system/%{name}.service
%config(noreplace) /etc/sysconfig/%{name}
%attr(-,jenkins,jenkins) /var/lib/jenkins


%changelog
* Thu Jun 29 2017 tigran.mkrtchyan@desy.de
- RPM-izing swarm slave
