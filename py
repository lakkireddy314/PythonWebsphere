# updateGlobalSecurityCustomProperties.py
import sys
import os

# Debug: print all arguments to see what wsadmin is passing
print "sys.argv:", sys.argv

if len(sys.argv) < 1:
    print "Usage: wsadmin.sh -lang jython -f updateGlobalSecurityCustomProperties.py <globalCustom.properties>"
    sys.exit(1)

# Use the last argument as the properties file.
propertiesFile = sys.argv[-1]
print "Using properties file: %s" % propertiesFile

def loadProperties(filename):
    """
    Load properties from a file into a dictionary.
    Lines starting with '#' or empty lines are skipped.
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

# Sanity check: ensure that properties is a dict
if not isinstance(properties, dict):
    print "Loaded properties is not a dictionary!"
    sys.exit(1)

# Retrieve the global security configuration object.
security = AdminConfig.getid("/Security:/")
if not security:
    print "Global Security configuration not found. Exiting."
    sys.exit(1)

# Retrieve existing global security custom properties using the "Property" datatype.
existingProps = {}
customProps = AdminConfig.list("Property", security)

# Normalize customProps into a list:
if customProps:
    if hasattr(customProps, "splitlines"):
        cp_list = customProps.splitlines()
    elif isinstance(customProps, list):
        cp_list = customProps
    else:
        cp_list = [customProps]
    for cp in cp_list:
        name = AdminConfig.showAttribute(cp, "name")
        existingProps[name] = cp

# Iterate through each property from the file.
for key, value in properties.items():
    if key in existingProps:
        print "Property '%s' already exists. Skipping." % key
    else:
        params = [['name', key], ['value', value]]
        newProp = AdminConfig.create("Property", security, params)
        print "Created global security property '%s' with value '%s'" % (key, value)
        AdminConfig.save()
