# template: default
%global gem_name statsd-instrument

Name: rubygem-%{gem_name}
Version: 2.9.2
Release: 1%{?dist}
Summary: A StatsD client for Ruby apps
License: MIT
URL: https://github.com/Shopify/statsd-instrument
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem

# start specfile generated dependencies
Requires: ruby
BuildRequires: ruby
BuildRequires: rubygems-devel
BuildArch: noarch
# end specfile generated dependencies

%description
A StatsD client for Ruby apps. Provides metaprogramming methods to inject
StatsD instrumentation into your code.


%package doc
Summary: Documentation for %{name}
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{name}.

%prep
%setup -q -n  %{gem_name}-%{version}

%build
# Create the gem as gem install only works on a gem file
gem build ../%{gem_name}-%{version}.gemspec

# %%gem_install compiles any C extensions and installs the gem into ./%%gem_dir
# by default, so that we can move it into the buildroot in %%install
%gem_install

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

%files
%dir %{gem_instdir}
%exclude %{gem_instdir}/.github
%exclude %{gem_instdir}/.gitignore
%exclude %{gem_instdir}/.rubocop-https---shopify-github-io-ruby-style-guide-rubocop-yml
%exclude %{gem_instdir}/.rubocop.yml
%exclude %{gem_instdir}/.yardopts
%license %{gem_instdir}/LICENSE
%{gem_libdir}
%exclude %{gem_instdir}/shipit.rubygems.yml
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/CHANGELOG.md
%doc %{gem_instdir}/CONTRIBUTING.md
%{gem_instdir}/Gemfile
%doc %{gem_instdir}/README.md
%{gem_instdir}/Rakefile
%exclude %{gem_instdir}/statsd-instrument.gemspec
%{gem_instdir}/benchmark
%{gem_instdir}/test

%changelog
* Tue Jul 26 2022 Ewoud Kohl van Wijngaarden <ewoud@kohlvanwijngaarden.nl> - 2.9.2-1
- Update to 2.9.2

* Thu Mar 11 2021 Eric D. Helms <ericdhelms@gmail.com> - 2.1.4-4
- Rebuild against rh-ruby27

* Wed Apr 08 2020 Zach Huntington-Meath <zhunting@redhat.com> - 2.1.4-3
- Bump to release for EL8

* Wed Sep 05 2018 Eric D. Helms <ericdhelms@gmail.com> - 2.1.4-2
- Rebuild for Rails 5.2 and Ruby 2.5

* Thu Apr 05 2018 Ewoud Kohl van Wijngaarden <ewoud@kohlvanwijngaarden.nl> 2.1.4-1
- Add rubygem-statsd-instrument generated by gem2rpm using the scl template

