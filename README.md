# Social Network API

This is a Django-based Social Network API that allows users to sign up, log in, search for other users, send and respond to friend requests, list friends, and list pending friend requests.

## Features

- User Registration and Login
- Search Users by Email and Name
- Send, Accept, and Reject Friend Requests
- List Friends
- List Pending Friend Requests
- Throttling for Friend Request Sending

## Installation

### Prerequisites

- Python 3.8 or later
- Django 5.0.6
- Virtualenv

# Documentation

## Application Setup

### Setting Up the Repository and Environment

#### 1. Cloning the Repository

First, clone the repository to your local machine using git. Open a terminal and run the following command:

```bash
git  clone  https://github.com/Shashank9928/Social-Network.git

cd  Social-Network
```

#### 2. Setting Up a Virtual Environment

It's recommended to use a virtual environment for Python projects to manage dependencies separately from your global Python installation. If you haven't installed `virtualenv` yet, you can install it using pip:

```bash
pip  install  virtualenv
```

Create a new virtual environment in the project directory:

```bash
python  -m  venv  ve
```

Activate the virtual environment:

- On Windows:

```bash
.\ve\Scripts\activate
```

- On macOS and Linux:

```bash
source  ve/bin/activate
```

#### 3. Installing Dependencies

With the virtual environment activated, install the project dependencies:

```bash
pip  install  -r  requirements.txt
```

### Configuring the Application

#### 1. Setting Up the Database

If your Django project uses a database that requires initial setup (like PostgreSQL or MySQL), configure it accordingly. For SQLite (the default), no additional setup is required.

#### 2. Migrations

Run the following commands to perform database migrations:

```bash
python  manage.py  makemigrations
python  manage.py  migrate
```

#### 3. Creating a Superuser

To access the Django admin panel and authenticate API requests, create a superuser:
If you are using the provided Database in Repository Pre-existed superuser:
**Username: social
Password: 1234**

```bash
python  manage.py  createsuperuser
```

Follow the prompts to set the username, email, and password.

### Running the Application

Start the Django development server with the following command:

```bash
python  manage.py  runserver
```

The server will start, typically accessible via `http://127.0.0.1:8000/`.

### Accessing the Admin Panel

You can access the Django admin panel by navigating to `http://127.0.0.1:8000/admin` in your web browser. Log in using the superuser credentials you created earlier to manage your application’s data.

