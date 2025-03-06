# /tmp/updateSecurityCustomProperties_with_AdminTask_check.py
import sys
import os
import re

# Check that a properties file path is provided.
if len(sys.argv) != 2:
    print "Usage: wsadmin.sh -lang jython -f /tmp/updateSecurityCustomProperties_with_AdminTask_check.py <properties_file_path>"
    sys.exit(1)

# Normalize the properties file path (expands ~ and converts to absolute path).
propertiesFile = sys.argv[1].strip()
propertiesFile = os.path.abspath(os.path.expanduser(propertiesFile))
print "Using properties file: " + propertiesFile

def loadProperties(filename):
    """
    Read properties from a file and return a dictionary.
    Each valid line should be in the format: name=value.
    Blank lines or lines starting with '#' are ignored.
    """
    if not os.path.exists(filename):
        print "Property file not found: " + filename
        sys.exit(1)
    props = {}
    try:
        f = open(filename, "r")
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" not in line:
                print "Skipping invalid property line: " + line
                continue
            key, value = line.split("=", 1)
            props[key.strip()] = value.strip()
        f.close()
    except Exception, e:
        print "Error reading file: " + str(e)
        sys.exit(1)
    return props

def parseActiveCustomProperties(propStr):
    """
    Given a string of active custom properties in the format:
      [[prop1 value1] [prop2 value2] ...]
    parse and return a dictionary {prop1: value1, ...}.
    """
    propStr = propStr.strip()
    if propStr.startswith("[") and propStr.endswith("]"):
        propStr = propStr[1:-1].strip()
    props = {}
    # Find all [name value] pairs using regex.
    pairs = re.findall(r'\[([^\]]+)\]', propStr)
    for pair in pairs:
        parts = pair.split()
        if len(parts) >= 2:
            name = parts[0]
            value = " ".join(parts[1:])
            props[name] = value
    return props

# Load new properties from the file.
newProps = loadProperties(propertiesFile)
print "New properties from file:", newProps

# Retrieve the current active security custom properties as a string.
activeStr = AdminTask.showActiveSecuritySettings("[-customProperties]")
print "Active custom properties string:", activeStr

# Parse active properties into a dictionary.
activeProps = {}
if activeStr and activeStr.strip() != "":
    activeProps = parseActiveCustomProperties(activeStr)
print "Active properties parsed:", activeProps

# Merge active properties with new ones.
# Only add a new property if its name does not exist already.
combinedProps = activeProps.copy()
for key, value in newProps.items():
    if key in activeProps:
        print "Property '%s' already exists with value '%s'. Skipping." % (key, activeProps[key])
    else:
        combinedProps[key] = value
        print "Adding property '%s' with value '%s'." % (key, value)

# Build the custom properties string for the command.
# Each property is formatted as [name value].
customPropsList = []
for key, value in combinedProps.items():
    customPropsList.append("[" + key + " " + value + "]")
customPropsStr = "[" + " ".join(customPropsList) + "]"
cmd = "[-customProperties " + customPropsStr + "]"
print "Executing AdminTask.setAdminActiveSecuritySettings with parameters:", cmd

# Execute the command and save the configuration.
AdminTask.setAdminActiveSecuritySettings(cmd)
AdminConfig.save()

print "Security custom properties updated successfully."
