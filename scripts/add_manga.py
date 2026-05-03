import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client["elibrary"]
collection = db["books"]

MANGA_BOOKS = [
    {
        "title": "Old Boy",
        "author": "Garon Tsuchiya",
        "category": ["manga", "thriller", "mystery"],
        "description": "Ten years ago, they took him. He doesn't know who. He doesn't know why. After ten years of solitary confinement, he's suddenly released. Now he has five days to find out why.",
        "rating": 4.8,
        "cover": "https://covers.openlibrary.org/b/id/12648957-L.jpg",
        "pdf_url": "https://openlibrary.org/works/OL15843468W/Old_Boy"
    },
    {
        "title": "Lone Wolf and Cub",
        "author": "Kazuo Koike",
        "category": ["manga", "history", "action"],
        "description": "The epic tale of Ogami Itto, the Shogun's executioner who is framed for treason and forced to walk the path of the demon as an assassin for hire, accompanied by his young son.",
        "rating": 4.9,
        "cover": "https://covers.openlibrary.org/b/id/12648959-L.jpg",
        "pdf_url": "https://openlibrary.org/works/OL2747161W/Lone_Wolf_and_Cub"
    },
    {
        "title": "Death Note",
        "author": "Tsugumi Ohba",
        "category": ["manga", "supernatural", "thriller"],
        "description": "Light Yagami is an ace student with great prospects—and he's bored out of his mind. But all that changes when he finds the Death Note, a notebook dropped by a rogue Shinigami death god.",
        "rating": 4.9,
        "cover": "https://covers.openlibrary.org/b/id/12648961-L.jpg",
        "pdf_url": "https://openlibrary.org/works/OL2937748W/Death_Note"
    },
    {
        "title": "Naruto, Vol. 1",
        "author": "Masashi Kishimoto",
        "category": ["manga", "action", "fantasy"],
        "description": "Twelve years ago the Village Hidden in the Leaves was attacked by a fearsome threat—a nine-tailed fox spirit. Follow Naruto Uzumaki as he seeks to become the greatest ninja in the village.",
        "rating": 4.7,
        "cover": "https://covers.openlibrary.org/b/id/12648963-L.jpg",
        "pdf_url": "https://openlibrary.org/works/OL2947155W/Naruto"
    },
    {
        "title": "One Piece, Vol. 1",
        "author": "Eiichiro Oda",
        "category": ["manga", "adventure", "fantasy"],
        "description": "Join Monkey D. Luffy and his swashbuckling crew in their search for the ultimate treasure, One Piece. An epic pirate adventure filled with humor and action.",
        "rating": 4.9,
        "cover": "https://covers.openlibrary.org/b/id/12648965-L.jpg",
        "pdf_url": "https://openlibrary.org/works/OL15160867W/One_Piece"
    }
]

def add_manga():
    print("Adding Manga books to PageHaven...")
    added = 0
    for manga in MANGA_BOOKS:
        collection.update_one(
            {"title": manga["title"]},
            {"$set": manga},
            upsert=True
        )
        added += 1
        print(f"  - {manga['title']}")
    
    print(f"\nSuccessfully added {added} Manga books!")

if __name__ == "__main__":
    add_manga()
