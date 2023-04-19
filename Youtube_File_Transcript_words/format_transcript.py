import sys
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build


def format_transcript(doc_id):
    SCOPES = ['https://www.googleapis.com/auth/documents']

    creds = None
    if sys.argv[-1] == 'token.pickle':
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('docs', 'v1', credentials=creds)

    doc = service.documents().get(documentId=doc_id).execute()
    requests = []

    for index, element in enumerate(doc['body']['content']):
        if 'paragraph' in element:
            paragraph_text = element['paragraph']['elements'][0]['textRun']['content']

            # Apply formatting for speaker names
            if paragraph_text.strip().endswith(':'):
                requests.append({
                    'updateTextStyle': {
                        'range': {
                            'startIndex': element['startIndex'],
                            'endIndex': element['endIndex']
                        },
                        'textStyle': {
                            'bold': True,
                            'fontSize': {
                                'magnitude': 14,
                                'unit': 'PT'
                            },
                            'weightedFontFamily': {
                                'fontFamily': 'Arial'
                            }
                        },
                        'fields': 'bold,fontSize,weightedFontFamily'
                    }
                })

            # Apply formatting for timestamps
            elif paragraph_text.strip().startswith('[') and paragraph_text.strip().endswith(']'):
                requests.append({
                    'updateTextStyle': {
                        'range': {
                            'startIndex': element['startIndex'],
                            'endIndex': element['endIndex']
                        },
                        'textStyle': {
                            'italic': True,
                            'fontSize': {
                                'magnitude': 10,
                                'unit': 'PT'
                            },
                            'weightedFontFamily': {
                                'fontFamily': 'Arial'
                            }
                        },
                        'fields': 'italic,fontSize,weightedFontFamily'
                    }
                })

            # Apply formatting for the spoken content
            else:
                requests.append({
                    'updateTextStyle': {
                        'range': {
                            'startIndex': element['startIndex'],
                            'endIndex': element['endIndex']
                        },
                        'textStyle': {
                            'bold': False,
                            'fontSize': {
                                'magnitude': 12,
                                'unit': 'PT'
                            },                             'weightedFontFamily': {
                                'fontFamily': 'Arial'
                            }
                        },
                        'fields': 'bold,fontSize,weightedFontFamily'
                    }
                })

    # Execute the requests
    result = service.documents().batchUpdate(
        documentId=doc_id, body={'requests': requests}).execute()
    return result


if __name__ == '__main__':
    document_id = sys.argv[1]
    format_transcript(document_id)
