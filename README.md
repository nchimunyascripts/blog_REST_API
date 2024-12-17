# FastAPI Blog API Documentation

**Version**: `0.1.0`  
**OpenAPI**: `3.1`  
**OpenAPI Schema**: [`/openapi.json`](#)

---

## **Authorization**

This API requires token-based authentication. Use the `/login` endpoint to generate an access token. Include the token in your requests:

```http
Authorization: Bearer <access_token>
```

---

## **Posts**

### **GET** `/posts/`

**Description**: Retrieve a list of blog posts.  
**Responses**:

- **200 OK**: Returns a list of posts.

---

### **POST** `/posts/`

**Description**: Create a new blog post.  
**Request Body**:

- **Required**:
  - `title` (string): Title of the post.
  - `content` (string): Content of the post.
  - `published` (boolean, default: `true`): Post status.

**Responses**:

- **201 Created**: Returns the created post.
- **422 Unprocessable Entity**: Validation error.

**Schema**:

```json
{
  "title": "string",
  "content": "string",
  "published": true
}
```

---

### **GET** `/posts/{_id}`

**Description**: Retrieve a single post by ID.  
**Parameters**:

- `_id` (integer): The ID of the post.

**Responses**:

- **200 OK**: Returns the requested post.
- **404 Not Found**: Post not found.

---

### **DELETE** `/posts/{_id}`

**Description**: Delete a post by ID.  
**Parameters**:

- `_id` (integer): The ID of the post.

**Responses**:

- **204 No Content**: Successfully deleted.
- **404 Not Found**: Post not found.

---

### **PUT** `/posts/{_id}`

**Description**: Update an existing post.  
**Parameters**:

- `_id` (integer): The ID of the post.

**Request Body**:

- `title` (string): Updated title.
- `content` (string): Updated content.
- `published` (boolean, default: `true`): Updated status.

**Responses**:

- **200 OK**: Returns the updated post.
- **404 Not Found**: Post not found.
- **422 Unprocessable Entity**: Validation error.

---

## **Users**

### **POST** `/users/`

**Description**: Create a new user account.  
**Request Body**:

- **Required**:
  - `email` (string, email format): User email.
  - `password` (string): User password.

**Responses**:

- **201 Created**: User created successfully.
- **422 Unprocessable Entity**: Validation error.

**Schema**:

```json
{
  "email": "user@example.com",
  "password": "string"
}
```

---

### **GET** `/users/{_id}`

**Description**: Retrieve a user by ID.  
**Parameters**:

- `_id` (integer): The ID of the user.

**Responses**:

- **200 OK**: Returns user details.
- **404 Not Found**: User not found.

---

## **Authentication**

### **POST** `/login`

**Description**: Authenticate and generate an access token.  
**Request Body**:

- **grant_type** (string | null)
- **username** (string): User email.
- **password** (string): User password.
- **scope** (string)
- **client_id** (string | null)
- **client_secret** (string | null)

**Responses**:

- **200 OK**: Returns access token.
- **401 Unauthorized**: Invalid credentials.

**Schema**:

```json
{
  "access_token": "string",
  "token_type": "string"
}
```

---

## **Vote**

### **POST** `/vote/`

**Description**: Vote on a post.  
**Request Body**:

- **post_id** (integer): ID of the post.
- **dir** (integer, ≤ 1): Direction of the vote (1 = upvote, 0 = downvote).

**Responses**:

- **201 Created**: Vote registered successfully.
- **404 Not Found**: Post not found.

**Schema**:

```json
{
  "post_id": 1,
  "dir": 1
}
```

---

## **Default**

### **GET** `/`

**Description**: Root endpoint.  
**Responses**:

- **200 OK**: API status check.

---

## **Schemas**

### **Post**

```json
{
  "title": "string",
  "content": "string",
  "published": true,
  "id": 1,
  "created_at": "2024-06-01T00:00:00",
  "owner_id": 1,
  "owner": {
    "id": 1,
    "email": "user@example.com",
    "created_at": "2024-06-01T00:00:00"
  }
}
```

### **User**

```json
{
  "id": 1,
  "email": "user@example.com",
  "created_at": "2024-06-01T00:00:00"
}
```

### **Vote**

```json
{
  "post_id": 1,
  "dir": 1
}
```

### **ValidationError**

```json
{
  "loc": ["string", "integer"],
  "msg": "string",
  "type": "string"
}
```

---

### **Example Authorization Request**

1. **Login**:

```bash
curl -X POST "http://localhost:8000/login" -d "username=user@example.com&password=secret"
```

2. **Authenticated Request**:

```bash
curl -X GET "http://localhost:8000/posts/" -H "Authorization: Bearer <access_token>"
```

---

This documentation outlines the API endpoints, schemas, and expected behaviors for the FastAPI-based Blog API. For more details, refer to the OpenAPI JSON schema at `/openapi.json`.
