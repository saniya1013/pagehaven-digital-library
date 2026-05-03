/* =============================================
   PageHaven — Dashboard Script (script.js)
   Handles book fetching, search, and filtering
   ============================================= */

(function () {
  'use strict';

  const container    = document.getElementById('books-container');
  const searchInput  = document.getElementById('search-input');
  const filterChips  = document.getElementById('filter-chips');

  // Guard: only run on dashboard page
  if (!container) return;

  let allBooks = [];
  let activeCategory = 'all';

  // Show loading
  container.innerHTML = `
    <div class="loading-state" style="grid-column: 1 / -1;">
      <div class="spinner"></div>
      <p>Loading your library...</p>
    </div>`;

  // Fetch books from API
  fetch('/books')
    .then(res => res.json())
    .then(data => {
      if (data.error) {
        showEmpty('Something went wrong', data.error);
        return;
      }
      allBooks = Array.isArray(data) ? data : [];
      if (allBooks.length === 0) {
        showEmpty('No books yet', 'Run the data ingestion script to populate the library.');
        return;
      }
      buildCategoryChips();
      renderBooks(allBooks);
    })
    .catch(err => {
      console.error('Fetch error:', err);
      showEmpty('Connection error', 'Could not reach the server. Please try again.');
    });

  // ---- Render Book Cards ----
  function renderBooks(books) {
    container.innerHTML = '';

    if (books.length === 0) {
      showEmpty('No results', 'Try a different search term or category.');
      return;
    }

    books.forEach((book, i) => {
      const card = document.createElement('div');
      card.className = 'book-card';
      card.style.animationDelay = `${i * 0.04}s`;
      card.style.animation = 'fadeUp 0.5s ease-out both';

      const rating = book.rating ? book.rating.toFixed(1) : '—';
      const categories = (book.category || [])
        .map(c => `<span class="category-tag">${capitalize(c)}</span>`)
        .join('');

      card.innerHTML = `
        <div class="cover-wrap">
          <img src="${book.cover || ''}" alt="${escapeHtml(book.title)}" loading="lazy"
               onerror="this.style.display='none'">
          <div class="cover-overlay"></div>
          <div class="card-badge">★ ${rating}</div>
        </div>
        <div class="card-body">
          <h3>${escapeHtml(book.title)}</h3>
          <p class="author">${escapeHtml(book.author || 'Unknown')}</p>
          <div class="category-tags">${categories}</div>
        </div>`;

      card.addEventListener('click', () => {
        window.location.href = `/book?id=${book._id}`;
      });

      container.appendChild(card);
    });
  }

  // ---- Category Chips ----
  function buildCategoryChips() {
    const cats = new Set();
    allBooks.forEach(b => (b.category || []).forEach(c => cats.add(c)));
    [...cats].sort().forEach(cat => {
      const chip = document.createElement('button');
      chip.className = 'chip';
      chip.dataset.category = cat;
      chip.textContent = capitalize(cat);
      filterChips.appendChild(chip);
    });
  }

  // Chip click delegation
  if (filterChips) {
    filterChips.addEventListener('click', e => {
      const chip = e.target.closest('.chip');
      if (!chip) return;
      filterChips.querySelectorAll('.chip').forEach(c => c.classList.remove('active'));
      chip.classList.add('active');
      activeCategory = chip.dataset.category;
      applyFilters();
    });
  }

  // ---- Search ----
  if (searchInput) {
    const suggestionBox = document.getElementById('search-suggestions');

    searchInput.addEventListener('input', debounce(async (e) => {
      const q = e.target.value.trim();
      
      // Handle suggestions
      if (q.length > 1) {
        const res = await fetch(`/books/suggest?q=${encodeURIComponent(q)}`);
        const suggestions = await res.json();
        
        if (suggestions.length > 0 && !suggestions.error) {
          suggestionBox.innerHTML = suggestions.map(s => `
            <div class="suggestion-item" data-id="${s.id}">
              <span>🔍</span> ${s.title}
            </div>
          `).join('');
          suggestionBox.style.display = 'block';
        } else {
          suggestionBox.style.display = 'none';
        }
      } else {
        suggestionBox.style.display = 'none';
      }

      applyFilters();
    }, 250));

    // Handle suggestion click
    suggestionBox.addEventListener('click', (e) => {
      const item = e.target.closest('.suggestion-item');
      if (item) {
        window.location.href = `/book?id=${item.dataset.id}`;
      }
    });

    // Hide suggestions when clicking outside
    document.addEventListener('click', (e) => {
      if (!e.target.closest('.search-bar')) {
        suggestionBox.style.display = 'none';
      }
    });
  }

  function applyFilters() {
    const query = (searchInput ? searchInput.value : '').toLowerCase().trim();
    let filtered = allBooks;

    if (activeCategory !== 'all') {
      filtered = filtered.filter(b =>
        (b.category || []).some(c => c.toLowerCase() === activeCategory.toLowerCase())
      );
    }
    if (query) {
      filtered = filtered.filter(b =>
        (b.title || '').toLowerCase().includes(query) ||
        (b.author || '').toLowerCase().includes(query) ||
        (b.category || []).some(c => c.toLowerCase().includes(query))
      );
    }
    renderBooks(filtered);
  }

  // ---- Helpers ----
  async function apiFetch(url, options = {}) {
    const token = localStorage.getItem('access_token');
    const defaultOptions = {
      headers: {
        'Content-Type': 'application/json',
        ...(token ? { 'Authorization': `Bearer ${token}` } : {})
      }
    };
    
    const res = await fetch(url, { ...defaultOptions, ...options });
    
    if (res.status === 401) {
      localStorage.clear();
      window.location.href = '/auth';
      return null;
    }
    
    return res;
  }

  function showEmpty(title, msg) {
    container.innerHTML = `
      <div class="empty-state" style="grid-column: 1 / -1;">
        <div class="icon">📭</div>
        <h3>${title}</h3>
        <p>${msg}</p>
      </div>`;
  }

  function capitalize(s) {
    return s.charAt(0).toUpperCase() + s.slice(1);
  }

  function escapeHtml(str) {
    const div = document.createElement('div');
    div.textContent = str || '';
    return div.innerHTML;
  }

  function debounce(fn, ms) {
    let timer;
    return function (...args) {
      clearTimeout(timer);
      timer = setTimeout(() => fn.apply(this, args), ms);
    };
  }
})();

