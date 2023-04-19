BASE_URL = "https://jsonplaceholder.typicode.com"

ENDPOINTS = {
    'posts': {
        'url': f"{BASE_URL}/posts",
        'schema': {
            'id': int,
            'userId': int,
            'title': str,
            'body': str,
        }
    },
    'users': {
        'url': f"{BASE_URL}/users",
        'schema': {
            'id': int,
            'name': str,
            'username': str,
            'email': str,
            'address': dict,
            'phone': str,
            'website': str,
            'company': dict,
        }
    },
}
