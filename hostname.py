# Connect to the WebSphere Admin Service
# Assumes this script is run using wsadmin tool

# Import the required module
import AdminControl

# Get the deployment manager's process
def get_deployment_manager_hostname():
    dmgr_object = AdminControl.completeObjectName('type=DeploymentManager,*')
    if dmgr_object:
        host = AdminControl.getAttribute(dmgr_object, 'host')
        print("Deployment Manager Hostname: " + host)
    else:
        print("Deployment Manager not found.")

# Get the node agents' hostnames
def get_node_agents_hostnames():
    node_agents = AdminControl.queryNames('type=NodeAgent,*').splitlines()
    if node_agents:
        for node_agent in node_agents:
            host = AdminControl.getAttribute(node_agent, 'host')
            node_name = AdminControl.getAttribute(node_agent, 'nodeName')
            print(f"Node Agent Hostname for {node_name}: {host}")
    else:
        print("No Node Agents found.")

# Main execution
if __name__ == "__main__":
    print("Fetching Deployment Manager and Node Agents hostnames...")
    get_deployment_manager_hostname()
    get_node_agents_hostnames()
