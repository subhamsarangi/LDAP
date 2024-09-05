# LDAP - Lightweight Directory Access Protocol

## INSTALL LDAP AND START SERVICE
sudo apt-get install ldap-utils slapd
sudo dpkg-reconfigure slapd
sudo systemctl start slapd.service


## FIREWALL EXCEPTION FOR EXTERNAL CONNECTIONS
sudo ufw allow ldap


## EDIT CONFIG FILE
sudo nano /etc/ldap/ldap.conf

```
BASE     dc=mycompany,dc=local
URI      ldap://localhost
```
or 
```
BASE     dc=rpa,dc=ibm,dc=com
URI      ldap://rpa.ibm.com
```