*** Settings ***
Library  RequestsLibrary
Library  JSONLibrary
Variables  api_endpoints.py

*** Variables ***
${POSTS_URL}  https://jsonplaceholder.typicode.com/posts
${USERS_URL}  https://jsonplaceholder.typicode.com/users

*** Test Cases ***
Get All Posts And Verify Schema
    Create Session  JsonPlaceholder  ${POSTS_URL}
    ${response}=  GET On Session  JsonPlaceholder  /
    Status Should Be  200  ${response}
    ${json_data}=  Set Variable  ${response.json()}
    Verify JSON Schema  ${json_data}  ${ENDPOINTS.posts.schema}

Get All Users And Verify Schema
    Create Session  JsonPlaceholder  ${USERS_URL}
    ${response}=  GET On Session  JsonPlaceholder  /
    Status Should Be  200  ${response}
    ${json_data}=  Set Variable  ${response.json()}
    Verify JSON Schema  ${json_data}  ${ENDPOINTS.users.schema}

*** Keywords ***
Verify JSON Schema
    [Arguments]  ${json_data}  ${schema}
    FOR  ${item}  IN  @{json_data}
        FOR  ${key}  ${value}  IN  @{schema.items()}
            ${item_value}=  Get Value From JSON  ${item}  ${key}
            Should Be True  isinstance(${item_value}, ${value})  "Value for key '${key}' is not of type ${value}"
        END
    END
