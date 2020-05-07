# template: smart_proxy_plugin
%{?scl:%scl_package rubygem-%{gem_name}}
%{!?scl:%global pkg_name %{name}}

%{!?_root_datadir:%global _root_datadir %{_datadir}}
%{!?_root_localstatedir:%global _root_localstatedir %{_localstatedir}}
%{!?_root_sysconfdir:%global _root_sysconfdir %{_sysconfdir}}

%global gem_name smart-proxy-probing
%global plugin_name smart-proxy-probing

%global foreman_proxy_min_version 1.25
%global foreman_proxy_dir %{_root_datadir}/foreman-proxy
%global foreman_proxy_statedir %{_root_localstatedir}/foreman-proxy
%global foreman_proxy_bundlerd_dir %{foreman_proxy_dir}/bundler.d
%global foreman_proxy_settingsd_dir %{_root_sysconfdir}/foreman-proxy/settings.d
%global smart_proxy_dynflow_bundlerd_dir %{!?scl:/opt/theforeman/tfm/root}%{_datadir}/smart_proxy_dynflow_core/bundler.d

Name: %{?scl_prefix}rubygem-%{gem_name}
Version: 0.0.2
Release: 4%{?foremandist}%{?dist}
Summary: Gem to allow probing through smart-proxy
Group: Applications/Internet
License: GPLv3
URL: https://github.com/adamruzicka/smart-proxy-probing
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem

%if 0%{?rhel} == 7
Requires: tfm-rubygem(foreman_probing_core)
%else
Requires: rubygem(foreman_probing_core)
%endif

# start specfile generated dependencies
Requires: foreman-proxy >= %{foreman_proxy_min_version}
Requires: %{?scl_prefix_ruby}ruby(release)
Requires: %{?scl_prefix_ruby}ruby
Requires: %{?scl_prefix_ruby}ruby(rubygems)
Requires: %{?scl_prefix}rubygem(smart_proxy_dynflow) < 0.3.0
Requires: %{?scl_prefix}rubygem(smart_proxy_dynflow) >= 0.1.0
BuildRequires: %{?scl_prefix_ruby}ruby(release)
BuildRequires: %{?scl_prefix_ruby}ruby
BuildRequires: %{?scl_prefix_ruby}rubygems-devel
BuildArch: noarch
Provides: %{?scl_prefix}rubygem(%{gem_name}) = %{version}
Provides: foreman-proxy-plugin-%{plugin_name} = %{version}
# end specfile generated dependencies

%{?scl:Obsoletes: rubygem-%{gem_name}}

%description
Gem to allow probing through smart-proxy.


%package doc
Summary: Documentation for %{name}
Group: Documentation
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%{?scl:Obsoletes: rubygem-%{gem_name}-doc}

%description doc
Documentation for %{name}.

%prep
%{?scl:scl enable %{scl} - << \EOF}
gem unpack %{SOURCE0}
%{?scl:EOF}

%setup -q -D -T -n  %{gem_name}-%{version}

%{?scl:scl enable %{scl} - << \EOF}
gem spec %{SOURCE0} -l --ruby > %{gem_name}.gemspec
%{?scl:EOF}

%build
# Create the gem as gem install only works on a gem file
%{?scl:scl enable %{scl} - << \EOF}
gem build %{gem_name}.gemspec
%{?scl:EOF}

# %%gem_install compiles any C extensions and installs the gem into ./%%gem_dir
# by default, so that we can move it into the buildroot in %%install
%{?scl:scl enable %{scl} - << \EOF}
%gem_install
%{?scl:EOF}

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

# bundler file
mkdir -p %{buildroot}%{foreman_proxy_bundlerd_dir}
cat <<EOF > %{buildroot}%{foreman_proxy_bundlerd_dir}/%{plugin_name}.rb
gem 'smart-proxy-probing'
EOF

# sample config
mkdir -p %{buildroot}%{foreman_proxy_settingsd_dir}
mv %{buildroot}%{gem_instdir}/settings.d/probing.yml.example \
   %{buildroot}%{foreman_proxy_settingsd_dir}/probing.yml

mkdir -p %{buildroot}%{smart_proxy_dynflow_bundlerd_dir}
cat <<EOF > %{buildroot}%{smart_proxy_dynflow_bundlerd_dir}/foreman_probing_core.rb
gem 'foreman_probing_core'
EOF

%files
%dir %{gem_instdir}
%config(noreplace) %attr(0640, root, foreman-proxy) %{foreman_proxy_settingsd_dir}/probing.yml
%license %{gem_instdir}/LICENSE
%{gem_instdir}/bundler.plugins.d
%{gem_libdir}
%{gem_instdir}/settings.d
%{foreman_proxy_bundlerd_dir}/%{plugin_name}.rb
%exclude %{gem_cache}
%{gem_spec}
%{smart_proxy_dynflow_bundlerd_dir}/foreman_probing_core.rb

%files doc
%doc %{gem_docdir}


%changelog
* Tue Jan 07 2020 Eric D. Helms <ericdhelms@gmail.com> - 0.0.2-4
- Build for SCL

* Mon Dec 16 2019 Eric D. Helms <ericdhelms@gmail.com> - 0.0.2-3
- Update to SCL based template

* Thu May 16 2019 Eric D. Helms <ericdhelms@gmail.com> - 0.0.2-2
- Require SCL prefix only on EL7

* Thu Jul 19 2018 Dirk Goetz <dirk.goetz@netways.de> 0.0.2-1
- Add rubygem-smart-proxy-probing generated by gem2rpm using the smart_proxy_plugin template