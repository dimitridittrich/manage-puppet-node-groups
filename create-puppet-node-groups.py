import os
import requests
import sys
import json
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def get_nodes(token, puppet_server_url):
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "X-Authentication": token
    }
    try:
        response = requests.get(
            f"{puppet_server_url}/classifier-api/v1/groups", headers=headers, verify=False)
        json_response = response.json()
        return json_response
    except:
        return False


def filter_node_equals(nodes, parameter, value):
    responses = []
    for node in nodes:
        if node[parameter] == value:
            responses.append(node)
    return responses


def filter_node_contains(nodes, parameter, value):
    responses = []
    for node in nodes:
        if value in node[parameter]:
            responses.append(node)
    return responses


def create_product_name_parent_node2_payload(product_name, environment, env_identifier, azure_subscription_id, parent_node_id):
    return {
        "name": f"{product_name}-{env_identifier}",
        "environment": environment,
        "classes": {
            "abi_sentinelone": {},
            "abi_flexera": {}
        },
        "rule": [
            "and",
                [
                    "=",
                    [
                        "fact",
                        "az_metadata",
                        "compute",
                        "subscriptionId"
                    ],
                    azure_subscription_id
                ], [
                    "=",
                    [
                        "fact",
                        "az_metadata",
                        "compute",
                        "tagsList",
                        "name"
                    ],
                    'puppet.node_match'
                ], [
                    "=",
                    [
                        "fact",
                        "az_metadata",
                        "compute",
                        "tagsList",
                        "value"
                    ],
                    product_name
                ], [
                    "=",
                    [
                        "fact",
                        "az_metadata",
                        "compute",
                        "tagsList",
                        "name"
                    ],
                    "tagname.environment"
                ]
        ],
        "parent": parent_node_id
    }


def create_product_node_payload(product_name, parent_node_id):
    return {
        "name": f"{product_name}",
        "environment": 'production',
        "classes": {
            "abi_sentinelone": {},
            "abi_flexera": {}
        },
        "rule": [
            "and",
                [
                    "~",
                    [
                        "fact",
                        "az_metadata",
                        "compute",
                        "tags"
                    ],
                    f'puppet.node_match:{product_name}'
                ]
        ],
        "parent": parent_node_id
    }


def create_product_node_env_payload(product_name, environment, env_identifier, parent_node_id):
    return {
        "name": f"{product_name}-{env_identifier}",
        "environment": environment,
        "classes": {
            "abi_sentinelone": {},
            "abi_flexera": {}
        },
        "rule": [
            "and",
            [
                "~",
                [
                    "fact",
                    "az_metadata",
                    "compute",
                    "tags"
                ],
                f'tagname.environment:{env_identifier}'
            ]
        ],
        "parent": parent_node_id
    }


def create_node_group(token, payload, puppet_server_url):
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "X-Authentication": token
    }

    request = requests.post(
        f"{puppet_server_url}/classifier-api/v1/groups",
        data=json.dumps(payload),
        headers=headers,
        verify=False
    )
    return request


def main(PUPPETSERVER_URL="https://puppet.test.com.br:4433", PRODUCT_NAME=sys.argv[1], BREWZONE_NAME=sys.argv[2], TOKEN=os.environ["PUPPET_TOKEN"]):
    nodes = get_nodes(TOKEN, PUPPETSERVER_URL)
    print(nodes)
    print("==============================")

    brewzone_products_parent_node = filter_node_equals(
        nodes, 'name', f'{BREWZONE_NAME}-products')
    # print(brewzone_products_parent_node)
    # print("==============================")

    if len(brewzone_products_parent_node) == 0:
        # print("Brewzone Node Group doesn't exists.")
        return False

    product_name_parent_node = filter_node_equals(
        nodes, 'name', f'{PRODUCT_NAME}')
    # print(product_name_parent_node)
    # print("==============================")

    if len(product_name_parent_node) == 0:
        product_payload = create_product_node_payload(
            product_name=PRODUCT_NAME, parent_node_id=brewzone_products_parent_node[0]["id"])
        # print(product_payload)

        create_node = create_node_group(
            TOKEN, product_payload, PUPPETSERVER_URL)
        # print(create_node.status_code)
        # print(create_node.json())

        _nodes = get_nodes(TOKEN, PUPPETSERVER_URL)
        # print(_nodes)
        # print("==============================")

        product_name_parent_node2 = filter_node_equals(
            _nodes, 'name', f'{PRODUCT_NAME}')
        # print(product_name_parent_node2)
        # print("==============================")

        if len(product_name_parent_node2) != 0:
            product_dev_payload = create_product_node_env_payload(product_name=PRODUCT_NAME, environment='development',
                                                                  env_identifier='dev', parent_node_id=product_name_parent_node2[0]["id"])
            product_stg_payload = create_product_node_env_payload(product_name=PRODUCT_NAME, environment='production',
                                                                  env_identifier='stg', parent_node_id=product_name_parent_node2[0]["id"])
            product_prd_payload = create_product_node_env_payload(product_name=PRODUCT_NAME, environment='production',
                                                                  env_identifier='prd', parent_node_id=product_name_parent_node2[0]["id"])
            create_node_dev = create_node_group(
                TOKEN, product_dev_payload, PUPPETSERVER_URL)
            # print(create_node.status_code)
            # print(create_node.json())
            create_node_stg = create_node_group(
                TOKEN, product_stg_payload, PUPPETSERVER_URL)
            create_node_prd = create_node_group(
                TOKEN, product_prd_payload, PUPPETSERVER_URL)
            if create_node_dev.status_code == 200 and create_node_stg.status_code == 200 and create_node_prd.status_code == 200:
                return True
            else:
                return False
        else:
            # print("Product Node Group Environment already exists.")
            return False
    else:
        # print("Product Node Group already exists.")
        return False


main()
