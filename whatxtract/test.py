import os
import csv
import json

STORE_PATH = 'D:\\PyCharm\\test\\model-storage.json'

def extract_chat_list():
    with open(STORE_PATH, 'r', encoding='utf-8') as f:
        snapshot_data = json.load(f)

        # Extract only id and name
        data_list = snapshot_data['chat']

        print('Total chats:', len(data_list))
        for i, data in enumerate(data_list, 1):
            print(f"[{i:03}] {data['id'].split('@')[0]:<15} {data['name']}")


def extract_contacts():
    with open(STORE_PATH, 'r', encoding='utf-8') as f:
        snapshot_data = json.load(f)

        data_list = snapshot_data['contact']
        data_list = [x for x in data_list if x.get('isAddressBookContact') and x.get('phoneNumber')]
        print('Total Contacts:', len(data_list))
        for i, data in enumerate(data_list, 1):
            print(f"[{i}] {data}")
            # print(f"[{i:03}] {data['id']:<18} {data.get('phoneNumber','PN'):<15} {data.get('name','name'):<20} {data.get('pushname','pushname'):<20}")

        headers = ['id', 'name', 'shortName', 'phoneNumber']

        export_data_list = []
        for d in data_list:
            export_data_list.append({k:d.get(k,'') for k in headers})

        filename = 'D:\\PyCharm\\test\\contacts.csv'
        filepath = os.path.join(os.getcwd(), filename)
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()
            writer.writerows(export_data_list)


if __name__ == '__main__':
    extract_contacts()
