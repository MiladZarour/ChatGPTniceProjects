*** Settings ***
Library  RequestsLibrary
Library  JSONLibrary
Variables  api_endpoints.py

*** Test Cases ***
Get All Posts And Verify Schema
    ${url}=  Get Variable Value  ${ENDPOINTS.posts.url}
    Create Session  JsonPlaceholder  ${url}/
    ${response}=  GET On Session  JsonPlaceholder  /
    Status Should Be  200  ${response}
    ${json_data}=  Set Variable  ${response.json()}
    Verify JSON Schema  ${json_data}  ${ENDPOINTS.posts.schema}

Get All Users And Verify Schema
    ${url}=  Get Variable Value  ${ENDPOINTS.users.url}
    Create Session  JsonPlaceholder  ${url}/
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
