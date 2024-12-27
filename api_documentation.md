# API Documentation

## Authentication

See Djoser docs for [Base Endpoints](https://djoser.readthedocs.io/en/latest/base_endpoints.html) and [Token Endpoints](https://djoser.readthedocs.io/en/latest/token_endpoints.html).

Following operation requires a token acquired from the token endpoint. Put it inside the header like:

````http
Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
````

## File Operations

### List Files
**Endpoint:** `GET /files/`

**Description:**  
List all files uploaded by the authenticated user.

**Response:**
```json
[
    {
        "id": "uuid",
        "file": "url",
        "owner": "user_id",
        "created_at": "timestamp"
    }
]
```

### Upload File
**Endpoint:** `POST /files/`

**Description:**  
Upload a new file. The file should be sent as form-data with the file field.

**Request:**
- Content-Type: multipart/form-data
- Body: file (binary)

**Response:**
```json
{
    "id": "uuid",
    "file": "url",
    "owner": "user_id",
    "created_at": "timestamp"
}
```

### Get File Details
**Endpoint:** `GET /files/{id}/`

**Description:**  
Get details of a specific file.

**Response:**
```json
{
    "id": "uuid",
    "file": "url",
    "owner": "user_id",
    "created_at": "timestamp"
}
```

### Delete File
**Endpoint:** `DELETE /files/{id}/`

**Description:**  
Delete a specific file.

**Response:**
- 204 No Content

**Notes:**
- Users can only access their own files
- File URLs are absolute paths to the media files

## User Operations

### Get User Details
**Endpoint:** `GET /users/{id}/`

**Description:**  
Get details of a specific user.

**Response:**
```json
{
    "id": "user_id",
    "username": "username",
    "profile": {
        "id": "profile_id",
        "bio": "text",
        "profile_picture": "file_id",
        "date_of_birth": "date",
        "location": "string"
    }
}
```

### Manage Profile
**Endpoint:** `GET|POST|PUT|PATCH /users/profile/`

**Description:**  
Manage the authenticated user's profile.

**GET Response:**
```json
{
    "id": "profile_id",
    "bio": "text",
    "profile_picture": "file_id",
    "date_of_birth": "date",
    "location": "string"
}
```

**POST Request:**
```json
{
    "bio": "text",
    "profile_picture": "file_id",
    "date_of_birth": "date",
    "location": "string"
}
```

**PUT/PATCH Request:**
```json
{
    "bio": "text",
    "profile_picture": "file_id",
    "date_of_birth": "date",
    "location": "string"
}
```

**Response:**
```json
{
    "id": "profile_id",
    "bio": "text",
    "profile_picture": "file_id",
    "date_of_birth": "date",
    "location": "string"
}
```

### Follow User
**Endpoint:** `POST /users/{id}/follow/`

**Description:**  
Follow another user.

**Response:**
```json
{
    "id": "follower_id",
    "follower": {
        "id": "user_id",
        "username": "username"
    },
    "followed": {
        "id": "user_id",
        "username": "username"
    },
    "created_at": "timestamp"
}
```

### Unfollow User
**Endpoint:** `DELETE /users/{id}/unfollow/`

**Description:**  
Unfollow a user.

**Response:**
- 204 No Content

### Check Following Status
**Endpoint:** `GET /users/{id}/is_following/`

**Description:**  
Check if the authenticated user is following another user.

**Response:**
```json
{
    "is_following": true|false
}
```

### Get Followers
**Endpoint:** `GET /users/{id}/followers/`

**Description:**  
Get list of users following the specified user.

**Response:**
```json
[
    {
        "id": "follower_id",
        "follower": {
            "id": "user_id",
            "username": "username"
        },
        "followed": {
            "id": "user_id",
            "username": "username"
        },
        "created_at": "timestamp"
    }
]
```

### Get Following
**Endpoint:** `GET /users/{id}/following/`

**Description:**  
Get list of users the specified user is following.

**Response:**
```json
[
    {
        "id": "follower_id",
        "follower": {
            "id": "user_id",
            "username": "username"
        },
        "followed": {
            "id": "user_id",
            "username": "username"
        },
        "created_at": "timestamp"
    }
]
```

**Notes:**
- Users can only modify their own profile
- Following relationships are unique (cannot follow same user multiple times)

## Post Operations

### List Posts
**Endpoint:** `GET /posts/`

**Description:**  
List all posts with their comments and likes.

**Response:**
```json
[
    {
        "id": "post_id",
        "user": {
            "id": "user_id",
            "username": "username"
        },
        "content": "text",
        "created_at": "timestamp",
        "updated_at": "timestamp",
        "media_files": [
            {
                "id": "file_id",
                "file": "url",
                "owner": "user_id",
                "created_at": "timestamp"
            }
        ],
        "comments": [
            {
                "id": "comment_id",
                "user": {
                    "id": "user_id",
                    "username": "username"
                },
                "content": "text",
                "created_at": "timestamp",
                "updated_at": "timestamp"
            }
        ],
        "likes": [
            {
                "id": "like_id",
                "user": {
                    "id": "user_id",
                    "username": "username"
                },
                "created_at": "timestamp"
            }
        ]
    }
]
```

### Create Post
**Endpoint:** `POST /posts/`

**Description:**  
Create a new post.

**Request:**
```json
{
    "content": "text",
    "media_files": ["file_id"]
}
```

**Response:**
```json
{
    "id": "post_id",
    "user": {
        "id": "user_id",
        "username": "username"
    },
    "content": "text",
    "created_at": "timestamp",
    "updated_at": "timestamp",
    "media_files": [
        {
            "id": "file_id",
            "file": "url",
            "owner": "user_id",
            "created_at": "timestamp"
        }
    ],
    "comments": [],
    "likes": []
}
```

### Get Post Details
**Endpoint:** `GET /posts/{id}/`

**Description:**  
Get details of a specific post.

**Response:**
```json
{
    "id": "post_id",
    "user": {
        "id": "user_id",
        "username": "username"
    },
    "content": "text",
    "created_at": "timestamp",
    "updated_at": "timestamp",
    "media_files": [
        {
            "id": "file_id",
            "file": "url",
            "owner": "user_id",
            "created_at": "timestamp"
        }
    ],
    "comments": [
        {
            "id": "comment_id",
            "user": {
                "id": "user_id",
                "username": "username"
            },
            "content": "text",
            "created_at": "timestamp",
            "updated_at": "timestamp"
        }
    ],
    "likes": [
        {
            "id": "like_id",
            "user": {
                "id": "user_id",
                "username": "username"
            },
            "created_at": "timestamp"
        }
    ]
}
```

### Update Post
**Endpoint:** `PUT|PATCH /posts/{id}/`

**Description:**  
Update a post.

**Request:**
```json
{
    "content": "text",
    "media_files": ["file_id"]
}
```

**Response:**
```json
{
    "id": "post_id",
    "user": {
        "id": "user_id",
        "username": "username"
    },
    "content": "text",
    "created_at": "timestamp",
    "updated_at": "timestamp",
    "media_files": [
        {
            "id": "file_id",
            "file": "url",
            "owner": "user_id",
            "created_at": "timestamp"
        }
    ],
    "comments": [
        {
            "id": "comment_id",
            "user": {
                "id": "user_id",
                "username": "username"
            },
            "content": "text",
            "created_at": "timestamp",
            "updated_at": "timestamp"
        }
    ],
    "likes": [
        {
            "id": "like_id",
            "user": {
                "id": "user_id",
                "username": "username"
            },
            "created_at": "timestamp"
        }
    ]
}
```

### Delete Post
**Endpoint:** `DELETE /posts/{id}/`

**Description:**  
Delete a post.

**Response:**
- 204 No Content

### Like Post
**Endpoint:** `POST /posts/{id}/like/`

**Description:**  
Like a post.

**Response:**
```json
{
    "id": "like_id",
    "user": {
        "id": "user_id",
        "username": "username"
    },
    "created_at": "timestamp"
}
```

### Unlike Post
**Endpoint:** `DELETE /posts/{id}/unlike/`

**Description:**  
Unlike a post.

**Response:**
- 204 No Content

### Get Post Comments
**Endpoint:** `GET /posts/{id}/comments/`

**Description:**  
Get comments for a post.

**Response:**
```json
[
    {
        "id": "comment_id",
        "user": {
            "id": "user_id",
            "username": "username"
        },
        "content": "text",
        "created_at": "timestamp",
        "updated_at": "timestamp"
    }
]
```

### Add Comment
**Endpoint:** `POST /posts/{id}/comments/`

**Description:**  
Add a comment to a post.

**Request:**
```json
{
    "content": "text"
}
```

**Response:**
```json
{
    "id": "comment_id",
    "user": {
        "id": "user_id",
        "username": "username"
    },
    "content": "text",
    "created_at": "timestamp",
    "updated_at": "timestamp"
}
```

**Notes:**
- Users can only modify their own posts
- Media files must be uploaded first using the file API
- Likes are unique per user-post combination

## Message Operations

### List Messages
**Endpoint:** `GET /chat/messages/`

**Description:**  
List all messages for the authenticated user (both sent and received).

**Response:**
```json
[
    {
        "id": "message_id",
        "sender": {
            "id": "user_id",
            "username": "username"
        },
        "recipient": {
            "id": "user_id",
            "username": "username"
        },
        "content": "text",
        "timestamp": "datetime",
        "is_read": true|false,
        "is_delivered": true|false
    }
]
```

### Send Message
**Endpoint:** `POST /chat/messages/`

**Description:**  
Send a new message.

**Request:**
```json
{
    "recipient": "username",
    "content": "text"
}
```

**Response:**
```json
{
    "id": "message_id",
    "sender": {
        "id": "user_id",
        "username": "username"
    },
    "recipient": {
        "id": "user_id",
        "username": "username"
    },
    "content": "text",
    "timestamp": "datetime",
    "is_read": false,
    "is_delivered": false
}
```

### Mark Message as Read
**Endpoint:** `POST /chat/messages/{id}/mark_read/`

**Description:**  
Mark a received message as read.

**Response:**
```json
{
    "status": "message marked as read"
}
```

### Get Unread Message Count
**Endpoint:** `GET /chat/messages/unread_count/`

**Description:**  
Get count of unread messages.

**Response:**
```json
{
    "unread_count": number
}
```

### Get Conversation
**Endpoint:** `GET /chat/messages/conversation/?with=username`

**Description:**  
Get conversation history with a specific user.

**Response:**
```json
[
    {
        "id": "message_id",
        "sender": {
            "id": "user_id",
            "username": "username"
        },
        "recipient": {
            "id": "user_id",
            "username": "username"
        },
        "content": "text",
        "timestamp": "datetime",
        "is_read": true|false,
        "is_delivered": true|false
    }
]
```

### Set Online Status
**Endpoint:** `POST /chat/status/set_online/`

**Description:**  
Set user status to online.

**Response:**
```json
{
    "status": "online"
}
```

### Set Offline Status
**Endpoint:** `POST /chat/status/set_offline/`

**Description:**  
Set user status to offline.

**Response:**
```json
{
    "status": "offline"
}
```

### Set Typing Status
**Endpoint:** `POST /chat/status/set_typing/`

**Description:**  
Set user typing status.

**Response:**
```json
{
    "status": "typing"
}
```

### Stop Typing Status
**Endpoint:** `POST /chat/status/stop_typing/`

**Description:**  
Clear user typing status.

**Response:**
```json
{
    "status": "stopped typing"
}
```

**Notes:**
- Users can only access their own messages
- Messages are automatically marked as delivered when retrieved
- Typing status is automatically cleared after a short timeout
