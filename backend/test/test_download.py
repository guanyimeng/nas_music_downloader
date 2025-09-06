import requests

url = "http://127.0.0.1:8000/download"
data = {"url": "https://www.youtube.com/watch?v=IhuPnNYQyLk&list=RDIhuPnNYQyLk&start_radio=1&pp=ygUMcHN5ayBwb3BwaW5noAcB"}
response = requests.post(url, json=data)
print("Status Code:", response.status_code)
print("Response JSON:", response.json())

# return sample
# Status Code: 200
# Response JSON: {'status': 'Rick Astley - Never Gonna Give You Up (Official Video) (4K Remaster).mp3success; Uploaded to NAS successfully ✅', 'history': ['Rick Astley - Never Gonna Give You Up (Official Video) (4K Remaster).mp3success; Uploaded to NAS successfully ✅']}

