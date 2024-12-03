# fmc_export_objects
This project can be used to export all objects from a Cisco Firepower Management Center using REST API to a CSV file.

## Features

    * None, other than what it does

## Requirements

    * Python 3.7+
    * Whats in the requirements.txt file

## Usage

Enter information when you run script, and a file named "all_objects.csv" should be created in script directory.

If it doesn't work, too bad... (but let me know) I'm new to this :'(

## csv format

name,type,value

In case of NetworkObjectGroups or PortObjectGroups, the object will be presented multiple times with different values.
example provided in examples folder.
