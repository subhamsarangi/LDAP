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

### note: to change things in OpenLDAP, create LDIF files with information about what you want to change. Do not edit the LDIF files in the /etc/ldap/slapd.d or /etc/openldap/slapd.d manually.


## CREATE PASSWORD HASH
slappasswd
> {SSHA}AxNb1aLz4GFHvcxDFHOGy+4RIfCder8y


## STEPS TO RUN LDIF
create ldif file -> run ldap command


## ROOT USER (olcRootDN)
nano rootpw.ldif
```
dn: olcDatabase={1}mdb,cn=config
changetype: modify
add: olcRootPW
olcRootPW: {SSHA}AxNb1aLz4GFHvcxDFHOGy+4RIfCder8y
```
ldapadd -Y EXTERNAL -H ldapi:/// -f rootpw.ldif


## DELETE ROOT USER
nano remove_rootpw.ldif
```
dn: olcDatabase={1}mdb,cn=config
changetype: modify
delete: olcRootPW
```
ldapmodify -Y EXTERNAL -H ldapi:/// -f remove_rootpw.ldif


## IMPORT BASIC LDAP SCHEMAS
ldapadd -Y EXTERNAL -H ldapi:/// -f /etc/ldap/schema/cosine.ldif

ldapadd -Y EXTERNAL -H ldapi:/// -f /etc/ldap/schema/nis.ldif

ldapadd -Y EXTERNAL -H ldapi:/// -f /etc/ldap/schema/inetorgperson.ldif

ldapadd -Y EXTERNAL -H ldapi:/// -f /etc/ldap/schema/openldap.ldif

ldapadd -Y EXTERNAL -H ldapi:/// -f /etc/ldap/schema/dyngroup.ldif


## MANAGER USER
nano manager.ldif
```
dn: olcDatabase={1}mdb,cn=config
changetype: modify
replace: olcSuffix
olcSuffix: dc=mycompany,dc=local

dn: olcDatabase={1}mdb,cn=config
changetype: modify
replace: olcRootDN
olcRootDN: cn=Manager,dc=mycompany,dc=local

dn: olcDatabase={1}mdb,cn=config
changetype: modify
add: olcRootPW
olcRootPW: {SSHA}AxNb1aLz4GFHvcxDFHOGy+4RIfCder8y
```
ldapmodify -Y EXTERNAL -H ldapi:/// -f manager.ldif


## ORG GROUPS
nano org.ldif
```
dn: dc=mycompany,dc=local
objectClass: top
objectClass: dcObject
objectclass: organization
o: My LDAP Server
dc: mycompany

dn: cn=Manager,dc=mycompany,dc=local
objectClass: organizationalRole
cn: Manager
description: LDAP Manager

dn: ou=ldapusers,dc=mycompany,dc=local
objectClass: organizationalUnit
ou: ldapUsers
```
ldapadd -x -D cn=Manager,dc=mycompany,dc=local -W -f org.ldif


## REGISTER USER
nano addUserName.ldif
```
dn: cn=User Name,dc=mycompany,dc=local
changetype: add
objectClass: inetOrgPerson
objectClass: organizationalPerson
objectClass: person
objectClass: top
uid: subham
cn: Subham Sarangi
sn: subham
displayName: Subham Sarangi
mail: subham@yopmail.com
userPassword: {SSHA}pIfHfUUd1dLDvy3JJWINodLy0Fan+3zb
```
ldapadd -D "cn=Manager,dc=mycompany,dc=local" -W -f addUserName.ldif


## MODIFY USER
nano modifyUserName.ldif
```
dn: cn=User Name,dc=mycompany,dc=local
changetype: modify
replace: cn
cn: New Name
```
ldapmodify -D "cn=Manager,dc=mycompany,dc=local" -W -f modifyUserName.ldif


## TEST 
ldapsearch -x -H ldap://localhost -b dc=mycompany,dc=local
ldapsearch -x -b "dc=mycompany,dc=local" "(objectclass=*)"

#### does not work 
ldapsearch -Y EXTERNAL -H ldapi:/// -b "cn=config" "(olcRootPW=*)"

### docs:
https://ibm.com/docs/en/rpa/23.0?topic=ldap-installing-configuring-openldap