/* =============================================
   PageHaven — Visual Enhancements (no logic)
   3D tilt · Scroll reveal · Particles · Navbar
   ============================================= */

// ---- 3D Tilt on Book Cards ----
(function () {
  function initTilt() {
    document.querySelectorAll('.book-card').forEach(card => {
      card.addEventListener('mousemove', (e) => {
        const rect = card.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;
        const centerX = rect.width / 2;
        const centerY = rect.height / 2;
        const rotateX = ((y - centerY) / centerY) * -8;
        const rotateY = ((x - centerX) / centerX) * 8;
        card.style.transform =
          `perspective(800px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) scale(1.03)`;
      });
      card.addEventListener('mouseleave', () => {
        card.style.transform = '';
      });
    });
  }
  // Re-init after books render (MutationObserver)
  const grid = document.getElementById('books-container');
  if (grid) {
    const obs = new MutationObserver(() => initTilt());
    obs.observe(grid, { childList: true });
  }
})();

// ---- 3D Tilt on Detail Cover ----
(function () {
  const cover = document.querySelector('.detail-cover');
  if (!cover) return;
  cover.addEventListener('mousemove', (e) => {
    const rect = cover.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;
    const rotateX = ((y - rect.height / 2) / (rect.height / 2)) * -10;
    const rotateY = ((x - rect.width / 2) / (rect.width / 2)) * 10;
    cover.style.transform =
      `perspective(800px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) scale(1.04)`;
  });
  cover.addEventListener('mouseleave', () => {
    cover.style.transform = '';
  });
})();

// ---- Scroll Reveal ----
(function () {
  document.querySelectorAll('.feature-card, .section-header, .cta-section h2, .cta-section p, .dashboard-header')
    .forEach(el => el.classList.add('reveal'));

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
      }
    });
  }, { threshold: 0.15 });

  document.querySelectorAll('.reveal').forEach(el => observer.observe(el));
})();

// ---- Floating Particles in Hero ----
(function () {
  const hero = document.querySelector('.hero');
  if (!hero) return;
  for (let i = 0; i < 15; i++) {
    const p = document.createElement('div');
    p.className = 'particle';
    const size = Math.random() * 8 + 3;
    p.style.width = size + 'px';
    p.style.height = size + 'px';
    p.style.left = Math.random() * 100 + '%';
    p.style.bottom = '-20px';
    p.style.animationDuration = (Math.random() * 10 + 8) + 's';
    p.style.animationDelay = (Math.random() * 10) + 's';
    hero.appendChild(p);
  }
})();

// ---- Navbar shadow on scroll ----
(function () {
  const nav = document.querySelector('.navbar');
  if (!nav) return;
  window.addEventListener('scroll', () => {
    nav.classList.toggle('scrolled', window.scrollY > 20);
  }, { passive: true });
})();