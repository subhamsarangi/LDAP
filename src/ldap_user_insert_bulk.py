from ldap3 import Server, Connection, ALL
import hashlib
import base64
import os

# LDAP server details
ldap_server = 'ldap://localhost'  # Adjust if needed
admin_dn = 'cn=Manager,dc=mycompany,dc=local'  # LDAP admin user DN
password = 'butcher'  # Admin user password
base_dn = 'dc=mycompany,dc=local'  # Base DN for adding users

def generate_ssha_hash(password):
    # Generate a random salt
    salt = os.urandom(16)

    # Create SHA-1 hash of the password combined with the salt
    sha1 = hashlib.sha1(password.encode('utf-8') + salt).digest()

    # Create SSHA hash by combining SHA-1 hash and salt
    ssha = sha1 + salt

    # Encode SSHA hash in base64
    ssha_base64 = base64.b64encode(ssha).decode('utf-8')

    # Return SSHA hash in LDAP format
    return f'{{SSHA}}{ssha_base64}'

def add_users(users):
    try:
        # Connect to the LDAP server
        server = Server(ldap_server, get_info=ALL)
        conn = Connection(server, user=admin_dn, password=password, auto_bind=True)

        # Iterate through the user list and add each user
        for user in users:
            dn = f"cn={user['cn']},{base_dn}"
            attributes = {
                'objectClass': ['inetOrgPerson', 'organizationalPerson', 'person', 'top'],
                'cn': user['cn'],
                'sn': user['sn'],
                'uid': user['uid'],
                'displayName': user['displayName'],
                'mail': user['mail'],
                'userPassword': generate_ssha_hash(user['pwd'])
            }
            
            # Add the user to the directory
            conn.add(dn, attributes=attributes)
            
            if conn.result['description'] == 'success':
                print(f"Success: User {user['cn']} added!")
            else:
                print(f"Failed to add {user['cn']}: {conn.result['description']}")

    except Exception as e:
        print("An error occurred:", e)

    finally:
        # Ensure the connection is properly closed
        if conn.bound:
            conn.unbind()

# Example users to add
users = [
    {
        'cn': 'John Doe',
        'sn': 'Doe',
        'uid': 'jdoe',
        'displayName': 'John Doe',
        'mail': 'jdoe@example.com',
        'pwd': 'password1'
    },
    {
        'cn': 'Jane Smith',
        'sn': 'Smith',
        'uid': 'jsmith',
        'displayName': 'Jane Smith',
        'mail': 'jsmith@example.com',
        'pwd': 'password2'
    },
    {
        'cn': 'Alice Johnson',
        'sn': 'Johnson',
        'uid': 'ajohnson',
        'displayName': 'Alice Johnson',
        'mail': 'ajohnson@example.com',
        'pwd': 'password3'
    }
]

add_users(users)
