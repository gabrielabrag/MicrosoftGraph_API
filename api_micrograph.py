import msal
from datetime import date
import pandas as pd
import requests
import pyodbc
import numpy as np

#Buscar token 
# Enter the details of your AAD app registration
client_id = 'client_id'
client_secret = 'client_secret'
authority = 'authority'
scope = ['https://graph.microsoft.com/.default']

# Create an MSAL instance providing the client_id, authority and client_credential parameters
client = msal.ConfidentialClientApplication(client_id, authority=authority, client_credential=client_secret)
# First, try to lookup an access token in cache
token_result = client.acquire_token_silent(scope, account=None)

# If the token is available in cache, save it to a variable
if token_result:
    access_token = 'Bearer ' + token_result['access_token']
# If the token is not available in cache, acquire a new one from Azure AD and save it to a variable
if not token_result:
    token_result = client.acquire_token_for_client(scopes=scope)
    access_token = 'Bearer ' + token_result['access_token']

PARAMETRO = { 'authorization':  access_token ,
                            'Accept': 'application/json;odata.metadata=minimal;odata.streaming=true',
                            'Content-Type': 'application/json;odata.metadata=minimal;odata.streaming=true'}

print(access_token)

#Puxando dados da api com filtro por data 
hoje= date.today()
dtatual=str(hoje)
API_URI = "https://graph.microsoft.com/v1.0/auditLogs/signIns?$filter=(createdDateTime ge "+(dtatual)+"T00:00:00Z AND createdDateTime le "+(dtatual)+"T23:59:00Z)"
api_LOG_response = requests.get(API_URI, headers=PARAMETRO)

data= api_LOG_response.json()
df_LOG = pd.json_normalize(data,record_path=['value'])
df_LOG.columns = (df_LOG.columns.str.replace('.', ''))

print(df_LOG)
