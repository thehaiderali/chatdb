import sqlite3
import random

# Connect (creates file if not exists)
conn = sqlite3.connect("test.db")
c = conn.cursor()

# --- Schema ---
c.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
)
""")

c.execute("""
CREATE TABLE IF NOT EXISTS posts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
)
""")

c.execute("""
CREATE TABLE IF NOT EXISTS comments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    post_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    content TEXT NOT NULL,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(post_id) REFERENCES posts(id) ON DELETE CASCADE,
    FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
)
""")

conn.commit()

# --- Sample Data Pools ---
sample_names = [
    "Alice Johnson", "Bob Smith", "Charlie Brown", "Diana Prince", "Ethan Hunt",
    "Fiona Gallagher", "George Miller", "Hannah Scott", "Ian McGregor", "Julia Adams",
    "Kevin Parker", "Laura Chen", "Michael Jordan", "Nina Williams", "Oscar Wilde",
    "Paula Simmons", "Quincy Jones", "Rachel Green", "Sam Fisher", "Tina Turner",
    "Uma Thurman", "Victor Stone", "Wendy Harris", "Xander Cage", "Yara Shahidi",
    "Zane Malik"
]

sample_titles = [
    "The Future of AI", "Healthy Living", "Travel Diaries", "Python Tips", "Movie Review",
    "Space Exploration", "Music Trends", "Sports Highlights", "Cooking Hacks", "Tech Startups",
    "Mindfulness Practice", "Climate Change", "History Facts", "Photography Basics",
    "Gaming Culture", "Financial Freedom", "Work-Life Balance", "Book Reviews", "Art Movements",
    "Education in 21st Century"
]

sample_contents = [
    "Artificial Intelligence is rapidly transforming industries worldwide.",
    "Maintaining a balanced diet and regular exercise is key to healthy living.",
    "Exploring Japan was a dream come true, with its culture and food.",
    "List comprehensions are a powerful way to write cleaner code in Python.",
    "The latest blockbuster was thrilling and action-packed, worth watching twice.",
    "SpaceX has revolutionized modern space exploration with reusable rockets.",
    "Streaming platforms have completely changed how we consume music.",
    "The last NBA season had unforgettable moments and legendary plays.",
    "Quick and easy cooking hacks can save you hours in the kitchen.",
    "Tech startups are disrupting industries with new innovations every year.",
    "Mindfulness meditation reduces stress and improves focus significantly.",
    "Global warming continues to pose major challenges to humanity.",
    "Ancient civilizations provide insights into our modern world.",
    "Photography basics like lighting and framing make a huge difference.",
    "Gaming culture is booming with esports and online communities.",
    "Financial independence requires discipline, saving, and investments.",
    "Maintaining work-life balance improves mental and physical health.",
    "Book reviews help readers find the right story at the right time.",
    "Art movements shape the way we perceive creativity and culture.",
    "Education in the 21st century must adapt to digital innovation."
]

sample_comments = [
    "Great post, very informative!",
    "I totally agree with your points.",
    "Thanks for sharing this valuable insight.",
    "Could you expand more on this topic?",
    "I had a different experience, but this is insightful.",
    "Love the way you explained it!",
    "This is exactly what I was looking for.",
    "Interesting perspective, thanks!",
    "I think there are other sides to consider.",
    "Well-written and easy to understand.",
    "This is going to help me in my project.",
    "Do you have references for this?",
    "Super helpful, keep it up!",
    "I learned something new today.",
    "This resonates with my experience.",
    "Looking forward to more posts like this.",
    "Clear and concise explanation.",
    "Brilliantly written!",
    "I respectfully disagree with this point.",
    "Could you provide some examples?"
]

# --- Seeder functions ---
def seed_users(n=50):
    for i in range(n):
        name = random.choice(sample_names)
        email = f"user{i}@example.com"   # unique email
        try:
            c.execute("INSERT INTO users (name, email) VALUES (?, ?)", (name, email))
        except sqlite3.IntegrityError:
            pass
    conn.commit()

def seed_posts(n=50):
    c.execute("SELECT id FROM users")
    user_ids = [row[0] for row in c.fetchall()]
    for i in range(n):
        user_id = random.choice(user_ids)
        title = random.choice(sample_titles)
        content = random.choice(sample_contents)
        c.execute("INSERT INTO posts (user_id, title, content) VALUES (?, ?, ?)",
                  (user_id, title, content))
    conn.commit()

def seed_comments(n=50):
    c.execute("SELECT id FROM users")
    user_ids = [row[0] for row in c.fetchall()]
    c.execute("SELECT id FROM posts")
    post_ids = [row[0] for row in c.fetchall()]
    for i in range(n):
        user_id = random.choice(user_ids)
        post_id = random.choice(post_ids)
        content = random.choice(sample_comments)
        c.execute("INSERT INTO comments (post_id, user_id, content) VALUES (?, ?, ?)",
                  (post_id, user_id, content))
    conn.commit()

def seed_all():
    seed_users(50)
    seed_posts(50)
    seed_comments(50)

# --- Run Seeder ---
seed_all()

# Example query
c.execute("SELECT users.name, posts.title FROM posts JOIN users ON posts.user_id = users.id LIMIT 10")
print(c.fetchall())

conn.close()
