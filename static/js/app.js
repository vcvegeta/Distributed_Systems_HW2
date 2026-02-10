// ============================================================
// Part 2 – JavaScript (Frontend Logic)
// Handles all CRUD operations and search via the FastAPI
// REST endpoints.  Each function corresponds to a Part 2
// question (Q1 – Q4).
// ============================================================

// Base URL for the books API
const API_URL = '/api/books';

// Load the book list as soon as the page is ready
document.addEventListener('DOMContentLoaded', () => {
    loadBooks();
});


// ---- Fetch and display all books ----

async function loadBooks() {
    // Fetches the full list of books from the server and
    // populates the HTML table.
    try {
        const response = await fetch(API_URL);
        if (!response.ok) throw new Error('Failed to fetch books');

        const books = await response.json();
        displayBooks(books);
    } catch (error) {
        console.error('Error loading books:', error);
        alert('Failed to load books');
    }
}


// Render the array of book objects into the table body
function displayBooks(books) {
    const tbody = document.getElementById('bookTableBody');
    tbody.innerHTML = '';

    books.forEach(book => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${book.id}</td>
            <td>${book.title}</td>
            <td>${book.author}</td>
        `;
        tbody.appendChild(row);
    });
}


// ============================================================
// Part 2 – Q1: Add a new book
// Reads the Title and Author inputs, sends a POST request,
// then refreshes the table to show the newly added book.
// ============================================================

async function createBook() {
    const titleInput  = document.getElementById('createTitle');
    const authorInput = document.getElementById('createAuthor');
    const title  = titleInput.value.trim();
    const author = authorInput.value.trim();

    // Basic client-side validation
    if (!title || !author) {
        alert('Please enter both a book title and an author name');
        return;
    }

    try {
        const response = await fetch(API_URL, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ title: title, author: author })
        });

        if (!response.ok) {
            const err = await response.json();
            throw new Error(err.detail || 'Failed to create book');
        }

        const newBook = await response.json();
        console.log('Created book:', newBook);

        // Clear the input fields and reload the list
        titleInput.value  = '';
        authorInput.value = '';
        await loadBooks();
        alert(`Book "${newBook.title}" by ${newBook.author} added!`);
    } catch (error) {
        console.error('Error creating book:', error);
        alert('Failed to create book: ' + error.message);
    }
}


// ============================================================
// Part 2 – Q2: Update a book by its ID
// Example usage: update ID 1 → title "Harry Potter",
// author "J.K. Rowling".  After the PUT request the table
// is refreshed with updated data.
// ============================================================

async function updateBook() {
    const idInput     = document.getElementById('updateId');
    const titleInput  = document.getElementById('updateTitle');
    const authorInput = document.getElementById('updateAuthor');
    const id     = parseInt(idInput.value);
    const title  = titleInput.value.trim();
    const author = authorInput.value.trim();

    if (!id || !title || !author) {
        alert('Please enter the Book ID, new title, and new author');
        return;
    }

    try {
        const response = await fetch(`${API_URL}/${id}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ title: title, author: author })
        });

        if (!response.ok) {
            const err = await response.json();
            throw new Error(err.detail || 'Failed to update book');
        }

        const updated = await response.json();
        console.log('Updated book:', updated);

        // Clear inputs and reload
        idInput.value     = '';
        titleInput.value  = '';
        authorInput.value = '';
        await loadBooks();
        alert(`Book ID ${id} updated to "${updated.title}" by ${updated.author}`);
    } catch (error) {
        console.error('Error updating book:', error);
        alert('Failed to update book: ' + error.message);
    }
}


// ============================================================
// Part 2 – Q3: Delete the book with the highest ID
// Sends a DELETE request to a dedicated endpoint that
// automatically finds and removes the highest-ID book.
// ============================================================

async function deleteHighestBook() {
    if (!confirm('Are you sure you want to delete the book with the highest ID?')) {
        return;
    }

    try {
        const response = await fetch(`${API_URL}/highest`, {
            method: 'DELETE'
        });

        if (!response.ok) {
            const err = await response.json();
            throw new Error(err.detail || 'Failed to delete book');
        }

        console.log('Deleted book with highest ID');
        await loadBooks();
        alert('Book with the highest ID has been deleted!');
    } catch (error) {
        console.error('Error deleting book:', error);
        alert('Failed to delete book: ' + error.message);
    }
}


// ============================================================
// Part 2 – Q4: Search for books by title
// Sends the search term as a query parameter.  The API
// returns only books whose title contains the search string
// (case-insensitive).
// ============================================================

async function searchBooks() {
    const searchInput = document.getElementById('searchInput');
    const query = searchInput.value.trim();

    if (!query) {
        alert('Please enter a search term');
        return;
    }

    try {
        // The backend accepts an optional ?search= query param
        const response = await fetch(`${API_URL}?search=${encodeURIComponent(query)}`);
        if (!response.ok) throw new Error('Search failed');

        const results = await response.json();
        displayBooks(results);
    } catch (error) {
        console.error('Error searching books:', error);
        alert('Search failed: ' + error.message);
    }
}


// Clear the search input and reload the full book list
async function clearSearch() {
    document.getElementById('searchInput').value = '';
    await loadBooks();
}
