# FastAPI Notes CRUD Application

A minimal CRUD API for managing notes with JWT authentication built with FastAPI.

## Features

- **User Authentication**: JWT-based authentication with registration and login
- **Notes CRUD**: Create, Read, Update, Delete operations for notes
- **User Isolation**: Each user can only access their own notes
- **Race Condition Prevention**: Optimistic locking for concurrent updates
- **Input Validation**: Pydantic models for request/response validation
- **Database**: SQLite with SQLAlchemy ORM

## API Routes

### Authentication Routes

| Method | Path | Description | Request Body | Response |
|--------|------|-------------|--------------|----------|
| POST | `/auth/register` | Register new user | `{"username": "string", "email": "email", "password": "string"}` | `{"id": int, "username": "string", "email": "email", "created_at": "datetime"}` |
| POST | `/auth/login` | Login user | `{"username": "string", "password": "string"}` | `{"access_token": "string", "token_type": "bearer"}` |

### User Routes

| Method | Path | Description | Headers | Response |
|--------|------|-------------|---------|----------|
| GET | `/users/me` | Get current user profile | `Authorization: Bearer <token>` | `{"id": int, "username": "string", "email": "email", "created_at": "datetime"}` |

### Notes Routes

| Method | Path | Description | Headers | Request Body | Response |
|--------|------|-------------|---------|--------------|----------|
| POST | `/notes` | Create new note | `Authorization: Bearer <token>` | `{"title": "string", "content": "string"}` | `{"id": int, "title": "string", "content": "string", "created_at": "datetime", "updated_at": "datetime", "owner_id": int, "version": int}` |
| GET | `/notes` | Get all user notes | `Authorization: Bearer <token>` | - | `[{note_object}, ...]` |
| GET | `/notes/{id}` | Get specific note | `Authorization: Bearer <token>` | - | `{note_object}` |
| PUT | `/notes/{id}` | Update note | `Authorization: Bearer <token>` | `{"title": "string", "content": "string", "version": int}` | `{updated_note_object}` |
| DELETE | `/notes/{id}` | Delete note | `Authorization: Bearer <token>` | - | `204 No Content` |

### Utility Routes

| Method | Path | Description | Response |
|--------|------|-------------|----------|
| GET | `/health` | Health check | `{"status": "healthy"}` |

## Database Schema

### Users Table
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    hashed_password VARCHAR(128) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

### Notes Table
```sql
CREATE TABLE notes (
    id INTEGER PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    content TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    owner_id INTEGER NOT NULL REFERENCES users(id),
    version INTEGER DEFAULT 1 NOT NULL
);
```

## Authentication Choice

**Chosen: JWT (JSON Web Tokens)**

**Why JWT:**
1. **Stateless**: No server-side session storage required
2. **Scalable**: Easy to scale horizontally across multiple servers
3. **Standard**: Industry-standard authentication method
4. **Secure**: Cryptographically signed tokens prevent tampering
5. **Flexible**: Can include custom claims and expiration times
6. **Mobile-friendly**: Works well with mobile apps and SPAs

**Security Features:**
- Passwords are hashed using bcrypt
- Tokens expire after 30 minutes
- Bearer token authentication in headers
- User isolation (users can only access their own notes)

## Race Condition Mitigation

**Problem**: Concurrent Note Updates (Lost Update Problem)

**Scenario**: Two users (or same user in different tabs) try to update the same note simultaneously:
1. User A fetches note (version 1)
2. User B fetches same note (version 1)
3. User A updates note → saves with version 2
4. User B updates note → overwrites User A's changes

**Mitigation: Optimistic Locking**

**Implementation:**
1. Each note has a `version` field that increments on every update
2. Update requests must include the current version number
3. Server checks if the provided version matches the database version
4. If versions don't match → HTTP 409 Conflict with current version
5. Client must refresh data and retry with new version

**Code Example:**
```python
# Client sends update with version
PUT /notes/123
{
    "title": "Updated Title",
    "content": "Updated content", 
    "version": 1  # Version when data was fetched
}

# If note was already updated by another user:
HTTP 409 Conflict
{
    "detail": "Note has been modified by another user. Please refresh and try again."
}
Headers: X-Current-Version: 2
```

**Benefits:**
- Prevents silent data loss
- User-friendly error messages
- Forces explicit conflict resolution
- No database locks needed
- Scales well under high concurrency

## Installation and Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the application:**
   ```bash
   python main.py
   ```

3. **Access the API:**
   - API: http://localhost:8000
   - Interactive docs: http://localhost:8000/docs
   - Alternative docs: http://localhost:8000/redoc

4. **Run tests:**
   ```bash
   pytest test_main.py -v
   ```

## Environment Variables

- `SECRET_KEY`: JWT signing secret (change in production)

## Error Handling

The API returns appropriate HTTP status codes:
- `200`: Success
- `201`: Created
- `204`: No Content (successful deletion)
- `400`: Bad Request (validation errors)
- `401`: Unauthorized (invalid/missing token)
- `404`: Not Found (resource doesn't exist)
- `409`: Conflict (race condition, duplicate user)
- `422`: Unprocessable Entity (validation errors)
