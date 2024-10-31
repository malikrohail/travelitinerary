import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
CONFIG_FILE = 'credentials.json'

def get_gmail_credentials():
    """
    Get the credentials for the Gmail API
    """
    creds = None
    if not creds or not creds.valid:
        try:
            flow = InstalledAppFlow.from_client_secrets_file(CONFIG_FILE, SCOPES)
            # Specifying 127.0.0.1 instead of localhost cause of port issues
            creds = flow.run_local_server(
                host='127.0.0.1',
                port=8080,
                success_message='The auth flow is complete; you may close this window.'
            )
            with open('token.json', 'w') as token:
                token.write(creds.to_json())
        except Exception as e:
            print(f"Error during authentication: {str(e)}")
            raise
    return creds

def test_gmail_connection():
    try:
        print("Starting Gmail connection test...")
        print("Getting credentials...")
        creds = get_gmail_credentials()
        print("Building service...")
        service = build('gmail', 'v1', credentials=creds)
        
        print("Fetching user profile...")
        
    except Exception as e:
        print(f"Error testing Gmail connection: {str(e)}")
        import traceback
        traceback.print_exc()  # This will print the full error traceback
if __name__ == "__main__":
    test_gmail_connection()