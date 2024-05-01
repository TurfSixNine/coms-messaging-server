import requests

base = "http://127.0.0.1:5000/"
# response = requests.post(base + "/group", {
#     "name": "group 1",
#     "members":[{ 
#         "number":"+2348156811122",
#         "name":"Ayo",
#         }],
    
# })

response = requests.get(base+"/insights")

print(response.json())


