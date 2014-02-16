Name:		ocsidm
Version:	1.1
Release:        1
Summary:	Pythonmenu for easy handling of ORACLE_SIDs from /etc/oratab
License:	GPL
URL:		https://github.com/Rendanic/pythonmenu/tree/master/ocsidm
BuildArch:      noarch
BuildRoot:      %{_tmppath}/%{name}-build
Group:          Database/Tools
Vendor:         Thorsten Bruhns (thorsten.bruhns@opitz-consulting.com)


#BuildRequires:	
#Requires:	newt-python

# Turn off the brp-python-bytecompile script
%global __os_install_post %(echo '%{__os_install_post}' | sed -e 's!/usr/lib[^[:space:]]*/brp-python-bytecompile[[:space:]].*$!!g')

%description
Pythonmenu for easy handling of ORACLE_SIDs from /etc/oratab.
The script reads /etc/oratab. Only SIDs with existing PFile or SPFile in $ORACLE_HOME/dbs are listed!
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
* Sun Feb 16 2014 Thorsten Bruhns <thorsten.bruhns@opitz-consulting.com> (1.1)
    - turn off byte compile while building the RPM
* Sun Dec 15 2013 Thorsten Bruhns <thorsten.bruhns@opitz-consulting.com> (1.0)
    - initial release
