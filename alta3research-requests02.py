#!/usr/bin/python3
"""
Will Park | Python Flask Project (Project 3) - Part 2

Get request sender that uses requests to target Flask App API from Part 1.
It makes the JSON response from the Flask API to a more human readable format. 
"""

# import necessary modules for format converting and pretty printing
import requests
import yaml
import pprint
import csv

def main():
    """runtime code"""

    ## Flask API URL
    my_api = "http://127.0.0.1:2224/employees"

    ## parse the returned JSON response from Flask API as a Pythonic data (list) and save it as variable "json_response"
    response = requests.get(my_api).json()

    ## process "response" as yaml and save it as variable "yaml_data"
    yaml_data = yaml.dump(response, sort_keys=False)

    ## create an instance of PrettyPrinter with indentation of 4 for each nesting level
    pp = pprint.PrettyPrinter(indent=4)

    ## print to the terminal using the created PrettyPrinter instance
    pp.pprint(yaml_data)

    ## save the keys of the first dictionary in response (response is a list of dictionaries)
    keys = response[0].keys()

    ## open employees.csv and write into it
    with open("employees.csv", "w", newline="") as output:
        # create an instance of csv module's DictWriter class
        dict_writer = csv.DictWriter(output, keys)
        # using DictWriter's writeheader and writerows functions, start writing a csv file using the response
        dict_writer.writeheader()
        dict_writer.writerows(response)

## best practice for using __main__
if __name__ == "__main__":
    main()