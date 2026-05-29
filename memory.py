import sqlite3

conn = sqlite3.connect(
"memory.db",
check_same_thread=False
)

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS memory (
id INTEGER PRIMARY KEY AUTOINCREMENT,
user_id TEXT,
role TEXT,
content TEXT
)
""")

conn.commit()

def save_message(user_id, role, content):

```
cursor.execute(
    """
    INSERT INTO memory (
        user_id,
        role,
        content
    )
    VALUES (?, ?, ?)
    """,
    (
        user_id,
        role,
        content
    )
)

conn.commit()
```

def load_memory(user_id):

```
cursor.execute(
    """
    SELECT role, content
    FROM memory
    WHERE user_id=?
    ORDER BY id DESC
    LIMIT 10
    """,
    (user_id,)
)

rows = cursor.fetchall()

rows.reverse()

messages = []

for row in rows:

    messages.append({
        "role": row[0],
        "content": row[1]
    })

return messages
```
