#
# Conditional build:
%bcond_with	doc	# Sphinx documentation (not included in sdist)
%bcond_with	tests	# unit tests (not included in sdist)

Summary:	Extended CommonMark compliant parser with bridges to docutils and Sphinx
Summary(pl.UTF-8):	Rozszerzony parser zgodny z CommonMark z interfejsami do docutils i Sphinksa
Name:		python3-myst_parser
Version:	4.0.0
Release:	5
License:	MIT
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/myst-parser/
Source0:	https://pypi.debian.net/myst-parser/myst_parser-%{version}.tar.gz
# Source0-md5:	e702667009f8e1d054d0de2718276384
Patch0:		myst_parser-deps.patch
URL:		https://pypi.org/project/myst-parser/
BuildRequires:	python3-build
BuildRequires:	python3-flit_core >= 3.4
BuildRequires:	python3-flit_core < 4
BuildRequires:	python3-modules >= 1:3.10
BuildRequires:	python3-installer
%if %{with tests}
BuildRequires:	python3-PyYAML
BuildRequires:	python3-Sphinx >= 7
BuildRequires:	python3-Sphinx < 9
BuildRequires:	python3-bs4
BuildRequires:	python3-defusedxml
BuildRequires:	python3-docutils >= 0.19
BuildRequires:	python3-docutils < 0.22
BuildRequires:	python3-jinja2
BuildRequires:	python3-markdown-it-py >= 3.0
BuildRequires:	python3-markdown-it-py < 4
BuildRequires:	python3-mdit-py-plugins >= 0.4.1
BuildRequires:	python3-mdit-py-plugins < 0.5
BuildRequires:	python3-pytest >= 8
BuildRequires:	python3-pytest < 9
BuildRequires:	python3-pytest-cov
BuildRequires:	python3-pytest-param-files >= 0.6.0
BuildRequires:	python3-pytest-param-files < 0.7
BuildRequires:	python3-pytest-regressions
BuildRequires:	python3-sphinx_pytest
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 2.044
%if %{with doc}
BuildRequires:	python3-ipython
BuildRequires:	python3-sphinx_autodoc2 >= 0.5.0
BuildRequires:	python3-sphinx_autodoc2 < 0.6
BuildRequires:	python3-sphinx_book_theme >= 1.1
BuildRequires:	python3-sphinx_book_theme < 2
BuildRequires:	python3-sphinx_copybutton
BuildRequires:	python3-sphinx_design
BuildRequires:	python3-sphinx_panels >= 0.5.2
BuildRequires:	python3-sphinx_pyscript
BuildRequires:	python3-sphinx_tippy >= 0.4.3
BuildRequires:	python3-sphinx_togglebutton
BuildRequires:	python3-sphinxcontrib-bibtex >= 2.1
# disabled in pyproject.toml (as of 4.0.0)
#BuildRequires:	python3-sphinxcontrib-mermaid >= 0.7.1
#BuildRequires:	python3-sphinxcontrib-mermaid < 0.8
BuildRequires:	python3-sphinxext-opengraph >= 0.9.0
BuildRequires:	python3-sphinxext-opengraph < 0.10
BuildRequires:	python3-sphinxext-rediraffe >= 0.2.7
BuildRequires:	python3-sphinxext-rediraffe < 0.3
BuildRequires:	sphinx-pdg-3 >= 7
%endif
Requires:	python3-modules >= 1:3.10
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
%setup -q -n myst_parser-%{version}
%patch -P0 -p1

%build
%py3_build_pyproject

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

%py3_install_pyproject

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGELOG.md LICENSE README.md
%attr(755,root,root) %{_bindir}/myst-anchors
%attr(755,root,root) %{_bindir}/myst-docutils-demo
%attr(755,root,root) %{_bindir}/myst-docutils-html
%attr(755,root,root) %{_bindir}/myst-docutils-html5
%attr(755,root,root) %{_bindir}/myst-docutils-latex
%attr(755,root,root) %{_bindir}/myst-docutils-pseudoxml
%attr(755,root,root) %{_bindir}/myst-docutils-xml
%attr(755,root,root) %{_bindir}/myst-inv
%{py3_sitescriptdir}/myst_parser
%{py3_sitescriptdir}/myst_parser-%{version}.dist-info

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/build/html/*
%endif
