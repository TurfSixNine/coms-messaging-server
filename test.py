import requests

# base = "http://127.0.0.1:5000/"
# # response = requests.post(base + "/group", {
# #     "name": "group 1",
# #     "members":[{ 
# #         "number":"+2348156811122",
# #         "name":"Ayo",
# #         }],
    
# # })

# response = requests.get(base+"/insights")

# print(response.json())


# import requests

# Constants
BASE_URL =  "http://localhost:5001/" #"https://api.coms-messaging-21078062.com/"

SIGN_IN_URL = f"{BASE_URL}/auth/sign-in"
SIGN_IN_PAYLOAD = {
    "email": "test@test.com",
    "password": "123456"
}
GROUP_URL = f"{BASE_URL}/group"
GROUP_PAYLOAD = {
    "name": "Test4",
    "numbers": [
        {
            "code": "+44",
            "number" : "7876159566"
        }
    ]
}
MESSAGES_URL = f"{BASE_URL}/messages"
MESSAGE_PAYLOAD_TEMPLATE = {
    "types": ["SMS", "TTS"],
    "title": "Postman Test",
    "body": "This is a postman test",
    "groupId": ""
}

def sign_in():
    response = requests.post(SIGN_IN_URL, json=SIGN_IN_PAYLOAD)
    response.raise_for_status()
    return response.json()["token"]

def create_group(token):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(GROUP_URL, json=GROUP_PAYLOAD, headers=headers)
    response.raise_for_status()
    return response.json()[0]["id"]

def send_message(token, group_id):
    headers = {"Authorization": f"Bearer {token}"}
    message_payload = MESSAGE_PAYLOAD_TEMPLATE.copy()
    message_payload["groupId"] = group_id
    response = requests.post(MESSAGES_URL, json=message_payload, headers=headers)
    response.raise_for_status()

def main():
    try:
        token = sign_in()
        group_id = create_group(token)
        for _ in range(100000):
            send_message(token, group_id)
        print(f"Iteration completed successfully")
    except requests.RequestException as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
