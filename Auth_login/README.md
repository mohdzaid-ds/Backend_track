# Auth_login with fastAPI and supabase

A backend authentication service built with **FastAPI** and **Supabase Authentication**. This project implements user signup, login, JWT-protected endpoints, logout, and public API access.

The project was completed as part of the **FlyRank Backend AI Engineering Internship – Authentication & Login assignment**.

---

## Project Overview

The purpose of this assignment is to build a secure authentication layer for a FastAPI application using Supabase as the authentication provider.

The project demonstrates:

* User registration
* User login
* JWT-based authentication
* Protected API endpoints
* Public API endpoints
* Token validation
* Reusable FastAPI authentication dependencies
* User logout
* Swagger/OpenAPI authentication testing
* Environment variable management

---

## Technologies Used

* **Python**
* **FastAPI**
* **Supabase**
* **PyJWT**
* **Cryptography**
* **python-dotenv**
* **Uvicorn**
* **Swagger UI / OpenAPI**

---

## Project Structure

```text
Auth_login/
│
├── main.py
├── auth.py
├── supabase_client.py
├── requirements.txt
├── .env
├── .env.example
├── .gitignore
└── README.md
```

### File Description

| File                 | Purpose                                                   |
| -------------------- | --------------------------------------------------------- |
| `main.py`            | FastAPI application and API endpoints                     |
| `auth.py`            | JWT validation and reusable authentication dependency     |
| `supabase_client.py` | Supabase client configuration                             |
| `requirements.txt`   | Python dependencies                                       |
| `.env`               | Local environment variables and secrets                   |
| `.env.example`       | Example environment variable template                     |
| `.gitignore`         | Prevents sensitive/unnecessary files from being committed |
| `README.md`          | Project documentation                                     |

---

# Assignment Stages

## Stage 0 — Supabase and FastAPI Setup

The application was connected to a Supabase project and configured to run locally using FastAPI.

Environment variables are loaded using `python-dotenv`.

The actual `.env` file must remain private and should **never be committed to GitHub**.

---

## Stage 1 — Authentication

Two authentication endpoints were implemented.

### Signup

```http
POST /auth/signup
```

Creates a new user account using an email address and password.

### Login

```http
POST /auth/login
```

Authenticates an existing user and returns authentication tokens.

The access token is subsequently used to access protected endpoints.

---

## Stage 2 — Public and Protected Routes

A public endpoint and protected profile endpoint were added.

### Public Information

```http
GET /public/info
```

This endpoint does not require authentication.

### Protected Profile

```http
GET /protected/profile
```

This endpoint requires a valid:

```text
Authorization: Bearer <access_token>
```

header.

---

## Stage 3 — JWT Verification

The application validates the JWT access token before allowing access to protected endpoints.

JWT signing keys are obtained through Supabase's JWKS endpoint.

The authentication logic is centralized in `auth.py` so protected endpoints can reuse the same authentication dependency.

Invalid or expired tokens are rejected with an HTTP `401 Unauthorized` response.

---

## Stage 4 — Reusable Authentication Guard

A reusable FastAPI dependency was created:

```python
get_current_user
```

Protected endpoints use this dependency rather than implementing authentication logic separately.

For example:

```python
@app.get("/protected/profile")
def profile(user=Depends(get_current_user)):
    ...
```

This approach allows multiple endpoints to share the same authentication mechanism.

### Logout

```http
POST /auth/logout
```

Logout is also a protected endpoint and requires a valid access token.

On successful logout, the API returns:

```text
204 No Content
```

### Dashboard

```http
GET /protected/dashboard
```

The dashboard is another protected endpoint demonstrating that the same authentication dependency can be reused.

---

# API Reference

| Method | Endpoint               | Authentication | Description                         |
| ------ | ---------------------- | -------------- | ----------------------------------- |
| `POST` | `/auth/signup`         | No             | Register a new user                 |
| `POST` | `/auth/login`          | No             | Authenticate a user                 |
| `GET`  | `/public/info`         | No             | Access public information           |
| `GET`  | `/protected/profile`   | Yes            | Access authenticated user's profile |
| `POST` | `/auth/logout`         | Yes            | Log out an authenticated user       |
| `GET`  | `/protected/dashboard` | Yes            | Access protected dashboard          |

---

# Authentication Flow

The authentication flow works as follows:

```text
                    ┌─────────────────┐
                    │     Client      │
                    └────────┬────────┘
                             │
                             ▼
                    POST /auth/signup
                             │
                             ▼
                       ┌───────────┐
                       │  Supabase │
                       │   Auth    │
                       └───────────┘
                             │
                             ▼
                       User Created
                             │
                             │
                    POST /auth/login
                             │
                             ▼
                       ┌───────────┐
                       │  Supabase │
                       │   Auth    │
                       └─────┬─────┘
                             │
                             ▼
                       Access Token
                             │
                             ▼
                  Authorization: Bearer
                             │
                             ▼
                       ┌───────────┐
                       │  FastAPI  │
                       └─────┬─────┘
                             │
                             ▼
                    get_current_user
                             │
                             ▼
                       JWT Validation
                             │
                       ┌─────┴─────┐
                       │           │
                     Valid       Invalid
                       │           │
                       ▼           ▼
                    Endpoint      401
                    Response
```

---

# Requirements

Make sure the following are installed:

* Python 3.10+
* Supabase account
* Git
* VS Code or another code editor

---

# Installation

