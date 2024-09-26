def get_deployment_manager_hostname():
    """Function to get the Deployment Manager's hostname"""
    try:
        # Find the Deployment Manager object in the WebSphere environment
        dmgr_object = AdminControl.completeObjectName('type=DeploymentManager,*')
        if dmgr_object:
            # Get the hostname attribute of the Deployment Manager
            hostname = AdminControl.getAttribute(dmgr_object, 'host')
            print(f"Deployment Manager Hostname: {hostname}")
        else:
            print("Deployment Manager not found.")
    except:
        print("Error retrieving Deployment Manager hostname.")

def get_node_agents_hostnames():
    """Function to get the hostnames of all Node Agents"""
    try:
        # Find all Node Agent objects in the WebSphere environment
        node_agents = AdminControl.queryNames('type=NodeAgent,*').splitlines()
        if node_agents:
            for node_agent in node_agents:
                # Get the node agent's host and node name
                hostname = AdminControl.getAttribute(node_agent, 'host')
                node_name = AdminControl.getAttribute(node_agent, 'nodeName')
                print(f"Node Agent Hostname for {node_name}: {hostname}")
        else:
            print("No Node Agents found.")
    except:
        print("Error retrieving Node Agents hostnames.")

# Main script execution
if __name__ == '__main__':
    print("Fetching Deployment Manager and Node Agents hostnames...")
    get_deployment_manager_hostname()
    get_node_agents_hostnames()
