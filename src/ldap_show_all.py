from ldap3 import Server, Connection, ALL, SUBTREE

# Set up the LDAP server and connection
ldap_server = 'ldap://localhost'  # Adjust this if needed
base_dn = 'dc=mycompany,dc=local'  # Base DN to search
user_dn = 'cn=Manager,dc=mycompany,dc=local'  # LDAP admin user
password = 'butcher'  # Admin user password

# Connect to the LDAP server
server = Server(ldap_server, get_info=ALL)
connection = Connection(server, user=user_dn, password=password, auto_bind=True)

# Perform an LDAP search
search_filter = '(objectclass=*)'  # Filter to match all objects
search_scope = SUBTREE  # Search the entire subtree

# Execute the search
connection.search(base_dn, search_filter, search_scope, attributes=['*'])

# Print the results
for entry in connection.entries:
    print(entry)

# Close the connection
connection.unbind()