**Default Server Url**: [http://127.0.0.1:8000](http://127.0.0.1:8000/)

# API-DOCUMENTATION

## Authentication

### Overview

All API requests, with the exception of the login endpoint, require authentication. Our system utilizes token-based authentication to secure access and ensure that operations are performed by authenticated users.

### Creating a Superuser

Before authenticating, you must have a superuser account. If you haven't already set up a superuser, you can create one using the following command:

bash: `python manage.py createsuperuser`

Follow the prompts to set the username, email, and password for the superuser.

### Using a Pre-configured Superuser

If you are using the provided database (`db.sqlite3` from this repository), a superuser with the following credentials is already set up:

- **Username:** social

- **Password:** 1234

You can use these credentials to test and interact with the API without setting up a new superuser.

Include the token in the HTTP header as follows:

`Authorization: Token <YOUR_TOKEN>`

Replace `<YOUR_TOKEN>` with the token you received from the login response.

### 1. **User Signup**

**Endpoint:** `/api/signup/`

**Method:** POST

**Permissions:** Allow any user (authenticated or not)

**Description:**

Create a new user account.

**Request Parameters:**

- `email` (string): The user's email.
- `password` (string): The user's password.
- `name` (string): The user's name.
- `phone` (string): The user's phone number.

**Responses:**

- **200 OK**: Successful authentication.

- **Body**:

```json
{
  "id": 1,
  "email": "sample@example.com",
  "name": "sample",
  "phone": "Doe02"
}
```

- **400 Bad Request**: Data validation failed.

- **Body**:

```json
{
  "error": "Validation errors here."
}
```

### 2. **User Login**

**Endpoint:** `/api/login/`

**Methods:** POST

**Permissions:** Allow any user (authenticated or not)

**Description:**

Log in to the application.

**Request Parameters:**

- `email` (string): The user's email.
- `password` (string): The user's password.

**Responses:**

- **200 OK**: Successful authentication.

- **Body:**

```json
{
  "token": "367d5c117ca25044a0d2442e4fb611d4fbd28572"
}
```

**400 Bad Request**: Missing email or password.

- **Body:**

  ```json
  {
    "error": "Both email and password are required."
  }
  ```

- **401 Unauthorized**: Invalid email or password.
  - **Body:**

    ```json
    {
      "error": "Invalid credentials"
    }
    ```
- **405 Method Not Allowed**: If any method other than POST is used.
  - **Body:**

    ```json
    {
      "error": "<METHOD> method not allowed."
    }
    ```

## 3. **Search Users**

**Endpoint:** `api/search/?q=YourQuery`

**Method:** GET

**Permissions:** Authenticated Users

**Headers:**

- `Authorization: Token <YOUR_TOKEN>`

**Description:**

Search for users by email or name (paginated, 10 records per page).

**Query Parameters:**

- `q` (string): Search keyword.

**Responses:**

- **200 OK**: Successfully retrieved list of users.
  - **Body:**

```json
[
  {
    "id": 2,
    "email": "john02@example.com",
    "name": "John Doe",
    "phone": "1234567890"
  },
  {
    "id": 3,
    "email": "jane@example.com",
    "name": "Jane Doe",
    "phone": "0987654321"
  }
]
```

### **Send Friend Request**

**Endpoint:** `/api/friend-request/send/`

**Method:** POST

**Permissions:** Authenticated Users

**Headers:**

- `Authorization: Token <YOUR_TOKEN>`
- `Content-Type: application/json`

**Description:**

Send a friend request to another user.

**Request Parameters:**

- `email` (string): The email of the user to whom the friend request is being sent.

**Responses:**

- **201 Created**: Friend request successfully sent.

  - **Body:**

    ```json
    {
      "status": "friend request sent"
    }
    ```

- **400 Bad Request**: Data validation failed or friend request already sent.

  - **Body:**

    ```json
    {
      "error": "Validation errors here."
    }
    ```

## 5. **Respond to Friend Request**

**Endpoint:** `/api/friend-request/respond/`

**Method:** POST

**Permissions:** Authenticated Users

**Headers:**

- `Authorization: Token <YOUR_TOKEN>`
- `Content-Type: application/json`

**Description:**

Accept or reject a friend request.

**Request Parameters:**

- `friend_request_id` (integer): The ID of the friend request.
- `action` (string): The action to be taken ('accept' or 'reject').

**Responses:**

- **200 OK**: Friend request successfully responded to.

  - **Body:**

    ```json
    {
      "status": "friend request accepted"
    }
    ```

  - **Body:**

    ```json
    {
      "status": "friend request rejected"
    }
    ```

- **400 Bad Request**: Data validation failed.
  - **Body:**

    ```json
    {
      "error": "Validation errors here."
    }
    ```

## 6. **List Friends**

**Endpoint:** `/api/friends/`

**Method:** GET

**Permissions:** Authenticated Users

**Headers:**

- `Authorization: Token <YOUR_TOKEN>`
- `Content-Type: application/json`

**Description:**

List all friends of the authenticated user.

**Responses:**

- **200 OK**: Successfully retrieved list of friends.
  - **Body:**

    ```json
    [
      {
        "id": 1,
        "from_user": {
          "id": 2,
          "email": "john01@example.com",
          "name": "John",
          "phone": "1234567890"
        },
        "to_user": {
          "id": 3,
          "email": "jane@example.com",
          "name": "Jane",
          "phone": "0987654321"
        },
        "status": "accepted"
      }
    ]
    ```

## 7. **List Pending Friend Requests**

**Endpoint:** `/api/friend-requests/pending/`

**Method:** GET

**Permissions:** Authenticated Users

**Headers:**

- `Authorization: Token <YOUR_TOKEN>`
- `Content-Type: application/json`

**Description:**

List all pending friend requests received by the authenticated user.

**Responses:**

- **200 OK**: Successfully retrieved list of pending friend requests.

  - **Body:**

    ```json
    [
      {
        "id": 2,
        "from_user": {
          "id": 2,
          "email": "john01@example.com",
          "name": "John",
          "phone": "1234567890"
        },
        "to_user": {
          "id": 3,
          "email": "jane@example.com",
          "name": "Jane",
          "phone": "0987654321"
        },
        "status": "pending"
      }
    ]
    ```

### Note

- Ensure that the `Authorization` token is included in the request headers for all protected endpoints.
- Use the `friend_request_id` from the response when responding to friend requests.
- The search functionality supports searching by both email and name.
