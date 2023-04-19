ENDPOINTS = {
    "posts": {
        "url": "https://jsonplaceholder.typicode.com/posts",
        "schema": {
            "userId": int,
            "id": int,
            "title": str,
            "body": str
        }
    },
    "users": {
        "url": "https://jsonplaceholder.typicode.com/users",
        "schema": {
            "id": int,
            "name": str,
            "username": str,
            "email": str,
            "address": dict,
            "phone": str,
            "website": str,
            "company": dict
        }
    }
}
