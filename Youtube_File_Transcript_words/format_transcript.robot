*** Settings ***
Library  Process

*** Variables ***
${DOC_ID}  <your-document-id>

*** Test Cases ***
Format Transcript
    ${result}=  Run Process  python  format_transcript.py  ${DOC_ID}
    Log  ${result.stdout}
