from ldap3 import Server, Connection, ALL, SUBTREE

# Set up the LDAP server and connection
ldap_server = 'ldap://localhost'  # Adjust this if needed
base_dn = 'dc=mycompany,dc=local'  # Base DN to search
user_dn = 'cn=Manager,dc=mycompany,dc=local'  # LDAP admin user
password = 'butcher'  # Admin user password

# Connect to the LDAP server
server = Server(ldap_server, get_info=ALL)
connection = Connection(server, user=user_dn, password=password, auto_bind=True)

# Perform an LDAP search to get all users
search_filter = '(&(objectClass=inetOrgPerson))'  # Filter to match all users (inetOrgPerson)
search_scope = SUBTREE  # Search the entire subtree

# Execute the search
connection.search(base_dn, search_filter, search_scope, attributes=['cn', 'uid', 'mail'])

# Print the results (all users)
print("List of Users:")
for entry in connection.entries:
    print(f"User: {entry.cn}")
    if 'uid' in entry:
        print(f"  UID: {entry.uid}")
    if 'mail' in entry:
        print(f"  Email: {entry.mail}")

# Close the connection
connection.unbind()
