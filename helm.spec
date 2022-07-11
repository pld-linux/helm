%define		vendor_version	3.9.0

Summary:	The Kubernetes Package Manager
Name:		helm
Version:	3.9.0
Release:	1
License:	Apache v2.0
Group:		Applications
Source0:	https://github.com/helm/helm/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	b1d13b6f0dcc04a4142673963d02cf56
Source1:	%{name}-vendor-%{vendor_version}.tar.xz
# Source1-md5:	8684380701fb8a0a43d3d2870a940b79
URL:		https://helm.sh/
BuildRequires:	golang >= 1.16
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 2.009
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
ExclusiveArch:	%go_arches
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_debugsource_packages	0

%description
Helm is a tool for managing Charts. Charts are packages of
pre-configured Kubernetes resources.

Use Helm to:
- Find and use popular software packaged as Helm Charts to run in
  Kubernetes
- Share your own applications as Helm Charts
- Create reproducible builds of your Kubernetes applications
- Intelligently manage your Kubernetes manifest files
- Manage releases of Helm packages

%package -n bash-completion-helm
Summary:	Bash completion for helm command line
Group:		Applications/Shells
Requires:	%{name} = %{version}-%{release}
Requires:	bash-completion >= 2.0
BuildArch:	noarch

%description -n bash-completion-helm
Bash completion for helm command line.

%package -n fish-completion-helm
Summary:	fish-completion for helm
Group:		Applications/Shells
Requires:	%{name} = %{version}-%{release}
Requires:	fish
BuildArch:	noarch

%description -n fish-completion-helm
fish-completion for helm.

%package -n zsh-completion-helm
Summary:	ZSH completion for helm command line
Group:		Applications/Shells
Requires:	%{name} = %{version}-%{release}
Requires:	zsh
BuildArch:	noarch

%description -n zsh-completion-helm
ZSH completion for helm command line.

%prep
%setup -q -a1

%{__mv} %{name}-%{vendor_version}/vendor .

%build
ldflags="\
	-X helm.sh/helm/v3/internal/version.version=%{version} \
	-X helm.sh/helm/v3/internal/version.metadata= \
	-X helm.sh/helm/v3/internal/version.gitCommit= \
"
%__go build -v -mod=vendor -ldflags="$ldflags" -o target/helm ./cmd/helm

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{bash_compdir},%{fish_compdir},%{zsh_compdir}}
install -p target/helm $RPM_BUILD_ROOT%{_bindir}

./target/helm completion bash > $RPM_BUILD_ROOT%{bash_compdir}/helm
./target/helm completion fish > $RPM_BUILD_ROOT%{fish_compdir}/helm.fish
./target/helm completion zsh > $RPM_BUILD_ROOT%{zsh_compdir}/_helm

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/helm

%files -n bash-completion-helm
%defattr(644,root,root,755)
%{bash_compdir}/helm

%files -n fish-completion-helm
%defattr(644,root,root,755)
%{fish_compdir}/helm.fish

%files -n zsh-completion-helm
%defattr(644,root,root,755)
%{zsh_compdir}/_helm
