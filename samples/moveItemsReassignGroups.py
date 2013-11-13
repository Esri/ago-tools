#### Move all items from one account to another, reassign ownership of all groups, or add user to another user's groups

# Requires admin role
# If you want to do all three tasks at once, see migrateAccount or migrateAccounts functions

from agoTools.admin import Admin
agoAdmin = Admin(<username>)  # Replace <username> with your admin username

agoAdmin.reassignAllUser1ItemsToUser2(agoAdmin, <userFrom>, <userTo>)  #Replace with your current and new account usernames
agoAdmin.reassignAllGroupOwnership(agoAdmin, <userFrom>, <userTo>)
agoAdmin.addUser2ToAllUser1Groups(agoAdmin, <userFrom>, <userTo>)