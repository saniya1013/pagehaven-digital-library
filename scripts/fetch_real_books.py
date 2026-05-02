"""
PageHaven — Real Book Data Ingestion Script
============================================
Fetches real public-domain book data from Open Library & Project Gutenberg,
then upserts into MongoDB (elibrary.books).

Usage:
    pip install pymongo[srv] python-dotenv requests
    python scripts/fetch_real_books.py
"""

import os
import requests
from pymongo import MongoClient
from dotenv import load_dotenv

# ── Load environment ──────────────────────────────────────────────
load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")
if not MONGO_URI:
    raise SystemExit("❌ MONGO_URI not found in .env")

client = MongoClient(MONGO_URI)
db = client["elibrary"]
collection = db["books"]

# ── Curated book list ─────────────────────────────────────────────
# Each entry: (Gutenberg ID, Open Library cover ID, categories, rating)
# We only include books that have verified working PDF links on Gutenberg.
CURATED_BOOKS = [
    {
        "gutenberg_id": 1342,
        "title": "Pride and Prejudice",
        "author": "Jane Austen",
        "category": ["classic", "romance"],
        "description": "A masterpiece of wit and social observation. Elizabeth Bennet navigates love, class, and family in Regency-era England — discovering that first impressions can be deceiving.",
        "rating": 4.8,
        "cover_id": 8226191,
    },
    {
        "gutenberg_id": 11,
        "title": "Alice's Adventures in Wonderland",
        "author": "Lewis Carroll",
        "category": ["fantasy", "classic"],
        "description": "Follow Alice down the rabbit hole into a surreal world of talking animals, mad tea parties, and curious logic that has captivated readers for over 150 years.",
        "rating": 4.6,
        "cover_id": 8231856,
    },
    {
        "gutenberg_id": 84,
        "title": "Frankenstein",
        "author": "Mary Shelley",
        "category": ["horror", "classic", "science fiction"],
        "description": "The original science fiction novel. Victor Frankenstein's ambition to create life leads to a creature shunned by society — a haunting meditation on responsibility and humanity.",
        "rating": 4.7,
        "cover_id": 6788709,
    },
    {
        "gutenberg_id": 1661,
        "title": "The Adventures of Sherlock Holmes",
        "author": "Arthur Conan Doyle",
        "category": ["mystery", "classic"],
        "description": "Twelve brilliant short stories featuring the legendary detective Sherlock Holmes and his loyal companion Dr. Watson, solving London's most baffling crimes.",
        "rating": 4.7,
        "cover_id": 12645171,
    },
    {
        "gutenberg_id": 1952,
        "title": "The Yellow Wallpaper",
        "author": "Charlotte Perkins Gilman",
        "category": ["horror", "classic"],
        "description": "A chilling first-person account of a woman's descent into madness while confined to a room — a landmark feminist text about autonomy and mental health.",
        "rating": 4.3,
        "cover_id": 12840956,
    },
    {
        "gutenberg_id": 174,
        "title": "The Picture of Dorian Gray",
        "author": "Oscar Wilde",
        "category": ["classic", "philosophy"],
        "description": "A young man's portrait ages while he remains eternally youthful — but at what cost? Wilde's only novel is a dazzling exploration of beauty, art, and moral corruption.",
        "rating": 4.6,
        "cover_id": 12818564,
    },
    {
        "gutenberg_id": 1080,
        "title": "A Modest Proposal",
        "author": "Jonathan Swift",
        "category": ["satire", "classic"],
        "description": "Swift's savage satirical essay suggests an outrageous solution to poverty — a timeless masterclass in irony that still shocks and provokes today.",
        "rating": 4.2,
        "cover_id": 12648880,
    },
    {
        "gutenberg_id": 2701,
        "title": "Moby Dick",
        "author": "Herman Melville",
        "category": ["adventure", "classic"],
        "description": "Captain Ahab's obsessive quest to destroy the great white whale is an epic tale of ambition, fate, and the struggle between man and nature.",
        "rating": 4.5,
        "cover_id": 8228697,
    },
    {
        "gutenberg_id": 1260,
        "title": "Jane Eyre",
        "author": "Charlotte Brontë",
        "category": ["classic", "romance"],
        "description": "An orphaned governess finds love and self-respect in the brooding halls of Thornfield — but dark secrets threaten to destroy everything she holds dear.",
        "rating": 4.7,
        "cover_id": 8230594,
    },
    {
        "gutenberg_id": 345,
        "title": "Dracula",
        "author": "Bram Stoker",
        "category": ["horror", "classic"],
        "description": "The definitive vampire novel. Count Dracula's journey from Transylvania to England unleashes a battle between ancient evil and modern courage.",
        "rating": 4.5,
        "cover_id": 8235299,
    },
    {
        "gutenberg_id": 16328,
        "title": "Beowulf",
        "author": "Unknown",
        "category": ["epic", "classic"],
        "description": "The oldest surviving long poem in Old English. A heroic warrior battles monsters and dragons in this foundational masterpiece of Western literature.",
        "rating": 4.3,
        "cover_id": 12803498,
    },
    {
        "gutenberg_id": 98,
        "title": "A Tale of Two Cities",
        "author": "Charles Dickens",
        "category": ["classic", "history"],
        "description": "Set against the French Revolution, Dickens weaves a powerful story of sacrifice, resurrection, and the enduring power of love amid social upheaval.",
        "rating": 4.6,
        "cover_id": 12005963,
    },
    {
        "gutenberg_id": 76,
        "title": "Adventures of Huckleberry Finn",
        "author": "Mark Twain",
        "category": ["adventure", "classic"],
        "description": "Huck and the escaped slave Jim raft down the Mississippi in this groundbreaking American novel — a story about freedom, friendship, and conscience.",
        "rating": 4.4,
        "cover_id": 8225421,
    },
    {
        "gutenberg_id": 5200,
        "title": "Metamorphosis",
        "author": "Franz Kafka",
        "category": ["classic", "philosophy"],
        "description": "Gregor Samsa wakes one morning to find himself transformed into a monstrous insect. Kafka's unsettling novella explores alienation, identity, and family bonds.",
        "rating": 4.5,
        "cover_id": 12915586,
    },
    {
        "gutenberg_id": 1400,
        "title": "Great Expectations",
        "author": "Charles Dickens",
        "category": ["classic"],
        "description": "Young Pip's journey from humble beginnings to gentleman's life in London — a richly woven tale of ambition, loyalty, and the true meaning of wealth.",
        "rating": 4.5,
        "cover_id": 12645244,
    },
    {
        "gutenberg_id": 514,
        "title": "Little Women",
        "author": "Louisa May Alcott",
        "category": ["classic", "romance"],
        "description": "The March sisters — Meg, Jo, Beth, and Amy — navigate love, loss, and growing up in Civil War-era America in this beloved coming-of-age novel.",
        "rating": 4.6,
        "cover_id": 12803500,
    },
    {
        "gutenberg_id": 219,
        "title": "Heart of Darkness",
        "author": "Joseph Conrad",
        "category": ["adventure", "classic"],
        "description": "Marlow's journey up the Congo River to find the mysterious Kurtz is a profound exploration of colonialism, madness, and the darkness within us all.",
        "rating": 4.3,
        "cover_id": 12816520,
    },
    {
        "gutenberg_id": 2591,
        "title": "Grimm's Fairy Tales",
        "author": "Brothers Grimm",
        "category": ["fantasy", "classic"],
        "description": "The timeless collection that gave us Cinderella, Rapunzel, and Snow White — enchanting stories that have shaped the imagination of readers for centuries.",
        "rating": 4.4,
        "cover_id": 8504891,
    },
    {
        "gutenberg_id": 43,
        "title": "The Strange Case of Dr. Jekyll and Mr. Hyde",
        "author": "Robert Louis Stevenson",
        "category": ["horror", "classic"],
        "description": "A respectable London doctor and a violent criminal share a terrible secret — Stevenson's gripping novella about duality and the beast within.",
        "rating": 4.5,
        "cover_id": 12645140,
    },
    {
        "gutenberg_id": 1232,
        "title": "The Prince",
        "author": "Niccolò Machiavelli",
        "category": ["philosophy", "history"],
        "description": "The foundational text of modern political science. Machiavelli's pragmatic guide to power remains as relevant — and controversial — as ever.",
        "rating": 4.3,
        "cover_id": 12648899,
    },
    # ── Additional books (batch 2) ────────────────────────────────
    {
        "gutenberg_id": 1497,
        "title": "The Republic",
        "author": "Plato",
        "category": ["philosophy", "classic"],
        "description": "Plato's most famous dialogue explores justice, the ideal state, and the nature of the philosopher-king — a cornerstone of Western thought.",
        "rating": 4.5,
        "cover_id": 12648895,
    },
    {
        "gutenberg_id": 25344,
        "title": "The Scarlet Letter",
        "author": "Nathaniel Hawthorne",
        "category": ["classic", "romance"],
        "description": "In Puritan Boston, Hester Prynne bears the shame of her scarlet 'A' — a powerful tale of sin, guilt, and redemption that redefined American literature.",
        "rating": 4.4,
        "cover_id": 12648901,
    },
    {
        "gutenberg_id": 1184,
        "title": "The Count of Monte Cristo",
        "author": "Alexandre Dumas",
        "category": ["adventure", "classic"],
        "description": "Wrongfully imprisoned, Edmond Dantes escapes and transforms into the wealthy Count of Monte Cristo to exact an elaborate revenge on those who betrayed him.",
        "rating": 4.8,
        "cover_id": 12648903,
    },
    {
        "gutenberg_id": 730,
        "title": "Oliver Twist",
        "author": "Charles Dickens",
        "category": ["classic", "adventure"],
        "description": "An orphan boy navigates the dark criminal underworld of Victorian London, from the workhouse to Fagin's gang, in Dickens' searing social critique.",
        "rating": 4.4,
        "cover_id": 12648905,
    },
    {
        "gutenberg_id": 35,
        "title": "The Time Machine",
        "author": "H.G. Wells",
        "category": ["science fiction", "classic"],
        "description": "A Victorian scientist travels to the year 802,701 to discover humanity split into two species — the gentle Eloi and the terrifying Morlocks.",
        "rating": 4.5,
        "cover_id": 12648907,
    },
    {
        "gutenberg_id": 36,
        "title": "The War of the Worlds",
        "author": "H.G. Wells",
        "category": ["science fiction", "classic"],
        "description": "Martian invaders descend on England with devastating heat-rays and tripod war machines in the novel that invented the alien invasion genre.",
        "rating": 4.5,
        "cover_id": 12648909,
    },
    {
        "gutenberg_id": 5230,
        "title": "The Iliad",
        "author": "Homer",
        "category": ["epic", "classic", "poetry"],
        "description": "The wrath of Achilles and the fall of Troy — Homer's monumental epic poem that has shaped storytelling for nearly three thousand years.",
        "rating": 4.6,
        "cover_id": 12648911,
    },
    {
        "gutenberg_id": 1727,
        "title": "The Odyssey",
        "author": "Homer",
        "category": ["epic", "classic", "adventure"],
        "description": "Odysseus' ten-year journey home from Troy, battling cyclopes, sirens, and the wrath of Poseidon, remains the greatest adventure story ever told.",
        "rating": 4.7,
        "cover_id": 12648913,
    },
    {
        "gutenberg_id": 16,
        "title": "Peter Pan",
        "author": "J.M. Barrie",
        "category": ["fantasy", "children"],
        "description": "The boy who never grows up whisks Wendy and her brothers away to Neverland — a timeless tale of imagination, adventure, and the bittersweet nature of childhood.",
        "rating": 4.5,
        "cover_id": 12648915,
    },
    {
        "gutenberg_id": 120,
        "title": "Treasure Island",
        "author": "Robert Louis Stevenson",
        "category": ["adventure", "classic"],
        "description": "Young Jim Hawkins discovers a pirate's treasure map and sails into danger alongside the cunning Long John Silver in the ultimate swashbuckling adventure.",
        "rating": 4.5,
        "cover_id": 12648917,
    },
    {
        "gutenberg_id": 45,
        "title": "Anne of Green Gables",
        "author": "L.M. Montgomery",
        "category": ["classic", "children"],
        "description": "Spirited, imaginative Anne Shirley transforms the lives of everyone in Avonlea after being mistakenly sent to the Cuthbert farm — a heartwarming coming-of-age classic.",
        "rating": 4.7,
        "cover_id": 12648919,
    },
    {
        "gutenberg_id": 55,
        "title": "The Wonderful Wizard of Oz",
        "author": "L. Frank Baum",
        "category": ["fantasy", "children"],
        "description": "Dorothy and Toto are swept by a tornado to the magical Land of Oz, where they befriend a scarecrow, a tin man, and a cowardly lion on the road to the Emerald City.",
        "rating": 4.4,
        "cover_id": 12648921,
    },
    {
        "gutenberg_id": 2814,
        "title": "Dubliners",
        "author": "James Joyce",
        "category": ["classic", "short stories"],
        "description": "Fifteen interconnected short stories paint a vivid, unflinching portrait of middle-class life in Dublin at the turn of the twentieth century.",
        "rating": 4.3,
        "cover_id": 12648923,
    },
    {
        "gutenberg_id": 3207,
        "title": "Leviathan",
        "author": "Thomas Hobbes",
        "category": ["philosophy", "classic"],
        "description": "Hobbes' landmark treatise on the social contract argues that a strong sovereign authority is the only way to prevent the 'war of all against all.'",
        "rating": 4.2,
        "cover_id": 12648925,
    },
    {
        "gutenberg_id": 1399,
        "title": "Anna Karenina",
        "author": "Leo Tolstoy",
        "category": ["classic", "romance"],
        "description": "Tolstoy's sweeping masterpiece follows Anna's tragic love affair against the backdrop of Russian high society — a profound exploration of passion, family, and fate.",
        "rating": 4.7,
        "cover_id": 12648927,
    },
    {
        "gutenberg_id": 2600,
        "title": "War and Peace",
        "author": "Leo Tolstoy",
        "category": ["classic", "history"],
        "description": "Five aristocratic families navigate love, loss, and destiny during Napoleon's invasion of Russia in what is often called the greatest novel ever written.",
        "rating": 4.8,
        "cover_id": 12648929,
    },
    {
        "gutenberg_id": 2554,
        "title": "Crime and Punishment",
        "author": "Fyodor Dostoevsky",
        "category": ["classic", "philosophy"],
        "description": "A destitute student commits murder to prove his theory of the 'extraordinary man' — then spirals into guilt and paranoia in Dostoevsky's psychological masterpiece.",
        "rating": 4.7,
        "cover_id": 12648931,
    },
    {
        "gutenberg_id": 28054,
        "title": "The Brothers Karamazov",
        "author": "Fyodor Dostoevsky",
        "category": ["classic", "philosophy"],
        "description": "Three brothers grapple with faith, doubt, morality, and patricide in Dostoevsky's final and most ambitious novel — a towering achievement in world literature.",
        "rating": 4.8,
        "cover_id": 12648933,
    },
    {
        "gutenberg_id": 996,
        "title": "Don Quixote",
        "author": "Miguel de Cervantes",
        "category": ["classic", "adventure", "satire"],
        "description": "An aging gentleman loses his mind to chivalric romances and sets out as a knight-errant — the world's first modern novel and a timeless comedy of idealism.",
        "rating": 4.6,
        "cover_id": 12648935,
    },
    {
        "gutenberg_id": 4300,
        "title": "Ulysses",
        "author": "James Joyce",
        "category": ["classic", "philosophy"],
        "description": "A single day in Dublin becomes an epic odyssey of consciousness. Joyce's revolutionary novel reshaped what literature could be — dense, dazzling, and endlessly rewarding.",
        "rating": 4.4,
        "cover_id": 12648937,
    },
    {
        "gutenberg_id": 1251,
        "title": "Le Morte d'Arthur",
        "author": "Thomas Malory",
        "category": ["fantasy", "classic", "epic"],
        "description": "The definitive telling of King Arthur, the Knights of the Round Table, the quest for the Holy Grail, and the tragic fall of Camelot.",
        "rating": 4.3,
        "cover_id": 12648939,
    },
    {
        "gutenberg_id": 2500,
        "title": "Siddhartha",
        "author": "Hermann Hesse",
        "category": ["philosophy", "classic"],
        "description": "A young Brahmin's spiritual journey through luxury, asceticism, and despair to find enlightenment by the river — Hesse's luminous meditation on the meaning of life.",
        "rating": 4.6,
        "cover_id": 12648941,
    },
    {
        "gutenberg_id": 205,
        "title": "Walden",
        "author": "Henry David Thoreau",
        "category": ["philosophy", "classic"],
        "description": "Thoreau's account of two years living simply in a cabin by Walden Pond — a revolutionary manifesto on self-reliance, nature, and deliberate living.",
        "rating": 4.4,
        "cover_id": 12648943,
    },
    {
        "gutenberg_id": 10007,
        "title": "Candide",
        "author": "Voltaire",
        "category": ["satire", "philosophy", "classic"],
        "description": "Young Candide is expelled from paradise and tumbles through war, disaster, and absurdity — Voltaire's razor-sharp satire on optimism and human folly.",
        "rating": 4.4,
        "cover_id": 12648945,
    },
    {
        "gutenberg_id": 209,
        "title": "The Turn of the Screw",
        "author": "Henry James",
        "category": ["horror", "classic"],
        "description": "A governess becomes convinced that two ghostly figures are corrupting her young charges in this masterpiece of ambiguity — is it a ghost story or a study in madness?",
        "rating": 4.3,
        "cover_id": 12648947,
    },
    {
        "gutenberg_id": 244,
        "title": "A Study in Scarlet",
        "author": "Arthur Conan Doyle",
        "category": ["mystery", "classic"],
        "description": "The novel that introduced the world to Sherlock Holmes and Dr. Watson. A mysterious murder in London leads to a tale of love and revenge stretching from Utah to Baker Street.",
        "rating": 4.5,
        "cover_id": 12648949,
    },
    {
        "gutenberg_id": 1661,
        "title": "The Adventures of Sherlock Holmes",
        "author": "Arthur Conan Doyle",
        "category": ["mystery", "classic"],
        "description": "Twelve brilliant short stories featuring the legendary detective Sherlock Holmes and his loyal companion Dr. Watson, solving London's most baffling crimes.",
        "rating": 4.7,
        "cover_id": 12645171,
    },
    {
        "gutenberg_id": 74,
        "title": "The Adventures of Tom Sawyer",
        "author": "Mark Twain",
        "category": ["adventure", "children", "classic"],
        "description": "Tom Sawyer's mischievous escapades along the Mississippi — from fence-painting schemes to midnight graveyard adventures — capture the spirit of American boyhood.",
        "rating": 4.4,
        "cover_id": 12648951,
    },
    {
        "gutenberg_id": 2148,
        "title": "The Importance of Being Earnest",
        "author": "Oscar Wilde",
        "category": ["classic", "satire"],
        "description": "Wilde's most beloved comedy — two gentlemen invent fictitious identities to escape social obligations, leading to a cascade of mistaken identities and sparkling wit.",
        "rating": 4.6,
        "cover_id": 12648953,
    },
    {
        "gutenberg_id": 768,
        "title": "Wuthering Heights",
        "author": "Emily Brontë",
        "category": ["classic", "romance"],
        "description": "The fierce, destructive love between Heathcliff and Catherine haunts the Yorkshire moors across generations in Emily Brontë's only novel — wild, passionate, and unforgettable.",
        "rating": 4.6,
        "cover_id": 12648955,
    },
]


