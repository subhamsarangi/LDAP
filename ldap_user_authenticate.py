from ldap3 import Server, Connection, ALL, SUBTREE, NTLM
from getpass import getpass

# LDAP server details
ldap_server = 'ldap://localhost'  # Adjust if needed
base_dn = 'dc=mycompany,dc=local'  # Base DN to search

# Get email and password from user
email = input("Enter email: ")
password = getpass("Enter password: ")

# Connect to the LDAP server (anonymous bind to search for user DN)
server = Server(ldap_server, get_info=ALL)
connection = Connection(server, auto_bind=True)

# Search for the user by email
search_filter = f'(mail={email})'  # LDAP filter to search by email
connection.search(base_dn, search_filter, search_scope=SUBTREE, attributes=['cn', 'mail', 'uid'])

if connection.entries:
    user_dn = connection.entries[0].entry_dn  # Get the user DN
    print(f"User found: {user_dn}")
    
    # Try to bind (authenticate) with the found DN and the provided password
    user_connection = Connection(server, user=user_dn, password=password, auto_bind=False)
    
    if user_connection.bind():
        print("Success: Authentication successful!")
        user_connection.unbind()
    else:
        print("Failure: Invalid email or password!")
else:
    print("Failure: User not found!")

# Close the search connection
connection.unbind()
