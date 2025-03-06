# updateGlobalSecurityCustomProperties.py
import sys
import os

if len(sys.argv) != 2:
    print "Usage: wsadmin.sh -lang jython -f updateGlobalSecurityCustomProperties.py <globalCustom.properties>"
    sys.exit(1)

propertiesFile = sys.argv[1]

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

# Retrieve the global security configuration object.
security = AdminConfig.getid("/Security:/")
if not security:
    print "Global Security configuration not found. Exiting."
    sys.exit(1)

# Retrieve existing global security custom properties using "Property" as the datatype.
existingProps = {}
customProps = AdminConfig.list("Property", security)
if customProps:
    for cp in customProps.splitlines():
        name = AdminConfig.showAttribute(cp, "name")
        existingProps[name] = cp

# Iterate through each property from the file.
for key, value in properties.iteritems():
    if key in existingProps:
        print "Property '%s' already exists. Skipping." % key
    else:
        params = [['name', key], ['value', value]]
        newProp = AdminConfig.create("Property", security, params)
        print "Created global security property '%s' with value '%s'" % (key, value)
        AdminConfig.save()
