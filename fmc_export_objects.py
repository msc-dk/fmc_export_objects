import requests
import csv
from getpass import getpass
from fireREST import FMC

# disable SSL warnings
requests.packages.urllib3.disable_warnings()

#define variables
fmc_ip = input("Enter FMC IP: ")
username = input("Enter username for API access: ")
password = getpass("Password: ")
fmc = FMC(hostname=fmc_ip, username=username, password=password, domain='Global')
#initialize list with all FMC objects
object_all_list = []
convertable_object_list = []

#Get all FMC objects from FMC API and assign them to lists
def retrieve_objects(objects):
    for object in objects:
        object_info = {
            "name": object.get("name"),
            "id": object.get("id"),
            "type": object.get("type"),
            "value": object.get("value")
        }
        #If value hasn't been assigned, try to assign with different keys (for object groups)
        if object_info["value"]:
            pass
        elif object.get("literals"):
            object_info["value"] = object["literals"]
        elif object.get("objects"):
            object_info["value"] = object["objects"]
        elif object.get("port"):
            object_info["port"] = object["port"]
            object_info["protocol"] = object["protocol"]
        #Assign object to all_objects list
        object_all_list.append(object_info)


def put_objects_to_convertable_list():
    #Iterate over all objects
    for object in object_all_list:
        object_dict = {}
        object_dict["name"] = object["name"]
        object_dict["type"] = object["type"]
        #If the object is a network/host object, assign values according to CSV format and write to new list
        if object["type"] == "Network" or object["type"] == "Host":
            object_dict["value"] = object["value"]
            convertable_object_list.append(object_dict)           
        #If the object is a networkgroup object, assign values according to CSV format and write to new list
        elif object["type"] == "NetworkGroup":
            for subnet in object["value"]:
                unique_object_dict = object_dict.copy()
                #if the "value" key exists, write that value to as the item being added to the list
                #if the "value" key doesn't exist, then it is a host object in the group and key is named "name"
                unique_object_dict["value"] = subnet.get('value', subnet.get('name'))
                convertable_object_list.append(unique_object_dict)
        elif object["type"] == "ProtocolPortObject":
            object_dict["value"] = f"{object["protocol"]}/{object["port"]}"
            convertable_object_list.append(object_dict)
        elif object["type"] == "PortObjectGroup":
            for port in object["value"]:
                unique_object_dict = object_dict.copy()
                #Retrieve protocol info from object_all_list, because it doesn't exist in portobjectgroup value
                for item in object_all_list:
                    if item["id"] == port["id"]:
                        port_protocol = item["protocol"]
                unique_object_dict["value"] = f"{port_protocol}/{port["port"]}"
                convertable_object_list.append(unique_object_dict)
        else:
            print(f"object {object["name"]} didn't match a type, all objects weren't exported.")
            continue

def convert_list_to_csv():
    headers = ["name", "type", "value"]
    with open("all_objects.csv", "w") as f:
        write = csv.writer(f)
        write.writerow(headers)
        for object in convertable_object_list:
            csv_line = []
            for key in object:
                csv_line.append(object[key])
            write.writerow(csv_line)
        

def main():       
    retrieve_objects(fmc.object.host.get())
    retrieve_objects(fmc.object.network.get())
    retrieve_objects(fmc.object.networkgroup.get())
    retrieve_objects(fmc.object.port.get())
    retrieve_objects(fmc.object.portobjectgroup.get())
    put_objects_to_convertable_list()
    convert_list_to_csv()

if __name__ == "__main__":
    main()
    