#!/bin/bash

#==============================================================================================
# Define environment variable PUPPET_TOKEN
export PUPPET_TOKEN=your_token_here

#==============================================================================================
#Calling Python script with single line/parameters:
python3 ./create-puppet-node-groups.py your_repo_product_name your_subscription_name your_subscription_id

#==============================================================================================
#It's possible trigger the Python script with while calling a csv file with many parameters:

while IFS=',' read -r input1 input2 input3
do
    python3 ./create-puppet-node-groups.py "$input1" "$input2" "$input3"
done < inputs.csv

#==============================================================================================
