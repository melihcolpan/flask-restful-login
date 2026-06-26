# Flask-RESTful Login

A small, easy-to-read example of **token-based authentication** built with
[Flask](https://flask.palletsprojects.com/) and
[Flask-RESTful](https://flask-restful.readthedocs.io/). It shows how to register
users, log them in, issue short-lived access tokens and longer-lived refresh
tokens, and protect routes by user role (user / admin / super admin).

It is intentionally minimal so you can read the whole thing in an afternoon and
use it as a starting point for your own API.

---

## Features

- 🔐 **Register / Login / Logout** with JSON requests
- 🪙 **JWT-style access + refresh tokens** (signed and time-limited)
- 👮 **Role-based access** — `user`, `admin`, `super_admin`
- 🔑 **Passwords hashed with bcrypt** (never stored in plaintext)
- 🧪 A small **test suite** you can run in one command
- 🗄️ **SQLite** database (zero setup) via Flask-SQLAlchemy

## Tech stack

| Purpose            | Library                  |
| ------------------ | ------------------------ |
| Web framework      | Flask + Flask-RESTful    |
| Database / ORM     | Flask-SQLAlchemy + SQLite|
| Password hashing   | bcrypt                   |
| Token signing      | itsdangerous             |
| Auth header parsing| Flask-HTTPAuth           |

---

## Project structure

```
flask-restful-login/
├── main.py                     # App entry point (creates and runs the app)
├── requirements.txt
└── api/
    ├── conf/
    │   ├── auth.py             # Token serializers + auth object
    │   └── routes.py           # URL → handler wiring
    ├── handlers/
    │   └── UserHandlers.py     # Register, Login, Logout, Refresh, etc.
    ├── models/
    │   └── models.py           # User + Blacklist models, password hashing
    └── tests/                  # Unit tests
```

---

## Prerequisites

- **Python 3.8+**
- A tool to send HTTP requests. Any of these work:
  [httpie](https://httpie.io/) (used below), `curl`, Postman, or Insomnia.

---

## Quick start

```bash
# 1. Get the code
git clone https://github.com/melihcolpan/flask-restful-login
cd flask-restful-login

# 2. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate        # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set the required secrets (see the table below).
#    These can be any random strings — here we generate them automatically.
export JWT_SECRET=$(python -c "import secrets; print(secrets.token_hex(32))")
export REFRESH_JWT_SECRET=$(python -c "import secrets; print(secrets.token_hex(32))")
export SECRET_KEY=$(python -c "import secrets; print(secrets.token_hex(32))")

# 5. Run it
python main.py
```

The API is now running at **http://localhost:5000**.

> 💡 On Windows PowerShell, set a variable with `$env:JWT_SECRET="..."` instead
> of `export`.

### Environment variables

| Variable             | Required | Default | What it does                                            |
| -------------------- | :------: | ------- | ------------------------------------------------------- |
| `JWT_SECRET`         |   ✅     | –       | Signs **access** tokens. Keep it secret.                |
| `REFRESH_JWT_SECRET` |   ✅     | –       | Signs **refresh** tokens. Keep it secret.               |
| `SECRET_KEY`         |   ✅     | –       | Flask's secret key (sessions / security).               |
| `DEBUG`              |   ❌     | `False` | Set to `True` for the auto-reloading debug server.      |

The app **refuses to start** if a required secret is missing — this is on
purpose, so you never accidentally ship hardcoded secrets to production.

---

## How authentication works (the 30-second version)

1. You **register** a user, then **log in** with their email + password.
2. The server returns two tokens:
   - **`access_token`** — short-lived (1 hour). Send it on every protected
     request in the header `Authorization: Bearer <access_token>`.
   - **`refresh_token`** — longer-lived (2 hours). Use it to get a new access
     token when the old one expires, without logging in again.
3. **Logout** invalidates a refresh token by adding it to a blacklist.

---

## API reference

Base URL: `http://localhost:5000`

| Method | Endpoint                   | Auth required | Description                          |
| ------ | -------------------------- | :-----------: | ------------------------------------ |
| GET    | `/`                        | –             | Health check / hello message         |
| POST   | `/v1/auth/register`        | –             | Create a new user                    |
| POST   | `/v1/auth/login`           | –             | Log in, receive tokens               |
| POST   | `/v1/auth/refresh`         | –             | Exchange a refresh token for a new access token |
| POST   | `/v1/auth/logout`          | ✅ Bearer     | Invalidate a refresh token           |
| POST   | `/v1/auth/password_reset`  | ✅ Bearer     | Change your password                 |
| GET    | `/data_user`               | ✅ Bearer     | Example route for any logged-in user |
| GET    | `/data_admin`              | ✅ Admin      | Example route for admins             |
| GET    | `/data_super_admin`        | ✅ Super admin| Example route for super admins       |
| GET    | `/users`                   | ✅ Super admin| Search users by name/email/date      |

> **Note on roles:** `register` always creates a normal **`user`**. The `admin`
> and `super_admin` roles are assigned out-of-band (e.g. directly in the
> database) — there are intentionally no default admin accounts.

---

## Usage examples

The examples use [httpie](https://httpie.io/). A `curl` equivalent is shown for
the first two so you can adapt the rest.

### 1. Register

```bash
http POST :5000/v1/auth/register \
  username=alice password=s3cret email=alice@example.com
```

```bash
# curl version
curl -X POST http://localhost:5000/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"alice","password":"s3cret","email":"alice@example.com"}'
```

Response:

```json
{ "status": "registration completed." }
```

### 2. Login

```bash
http POST :5000/v1/auth/login email=alice@example.com password=s3cret
```

```bash
# curl version
curl -X POST http://localhost:5000/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"alice@example.com","password":"s3cret"}'
```

Response — copy the `access_token`, you'll need it next:

```json
{
  "access_token": "eyJ...",
  "refresh_token": "eyJ..."
}
```

### 3. Call a protected route

Pass the access token in the `Authorization` header:

```bash
http GET :5000/data_user Authorization:"Bearer <ACCESS_TOKEN>"
```

### 4. Refresh an expired access token

```bash
http POST :5000/v1/auth/refresh refresh_token=<REFRESH_TOKEN>
```

### 5. Change your password

```bash
http POST :5000/v1/auth/password_reset \
  Authorization:"Bearer <ACCESS_TOKEN>" \
  old_pass=s3cret new_pass=ev3nm0resecret
```

### 6. Logout (invalidate a refresh token)

```bash
http POST :5000/v1/auth/logout \
  Authorization:"Bearer <ACCESS_TOKEN>" \
  refresh_token=<REFRESH_TOKEN>
```

### 7. Search users (super admin only)

```bash
http GET :5000/users \
  Authorization:"Bearer <ACCESS_TOKEN>" \
  usernames==alice,bob \
  emails==alice@example.com,bob@example.com \
  start_date==01.01.1990 end_date==01.01.2050
```

---

## Running the tests

```bash
# Tests still need the secret env vars to import the app.
export JWT_SECRET=test REFRESH_JWT_SECRET=test SECRET_KEY=test

python -m unittest discover -s api/tests -p "tests_*.py"
```

You should see all tests pass.

---

## Security notes

This example follows a few basic good practices you should keep in your own apps:

- **No hardcoded secrets** — token secrets and `SECRET_KEY` come from the
  environment, and the app won't start without them.
- **Passwords are hashed with bcrypt** — the database never stores plaintext.
- **No default accounts** — there are no built-in admin users with known
  passwords.
- **Login doesn't leak which emails exist** — a wrong password and an unknown
  user return the same error.

For real production use you'd also want HTTPS, a production WSGI server
(e.g. gunicorn), a real database (PostgreSQL), and rate limiting.

---

## License

[MIT](LICENCE) — free to use, modify, and learn from.
