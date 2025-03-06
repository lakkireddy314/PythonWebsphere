# updateSecurityCustomProperties.py
import sys
import os

print "sys.argv:", sys.argv

if len(sys.argv) < 1:
    print "Usage: wsadmin.sh -lang jython -f updateSecurityCustomProperties.py <securityPropertiesFile>"
    sys.exit(1)

# Use the last argument as the properties file path.
propertiesFile = sys.argv[-1]
print "Using security properties file: %s" % propertiesFile

def loadProperties(filename):
    """
    Load properties from a file into a dictionary.
    Lines starting with '#' or blank lines are skipped.
    """
    if not os.path.exists(filename):
        print "Property file not found: %s" % filename
        sys.exit(1)
    
    props = {}
    try:
        f = open(filename, "r")
        lines = f.readlines()
        f.close()
        for line in lines:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if '=' not in line:
                print "Skipping invalid property line: %s" % line
                continue
            key, value = line.split('=', 1)
            props[key.strip()] = value.strip()
    except Exception, e:
        print "Error reading file: %s" % e
        sys.exit(1)
    return props

print "Loading properties from: %s" % propertiesFile
properties = loadProperties(propertiesFile)

# Retrieve the Security configuration object.
security = AdminConfig.getid("/Security:/")
if not security:
    print "Security configuration not found. Exiting."
    sys.exit(1)

# Retrieve existing custom property settings using the "Property" datatype.
existingProps = {}
customProps = AdminConfig.list("Property", security)
if customProps:
    # If customProps is a string, split it into a list;
    # if it's already a list, use it directly;
    # otherwise, wrap it in a list.
    if type(customProps) == type(''):
        cp_list = customProps.splitlines()
    elif type(customProps) == type([]):
        cp_list = customProps
    else:
        cp_list = [customProps]
        
    for cp in cp_list:
        name = AdminConfig.showAttribute(cp, "name")
        existingProps[name] = cp

# Iterate through each property from the file.
for key, value in properties.items():
    if key in existingProps:
        print "Security custom property '%s' already exists. Skipping." % key
    else:
        params = [['name', key], ['value', value]]
        newProp = AdminConfig.create("Property", security, params)
        print "Created security custom property '%s' with value '%s'" % (key, value)
        AdminConfig.save()
