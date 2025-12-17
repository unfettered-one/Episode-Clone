import requests, certifi
import os
url = 'https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2/resolve/main/./modules.json'
print(certifi.where())
resp = requests.head(url, verify=certifi.where())
print(resp.status_code)