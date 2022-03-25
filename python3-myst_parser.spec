#
# Conditional build:
%bcond_with	doc	# Sphinx documentation (not included in sdist)
%bcond_with	tests	# unit tests (not included in sdist)

Summary:	Extended CommonMark compliant parser with bridges to docutils and Sphinx
Summary(pl.UTF-8):	Rozszerzony parser zgodny z CommonMark z interfejsami do docutils i Sphinksa
Name:		python3-myst_parser
Version:	0.17.0
Release:	3
License:	MIT
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/myst-parser/
Source0:	https://files.pythonhosted.org/packages/source/m/myst-parser/myst-parser-%{version}.tar.gz
# Source0-md5:	06b63965cd30eeb7aa14d0779e5756a2
Patch0:		%{name}-docutils.patch
URL:		https://pypi.org/project/myst-parser/
BuildRequires:	python3-modules >= 1:3.7
BuildRequires:	python3-setuptools >= 1:46.4.0
%if %{with tests}
BuildRequires:	python3-PyYAML
BuildRequires:	python3-Sphinx >= 3.1
BuildRequires:	python3-Sphinx < 5
BuildRequires:	python3-bs4
BuildRequires:	python3-docutils >= 0.15
BuildRequires:	python3-docutils < 0.18
BuildRequires:	python3-jinja2
BuildRequires:	python3-markdown-it-py >= 1.0.0
BuildRequires:	python3-markdown-it-py < 3
BuildRequires:	python3-mdit-py-plugins >= 0.3.0
BuildRequires:	python3-pytest >= 6
BuildRequires:	python3-pytest-cov
BuildRequires:	python3-pytest-param-files >= 0.3.4
BuildRequires:	python3-pytest-regressions
BuildRequires:	python3-typing_extensions
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
BuildRequires:	sed >= 4.0
%if %{with doc}
BuildRequires:	python3-ipython
BuildRequires:	python3-sphinx_book_theme >= 0.1.0
BuildRequires:	python3-sphinx_panels >= 0.5.2
BuildRequires:	python3-sphinxcontrib-bibtex >= 2.1
BuildRequires:	python3-sphinxcontrib-mermaid >= 0.6.3
BuildRequires:	python3-sphinxext-opengraph >= 0.4.2
BuildRequires:	python3-sphinxext-rediraffe >= 0.2
BuildRequires:	sphinx-pdg-3
%endif
Requires:	python3-modules >= 1:3.7
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
MyST is a rich and extensible flavor of Markdown meant for technical
documentation and publishing.

%description -l pl.UTF-8
MyST to bogata i rozszerzalna odmiana notacji Markdown, przeznaczona
do dokumentacji i publikacji technicznych.

%package apidocs
Summary:	API documentation for Python myst_parser module
Summary(pl.UTF-8):	Dokumentacja API modułu Pythona myst_parser
Group:		Documentation

%description apidocs
API documentation for Python myst_parser module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu Pythona myst_parser.

%prep
%setup -q -n myst-parser-%{version}
%patch0 -p1

%{__sed} -i -e '/mdit-py-plugins/ s/~=/>=/' setup.cfg

%build
%py3_build

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
%{__python3} -m pytest tests
%endif

%if %{with doc}
cd docs
%{__python3} -m sphinx -W . build/html
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGELOG.md LICENSE README.md
%attr(755,root,root) %{_bindir}/myst-anchors
%attr(755,root,root) %{_bindir}/myst-docutils-html
%attr(755,root,root) %{_bindir}/myst-docutils-html5
%attr(755,root,root) %{_bindir}/myst-docutils-latex
%attr(755,root,root) %{_bindir}/myst-docutils-pseudoxml
%attr(755,root,root) %{_bindir}/myst-docutils-xml
%{py3_sitescriptdir}/myst_parser
%{py3_sitescriptdir}/myst_parser-%{version}-py*.egg-info

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/build/html/*
%endif
