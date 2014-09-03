# Requires admin role.
import csv, time,sys,arcpy
from agoTools.admin import Admin
adminAccount = arcpy.GetParameterAsText(0)
adminPassword =arcpy.GetParameterAsText(1)
className = arcpy.GetParameterAsText(2)
classSnippet = arcpy.GetParameterAsText(3)
csvFile = arcpy.GetParameterAsText(4)
userPrefix = arcpy.GetParameterAsText(5)
userPassword = arcpy.GetParameterAsText(6)
userRole = arcpy.GetParameterAsText(7)
instructorAccount = arcpy.GetParameterAsText(8)
provider = "arcgis"

if not adminAccount:
    adminAccount = "your ago account"
if not adminPassword:
    adminPassword = "your ago password"
if not className:
    className = "Sample Class"
if not classSnippet:
    classSnippet = "Snippet goes here"
if not csvFile:
    csvFile = r"C:\students.csv"
if not userPrefix:
    userPrefix = "labUser_"
if not userPassword:
    userPassword = "password1"
if not userRole:
    userRole = "account_user"
if not provider:
    provider = "arcgis"

##Unicode is not encoding properly so convert all arcpy params
adminAccount = str(adminAccount)
adminPassword = str(adminPassword)
className = str(className)
classSnippet = str(classSnippet)
userPrefix = str(userPrefix)
userPassword = str(userPassword)
userRole = str(userRole)
provider = str(provider)

arcpy.AddMessage("Logging in...")
try:
    agoAdmin = Admin(adminAccount,password=adminPassword)
except:
    arcpy.AddError("Login failed. Please re-enter your admin username and password.")
    sys.exit()


##Get roles from the portal so we can translate the user-entered name to the role id that the api needs.
##Also confirm that the user-entered role is valid.
allRoles = agoAdmin.getRoles()
##getRoles doesn't return predefined system roles, so we'll add those
roles = {'Administrator':'org_admin', 'Publisher':'org_publisher', 'Author':'org_author', 'User':'org_viewer'}
for role in allRoles:
    roles[role["name"]] = role["id"]
if not userRole in roles.keys():
    arcpy.AddError(userRole + " is not a valid role.")
    sys.exit()

roleId =roles[userRole]

arcpy.AddMessage("Creating Group...")
print "Creating Group..."
group = agoAdmin.createGroup(className,classSnippet)
description = "Lab account for " + className

if "group" in group:
    groupId = group["group"]["id"]
    arcpy.AddMessage("Creating Users...")
    print "Creating Users..."
    i = 1
    users = []
    sameNameCounter = 1

    with open(csvFile,"rb") as userFile:
        rows = csv.reader(userFile)
        for row in rows:
            userFirstName = row[0]
            userLastName = row[1]
            userEmail = row[2]
            username = userPrefix + "_" + userLastName

            if username in users:
                username += "_" + str(sameNameCounter)
                sameNameCounter +=1
            arcpy.AddMessage("creating " + username + "...")
            print "creating " + username + "..."
            agoAdmin.createUser(username,userPassword,userFirstName,userLastName,userEmail,description,roleId,provider)
            users.append(username)

    arcpy.AddMessage("Adding New Users to Group...")
    print "Adding Users to Group..."
    agoAdmin.addUsersToGroups(users,[groupId])
    if instructorAccount:
        arcpy.AddMessage("Reassigning group ownership to " + instructorAccount + "...")
        print "Reassigning group ownership to " + instructorAccount + "..."
        agoAdmin.reassignGroupOwnership(groupId,instructorAccount)
    print "Done"
else:
    arcpy.AddError("Failed to create group")
    arcpy.AddError(group["error"]["details"])
    print "Failed to create group: " + group["error"]["details"]

