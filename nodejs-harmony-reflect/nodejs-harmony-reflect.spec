%global npm_name harmony-reflect
%global enable_tests 0

Name: nodejs-%{npm_name}
Version: 1.5.1
Release: 1%{?dist}
Summary: ES5 shim for ES6 (ECMAScript 6) Reflect and Proxy objects
License: (Apache-2.0 OR MPL-1.1)
URL: https://github.com/tvcutsem/harmony-reflect
Source0: https://registry.npmjs.org/%{npm_name}/-/%{npm_name}-%{version}.tgz
BuildRequires: nodejs-packaging
BuildArch:  noarch
ExclusiveArch: %{nodejs_arches} noarch

%{?nodejs_find_provides_and_requires}

%define npm_cache_dir /tmp/npm_cache_%{name}-%{version}-%{release}
%description
%{summary}

%prep
%setup -q -n package

%build

%install
mkdir -p %{buildroot}%{nodejs_sitelib}/%{npm_name}
cp -pfr README.md index.d.ts package.json reflect.js %{buildroot}%{nodejs_sitelib}/%{npm_name}

%nodejs_symlink_deps

%clean
rm -rf %{buildroot} %{npm_cache_dir}

%if 0%{?enable_tests}
%check
%{nodejs_symlink_deps} --check
%endif

%files
%{nodejs_sitelib}/%{npm_name}

%doc README.md

%changelog
