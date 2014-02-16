Name:		ocsshmenu
Version:	1.1
Release:        1
Summary:	Pythonmenu for easy handling of ssh-connecions from a configfile.
License:	GPL
URL:		https://github.com/Rendanic/pythonmenu/tree/master/sshmenu
BuildArch:      noarch
BuildRoot:      %{_tmppath}/%{name}-build
Group:          System/Tools
Vendor:         Thorsten Bruhns (thorsten.bruhns@opitz-consulting.de)


#BuildRequires:	
Requires:	newt-python


# Turn off the brp-python-bytecompile script
%global __os_install_post %(echo '%{__os_install_post}' | sed -e 's!/usr/lib[^[:space:]]*/brp-python-bytecompile[[:space:]].*$!!g')

%description
Pythonmenu for easy handling of ssh-connections.
The scripts requires a parameter for a configuration file.
An example is at /usr/share/doc/ocsshmenu-%{version}/hostlist.cfg
This tool needs the Python Module snack.

%prep
wget -nc https://github.com/Rendanic/pythonmenu/raw/master/sshmenu/sshmenu.py
wget -nc https://github.com/Rendanic/pythonmenu/raw/master/sshmenu/hostlist.cfg

%install
mkdir -p $RPM_BUILD_ROOT/usr/bin
install -m 755 sshmenu.py $RPM_BUILD_ROOT/usr/bin


%clean
rm -rf $RPM_BUILD_ROOT
rm -rf %{_tmppath}/%{name}
rm -rf %{_topdir}/BUILD/%{name}


%files
%defattr(-,root,root)
/usr/bin/sshmenu.py
%doc hostlist.cfg



%changelog
* Sun Feb 16 2014 Thorsten Bruhns <thorsten.bruhns@opitz-consulting.de> (1.1)
    - turn off byte compile while building the RPM
* Sun Dec 15 2013 Thorsten Bruhns <thorsten.bruhns@opitz-consulting.de> (1.0)
    - initial release
