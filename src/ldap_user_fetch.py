from ldap3 import Server, Connection, ALL, SUBTREE

# LDAP server details
ldap_server = 'ldap://localhost'  # Adjust if needed
base_dn = 'dc=mycompany,dc=local'  # Base DN to search
admin_dn = 'cn=Manager,dc=mycompany,dc=local'  # LDAP admin user DN
password = 'butcher'  # Admin user password

def get_user_by_uid(uid):
    try:
        # Connect to the LDAP server
        server = Server(ldap_server, get_info=ALL)
        conn = Connection(server, user=admin_dn, password=password, auto_bind=True)

        # Search for the user with the specified uid
        search_filter = f'(uid={uid})'
        conn.search(base_dn, search_filter, search_scope=SUBTREE, attributes=['*'])

        # Check if the user was found
        if conn.entries:
            for entry in conn.entries:
                print(entry)
        else:
            print(f"No user found with uid: {uid}")

    except Exception as e:
        print("An error occurred:", e)

    finally:
        # Ensure the connection is properly closed
        if conn.bound:
            conn.unbind()

# Example usage
user_uid = 'ajohnson'  # Replace with the actual uid
get_user_by_uid(user_uid)
