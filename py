# /tmp/updateSecurityCustomProperties_with_AdminTask_check.py
import sys
import os
import re

# If no file path is provided, use a default path.
if len(sys.argv) < 2:
    propertiesFile = "/tmp/default.properties"
    print "No properties file argument provided. Using default properties file: " + propertiesFile
else:
    propertiesFile = sys.argv[-1].strip()

# Normalize the properties file path.
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
    Parse and return a dictionary {prop1: value1, ...}.
    """
    propStr = propStr.strip()
    if propStr.startswith("[") and propStr.endswith("]"):
        propStr = propStr[1:-1].strip()
    props = {}
    # Find all [name value] pairs using regex.
    pairs = r
