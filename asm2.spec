Summary:	A code manipulation tool to implement adaptable systems
Summary(pl):	Narzêdzie do obróbki kodu do implementowania systemów adaptacyjnych
Name:		asm2
Version:	2.1
Release:	0.1
License:	BSD-style
Group:		Development/Languages/Java
Source0:	http://download.forge.objectweb.org/asm/asm-%{version}.tar.gz
# Source0-md5:	dfd62160a88f13e236f9da7d2485c9ec
Source1:	http://asm.objectweb.org/current/asm-eng.pdf
# Source1-md5:	5f17bfac3563feb108793575f74ce27c
Source2:	http://asm.objectweb.org/doc/faq.html
# Source2-md5:	556c0df057bced41517491784d556acc
URL:		http://asm.objectweb.org/
BuildRequires:	ant
BuildRequires:	objectweb-anttask
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
ASM is a code manipulation tool to implement adaptable systems.

%description -l pl
ASM to narzêdzie do obróbki kodu do implementowania systemów
adaptacyjnych.

%package javadoc
Summary:	Javadoc for %{name}
Summary(pl):	Dokumentacja javadoc dla pakietu %{name}
Group:		Documentation

%description javadoc
Javadoc for %{name}.

%description javadoc -l pl
Dokumentacja javadoc dla pakietu %{name}.

%prep
%setup -q -n asm-%{version}
find . -name "*.jar" -exec rm -f {} \;
install -m 644 %{SOURCE1} .
install -m 644 %{SOURCE2} .

%build
ant -Dobjectweb.ant.tasks.path=$(build-classpath objectweb-anttask) jar jdoc

%install
rm -rf $RPM_BUILD_ROOT

# jars
install -d $RPM_BUILD_ROOT%{_javadir}/%{name}

for jar in output/dist/lib/*.jar; do
	newjar=$(echo $jar | sed /asm-/asm2-/)
	install ${jar} $RPM_BUILD_ROOT%{_javadir}/%{name}/`basename ${newjar}`
done

cd $RPM_BUILD_ROOT%{_javadir}/%{name}
for jar in *-%{version}*; do
	ln -sf ${jar} $(echo $jar | sed -e s/-%{version}//)
done
cd -

# javadoc
install -d $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
cp -pr output/dist/doc/javadoc/user/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
cd $RPM_BUILD_ROOT%{_javadocdir}
ln -sf %{name}-%{version} %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post javadoc
rm -f %{_javadocdir}/%{name}
ln -s %{name}-%{version} %{_javadocdir}/%{name}

%postun javadoc
if [ $1 -eq 0 ]; then
	rm -f %{_javadocdir}/%{name}
fi

%files
%defattr(644,root,root,755)
%doc README.txt faq.html asm-eng.pdf
%dir %{_javadir}/%{name}
%{_javadir}/%{name}/*.jar

%files javadoc
%defattr(644,root,root,755)
%dir %{_javadocdir}/%{name}-%{version}
%{_javadocdir}/%{name}-%{version}/*
%ghost %dir %{_javadocdir}/%{name}
