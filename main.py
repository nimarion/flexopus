from flexopus import FlexopusClient
import os

if __name__ == "__main__":
    flexopus_host = os.environ["FLEXOPUS_HOST"]
    flexopus_token = os.environ["FLEXOPUS_TOKEN"]
    client = FlexopusClient(flexopus_host, flexopus_token)
    print(client.getLocations())
    print(client.getEquipment())
    print(client.getSelfUser())
    print(client.getLocationsBookableStats())
    print(client.searchUsers({
        'name': 'marion',
        'isActive': 'false',
        'isFavoured': 'false'
    }))
    print(client.getCompanySettings())