#
# Conditional build:
%bcond_without gnome	# without gui package
%bcond_without odbc	# without odbc package
#
Summary:	Several utilities for using MS-Access .mdb files
Summary(pl):	Zbiór narzêdzi do u¿ywania plików MS-Access (.mdb)
Name:		mdbtools
Version:	0.5
Release:	0.1
License:	LGPL (library), GPL (gmdb2)
Group:		Development/Tools
Source0:	http://dl.sourceforge.net/mdbtools/%{name}-%{version}.tar.gz
# Source0-md5:	4a18bf96e67161101cade64526756d22
Patch0:		%{name}-glib.patch
URL:		http://mdbtools.sourceforge.net/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	glib2-devel >= 2.0.0
%{?with_gnome:BuildRequires:	libglade2-devel >= 2.0.0}
%{?with_gnome:BuildRequires:	libgnomeui-devel >= 2.0.0}
BuildRequires:	libtool
BuildRequires:	readline-devel
%{?with_odbc:BuildRequires:	unixODBC-devel >= 2.0.0}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_includedir	%{_prefix}/include/mdb

%description
* mdb-dump - simple hex dump utility for looking at mdb files
* mdb-schema - prints DDL for the specified table
* mdb-export - export table to CSV format
* mdb-tables - a simple dump of table names to be used with shell
  scripts
* mdb-header - generates a C header to be used in exporting mdb data
  to a C program
* mdb-parsecsv - generates a C program given a CSV file made with
  mdb-export
* mdb-sql - demo SQL engine program

%description -l pl
* mdb-dump - proste narzêdzie do robienia szesnastkowych zrzutów baz,
  s³u¿±ce do ogl±dania plików mdb
* mdb-schema - wypisuje DDL dla podanej tabeli
* mdb-export - eksportuje tabelê do formatu CSV
* mdb-tables - prosty zrzut nazw tabel do u¿ywania w skryptach pow³oki
* mdb-header - generuje nag³ówki C, do u¿ywania przy eksportowaniu
  danych mdb do programu w C
* mdb-parsecsv - generuje program w C na podstawie pliki CSV
  zrobionego przy u¿yciu mdb-export
* mdb-sql - program demonstracyjny silnika SQL

%package devel
Summary:	Header files for mdb library
Summary(pl):	Pliki nag³ówkowe biblioteki mdb
Group:		Development/Libraries
Requires:	%{name} = %{version}

%description devel
Header files for mdb library.

%description devel -l pl
Pliki nag³ówkowe biblioteki mdb.

%package static
Summary:	Static mdb library
Summary(pl):	Statyczna biblioteka mdb
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}

%description static
Static mdb library.

%description static -l pl
Statyczna biblioteka mdb.

%package odbc
Summary:	MDB Tools ODBC driver for unixODBC
Summary(pl):	Sterownik ODBC do MDB dla unixODBC
Group:		Libraries
Requires:	%{name} = %{version}
Requires:	unixODBC >= 2.0.0

%description odbc
MDB Tools ODBC driver for unixODBC.

%description odbc -l pl
Sterownik ODBC do MDB dla unixODBC.

%package gui
Summary:	gmdb2 - graphical interface for MDB Tools
Summary(pl):	gmdb2 - graficzny interfejs do narzêdzi MDB
Group:		Applications/Databases
Requires:	%{name} = %{version}
Requires:	glib2 >= 2.0.0
Requires:	libglade2 >= 2.0.0
Requires:	libgnomeui >= 2.0.0

%description gui
gmdb2 - graphical interface for MDB Tools.

%description gui -l pl
gmdb2 - graficzny interfejs do narzêdzi MDB.

%prep
%setup -q
%patch -p1

%build
rm -f acinclude.m4
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__automake}
%configure \
		--enable-sql \
%{?with_odbc:	--with-unixodbc=/usr}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%find_lang gmdb --with-gnome

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%post	odbc -p /sbin/ldconfig
%postun	odbc -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README TODO doc/faq.html
%attr(755,root,root) %{_bindir}/mdb-*
%attr(755,root,root) %{_bindir}/pr*
%attr(755,root,root) %{_bindir}/updrow
%attr(755,root,root) %{_libdir}/libmdb.so.*.*
%attr(755,root,root) %{_libdir}/libmdbsql.so.*.*
%{_mandir}/man1/mdb-*.1*

%files devel
%defattr(644,root,root,755)
%doc HACKING
%attr(755,root,root) %{_libdir}/libmdb*.so
%{_libdir}/libmdb*.la
%{_includedir}

%files static
%defattr(644,root,root,755)
%{_libdir}/libmdb*.a

%if %{with odbc}
%files odbc
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/unittest
%attr(755,root,root) %{_libdir}/libmdbodbc.so.*.*
%endif

%if %{with gnome}
%files gui -f gmdb.lang
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/gmdb2
%{_datadir}/gmdb
%endif
