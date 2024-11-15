import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
import base64
from bs4 import BeautifulSoup # for html parsing


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

def fetch_emails_with_terms(service, terms, max_results=1):
    """
    Fetch emails containing specified terms.
    """
    for term in terms:
        try:
            query = term  # Searching for emails containing the term
            print(f"Query: {query}")  # Debugging output
            results = service.users().messages().list(userId='me', q=query, maxResults=max_results).execute()
            messages = results.get('messages', [])

            if not messages:
                print(f"No messages found for term: {term}")
                continue

            for msg in messages:
                # Fetch the full message
                msg = service.users().messages().get(userId='me', id=msg['id']).execute()
                print(f"Email Subject: {msg['snippet']}")  # Print the email subject
                
                # Check if 'payload' exists and contains 'parts'
                if 'payload' in msg and 'parts' in msg['payload']:
                    for part in msg['payload']['parts']:
                        # Process each part
                        if 'body' in part and 'data' in part['body']:
                            # Decode the base64url encoded content
                            body_data = part['body']['data']
                            decoded_body = base64.urlsafe_b64decode(body_data).decode('utf-8')
                            
                            # Parse the HTML content
                            soup = BeautifulSoup(decoded_body, 'html.parser')
                            text_body = soup.get_text()  # Extract text from HTML
                            print(f"Email Body: {text_body}")  # Print the email body
                        # Check for attachments
                        if 'filename' in part and part['filename'].endswith('.pdf'):
                            attachment_id = part['body']['attachmentId']
                            attachment = service.users().messages().attachments().get(userId='me', messageId=msg['id'], id=attachment_id).execute()
                            pdf_data = base64.urlsafe_b64decode(attachment['data'])
                            # process the PDF data as needed
                            print(f"PDF Attachment: {part['filename']}")  # Print the name of the PDF attachment
                            # save it to a file:
                            with open(part['filename'], 'wb') as pdf_file:
                                pdf_file.write(pdf_data)
                                print(f"Saved PDF: {part['filename']}")  # Confirm saving the PDF
                else:
                    print("No parts found in the email.")
        except Exception as e:
            print(f"Error fetching emails for term '{term}': {str(e)}")

def test_gmail_connection():
    try:
        print("Starting Gmail connection test...")
        print("Getting credentials...")
        creds = get_gmail_credentials()
        print("Building service...")
        service = build('gmail', 'v1', credentials=creds)
        
        print("Fetching user profile...")
        
        # Fetch emails containing the terms 'reservation' and 'flight'
        fetch_emails_with_terms(service, ['reservation', 'flight'])
        
    except Exception as e:
        print(f"Error testing Gmail connection: {str(e)}")
        import traceback
        traceback.print_exc()  # This will print the full error traceback

if __name__ == "__main__":
    test_gmail_connection()