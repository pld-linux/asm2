Summary:	A code manipulation tool to implement adaptable systems
Summary(pl.UTF-8):	Narzędzie do obróbki kodu do implementowania systemów adaptacyjnych
Name:		asm2
Version:	2.2.3
Release:	1
License:	BSD-style
Group:		Development/Languages/Java
Source0:	http://download.forge.objectweb.org/asm/asm-%{version}.tar.gz
# Source0-md5:	7a92c87bf067925685cf68dcc0dd8998
Source1:	http://asm.objectweb.org/current/asm-eng.pdf
# Source1-md5:	5f17bfac3563feb108793575f74ce27c
Source2:	http://asm.objectweb.org/doc/faq.html
# Source2-md5:	cca9b825cf4398addb909bd1fa217a70
URL:		http://asm.objectweb.org/
BuildRequires:	ant
BuildRequires:	jpackage-utils
BuildRequires:	objectweb-anttask
BuildRequires:	rpm-javaprov
BuildRequires:	rpmbuild(macros) >= 1.300
Requires:	jpackage-utils
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
ASM is a code manipulation tool to implement adaptable systems.

%description -l pl.UTF-8
ASM to narzędzie do obróbki kodu do implementowania systemów
adaptacyjnych.

%package javadoc
Summary:	Javadoc for %{name}
Summary(pl.UTF-8):	Dokumentacja javadoc dla pakietu %{name}
Group:		Documentation
Requires:	jpackage-utils

%description javadoc
Javadoc for %{name}.

%description javadoc -l pl.UTF-8
Dokumentacja javadoc dla pakietu %{name}.

%prep
%setup -q -n asm-%{version}
find -name '*.jar' | xargs rm -vf
install -m 644 %{SOURCE1} .
install -m 644 %{SOURCE2} .

install -d test/lib

%build
export LC_ALL=en_US # source not in ASCII
%ant jar jdoc \
	-Dobjectweb.ant.tasks.path=$(build-classpath objectweb-anttask)

%install
rm -rf $RPM_BUILD_ROOT

# jars
install -d $RPM_BUILD_ROOT%{_javadir}/%{name}

for a in output/dist/lib/*.jar; do
	jar=${a##*/}
	jar2=asm2-${jar#asm-}
	cp -a output/dist/lib/$jar $RPM_BUILD_ROOT%{_javadir}/$jar2
	ln -s $jar2 $RPM_BUILD_ROOT%{_javadir}/${jar2%%-%{version}.jar}.jar
done

# javadoc
install -d $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
cp -pr output/dist/doc/javadoc/user/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
ln -s %{name}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{name} # ghost symlink

%clean
rm -rf $RPM_BUILD_ROOT

%post javadoc
ln -sf %{name}-%{version} %{_javadocdir}/%{name}

%files
%defattr(644,root,root,755)
%doc README.txt faq.html asm-eng.pdf
%{_javadir}/*.jar

%files javadoc
%defattr(644,root,root,755)
%{_javadocdir}/%{name}-%{version}
%ghost %{_javadocdir}/%{name}
