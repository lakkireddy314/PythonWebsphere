# This script should be run with WebSphere's wsadmin tool using the Jython language

def get_deployment_manager_hostname():
    """Retrieve the Deployment Manager hostname."""
    try:
        # Query the Deployment Manager MBean object
        dmgr_object = AdminControl.completeObjectName('type=DeploymentManager,*')
        if dmgr_object:
            # Get the host attribute (hostname) of the Deployment Manager
            hostname = AdminControl.getAttribute(dmgr_object, 'host')
            print("Deployment Manager Hostname:" + hostname)
        else:
            print("Deployment Manager not found.")
    except Exception as e:
        print(f"Error retrieving Deployment Manager hostname: {str(e)}")


def get_node_agents_hostnames():
    """Retrieve the hostnames of all Node Agents."""
    try:
        # Query the Node Agent MBean objects
        node_agents = AdminControl.queryNames('type=NodeAgent,*').splitlines()
        if node_agents:
            for node_agent in node_agents:
                # Get the host and node name attributes for each Node Agent
                hostname = AdminControl.getAttribute(node_agent, 'host')
                node_name = AdminControl.getAttribute(node_agent, 'nodeName')
                print("Node Agent Hostname for"+ node_name + ":" + hostname)
        else:
            print("No Node Agents found.")
    except Exception as e:
        print(f"Error retrieving Node Agents hostnames: {str(e)}")


# Main function to run the hostname retrieval
if __name__ == '__main__':
    print("Fetching Deployment Manager and Node Agents hostnames...")
    get_deployment_manager_hostname()
    get_node_agents_hostnames()
