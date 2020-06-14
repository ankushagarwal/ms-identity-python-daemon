import logging
import requests
# https://github.com/AzureAD/microsoft-authentication-library-for-python
import msal


# Optional logging
logging.basicConfig(level=logging.DEBUG)

config = {
  "authority": "https://login.microsoftonline.com/0e764dbe-944c-4623-8539-52ba164e79bb",
  "client_id": "74425ebe-eaf3-4448-b704-2643c2ae4822",
  "scope": [ "74425ebe-eaf3-4448-b704-2643c2ae4822/.default" ],
  "thumbprint": "4FE79A3F20CB21B3660005C9F3440655330BA093",
  "private_key_file": "private_key.pem",
  "mbs_endpoint": "https://aos.eastus.cloudapp.azure.com"
}

# Create a preferably long-lived app instance which maintains a token cache.
app = msal.ConfidentialClientApplication(
    config["client_id"], authority=config["authority"],
    client_credential={"thumbprint": config["thumbprint"], "private_key": open(config['private_key_file']).read()},
    # token_cache=...  # Default cache is in memory only.
                       # You can learn how to use SerializableTokenCache from
                       # https://msal-python.rtfd.io/en/latest/#msal.SerializableTokenCache
    )

# The pattern to acquire a token looks like this.
token = None

# Firstly, looks up a token from cache
token = app.acquire_token_silent(config["scope"], account=None)

if not token:
    logging.info("No suitable token exists in cache. Let's get a new one from AAD.")
    token = app.acquire_token_for_client(scopes=config["scope"])

print(token)

# preapproval_payload = {
#   'foo': 'bar'
# }
# headers = {
#   'Authorization': 'Bearer ' + token['access_token']
# }
# response = requests.post(config["mbs_endpoint"] + "/api/v1/preapproval", json=preapproval_payload)
# print(response)
