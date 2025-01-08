# API Documentation

## Authentication
All endpoints require authentication using a token. Obtain a token by sending a POST request to `/auth/token/login/` with username and password.

## Users

### Get User Profile
`GET /users/{id}/`
- Returns: Profile details
- Response Schema:
```json
{
  "id": "integer",
  "user": {
    "id": "integer",
    "username": "string"
  },
  "bio": "string",
  "profile_picture": "integer|null",
  "date_of_birth": "string|null (YYYY-MM-DD)",
  "location": "string",
  "following_count": "integer",
  "follower_count": "integer"
}
```

### Follow User
`POST /users/{id}/follow/`
- Returns: Follow relationship details
- Response Schema:
```json
{
  "id": "integer",
  "follower": {
    "id": "integer",
    "username": "string"
  },
  "followed": {
    "id": "integer",
    "username": "string"
  },
  "created_at": "string (ISO 8601 datetime)"
}
```

### Unfollow User
`DELETE /users/{id}/unfollow/`
- Returns: 204 No Content

### Get User Followers
`GET /users/{id}/followers/`
- Returns: List of followers
- Response Schema:
```json
[
  {
    "id": "integer",
    "follower": {
      "id": "integer",
      "username": "string"
    },
    "created_at": "string (ISO 8601 datetime)"
  }
]
```

### Get User Following
`GET /users/{id}/following/`
- Returns: List of followed users
- Response Schema:
```json
[
  {
    "id": "integer",
    "followed": {
      "id": "integer",
      "username": "string"
    },
    "created_at": "string (ISO 8601 datetime)"
  }
]
```

### Check Follow Status
`GET /users/{id}/is_following/`
- Returns: Follow status
- Response Schema:
```json
{
  "is_following": "boolean"
}
```

### Current User Profile
`GET /users/profile/`
- Returns: Current user's profile
- Response Schema:
```json
{
  "id": "integer",
  "user": {
    "id": "integer",
    "username": "string"
  },
  "bio": "string",
  "profile_picture": "integer|null",
  "date_of_birth": "string|null (YYYY-MM-DD)",
  "location": "string",
  "following_count": "integer",
  "follower_count": "integer"
}
```

## Posts

### Create Post
`POST /posts/`
- Parameters:
  - content: string
  - media_files: array of file IDs (optional)
- Returns: Created post details
- Response Schema:
```json
{
  "id": "integer",
  "user": {
    "id": "integer",
    "username": "string"
  },
  "content": "string",
  "created_at": "string (ISO 8601 datetime)",
  "updated_at": "string (ISO 8601 datetime)",
  "media_files": [
    {
      "id": "integer",
      "file": "string (URL)",
      "owner": "integer",
      "created_at": "string (ISO 8601 datetime)"
    }
  ],
  "comments": [],
  "likes": []
}
```

### Like Post
`POST /posts/{id}/like/`
- Returns: Like details
- Response Schema:
```json
{
  "id": "integer",
  "user": {
    "id": "integer",
    "username": "string"
  },
  "created_at": "string (ISO 8601 datetime)"
}
```

### Unlike Post
`DELETE /posts/{id}/unlike/`
- Returns: 204 No Content

### Get Post Comments
`GET /posts/{id}/comments/`
- Returns: List of comments
- Response Schema:
```json
[
  {
    "id": "integer",
    "user": {
      "id": "integer",
      "username": "string"
    },
    "content": "string",
    "created_at": "string (ISO 8601 datetime)",
    "updated_at": "string (ISO 8601 datetime)"
  }
]
```

### Add Comment
`POST /posts/{id}/comments/`
- Parameters:
  - content: string
- Returns: Created comment
- Response Schema:
```json
{
  "id": "integer",
  "user": {
    "id": "integer",
    "username": "string"
  },
  "content": "string",
  "created_at": "string (ISO 8601 datetime)",
  "updated_at": "string (ISO 8601 datetime)"
}
```

## Files

### Upload File
`POST /files/`
- Content-Type: multipart/form-data
- Parameters:
  - file: binary
- Returns: File details
- Response Schema:
```json
{
  "id": "integer",
  "file": "string (URL)",
  "owner": "integer",
  "created_at": "string (ISO 8601 datetime)"
}
```

### Get User Files
`GET /files/`
- Returns: List of user's files
- Response Schema:
```json
[
  {
    "id": "integer",
    "file": "string (URL)",
    "owner": "integer",
    "created_at": "string (ISO 8601 datetime)"
  }
]
```

## Notifications

### Get Notifications
`GET /notifications/notifications/`
- Returns: List of notifications
- Response Schema:
```json
[
  {
    "id": "integer",
    "user": {
      "id": "integer",
      "username": "string"
    },
    "post": {
      "id": "integer",
      "user": {
        "id": "integer",
        "username": "string"
      },
      "content": "string",
      "created_at": "string (ISO 8601 datetime)",
      "updated_at": "string (ISO 8601 datetime)",
      "media_files": [],
      "comments": [],
      "likes": []
    },
    "comment": "integer|null",
    "notification_type": "string (like|comment|reply)",
    "created_at": "string (ISO 8601 datetime)",
    "is_read": "boolean"
  }
]
```

### Mark Notification as Read
`POST /notifications/notifications/{id}/mark_as_read/`
- Returns: Success status
- Response Schema:
```json
{
  "status": "string"
}
```

### Mark All Notifications as Read
`POST /notifications/notifications/mark_all_as_read/`
- Returns: Success status
- Response Schema:
```json
{
  "status": "string"
}
