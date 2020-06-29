import logging
import requests
# https://github.com/AzureAD/microsoft-authentication-library-for-python
import msal


# Optional logging
logging.basicConfig(level=logging.DEBUG)

config = {
  # tenant id
  "authority": "https://login.microsoftonline.com/0e764dbe-944c-4623-8539-52ba164e79bb",
  "client_id": "d8416169-b121-4ca3-ab61-2b92659f2ec8",
  "scope": [ "d8416169-b121-4ca3-ab61-2b92659f2ec8/.default" ],
  # openssl x509 -in public_key_certificate.crt -fingerprint -noout | sed 's|:||g'
  "thumbprint": "F5F55423D518CC0808B53A624042259D0083E07E",
  "private_key_file": "/Users/kush/tmp/2020-06-15-16-53-44/private_key.pem",
  "mbs_endpoint": "http://localhost:8080"
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

preapproval_payload = {
  'currency': 'Coin1',
  'amount': 100000
}
headers = {
  'Authorization': 'Bearer ' + token['access_token']
}
response = requests.post(config["mbs_endpoint"] + "/api/v1/mint/pre_approval", headers=headers, json=preapproval_payload)
print(response)
