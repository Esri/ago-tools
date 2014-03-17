# Requires admin role.
import csv, time
from agoTools.admin import Admin

agoAdmin = Admin(<username>) # Replace <username> with your admin username.
users = agoAdmin.getUsers()

outputFile = 'c:/temp/users.csv'

with open(outputFile, 'wb') as output:
    dataWriter = csv.writer(output, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    # Write header row.
    dataWriter.writerow(['Full Name', 'Email', 'Username', 'Role', 'Date Created'])
    # Write user data.
    for user in users:
        dataWriter.writerow([user['fullName'].encode('utf-8'), user['email'].encode('utf-8'), user['username'].encode('utf-8'), user['role'], time.strftime("%Y-%m-%d",time.gmtime(user['created']/1000))])
