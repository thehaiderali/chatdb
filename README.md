---

# 🗄️ Talk to SQLite Database with LLM + Streamlit

This project demonstrates how to **interact with an SQLite database in plain English** using a **Large Language Model (LLM)**.
It includes:

* A **SQLite database** with `users`, `posts`, and `comments` tables.
* A **Python seeder script** to populate the database with 50 records in each table.
* A **LangChain + Gemini LLM integration** to convert natural language queries into SQL.
* A **Streamlit web app** to run queries and display results interactively.

---

## 📂 Project Structure

```
.
├── seed.py           # Creates schema and seeds 50 records per table
├── app.py            # Streamlit app (natural language to SQL)
├── .env              # Contains API key for Gemini
├── test.db           # SQLite database (auto-created)
└── README.md         # Documentation
```

---

## 🛠️ Requirements

* Python 3.9+
* Install dependencies:

```bash
pip install streamlit sqlite3 pandas python-dotenv langchain langchain-google-genai
```

---

## ⚙️ Environment Setup

1. Get a [Gemini API key](https://aistudio.google.com/app/apikey).
2. Create a `.env` file in the project root:

   ```
   GEMINI_API_KEY=your_api_key_here
   ```

---

## 📊 Database Schema

**users**

* `id` (INTEGER, PK, AUTOINCREMENT)
* `name` (TEXT, NOT NULL)
* `email` (TEXT, UNIQUE, NOT NULL)
* `created_at` (TIMESTAMP, default now)

**posts**

* `id` (INTEGER, PK, AUTOINCREMENT)
* `user_id` (FK → users.id)
* `title` (TEXT, NOT NULL)
* `content` (TEXT, NOT NULL)
* `created_at` (TIMESTAMP, default now)

**comments**

* `id` (INTEGER, PK, AUTOINCREMENT)
* `post_id` (FK → posts.id)
* `user_id` (FK → users.id)
* `content` (TEXT, NOT NULL)
* `created_at` (TIMESTAMP, default now)

---

## 🚀 Usage

### 1. Seed the database

```bash
python seed.py
```

This creates the schema and inserts **50 users, 50 posts, and 50 comments**.

### 2. Run the Streamlit app

```bash
streamlit run app.py
```

### 3. Ask questions in plain English

Examples:

* “Which users have written more than 3 posts?”
* “Show the 10 most recent posts with the author’s name.”
* “Find the post with the highest number of comments.”
* “List users who commented on their own posts.”

---

## ⚠️ Notes

* Some log warnings from `grpc` or `absl` may appear when running Gemini — they can be safely ignored.
* Streamlit deprecated `use_container_width`. Use `width="stretch"` for DataFrames.
* If you want to reset the database before reseeding, delete `test.db` and rerun `seed.py`.

---

## 📌 Roadmap

* [ ] Add **tabbed views** in Streamlit for browsing `users`, `posts`, and `comments`.
* [ ] Extend dataset with richer real-world content.
* [ ] Add visualization dashboards (e.g., top authors, comment trends).

---

## 📜 License

MIT License — free to use, modify, and share.

---
