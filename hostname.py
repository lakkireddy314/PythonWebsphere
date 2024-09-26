def get_deployment_manager_hostname():
    """Retrieve the hostname of the Deployment Manager"""
    try:
        # Get the Deployment Manager MBean object
        dmgr_object = AdminControl.completeObjectName('type=DeploymentManager,*')
        if dmgr_object:
            # Fetch the hostname attribute
            hostname = AdminControl.getAttribute(dmgr_object, 'host')
            print(f"Deployment Manager Hostname: {hostname}")
        else:
            print("Deployment Manager not found.")
    except Exception as e:
        print("Error retrieving Deployment Manager hostname: {str(e)}")

def get_node_agents_hostnames():
    """Retrieve the hostnames of all Node Agents"""
    try:
        # Get the list of Node Agent MBean objects
        node_agents = AdminControl.queryNames('type=NodeAgent,*').splitlines()
        if node_agents:
            for node_agent in node_agents:
                # Fetch the hostname and node name attributes
                hostname = AdminControl.getAttribute(node_agent, 'host')
                node_name = AdminControl.getAttribute(node_agent, 'nodeName')
                print("Node Agent Hostname for {node_name}: {hostname}")
        else:
            print("No Node Agents found.")
    except Exception as e:
        print(f"Error retrieving Node Agents hostnames: {str(e)}")

# Main function to execute the script
if __name__ == '__main__':
    print("Fetching Deployment Manager and Node Agents hostnames...")
    get_deployment_manager_hostname()
    get_node_agents_hostnames()
