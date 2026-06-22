import csv
import json

with open("users.json", "r", encoding="utf-8") as f:
    raw_users = json.load(f)

users = []
for user in raw_users:
    users.append({
        "name": user.get("name"),
        "gender": user.get("gender"),
        "address": user.get("address"),
        "age": user.get("age"),
        "books": []  # Список книг
    })

books = []
with open("books.csv", "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        books.append({
            "title": row.get("Title"),
            "author": row.get("Author"),
            "pages": int(row.get("Pages")) if row.get("Pages") else 0,
            "genre": row.get("Genre")
        })

for i, book in enumerate(books):
    user_index = i % len(users)
    users[user_index]["books"].append(book)

with open("result.json", "w", encoding="utf-8") as f:
    json.dump(users, f, ensure_ascii=False, indent=4)

print("Файл result.json успешно создан!")
