# manage-puppet-node-groups

This is a Python script to create groups of nodes on a Puppet server.

To use the script, it is necessary to have Python installed on the machine. The script also requires a valid authentication token for the Puppet server and the Puppet server URL.

The script has a main function called main() which is responsible for creating groups of nodes on the Puppet server. The arguments of this function are:

PUPPETSERVER_URL: The URL of the Puppet server. The default value is "https://puppet.test.com.br:4433".
PRODUCT_NAME: The name of the product for which the nodes will be created.
BREWZONE_NAME: The name of the zone where the nodes will be created.
TOKEN: The authentication token for the Puppet server.


The main function consumes the following functions:


1 - get_nodes(token, puppet_server_url)
This function is responsible for making a GET request to the Puppet Server API to obtain a list of registered nodes.
It takes two parameters: an authentication token and the Puppet Server URL. Returns a JSON object with node data.

2 - filter_node_equals(nodes, parameter, value)
This function receives three parameters: a JSON object containing the node data, a parameter to be used for filtering and the value to be searched.
The function filters the list of nodes, returning a new list containing only those nodes that have the desired value in the specified parameter.

3 - filter_node_contains(nodes, parameter, value)
Similar to the previous function, it takes three parameters. However, instead of fetching only exact values, this function filters the nodes that contain the specified value in a given property.

4 - create_product_name_parent_node2_payload(product_name, environment, env_identifier, azure_subscription_id, parent_node_id)
This function takes five parameters: the product name, the environment, an environment identifier, the Azure subscription ID, and the parent node ID.
Returns a JSON object with a payload that will be used to create a node group on Puppet Server.

5 - create_product_node_payload(product_name, parent_node_id)
It takes two parameters: the product name and the ID of the parent node. Returns a JSON object with a payload that will be used to create a node group on Puppet Server.

6 - create_product_node_env_payload(product_name, environment, env_identifier, parent_node_id)
It takes four parameters: the product name, the environment, an environment identifier, and the parent node ID. Returns a JSON object with a payload that will be used to create a node group on Puppet Server.

7 - create_node_group(token, payload, puppet_server_url)
This role is responsible for creating a node group on the Puppet Server. It takes three parameters: an authentication token, a payload containing group information, and the Puppet Server URL. Returns a response from the Puppet Server API indicating the success or failure of creating the group.


It is important to note that this script was developed for a specific scenario and may need adjustments to be used in other environments.
