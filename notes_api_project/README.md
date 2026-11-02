# Notes App - FastAPI + MongoDB + Redis (Beginner Project)

A simple notes app. One screen, all HTTP methods (GET, POST, PUT, DELETE) on the same page.

## 1. What to install (one time)
1. **Python 3.10+**  (tick "Add Python to PATH" while installing)
2. **MongoDB Community Server** + **MongoDB Compass**  (https://www.mongodb.com/try/download/community)
3. **Redis** (optional - app works without it, just no caching)
   - Windows: install **Memurai** (free Redis for Windows) OR use WSL: `sudo apt install redis-server` then `redis-server`
   - Mac: `brew install redis` then `redis-server`

## 2. Run in VS Code
Open this folder in VS Code, open the terminal (Ctrl + `) and type:

```
python -m venv venv
venv\Scripts\activate          (Mac/Linux: source venv/bin/activate)
pip install -r requirements.txt
uvicorn app.main:app --reload
```
Open **http://127.0.0.1:8000** in the browser. Done!
Top-right badges show MongoDB: ON / Redis: ON.

## 3. How the API connects to MongoDB
File: `app/database.py`
```python
mongo_client = MongoClient("mongodb://localhost:27017")
db = mongo_client["notes_app"]
notes_collection = db["notes"]
```
- `mongodb://localhost:27017` = address of MongoDB on your computer (default).
- If you can connect in Compass with this same address, the API connects too.
- If your MongoDB is somewhere else, change `MONGO_URL` in `app/config.py`.
- You do NOT need to create the database or collections. MongoDB creates them when the first note is saved.

## 4. See your data in MongoDB Compass
1. Open Compass -> click **Connect** (uses `mongodb://localhost:27017`)
2. Open database **notes_app**
3. Collection **notes** = all notes, collection **users** = all users
4. Add / edit / delete on the web page, then press the refresh button in Compass to see changes.

## 5. How to test everything on the one screen
| Do this | HTTP method | What you learn |
|---|---|---|
| Register, then Login | POST | Authentication |
| Add a note | POST | Pydantic validation (try a 1-letter title -> error) |
| Show Notes | GET | Pagination, sorting, filtering |
| Press Show Notes twice | GET | 1st = "database (MongoDB)", 2nd = "cache (Redis)" |
| Edit a note | PUT | Update |
| Delete as normal user | DELETE | 403 error = Authorization |
| Login as admin / admin123, delete | DELETE | Works! |
| Add note without login | POST | 401 error = Authentication |

The black "request log" box shows the method, URL, status code and response of the last action.

## 6. Folder structure (Layered architecture)
```
app/
  main.py                 starts the app
  config.py               settings (Mongo URL, Redis, cache time)
  database.py             MongoDB + Redis connections
  dependencies.py         login check + admin check
  models/schemas.py       Pydantic models (validation)
  routers/                LAYER 1: receives request, sends response
    notes.py, auth.py
  services/               LAYER 2: business logic (filter, sort, paginate, cache)
    note_service.py, auth_service.py, cache_service.py
  repositories/           LAYER 3: only talks to MongoDB
    note_repository.py, user_repository.py
  static/index.html       the single screen
```
Request flow:  **Browser -> Router -> Service -> Repository -> MongoDB**
Cache flow:    **Service -> Redis first; if not found -> Repository -> MongoDB -> save copy in Redis**

## 7. How to explain it (simple words)
- **Router**: "the waiter" - takes the order and brings the food. Does no cooking.
- **Service**: "the chef" - decides how to cook (filter, sort, pagination, caching).
- **Repository**: "the store room" - only fetches and stores things in MongoDB.
- **Pydantic**: "the security guard" - wrong data is stopped at the door (422 error).
- **Redis cache**: "sticky note" - remembers the last answer for 60 seconds so MongoDB is not asked again.
- **Authentication** = who are you? (login).  **Authorization** = what are you allowed to do? (only admin deletes).
- **Pagination** = `skip` and `limit`. Page 2 with 5 per page = skip 5, show next 5.
- **Status codes used**: 200 OK, 201 Created, 400 Bad request, 401 Not logged in, 403 Not allowed, 404 Not found, 409 Already exists, 422 Invalid data.

## 8. Common problems
- `MongoDB: OFF` badge -> MongoDB service is not running. Start it (Windows: Services -> MongoDB Server -> Start).
- `Redis: OFF` badge -> normal if Redis is not installed. The app still works.
- `No module named app` -> run the uvicorn command from the project folder (the one containing the `app` folder).

## 9. Note for real projects
Passwords here use sha256 and the token is a random string, to keep code easy. Real apps use bcrypt and JWT.
