Summary: Several utilities for using MS-Access .mdb files. 
Summary(pl): Zbiór narzêdzi do baz danych  MS-Access (pliki mdb). 
Name: mdbtools
Version: 0.4
Release: 0.1
Copyright: GPL
Group: Development/Tools
Source0: http://download.sourceforge.net/mdbtools/%{name}-%{version}.tar.gz
URL: http://mdbtools.sourceforge.net/
BuildRoot:      %{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define         _prefix         /usr


%description
mdb-dump   -- simple hex dump utility for looking at mdb files
mdb-schema -- prints DDL for the specified table
mdb-export -- export table to CSV format
mdb-tables -- a simple dump of table names to be used with shell scripts
mdb-header -- generates a C header to be used in exporting mdb data to a C prog.
mdb-parsecvs -- generates a C program given a CSV file made with mdb-export
mdb-sql -- demo SQL engine program


%prep
%setup -q

%build
%configure2_13
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS COPYING COPYING.LIB INSTALL README TODO NEWS
%attr(755,root,root) %{_bindir}/*
%dir %{_libdir}/*
