import requests
headers={
    'Content-type':'application/json;charset=utf-8', 
    'Accept':'application/json'
}
res = requests.post('http://localhost:5000/api/add_message/', json={"mytext":"lalala","parameters": {"temperature":12,"humidity":13},"mac": "23.3d.h5.65.kg"}, headers= headers)
if res.ok:
    print("ok")