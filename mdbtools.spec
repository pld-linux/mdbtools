#
# Conditional build:
%bcond_without	odbc	# ODBC driver
#
Summary:	Several utilities for using MS-Access .mdb files
Summary(pl.UTF-8):	Zbiór narzędzi do używania plików MS-Access (.mdb)
Name:		mdbtools
Version:	1.0.0
Release:	1
License:	LGPL v2+ (library), GPL v2+ (gmdb2)
Group:		Development/Tools
#Source0Download: https://github.com/mdbtools/mdbtools/releases
Source0:	https://github.com/brianb/mdbtools/releases/download/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	9925e13cc70f3693c1e358da8ea750e5
Patch0:		%{name}-odbc-dir.patch
URL:		http://mdbtools.sourceforge.net/
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake
BuildRequires:	bison >= 3
BuildRequires:	flex
BuildRequires:	glib2-devel >= 2.0.0
BuildRequires:	libtool >= 2:2
BuildRequires:	pkgconfig
BuildRequires:	readline-devel
BuildRequires:	rpmbuild(macros) >= 1.673
BuildRequires:	txt2man
%{?with_odbc:BuildRequires:	unixODBC-devel >= 2.0.0}
Requires:	%{name}-libs = %{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_includedir	%{_prefix}/include/mdb

%description
- mdb-dump - simple hex dump utility for looking at mdb files
- mdb-schema - prints DDL for the specified table
- mdb-export - export table to CSV format
- mdb-tables - a simple dump of table names to be used with shell
  scripts
- mdb-header - generates a C header to be used in exporting mdb data
  to a C program
- mdb-parsecsv - generates a C program given a CSV file made with
  mdb-export
- mdb-sql - demo SQL engine program

%description -l pl.UTF-8
- mdb-dump - proste narzędzie do robienia szesnastkowych zrzutów baz,
  służące do oglądania plików mdb
- mdb-schema - wypisuje DDL dla podanej tabeli
- mdb-export - eksportuje tabelę do formatu CSV
- mdb-tables - prosty zrzut nazw tabel do używania w skryptach powłoki
- mdb-header - generuje nagłówki C, do używania przy eksportowaniu
  danych mdb do programu w C
- mdb-parsecsv - generuje program w C na podstawie pliki CSV
  zrobionego przy użyciu mdb-export
- mdb-sql - program demonstracyjny silnika SQL

%package libs
Summary:	Shared libraries for mdbtools
Summary(pl.UTF-8):	Biblioteki współdzielone mdbtools
Group:		Libraries
Conflicts:	mdbtools < 0.6-0.pre1.3

%description libs
Shared libraries for mdbtools.

%description libs -l pl.UTF-8
Biblioteki współdzielone mdbtools.

%package devel
Summary:	Header files for mdb library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki mdb
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description devel
Header files for mdb library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki mdb.

%package static
Summary:	Static mdb library
Summary(pl.UTF-8):	Statyczna biblioteka mdb
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static mdb library.

%description static -l pl.UTF-8
Statyczna biblioteka mdb.

%package odbc
Summary:	MDB Tools ODBC driver for unixODBC
Summary(pl.UTF-8):	Sterownik ODBC do MDB dla unixODBC
Group:		Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	unixODBC >= 2.0.0

%description odbc
MDB Tools ODBC driver for unixODBC.

%description odbc -l pl.UTF-8
Sterownik ODBC do MDB dla unixODBC.

%prep
%setup -q
%patch0 -p1

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__automake}
%configure \
	--disable-silent-rules \
	--enable-sql \
	--with-bash-completion-dir=%{bash_compdir} \
	%{?with_odbc:--with-unixodbc=/usr}

%{__make} -j1

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/{libmdb,libmdbsql}.la

%if %{with odbc}
# ODBC libraries are meant to be dlopened
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libmdbodbc*.{la,a}
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%post	odbc -p /sbin/ldconfig
%postun	odbc -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS NEWS README.md
%attr(755,root,root) %{_bindir}/mdb-*
%{_mandir}/man1/mdb-*.1*
%{bash_compdir}/mdb-*

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libmdb.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libmdb.so.3
%attr(755,root,root) %{_libdir}/libmdbsql.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libmdbsql.so.3

%files devel
%defattr(644,root,root,755)
%doc HACKING.md
%attr(755,root,root) %{_libdir}/libmdb.so
%attr(755,root,root) %{_libdir}/libmdbsql.so
%{_includedir}
%{_pkgconfigdir}/libmdb.pc
%{_pkgconfigdir}/libmdbsql.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libmdb.a
%{_libdir}/libmdbsql.a

%if %{with odbc}
%files odbc
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libmdbodbc.so
%attr(755,root,root) %{_libdir}/libmdbodbcW.so
%endif
