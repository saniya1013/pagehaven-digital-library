<p align="center">
  <img src="https://img.icons8.com/color/96/book-shelf.png" alt="BookVerse Logo" width="80"/>
</p>

<h1 align="center">📖 BookVerse — Your Personal Digital Library</h1>

<p align="center">
  A modern, full-stack E-Library web application built with <strong>FastAPI</strong>, <strong>MongoDB</strong>, and a stunning <strong>Netflix-inspired</strong> frontend.<br/>
  Browse, discover, and read free public-domain classics — all in one beautiful interface.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python"/>
  <img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI"/>
  <img src="https://img.shields.io/badge/MongoDB-47A248?style=for-the-badge&logo=mongodb&logoColor=white" alt="MongoDB"/>
  <img src="https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white" alt="HTML5"/>
  <img src="https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white" alt="CSS3"/>
  <img src="https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black" alt="JavaScript"/>
</p>

---

## 📋 Table of Contents

- [About the Project](#-about-the-project)
- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Getting Started](#-getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Environment Setup](#environment-setup)
  - [Database Seeding](#database-seeding)
  - [Running the Application](#running-the-application)
- [Pages & UI](#-pages--ui)
- [API Endpoints](#-api-endpoints)
- [Database Schema](#-database-schema)
- [Data Ingestion Script](#-data-ingestion-script)
- [Book Collection](#-book-collection)
- [Design System](#-design-system)
- [Configuration](#-configuration)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)
- [License](#-license)
- [Acknowledgements](#-acknowledgements)

---

## 🔍 About the Project

**BookVerse** is a production-quality E-Library web application that provides a clean, modern interface for browsing and reading free public-domain books. The project features a fully decoupled architecture with a FastAPI backend serving RESTful APIs, MongoDB for data persistence, and a hand-crafted vanilla HTML/CSS/JS frontend inspired by Netflix's grid-based design language.

The library is pre-loaded with **20+ classic titles** sourced from [Project Gutenberg](https://www.gutenberg.org/) and [Open Library](https://openlibrary.org/), with verified working read-online links.

### Why BookVerse?

- 🎨 **Production-Level UI** — Not a classroom demo. Polished, animated, responsive.
- 📚 **Real Books** — Actual public-domain titles with working read-online links.
- ⚡ **Fast & Lightweight** — No heavy frameworks. Vanilla JS, minimal dependencies.
- 🔌 **Fully Decoupled** — Frontend communicates with backend via REST APIs.
- 🧩 **Easy to Extend** — Clean modular architecture; add features without breaking things.

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| **Landing Page** | Beautifully designed hero section with animated gradient blobs, feature cards, and CTA |
| **Book Dashboard** | Netflix-style responsive grid with book covers, ratings, and hover animations |
| **Real-Time Search** | Debounced search across titles, authors, and categories |
| **Category Filtering** | Dynamic filter chips auto-generated from book data |
| **Book Detail View** | Full book info — cover, author, star rating, description, category tags |
| **Read Online** | One-click "Read Book" button opens the book in a new tab via Project Gutenberg |
| **Data Ingestion** | Standalone Python script to fetch and seed real book data into MongoDB |
| **Upsert Logic** | No duplicate books — script can be safely re-run anytime |
| **URL Verification** | Ingestion script validates every book link before inserting |
| **Responsive Design** | Fully responsive from desktop (1280px) to mobile (320px) |
| **Smooth Animations** | Fade-in cards, hover scale effects, gradient transitions |
| **Loading & Error States** | Spinners, empty state messages, and graceful error handling |

---

## 🛠 Tech Stack

### Backend
| Technology | Purpose |
|------------|---------|
| **Python 3.10+** | Core language |
| **FastAPI** | High-performance async web framework |
| **Uvicorn** | ASGI server |
| **PyMongo** | MongoDB driver for Python |
| **Jinja2** | Server-side HTML template rendering |
| **python-dotenv** | Environment variable management |

### Frontend
| Technology | Purpose |
|------------|---------|
| **HTML5** | Semantic page structure |
| **CSS3** | Custom design system with CSS variables, gradients, and animations |
| **Vanilla JavaScript** | DOM manipulation, API fetching, search & filter logic |
| **Google Fonts** | Inter + Playfair Display typography |

### Database
| Technology | Purpose |
|------------|---------|
| **MongoDB Atlas** | Cloud-hosted NoSQL database |
| **Database:** `elibrary` | Main database |
| **Collection:** `books` | Book documents storage |

### Data Sources
| Source | Purpose |
|--------|---------|
| **Project Gutenberg** | Free public-domain book content (read-online links) |
| **Open Library** | Book cover images via Covers API |

---

## 📁 Project Structure

```
BookVerse/
│
├── .env                          # Environment variables (MONGO_URI, DB_NAME)
├── requirements.txt              # Python dependencies
├── README.md                     # This file
├── insert_real_books.py          # Legacy data insertion script
│
├── app/                          # Main application package
│   ├── main.py                   # FastAPI app entry point & route definitions
│   │
│   ├── database/                 # Database layer
│   │   └── db.py                 # MongoDB connection & collection exports
│   │
│   ├── models/                   # Pydantic data models
│   │   └── book.py               # Book schema definition
│   │
│   ├── routes/                   # API route handlers
│   │   └── book_routes.py        # /books and /book/{id} endpoints
│   │
│   ├── services/                 # Business logic layer
│   │   └── recommend.py          # (Future) Book recommendation engine
│   │
│   ├── templates/                # Jinja2 HTML templates
│   │   ├── index.html            # Landing page (served at /)
│   │   ├── home.html             # Book dashboard (served at /home)
│   │   └── book.html             # Book detail page (served at /book)
│   │
│   ├── static/                   # Static frontend assets
│   │   ├── style.css             # Complete design system & component styles
│   │   └── script.js             # Dashboard logic (fetch, search, filter, render)
│   │
│   ├── fetch_books.py            # Legacy fetch script
│   └── clear_db.py               # Utility: delete all books from DB
│
└── scripts/                      # Standalone scripts
    └── fetch_real_books.py       # Data ingestion — seeds MongoDB with 20 real books
```

---

## 🚀 Getting Started

### Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.10 or higher** — [Download Python](https://www.python.org/downloads/)
- **pip** — Comes bundled with Python
- **MongoDB Atlas account** (free tier) — [Create one here](https://www.mongodb.com/cloud/atlas/register)
- **Git** (optional) — For cloning the repository

Verify your Python installation:

```bash
python --version    # Should output Python 3.10+
pip --version       # Should output pip 22+
```

### Installation

1. **Clone the repository** (or download as ZIP):

```bash
git clone https://github.com/your-username/bookverse.git
cd bookverse
```

2. **Create a virtual environment** (recommended):

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

3. **Install dependencies**:

```bash
pip install -r requirements.txt
```

This installs:
| Package | Version | Purpose |
|---------|---------|---------|
| `fastapi` | Latest | Web framework |
| `uvicorn` | Latest | ASGI server |
| `pymongo[srv]` | Latest | MongoDB driver with SRV support |
| `python-dotenv` | Latest | `.env` file loader |
| `requests` | Latest | HTTP client (for data ingestion) |

### Environment Setup

Create a `.env` file in the project root (if it doesn't exist):

```env
MONGO_URI=mongodb+srv://<username>:<password>@<cluster>.mongodb.net/?appName=<appName>
DB_NAME=elibrary
```

> **⚠️ Important:** Replace `<username>`, `<password>`, `<cluster>`, and `<appName>` with your actual MongoDB Atlas credentials. Never commit this file to version control.

### Database Seeding

Populate your MongoDB database with 20 curated public-domain books:

```bash
# Windows (PowerShell)
$env:PYTHONIOENCODING='utf-8'; python scripts/fetch_real_books.py

# macOS / Linux
PYTHONIOENCODING=utf-8 python scripts/fetch_real_books.py
```

Expected output:
```
==================================================
  BookVerse — Data Ingestion Script
==================================================

  📘 Pride and Prejudice... ✅ Inserted
  📘 Alice's Adventures in Wonderland... ✅ Inserted
  📘 Frankenstein... ✅ Inserted
  ...
  📘 The Prince... ✅ Inserted

  ✅ Inserted: 20
  🔄 Updated:  0
  ❌ Failed:   0
  📊 Total in DB: 20

  Done! Your library is ready. 🎉
```

> **Note:** This script uses **upsert logic** — it's safe to run multiple times. Existing books will be updated, not duplicated.

### Running the Application

Start the FastAPI development server:

```bash
uvicorn app.main:app --reload
```

You should see:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Started reloader process
[OK] MongoDB Connected Successfully!
INFO:     Application startup complete.
```

Open your browser and navigate to:

| Page | URL |
|------|-----|
| **Landing Page** | [http://127.0.0.1:8000/](http://127.0.0.1:8000/) |
| **Book Dashboard** | [http://127.0.0.1:8000/home](http://127.0.0.1:8000/home) |
| **Book Detail** | [http://127.0.0.1:8000/book?id=BOOK_ID](http://127.0.0.1:8000/book?id=BOOK_ID) |

---

## 🖥 Pages & UI

### 1. Landing Page (`/`)

The entry point of BookVerse. Features a modern hero section with:

- **Animated gradient background** with floating blobs
- **Brand name** "BookVerse" with gradient typography
- **Tagline**: "Your Personal Digital Library"
- **Feature cards** highlighting key capabilities:
  - 📚 Read Books Online
  - 🌍 Free Public-Domain Books
  - ✨ Clean UI Experience
- **Call-to-action buttons**: "Get Started" → navigates to `/home`

### 2. Book Dashboard (`/home`)

The main library view with a Netflix-inspired layout:

- **Search bar** — Real-time debounced search across titles, authors, and categories
- **Category filter chips** — Dynamically generated from book data (All, Classic, Horror, Fantasy, etc.)
- **Book card grid** — Responsive grid with:
  - Cover image (from Open Library)
  - Star rating badge
  - Title and author
  - Category tags
  - Hover animation (scale + shadow elevation)
- **Click** any card → navigates to the book detail page
- **Loading state** — Spinner animation while fetching
- **Empty state** — Friendly message when no results match

### 3. Book Detail (`/book?id=...`)

A dedicated page for each book featuring:

- **Large cover image** with shadow elevation
- **Category tags** — Color-coded genre badges
- **Title** — Large serif typography (Playfair Display)
- **Author name** with subtle styling
- **Star rating** — Visual stars + numeric score
- **Description** — Rich, readable text block
- **"Read Book" button** — Opens the book on Project Gutenberg in a new tab (`target="_blank"`)
- **Back navigation** — Button + browser history support

---

## 📡 API Endpoints

BookVerse exposes two RESTful API endpoints:

### `GET /books`

Returns all books in the library.

**Request:**
```http
GET http://127.0.0.1:8000/books
```

**Response** `200 OK`:
```json
[
  {
    "_id": "6813c3a1f5e2a1b2c3d4e5f6",
    "title": "Pride and Prejudice",
    "author": "Jane Austen",
    "category": ["classic", "romance"],
    "description": "A masterpiece of wit and social observation...",
    "rating": 4.8,
    "cover": "https://covers.openlibrary.org/b/id/8226191-L.jpg",
    "pdf_url": "https://www.gutenberg.org/ebooks/1342.html.images"
  },
  ...
]
```

**Error Response:**
```json
{ "error": "Connection error message" }
```

---

### `GET /book/{book_id}`

Returns a single book by its MongoDB ObjectId.

**Request:**
```http
GET http://127.0.0.1:8000/book/6813c3a1f5e2a1b2c3d4e5f6
```

**Response** `200 OK`:
```json
{
  "_id": "6813c3a1f5e2a1b2c3d4e5f6",
  "title": "Pride and Prejudice",
  "author": "Jane Austen",
  "category": ["classic", "romance"],
  "description": "A masterpiece of wit and social observation...",
  "rating": 4.8,
  "cover": "https://covers.openlibrary.org/b/id/8226191-L.jpg",
  "pdf_url": "https://www.gutenberg.org/ebooks/1342.html.images"
}
```

**Error Response (book not found):**
```json
{ "error": "Book not found" }
```

**Error Response (invalid ID format):**
```json
{ "error": "'invalid_id' is not a valid ObjectId..." }
```

---

## 🗄 Database Schema

**Database:** `elibrary`  
**Collection:** `books`

Each document in the `books` collection follows this schema:

```json
{
  "_id": "ObjectId (auto-generated by MongoDB)",
  "title": "String — Book title",
  "author": "String — Author name",
  "category": ["Array of Strings — Genre/category tags"],
  "description": "String — Book summary/synopsis",
  "rating": "Float — Rating from 0.0 to 5.0",
  "cover": "String — URL to cover image (Open Library Covers API)",
  "pdf_url": "String — URL to read the book online (Project Gutenberg)"
}
```

### Example Document

```json
{
  "_id": "6813c3a1f5e2a1b2c3d4e5f6",
  "title": "The Adventures of Sherlock Holmes",
  "author": "Arthur Conan Doyle",
  "category": ["mystery", "classic"],
  "description": "Twelve brilliant short stories featuring the legendary detective Sherlock Holmes and his loyal companion Dr. Watson, solving London's most baffling crimes.",
  "rating": 4.7,
  "cover": "https://covers.openlibrary.org/b/id/12645171-L.jpg",
  "pdf_url": "https://www.gutenberg.org/ebooks/1661.html.images"
}
```

### Collections

| Collection | Purpose |
|------------|---------|
| `books` | Stores all book documents |
| `users` | Reserved for future user authentication feature |

---

## 🐍 Data Ingestion Script

**File:** `scripts/fetch_real_books.py`

This standalone Python script populates the MongoDB database with real book data. It runs independently of the FastAPI server.

### How It Works

1. **Loads** the `MONGO_URI` from the `.env` file
2. **Connects** to MongoDB Atlas (`elibrary.books` collection)
3. **Iterates** over 20 curated book entries with:
   - Verified Project Gutenberg read-online links
   - Open Library cover image URLs
   - Rich descriptions, categories, and ratings
4. **Verifies** each book link via an HTTP HEAD request
5. **Upserts** each book (insert if new, update if title already exists)
6. **Reports** final stats (inserted / updated / failed / total)

### Key Features

| Feature | Implementation |
|---------|---------------|
| **No duplicates** | Uses `update_one()` with `upsert=True` keyed on `title` |
| **URL validation** | HEAD request to verify each Gutenberg link is reachable |
| **Error handling** | Skips books with unreachable URLs, continues with the rest |
| **Safe to re-run** | Existing entries are updated, not duplicated |

### Usage

```bash
# Windows (PowerShell)
$env:PYTHONIOENCODING='utf-8'; python scripts/fetch_real_books.py

# macOS / Linux
PYTHONIOENCODING=utf-8 python scripts/fetch_real_books.py
```

> The `PYTHONIOENCODING=utf-8` flag is needed on Windows to handle emoji characters in console output.

---

## 📚 Book Collection

The library comes pre-loaded with **20 curated public-domain classics**:

| # | Title | Author | Categories | Rating |
|---|-------|--------|------------|--------|
| 1 | Pride and Prejudice | Jane Austen | Classic, Romance | ⭐ 4.8 |
| 2 | Alice's Adventures in Wonderland | Lewis Carroll | Fantasy, Classic | ⭐ 4.6 |
| 3 | Frankenstein | Mary Shelley | Horror, Classic, Sci-Fi | ⭐ 4.7 |
| 4 | The Adventures of Sherlock Holmes | Arthur Conan Doyle | Mystery, Classic | ⭐ 4.7 |
| 5 | The Yellow Wallpaper | Charlotte Perkins Gilman | Horror, Classic | ⭐ 4.3 |
| 6 | The Picture of Dorian Gray | Oscar Wilde | Classic, Philosophy | ⭐ 4.6 |
| 7 | A Modest Proposal | Jonathan Swift | Satire, Classic | ⭐ 4.2 |
| 8 | Moby Dick | Herman Melville | Adventure, Classic | ⭐ 4.5 |
| 9 | Jane Eyre | Charlotte Brontë | Classic, Romance | ⭐ 4.7 |
| 10 | Dracula | Bram Stoker | Horror, Classic | ⭐ 4.5 |
| 11 | Beowulf | Unknown | Epic, Classic | ⭐ 4.3 |
| 12 | A Tale of Two Cities | Charles Dickens | Classic, History | ⭐ 4.6 |
| 13 | Adventures of Huckleberry Finn | Mark Twain | Adventure, Classic | ⭐ 4.4 |
| 14 | Metamorphosis | Franz Kafka | Classic, Philosophy | ⭐ 4.5 |
| 15 | Great Expectations | Charles Dickens | Classic | ⭐ 4.5 |
| 16 | Little Women | Louisa May Alcott | Classic, Romance | ⭐ 4.6 |
| 17 | Heart of Darkness | Joseph Conrad | Adventure, Classic | ⭐ 4.3 |
| 18 | Grimm's Fairy Tales | Brothers Grimm | Fantasy, Classic | ⭐ 4.4 |
| 19 | The Strange Case of Dr. Jekyll and Mr. Hyde | Robert Louis Stevenson | Horror, Classic | ⭐ 4.5 |
| 20 | The Prince | Niccolò Machiavelli | Philosophy, History | ⭐ 4.3 |

All books are sourced from **Project Gutenberg** (read-online links) and **Open Library** (cover images).

---

## 🎨 Design System

BookVerse uses a carefully crafted design system implemented entirely in CSS custom properties.

### Color Palette

| Token | Value | Usage |
|-------|-------|-------|
| `--primary` | `#6366f1` (Indigo) | Primary brand color, buttons, links |
| `--primary-dark` | `#4f46e5` | Hover states, emphasis |
| `--primary-light` | `#818cf8` | Borders, subtle accents |
| `--accent` | `#8b5cf6` (Purple) | Gradient endpoints, highlights |
| `--bg` | `#f8f9fc` | Page background (soft white) |
| `--bg-card` | `#ffffff` | Card backgrounds |
| `--text` | `#1e293b` | Primary text color |
| `--text-secondary` | `#64748b` | Secondary text, descriptions |
| `--text-muted` | `#94a3b8` | Muted text, placeholders |

### Typography

| Font | Weight | Usage |
|------|--------|-------|
| **Playfair Display** | 700–900 | Headings, brand name, page titles |
| **Inter** | 300–900 | Body text, UI elements, buttons |

### Spacing & Layout

| Property | Value |
|----------|-------|
| Max content width | `1280px` |
| Card border radius | `16px` |
| Button border radius | `50px` (pill) |
| Grid gap | `28px` |
| Card aspect ratio (cover) | `2:3` |

### Responsive Breakpoints

| Breakpoint | Changes |
|------------|---------|
| `≤ 900px` | Detail page switches to single-column layout |
| `≤ 768px` | Mobile nav, smaller grid, reduced padding |
| `≤ 480px` | Two-column grid, full-width buttons |

### Animations

| Animation | Trigger | Duration |
|-----------|---------|----------|
| `fadeUp` | Page load | `0.5s ease-out` |
| `floatBlob` | Hero background | `8–10s infinite` |
| `spin` | Loading spinner | `0.8s linear infinite` |
| Card hover scale | `:hover` | `0.3s cubic-bezier` |
| Cover image zoom | Card `:hover` | `0.5s ease` |
| Button lift | `:hover` | `0.3s cubic-bezier` |

---

## ⚙ Configuration

### Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `MONGO_URI` | ✅ Yes | MongoDB Atlas connection string |
| `DB_NAME` | Optional | Database name (defaults to `elibrary`) |

### Server Options

```bash
# Default (development with hot-reload)
uvicorn app.main:app --reload

# Custom port
uvicorn app.main:app --reload --port 3000

# Production (without reload)
uvicorn app.main:app --host 0.0.0.0 --port 8000

# With multiple workers (production)
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

---

## ❓ Troubleshooting

### Common Issues

<details>
<summary><strong>🔴 UnicodeEncodeError on Windows</strong></summary>

**Error:**
```
UnicodeEncodeError: 'charmap' codec can't encode character '\u2705'
```

**Solution:** Set the encoding before running:
```bash
# PowerShell
$env:PYTHONIOENCODING='utf-8'; python scripts/fetch_real_books.py

# Or for the server
$env:PYTHONIOENCODING='utf-8'; uvicorn app.main:app --reload
```
</details>

<details>
<summary><strong>🔴 MongoDB Connection Error</strong></summary>

**Error:** `[ERROR] Connection Error: ...`

**Solutions:**
1. Verify your `MONGO_URI` in `.env` is correct
2. Ensure your IP is whitelisted in MongoDB Atlas (Network Access → Add IP → `0.0.0.0/0` for development)
3. Check your internet connection
4. Ensure the MongoDB Atlas cluster is running
</details>

<details>
<summary><strong>🔴 Module Not Found: app.routes.book_routes</strong></summary>

**Solution:** Run from the **project root directory**, not from inside `app/`:
```bash
# Correct (from project root)
cd bookverse
uvicorn app.main:app --reload

# Wrong (from inside app/)
cd bookverse/app
uvicorn main:app --reload    # ❌ This will fail
```
</details>

<details>
<summary><strong>🔴 No books showing on dashboard</strong></summary>

**Solutions:**
1. Run the data ingestion script first:
   ```bash
   python scripts/fetch_real_books.py
   ```
2. Check the browser console (F12 → Console) for API errors
3. Verify the `/books` endpoint returns data: visit `http://127.0.0.1:8000/books`
</details>

<details>
<summary><strong>🔴 Books cards appear but images don't load</strong></summary>

**Reason:** Open Library cover IDs may occasionally serve incorrect or missing images.

**Solution:** This is expected for some titles. The cards will still display correctly with the title, author, and rating badge.
</details>

---

## 🤝 Contributing

Contributions are welcome! Here's how to get started:

1. **Fork** the repository
2. **Create** a feature branch:
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **Commit** your changes:
   ```bash
   git commit -m "Add amazing feature"
   ```
4. **Push** to the branch:
   ```bash
   git push origin feature/amazing-feature
   ```
5. **Open** a Pull Request

### Ideas for Future Features

- [ ] 🔐 User authentication (sign up / login)
- [ ] 🔖 Bookmarking & reading lists
- [ ] ⭐ User ratings & reviews
- [ ] 🔍 Advanced search with filters (rating range, author, year)
- [ ] 📊 Reading progress tracker
- [ ] 🌙 Dark mode toggle
- [ ] 📱 Progressive Web App (PWA) support
- [ ] 🤖 AI-powered book recommendations (via `services/recommend.py`)

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

## 🙏 Acknowledgements

- **[Project Gutenberg](https://www.gutenberg.org/)** — Free public-domain e-books
- **[Open Library](https://openlibrary.org/)** — Book cover images via the Covers API
- **[FastAPI](https://fastapi.tiangolo.com/)** — Modern Python web framework
- **[MongoDB Atlas](https://www.mongodb.com/atlas)** — Cloud database service
- **[Google Fonts](https://fonts.google.com/)** — Inter & Playfair Display typefaces

---

<p align="center">
  Built with ❤️ by <strong>BookVerse Team</strong><br/>
  <sub>If you found this project helpful, please consider giving it a ⭐</sub>
</p>
