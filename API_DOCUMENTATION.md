# API Documentation

## Authentication
All endpoints require authentication using a token. Obtain a token by sending a POST request to `/auth/token/login/` with username and password.

## Profiles

### Get Current User Profile
`GET /profiles/me/`
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
  "background_image": "integer|null",
  "date_of_birth": "string|null (YYYY-MM-DD)",
  "location": "string",
  "following_count": "integer",
  "follower_count": "integer",
  "is_following": "boolean"
}
```

### Update Current User Profile
`PUT /profiles/me/`
- Parameters:
  - bio: string (optional)
  - profile_picture: integer (optional)
  - background_image: integer (optional)
  - date_of_birth: string (optional, YYYY-MM-DD)
  - location: string (optional)
- Returns: Updated profile
- Response Schema: Same as GET /profiles/me/

### Get User Profile
`GET /profiles/{id}/profile/`
- Returns: Profile details
- Response Schema: Same as GET /profiles/me/

### Follow User
`POST /profiles/{id}/follow/`
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
`POST /profiles/{id}/unfollow/`
- Returns: 204 No Content

### Get User Followers
`GET /profiles/{id}/followers/`
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
`GET /profiles/{id}/following/`
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
`GET /profiles/{id}/is_following/`
- Returns: Follow status
- Response Schema:
```json
{
  "is_following": "boolean"
}
```

## Posts

### Create Post
`POST /posts/`
- Parameters:
  - content: string (required)
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
  "likes": [
    {
      "id": "integer",
      "user": {
        "id": "integer",
        "username": "string"
      },
      "created_at": "string (ISO 8601 datetime)"
    }
  ]
}
```

### Get Post
`GET /posts/{id}/`
- Returns: Post details
- Response Schema: Same as POST /posts/

### Update Post
`PUT /posts/{id}/`
- Parameters:
  - content: string (required)
  - media_files: array of file IDs (optional)
- Returns: Updated post
- Response Schema: Same as POST /posts/

### Delete Post
`DELETE /posts/{id}/`
- Returns: 204 No Content

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
`POST /posts/{id}/unlike/`
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
  - content: string (required)
- Returns: Created comment
- Response Schema: Same as GET /posts/{id}/comments/

## Notifications

### Get Notifications
`GET /notifications/`
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
    "content": {
      "id": "integer",
      "user": {
        "id": "integer",
        "username": "string"
      },
      "content": "string",
      "created_at": "string (ISO 8601 datetime)",
      "updated_at": "string (ISO 8601 datetime)",
      "media_files": [],
      "likes": []
    },
    "notification_type": "string (like|comment|reply)",
    "created_at": "string (ISO 8601 datetime)",
    "is_read": "boolean"
  }
]
```

### Mark Notification as Read
`POST /notifications/{id}/mark_as_read/`
- Returns: Success status
- Response Schema:
```json
{
  "status": "string"
}
```

### Mark All Notifications as Read
`POST /notifications/mark_all_as_read/`
- Returns: Success status
- Response Schema:
```json
{
  "status": "string"
}
```

## Files

### Upload File
`POST /files/`
- Request: The file uploading
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

### Delete File
`DELETE /files/{id}/`
- Returns: 204 No Content
