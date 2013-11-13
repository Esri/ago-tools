#### Migrate person to a new account within the same Org

# Requires admin role
# Useful when migrating to Enterprise Logins.
# Reassigns all items/groups to new owner and
# adds userTo to all groups which userFrom is a member.'''

from agoTools.admin import Admin
myAgol = Admin('<username>')  # Replace <username> your ADMIN account

# for migrating a single account...
myAgol.migrateAccount(myAgol, '<userFrom>', '<userTo>')   # Replace with usernames between which you are moving items

# for migrating a batch of accounts...
myAgol.migrateAccounts(myAgol, <path to user mapping CSV>)   # Replace with path to CSV file with col1=userFrom, col2=userTo