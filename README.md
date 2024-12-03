# fmc_export_objects
This project can be used to export all objects from a Cisco Firepower Management Center using REST API to a CSV file.

I created it for my own usage to provide auditors with objects when exporting FMC rules with https://github.com/raghukul-cisco/csvExportFirepower.
The exported rules is shown with object names as values and as such was useless to auditors without the objects exported as well.

Decided to share the script to save time in case other people need it.

## Requirements

    * Python 3.7+
    * FireREST SDK (https://github.com/kaisero/fireREST)

## Usage

Enter information when you run script, and a file named "all_objects.csv" should be created in script directory.

If it doesn't work, too bad... (but let me know) I'm new to this :'(

## csv format

name,type,value

In case of NetworkObjectGroups or PortObjectGroups, the object will be presented multiple times with different values.
example provided in examples folder.
