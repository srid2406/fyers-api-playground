# Use the response link for auth which generates the auth code.
from fyers_apiv3 import fyersModel
from dotenv import load_dotenv
import os

load_dotenv()

client_id = os.getenv("CLIENT_ID")
secret_key = os.getenv("CLIENT_SECRET_KEY")
redirect_uri = "https://sridamul.me/"
response_type = "code"  
state = "sample_state"

session = fyersModel.SessionModel(
    client_id=client_id,
    secret_key=secret_key,
    redirect_uri=redirect_uri,
    response_type=response_type
)

response = session.generate_authcode()

print(response)
