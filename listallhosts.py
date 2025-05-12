# listHostnamesComplete.py
# wsadmin Jython script to print <name>: <hostName> for
#   1. DMGR profiles
#   2. Node Agents
#   3. WebSphere Web Servers (via a dedicated function)

# Helper to drop a trailing ')' from wsadmin output entries
def strip_trailing_paren(s):
    if s.endswith(')'):
        return s[:-1]
    return s

# Function to print nodeName: hostName for DMGR and Node Agents
def printNodeHostMappings(entries):
    for entry in entries:
        cfgPath   = strip_trailing_paren(entry.split('(', 1)[1])
        nodePath  = cfgPath.split('|', 1)[0]
        parts     = nodePath.split('/')
        cellName  = parts[1]
        nodeName  = parts[3]
        nodeId    = AdminConfig.getid('/Cell:%s/Node:%s/' % (cellName, nodeName))
        hostName  = AdminConfig.showAttribute(nodeId, 'hostName')
        print '%s: %s' % (nodeName, hostName)

# Function to print WebServerName: hostName for Web servers
def printWebHostMappings(webEntries):
    for entry in webEntries:
        # Extract logical name and containment path
        webName = entry.split('(')[0]
        cfgPath = strip_trailing_paren(entry.split('(', 1)[1])
        nodePath = cfgPath.split('|', 1)[0]
        parts    = nodePath.split('/')
        cellName = parts[1]
        nodeName = parts[3]

        # 1) Get the Server config object for this WebServer
        serverId = AdminConfig.getid(
            '/Cell:%s/Node:%s/Server:%s/' % (cellName, nodeName, webName)
        )

        # 2) Try reading hostName from the ServerIndex child
        siEntries = AdminConfig.list('ServerIndex', serverId).splitlines()
        if siEntries:
            hostName = AdminConfig.showAttribute(siEntries[0], 'hostName')
        else:
            # Fallback: use the Node’s hostName
            nodeId   = AdminConfig.getid('/Cell:%s/Node:%s/' % (cellName, nodeName))
            hostName = AdminConfig.showAttribute(nodeId, 'hostName')

        print '%s: %s' % (webName, hostName)

# --- Main Execution ---

# 1. Deployment Manager (DMGR)
dmgrEntries      = AdminTask.listServers('[-serverType DEPLOYMENT_MANAGER]').splitlines()
printNodeHostMappings(dmgrEntries)

# 2. Node Agents
nodeAgentEntries = AdminTask.listServers('[-serverType NODE_AGENT]').splitlines()
printNodeHostMappings(nodeAgentEntries)

# 3. Web Servers
webEntries = AdminTask.listServers('[-serverType WEB_SERVER]').splitlines()
printWebHostMappings(webEntries)
