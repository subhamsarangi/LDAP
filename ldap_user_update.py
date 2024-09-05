from ldap3 import Server, Connection, ALL, MODIFY_REPLACE

# LDAP server details
ldap_server = 'ldap://localhost'  # Adjust if needed
base_dn = 'dc=mycompany,dc=local'  # Base DN to search
admin_dn = 'cn=Manager,dc=mycompany,dc=local'  # LDAP admin user
password = 'butcher'  # Admin user password

# Connect to the LDAP server
server = Server(ldap_server, get_info=ALL)
admin_connection = Connection(server, user=admin_dn, password=password, auto_bind=True)

# DN of the entry to modify
dn_to_modify = 'cn=New Name,dc=mycompany,dc=local'

# Perform the modification
changes = {'cn': [(MODIFY_REPLACE, ['Subham Sharangi'])]}

# Execute the modification
admin_connection.modify(dn_to_modify, changes)

if admin_connection.result['description'] == 'success':
    print("Success: cn attribute updated!")
else:
    print("Failure:", admin_connection.result)

# Close the connection
admin_connection.unbind()
