# TODO:
# - move gmdb to /usr/X11R6/bin
# - add -gnome, -lib, -devel, -static subpackages
Summary:	Several utilities for using MS-Access .mdb files
Summary(pl):	Zbiór narzêdzi do u¿ywania plików MS-Access (.mdb)
Name:		mdbtools
Version:	0.4
Release:	0.2
License:	GPL
Group:		Development/Tools
Source0:	http://download.sourceforge.net/mdbtools/%{name}-%{version}.tar.gz
URL:		http://mdbtools.sourceforge.net/
BuildRequires:	readline-devel
BuildRequires:	unixODBC-devel
BuildRequires:	gnome-libs-devel
BuildRequires:	gtk+-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define         _prefix         /usr
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

%prep
%setup -q

%build
%configure2_13 \
	--enable-sql \
	--with-unixodbc=/usr
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS COPYING COPYING.LIB INSTALL README TODO NEWS
%attr(755,root,root) %{_bindir}/mdb*
%attr(755,root,root) %{_bindir}/pr*
%attr(755,root,root) %{_bindir}/unittest
#files gnome
%attr(755,root,root) %{_bindir}/gmdb
#files lib
%attr(755,root,root) %{_libdir}/libmdb*.so.*.*
#files devel
%{_includedir}
%{_libdir}/libmdb*.so
%{_libdir}/libmdb*.la
#files static
%{_libdir}/libmdb*.a