## 1. Clone the Repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
```

Move into the project directory:

```bash
cd Auth_login
```

---

## 2. Create a Virtual Environment

On Windows:

```powershell
python -m venv venv
```

Activate it:

```powershell
venv\Scripts\activate
```

You should see `(venv)` in your terminal after activation.

---

## 3. Install Dependencies

Install all required Python packages:

```powershell
pip install -r requirements.txt
```

If `requirements.txt` has not been created yet, the main dependencies are:

```text
fastapi
uvicorn
supabase
python-dotenv
PyJWT
cryptography
```

---

# Environment Configuration

Create a `.env` file in the project root.

Example:

```env
SUPABASE_URL=your_supabase_project_url
SUPABASE_KEY=your_supabase_anon_key
PORT=8000
```

### Important

Do **not** put real credentials in this README or upload them to GitHub.

The `.env` file should be included in `.gitignore`.

Example:

```gitignore
.env
venv/
__pycache__/
*.pyc
```

---

# `.env.example`

The repository should contain a safe example configuration:

```env
SUPABASE_URL=your_supabase_project_url
SUPABASE_KEY=your_supabase_anon_key
PORT=8000
```

This file contains placeholders only and does not contain real credentials.

---

# Supabase Configuration

Create a project in Supabase and obtain the project URL and API key from the Supabase project settings.

Add them to your local `.env` file.

For local practice/testing, configure the Supabase authentication settings according to the assignment requirements.

---

# Running the Application

Start the FastAPI development server with:

```powershell
uvicorn main:app --reload
```

The application should start on:

```text
http://localhost:8000
```

---

# Swagger Documentation

FastAPI automatically provides interactive API documentation.

Open:

```text
http://localhost:8000/docs
```

Swagger UI can be used to test all API endpoints.

For protected endpoints:

1. Register or log in a user.
2. Copy the returned access token.
3. Click **Authorize** in Swagger.
4. Enter the access token using the Bearer authentication scheme.
5. Execute the protected endpoint.

The protected endpoints should then be able to access the authenticated user.

---

# Testing the Authentication Flow

A typical testing sequence is:

### 1. Register

```http
POST /auth/signup
```

Provide:

```json
{
  "email": "user@example.com",
  "password": "your-password"
}
```

---

### 2. Login

```http
POST /auth/login
```

Provide the same credentials.

The response contains an access token.

---

### 3. Authorize Swagger

Click:

```text
Authorize
```

and provide the returned access token.

---

### 4. Test Public Endpoint

```http
GET /public/info
```

This endpoint should work without authentication.

---

### 5. Test Profile

```http
GET /protected/profile
```

A valid access token is required.

---

### 6. Test Dashboard

```http
GET /protected/dashboard
```

A valid access token is required.

---

### 7. Test Logout

```http
POST /auth/logout
```

A valid access token is required.

Successful logout returns:

```text
204 No Content
```

---

# Error Handling

The API uses appropriate HTTP status codes for authentication failures.

| Status | Meaning                                   |
| ------ | ----------------------------------------- |
| `200`  | Successful request                        |
| `201`  | User successfully created                 |
| `204`  | Successful logout with no response body   |
| `400`  | Invalid or missing request data           |
| `401`  | Authentication failed or token is invalid |
| `500`  | Unexpected server-side error              |

For example, an invalid authentication token results in:

```text
401 Unauthorized
```

---

# Security Considerations

This project follows several basic security practices:

* Secrets are stored in environment variables.
* `.env` is excluded from Git.
* Authentication is required for protected endpoints.
* JWT tokens are validated before accessing protected resources.
* Authentication logic is centralized in a reusable dependency.
* No real credentials should be included in the repository.
* `.env.example` contains placeholders rather than secrets.

Never commit:

```text
.env
```

or any file containing:

* Supabase secret keys
* API keys
* JWT secrets
* Passwords
* Access tokens
* Refresh tokens

---

# Learning Outcomes

This assignment demonstrates practical understanding of:

* FastAPI application development
* REST API endpoint design
* Supabase Authentication
* User registration and login
* JWT authentication
* JWT validation
* HTTP Bearer authentication
* FastAPI dependencies
* Protected routes
* Environment variables
* API testing with Swagger UI
* Basic backend security practices
* Git/GitHub project management

---

# Running the Project — Quick Reference

After cloning the repository:

```powershell
cd Auth_login
```

Create and activate the virtual environment:

```powershell
python -m venv venv
venv\Scripts\activate
```

Install dependencies:

```powershell
pip install -r requirements.txt
```

Configure `.env`:

```env
SUPABASE_URL=your_supabase_project_url
SUPABASE_KEY=your_supabase_anon_key
PORT=8000
```

Start the server:

```powershell
uvicorn main:app --reload
```

Open Swagger:

```text
http://localhost:8000/docs
```

---

# Assignment Completion

The project implements the required authentication workflow:

* [x] Supabase configuration
* [x] User signup
* [x] User login
* [x] Public endpoint
* [x] Protected profile endpoint
* [x] JWT verification
* [x] Reusable authentication dependency
* [x] Protected logout
* [x] Protected dashboard
* [x] Swagger API documentation
* [x] Environment variable configuration
* [x] `.env` protection
* [x] `.env.example`

---

## Author

**Mohd Zaid**

Backend AI Engineering Intern / AI & ML Student

This project was created as part of backend engineering and AI engineering internship coursework.

