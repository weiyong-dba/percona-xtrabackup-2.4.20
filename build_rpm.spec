Name:       percona-xtrabackup
Version:    2.4.20
Release:    1
License:    GPL
URL:        http://www.percona.io
Group:      applications/database
Source:     percona-xtrabackup-2.4.20.tar.gz
BuildRoot:  %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildRequires:  make,gcc,cmake
Packager:   weiyong@dba.com
Autoreq:    no
Summary: percona-xtrabackup-%{version} RPM

%description
percona-xtrabackup-%{version}

%define BASE_DIR /usr/local/xtrabackup-%{version}
%define _USER root
%define _GROUP root

%prep
%setup -q -n percona-xtrabackup-%{version}

%build
cmake -DBUILD_CONFIG=xtrabackup_release -DCMAKE_INSTALL_PREFIX=%{BASE_DIR}  -DWITH_BOOST=./boost
make %{?_smp_mflags} -j `cat /proc/cpuinfo | grep processor| wc -l`

%install
rm -fr %{buildroot}
make install DESTDIR=%{buildroot}

%pre
if [ -d %{BASE_DIR} ];then
        echo "Error: The base directory %{BASE_DIR} already exists, Aborting." ;
        exit 1
elif [ -e /usr/bin/innobackupex ];
then
        echo "Error: The file /usr/bin/innobackupex already exists, Aborting." ;
        exit 1
fi
mkdir -p %{BASE_DIR}

%post
ln -sf %{BASE_DIR}/bin/innobackupex /usr/bin/innobackupex
ln -sf %{BASE_DIR}/bin/xtrabackup /usr/bin/xtrabackup
ln -sf %{BASE_DIR}/bin/xbstream /usr/bin/xbstream

%preun

%postun
rm -rf %{BASE_DIR}
rm -f /usr/bin/innobackupex
rm -f /usr/bin/xtrabackup
rm -f /usr/bin/xbstream

%clean
rm -rf %{buildroot}

%files
%defattr(-, %{_USER}, %{_GROUP})
%attr(755, %{_USER}, %{_GROUP}) %{BASE_DIR}/*
/root/rpmbuild/BUILD/percona-xtrabackup-2.4.20/man/man1/innobackupex.1
/root/rpmbuild/BUILD/percona-xtrabackup-2.4.20/man/man1/xbcrypt.1
/root/rpmbuild/BUILD/percona-xtrabackup-2.4.20/man/man1/xbstream.1
/root/rpmbuild/BUILD/percona-xtrabackup-2.4.20/man/man1/xtrabackup.1

%changelog