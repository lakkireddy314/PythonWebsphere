# /tmp/updateSecurityCustomProperties_with_AdminTask_check.py
import sys
import os
import re

print "DEBUG: Starting script execution."

# If no file argument is provided, use a default file.
if len(sys.argv) < 2:
    propertiesFile = "/tmp/default.properties"
    print "DEBUG: No properties file argument provided. Using default properties file: " + propertiesFile
else:
    propertiesFile = sys.argv[-1].strip()

# Normalize the properties file path.
propertiesFile = os.path.abspath(os.path.expanduser(propertiesFile))
print "DEBUG: Using properties file: " + propertiesFile

def loadProperties(filename):
    """
    Read properties from a file and return a dictionary.
    Each valid line should be in the format: name=value.
    Blank lines or lines starting with '#' are ignored.
    This function reads the entire file content at once.
    """
    print "DEBUG: Loading properties from file: " + filename
    if not os.path.exists(filename):
        print "ERROR: Property file not found: " + filename
        sys.exit(1)
    props = {}
    try:
        f = open(filename, "r")
        content = f.read()
        f.close()
        # Split the content into lines.
        lines = content.splitlines()
        index = 0
        for line in lines:
            try:
                line = line.strip()
                if not line or line.startswith("#"):
                    index += 1
                    continue
                if "=" not in line:
                    print "DEBUG: Skipping invalid property line (no '=' found) at line %d: %s" % (index, line)
                    index += 1
                    continue
                key, value = line.split("=", 1)
                props[key.strip()] = value.strip()
            except Exception, e:
                print "ERROR: Exception processing line %d: %s; Exception: %s" % (index, line, e)
            index += 1
        print "DEBUG: Finished loading properties: " + str(props)
    except Exception, e:
        print "ERROR: Exception while reading file: " + str(e)
        sys.exit(1)
    return props

def parseActiveCustomProperties(propStr):
    """
    Given a string of active custom properties in the format:
      [[prop1 value1] [prop2 value2] ...]
    Parse and return a dictionary {prop1: value1, ...}.
    """
    print "DEBUG: Parsing active custom properties string."
    propStr = propStr.strip()
    if propStr.startswith("[") and propStr.endswith("]"):
        propStr = propStr[1:-1].strip()
    props = {}
    # Find all [name value] pairs using regex.
    pairs = re.findall(r'\[([^\]]+)\]', propStr)
    print "DEBUG: Found property pairs: " + str(pairs)
    for pair in pairs:
        parts = pair.split()
        if len(parts) >= 2:
            name = parts[0]
            value = " ".join(parts[1:])
            props[name] = value
    print "DEBUG: Parsed active properties: " + str(props)
    return props

# Load new properties from the file.
newProps = loadProperties(propertiesFile)
print "DEBUG: New properties loaded:", newProps

# Retrieve the current active security custom properties as a string.
try:
    activeStr = AdminTask.showActiveSecuritySettings("[-customProperties]")
    print "DEBUG: Active custom properties string retrieved:", activeStr
except Exception, e:
    print "ERROR: Exception while retrieving active custom properties: " + str(e)
    sys.exit(1)

# Parse active properties into a dictionary.
activeProps = {}
if activeStr and activeStr.strip() != "":
    activeProps = parseActiveCustomProperties(activeStr)
print "DEBUG: Active properties dictionary:", activeProps

# Merge active properties with new ones.
combinedProps = activeProps.copy()
for key, value in newProps.items():
    if key in activeProps:
        print "DEBUG: Property '%s' already exists with value '%s'. Skipping." % (key, activeProps[key])
    else:
        combinedProps[key] = value
        print "DEBUG: Adding property '%s' with value '%s'." % (key, value)

print "DEBUG: Combined properties:", combinedProps

# Build the custom properties string for the command.
customPropsList = []
for key, value in combinedProps.items():
    customPropsList.append("[" + key + " " + value + "]")
customPropsStr = "[" + " ".join(customPropsList) + "]"
cmd = "[-customProperties " + customPropsStr + "]"
print "DEBUG: Command to be executed: " + cmd

# Execute the command and save the configuration.
try:
    print "DEBUG: Executing AdminTask.setAdminActiveSecuritySettings..."
    AdminTask.setAdminActiveSecuritySettings(cmd)
    print "DEBUG: Command executed successfully."
except Exception, e:
    print "ERROR: Exception while executing AdminTask.setAdminActiveSecuritySettings: " + str(e)
    sys.exit(1)

try:
    AdminConfig.save()
    print "DEBUG: Configuration saved successfully."
except Exception, e:
    print "ERROR: Exception while saving configuration: " + str(e)
    sys.exit(1)

print "DEBUG: Security custom properties updated successfully."