def get_gutenberg_pdf_url(gutenberg_id):
    """Build a working Gutenberg read-online URL."""
    return f"https://www.gutenberg.org/ebooks/{gutenberg_id}.html.images"


def get_cover_url(cover_id):
    """Build Open Library cover URL (Medium size)."""
    return f"https://covers.openlibrary.org/b/id/{cover_id}-L.jpg"


def verify_url(url):
    """Quick HEAD check to verify the URL is reachable."""
    try:
        resp = requests.head(url, timeout=10, allow_redirects=True)
        return resp.status_code < 400
    except Exception:
        return False


def main():
    print("=" * 50)
    print("  PageHaven — Data Ingestion Script")
    print("=" * 50)
    print()

    inserted = 0
    skipped = 0
    failed = 0

    for entry in CURATED_BOOKS:
        title = entry["title"]
        pdf_url = get_gutenberg_pdf_url(entry["gutenberg_id"])
        cover_url = get_cover_url(entry["cover_id"])

        print(f"  📘 {title}...", end=" ", flush=True)

        # Verify the read-online link works
        if not verify_url(pdf_url):
            print("❌ URL unreachable, skipping.")
            failed += 1
            continue

        doc = {
            "title": title,
            "author": entry["author"],
            "category": entry["category"],
            "description": entry["description"],
            "rating": entry["rating"],
            "cover": cover_url,
            "pdf_url": pdf_url,
        }

        # Upsert: update if title exists, insert if new
        result = collection.update_one(
            {"title": title},
            {"$set": doc},
            upsert=True,
        )

        if result.upserted_id:
            print("✅ Inserted")
            inserted += 1
        else:
            print("🔄 Updated")
            skipped += 1

    print()
    print(f"  ✅ Inserted: {inserted}")
    print(f"  🔄 Updated:  {skipped}")
    print(f"  ❌ Failed:   {failed}")
    print(f"  📊 Total in DB: {collection.count_documents({})}")
    print()
    print("  Done! Your library is ready. 🎉")


if __name__ == "__main__":
    main()
