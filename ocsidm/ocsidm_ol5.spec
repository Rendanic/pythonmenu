Name:		ocsidm
Version:	1.0
Release:        1
Summary:	Pythonmenu for easy handling of ORACLE_SIDs from /etc/oratab
License:	GPL
URL:		https://github.com/Rendanic/pythonmenu/tree/master/ocsidm
BuildArch:      noarch
BuildRoot:      %{_tmppath}/%{name}-build
Group:          Database/Tools
Vendor:         Thorsten Bruhns (thorsten.bruhns@opitz-consulting.de)


#BuildRequires:	
Requires:	newt-python

%description
Pythonmenu for easy handling of ORACLE_SIDs from /etc/oratab
This tool needs the Python Module snack.

%prep
wget -nc https://github.com/Rendanic/pythonmenu/raw/master/ocsidm/ocsidm.py

%build

%install
mkdir -p $RPM_BUILD_ROOT/usr/bin
install -m 755 ocsidm.py $RPM_BUILD_ROOT/usr/bin


%clean
rm -rf $RPM_BUILD_ROOT
rm -rf %{_tmppath}/%{name}
rm -rf %{_topdir}/BUILD/%{name}


%files
%defattr(-,root,root)
/usr/bin/ocsidm.py
%doc



%changelog
* Sun Dec 15 2013 Thorsten Bruhns <thorsten.bruhns@opitz-consulting.de> 
    - initial release
