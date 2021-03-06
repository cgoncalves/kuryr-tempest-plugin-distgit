%global service kuryr
%global plugin kuryr-tempest-plugin
%global module kuryr_tempest_plugin
%global with_doc 0

%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

%if 0%{?fedora}
%global with_python3 1
%endif

%global common_desc \
This package contains Tempest tests to cover the kuryr-kubernetes project. \
Additionally it provides a plugin to automatically load these tests into Tempest.

Name:       python-%{service}-tests-tempest
Version:    0.1.0
Release:    1%{?dist}
Summary:    Tempest Integration of Kuryr and Kuryr-Kubernetes
License:    ASL 2.0
URL:        https://git.openstack.org/cgit/openstack/%{plugin}/

Source0:    http://tarballs.openstack.org/%{plugin}/%{plugin}-%{upstream_version}.tar.gz

BuildArch:  noarch

%description
%{common_desc}

%package -n python2-%{service}-tests-tempest
Summary: %{summary}
%{?python_provide:%python_provide python2-%{service}-tests-tempest}
BuildRequires:  python2-devel
BuildRequires:  python-pbr
BuildRequires:  python-setuptools
BuildRequires:  git
BuildRequires:  openstack-macros
BuildRequires:  python2-reno

Requires:   python-pbr
Requires:   python-six  >= 1.9.0
Requires:   python-tempest >= 1:12.2.0
Requires:   python-testrepository
Requires:   python-oslotest >= 1.10.0
Requires:   python-os-testr >= 0.8.0
Requires:   python-testtools
Requires:   python-kubernetes
# NOTE: 2.0.0 is not yet available in RDO repos. will specify version when
# that's done.
# Requires:   python-kubernetes >= 2.0.0

%description -n python2-%{service}-tests-tempest
%{common_desc}

%if 0%{?with_doc}
%package -n python-%{service}-tests-tempest-doc
Summary:        python-%{service}-tests-tempest documentation

BuildRequires:  python-sphinx
BuildRequires:  python-oslo-sphinx

%description -n python-%{service}-tests-tempest-doc
It contains the documentation for the example tempest tests.
%endif

%if 0%{?with_python3}
%package -n python3-%{service}-tests-tempest
Summary: %{summary}
%{?python_provide:%python_provide python3-%{service}-tests-tempest}
BuildRequires:  python3-devel
BuildRequires:  python3-pbr
BuildRequires:  python3-setuptools
BuildRequires:  python3-reno

Requires:   python3-pbr
Requires:   python3-six  >= 1.9.0
#Requires:   python3-tempest >= 1:12.2.0
Requires:   python3-testrepository
Requires:   python3-oslotest >= 1.10.0
Requires:   python3-os-testr >= 0.8.0
Requires:   python3-testtools
#Requires:   python3-kubernetes
# There are no python3 packages yet for the commented ones.

%description -n python3-%{service}-tests-tempest
%{common_desc}
%endif

%prep
%autosetup -n %{plugin}-%{upstream_version} -S git

# Let's handle dependencies ourseleves
%py_req_cleanup
# Remove bundled egg-ingo
rm -rf %{module}.egg-info

%build
%if 0%{?with_python3}
%py3_build
%endif
%py2_build

# Generate Docs
%if 0%{?with_doc}
%{__python2} setup.py build_sphinx
# remove the sphinx build leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}
%endif

%install
%if 0%{?with_python3}
%py3_install
%endif
%py2_install

%files -n python2-%{service}-tests-tempest
%license LICENSE
%doc README.rst
%{python2_sitelib}/%{module}
%{python2_sitelib}/*.egg-info

%if 0%{?with_python3}
%files -n python3-%{service}-tests-tempest
%license LICENSE
%doc README.rst
%{python3_sitelib}/%{module}
%{python3_sitelib}/*.egg-info
%endif

%if 0%{?with_doc}
%files -n python-%{service}-tests-tempest-doc
%doc doc/build/html
%license LICENSE
%endif

%changelog
* Wed Aug 30 2017 Chandan Kumar <chkumar@redhat.com> 0.1.0-1
- Update to 0.1.0
