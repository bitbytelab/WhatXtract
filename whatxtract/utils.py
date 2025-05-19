import os
import csv
import sys
import json
import time
import subprocess
from typing import Any
from pathlib import Path

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from constants import *
from logger_setup import setup_logger


def extract_chat_list(db_path=WAMS_DB_PATH, output_file=OUTPUT_DIR / 'extracted_chat_list.csv'):
    with db_path.open('r', encoding='utf-8') as f:
        snapshot_data = json.load(f)

        # Extract only id and name
        data_list = snapshot_data['chat']

        print('Total chats:', len(data_list))
        for i, data in enumerate(data_list, 1):
            print(f"[{i:03}] {data['id'].split('@')[0]:<15} {data['name']}")


def extract_contacts(db_path=WAMS_DB_PATH, output_file=OUTPUT_DIR / 'extracted_contacts.csv'):
    with db_path.open('r', encoding='utf-8') as file:
        snapshot_data = json.load(file)

        data_list = snapshot_data['contact']
        data_list = [x for x in data_list if x.get('isAddressBookContact') and x.get('phoneNumber')]
        print('Total Contacts:', len(data_list))
        for i, data in enumerate(data_list, 1):
            print(f'[{i}] {data}')
            # print(f"[{i:03}] {data['id']:<18} {data.get('phoneNumber','PN'):<15} {data.get('name','name'):<20} {data.get('pushname','pushname'):<20}")

        headers = ['id', 'name', 'shortName', 'phoneNumber']

        export_data_list = []
        for d in data_list:
            export_data_list.append({k:d.get(k,'') for k in headers})

        with output_file.open('w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()
            writer.writerows(export_data_list)

            print(f'[ ! ] extracted {len(export_data_list)} contacts. saved to: {output_file}')


def chunkify(lst, n):
    """Split list `lst` into `n` roughly equal parts"""
    return [lst[i::n] for i in range(n)]
