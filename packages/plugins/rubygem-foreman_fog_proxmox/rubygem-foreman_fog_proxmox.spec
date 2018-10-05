# FIXME:
#   1. Edit foreman requirement(s) and specify minimum version
#   2. Delete these lines
#
# Generated from foreman_fog_proxmox-0.5.2.gem by gem2rpm -*- rpm-spec -*-
# template: foreman_plugin
%{?scl:%scl_package rubygem-%{gem_name}}
%{!?scl:%global pkg_name %{name}}

%global gem_name foreman_fog_proxmox
%global plugin_name fog_proxmox
%global foreman_min_version FIXME

Name: %{?scl_prefix}rubygem-%{gem_name}
Version: 0.5.2
Release: 1%{?foremandist}%{?dist}
Summary: Foreman plugin that adds Proxmox VE compute resource using fog-proxmox
Group: Applications/Systems
License: GPL-3.0
URL: https://github.com/tristanrobert/foreman_proxmox
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem

# start generated dependencies
Requires: foreman >= %{foreman_min_version}
Requires: %{?scl_prefix_ruby}ruby(release)
Requires: %{?scl_prefix_ruby}ruby
Requires: %{?scl_prefix_ruby}ruby(rubygems)
Requires: %{?scl_prefix}rubygem(fog-proxmox) >= 0.5
Requires: %{?scl_prefix}rubygem(fog-proxmox) < 1
Requires: %{?scl_prefix}rubygem(deface)
BuildRequires: foreman-assets >= %{foreman_min_version}
BuildRequires: foreman-plugin >= %{foreman_min_version}
BuildRequires: %{?scl_prefix}rubygem(fog-proxmox) >= 0.5
BuildRequires: %{?scl_prefix}rubygem(fog-proxmox) < 1
BuildRequires: %{?scl_prefix}rubygem(deface)
BuildRequires: %{?scl_prefix_ruby}ruby(release)
BuildRequires: %{?scl_prefix_ruby}ruby
BuildRequires: %{?scl_prefix_ruby}rubygems-devel
BuildArch: noarch
Provides: %{?scl_prefix}rubygem(%{gem_name}) = %{version}
Provides: foreman-plugin-%{plugin_name} = %{version}
Provides: foreman-%{plugin_name} = %{version}
# end generated dependencies

%description
Foreman plugin adds Proxmox VE compute resource using fog-proxmox. It is
compatible with Foreman 1.17+.


%package doc
Summary: Documentation for %{pkg_name}
Group: Documentation
Requires: %{?scl_prefix}%{pkg_name} = %{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{pkg_name}.

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
cp -pa .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

%foreman_bundlerd_file
%foreman_precompile_plugin -s

%files
%dir %{gem_instdir}
%license %{gem_instdir}/LICENSE
%{gem_instdir}/app
%{gem_instdir}/config
%{gem_libdir}
%{gem_instdir}/locale
%exclude %{gem_cache}
%{gem_spec}
%{foreman_bundlerd_plugin}
%{foreman_assets_plugin}

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/README.md
%{gem_instdir}/Rakefile
%{gem_instdir}/test

%posttrans
%{foreman_restart}
exit 0

%changelog
* Fri Oct 05 2018 Tristan Robert <tristan.robert.44@gmail.com> 0.5.2-1
- Add rubygem-foreman_fog_proxmox generated by gem2rpm using the foreman_plugin template

