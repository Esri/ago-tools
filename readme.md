agolTools
=========

A Python package to assist with administering ArcGIS Online Organizations.

## Sample usage
 
#### Create a spreadsheet of all users in the org
	import csv
    from agolTools import admin
    myAgol = admin.admin()
    users = myAgol.getUsers()

    outputDir = 'c:/temp'
    outputFile = outputDir + '/users.csv'

    with open(outputFile, 'wb') as outputFile:
        dataWriter = csv.writer(outputFile, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        # Write header row.
        dataWriter.writerow(['Full Name', 'Username', 'Role'])
        #Write user data.
        for user in users:
            dataWriter.writerow([user['fullName'], user['username'], user['role']])