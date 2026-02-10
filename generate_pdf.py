#!/usr/bin/env python3
"""
Generate the final submission PDF for DATA-236 HW2.
Uses the fpdf2 library to create a well-formatted document
with all code and placeholder boxes for screenshots.
"""

from fpdf import FPDF
import os

# ── Paths to all source files ──────────────────────────────
BASE = os.path.dirname(os.path.abspath(__file__))

FILES = {
    "index.html":    os.path.join(BASE, "static", "index.html"),
    "styles.css":    os.path.join(BASE, "static", "css", "styles.css"),
    "app.js":        os.path.join(BASE, "static", "js", "app.js"),
    "main.py":       os.path.join(BASE, "main.py"),
    "state.py":      os.path.join(BASE, "realtygraph", "state.py"),
    "nodes.py":      os.path.join(BASE, "realtygraph", "nodes.py"),
    "router.py":     os.path.join(BASE, "realtygraph", "router.py"),
    "workflow.py":   os.path.join(BASE, "realtygraph", "workflow.py"),
    "run_graph.py":  os.path.join(BASE, "run_graph.py"),
}


def read(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def sanitize(text: str) -> str:
    """Replace unicode characters that latin-1 can't encode."""
    replacements = {
        "\u2014": "--",   # em-dash
        "\u2013": "-",    # en-dash
        "\u2018": "'",    # left single quote
        "\u2019": "'",    # right single quote
        "\u201c": '"',    # left double quote
        "\u201d": '"',    # right double quote
        "\u2026": "...",  # ellipsis
        "\u2192": "->",   # right arrow
        "\u2190": "<-",   # left arrow
        "\u2194": "<->",  # bidirectional arrow
        "\u2022": "*",    # bullet
        "\u00e9": "e",    # e-acute (just in case)
        "\u2500": "-",    # box drawing
        "\u2550": "=",    # double box drawing
    }
    for uc, repl in replacements.items():
        text = text.replace(uc, repl)
    # Final fallback: encode to latin-1, replacing anything left
    text = text.encode("latin-1", "replace").decode("latin-1")
    return text


class HW2PDF(FPDF):
    """Custom FPDF subclass with helpers for our homework layout."""

    # ── Header / Footer ────────────────────────────────────
    def header(self):
        if self.page_no() > 1:
            self.set_font("Helvetica", "I", 8)
            self.set_text_color(120, 120, 120)
            self.cell(0, 5, "DATA-236 Homework 2", align="L")
            self.ln(8)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(120, 120, 120)
        self.cell(0, 10, f"Page {self.page_no()}/{{nb}}", align="C")

    # ── Helpers ─────────────────────────────────────────────
    def section_title(self, title: str):
        """Big bold section title with a blue underline."""
        self.set_font("Helvetica", "B", 16)
        self.set_text_color(21, 101, 192)          # #1565c0
        self.cell(0, 10, sanitize(title), new_x="LMARGIN", new_y="NEXT")
        # blue line
        y = self.get_y()
        self.set_draw_color(21, 101, 192)
        self.set_line_width(0.6)
        self.line(self.l_margin, y, self.w - self.r_margin, y)
        self.ln(4)

    def sub_title(self, title: str):
        """Smaller bold heading."""
        self.set_font("Helvetica", "B", 12)
        self.set_text_color(40, 40, 40)
        self.cell(0, 8, sanitize(title), new_x="LMARGIN", new_y="NEXT")
        self.ln(2)

    def body_text(self, text: str):
        """Normal body paragraph."""
        self.set_font("Helvetica", "", 10)
        self.set_text_color(50, 50, 50)
        self.multi_cell(0, 5, sanitize(text))
        self.ln(2)

    def code_block(self, code: str, filename: str = ""):
        """Render code inside a light-grey box with monospace font."""
        if filename:
            self.set_font("Helvetica", "BI", 9)
            self.set_text_color(80, 80, 80)
            self.cell(0, 6, sanitize(f"File: {filename}"), new_x="LMARGIN", new_y="NEXT")
            self.ln(1)

        self.set_fill_color(245, 245, 245)
        self.set_draw_color(200, 200, 200)
        self.set_text_color(30, 30, 30)
        self.set_font("Courier", "", 7.5)

        # Clean the code text for fpdf (replace special chars)
        safe = sanitize(code.replace("\t", "    "))

        lines = safe.split("\n")
        line_h = 3.6
        box_x = self.l_margin
        box_w = self.w - self.l_margin - self.r_margin

        for line in lines:
            # Page break check
            if self.get_y() + line_h > self.h - self.b_margin - 10:
                self.add_page()
            self.set_fill_color(245, 245, 245)
            self.cell(box_w, line_h, sanitize(" " + line), fill=True,
                      new_x="LMARGIN", new_y="NEXT")

        self.ln(4)

    def screenshot_placeholder(self, label: str, height: int = 90):
        """Draw a dashed rectangle as a placeholder for a screenshot."""
        # Page break if not enough room
        if self.get_y() + height + 15 > self.h - self.b_margin:
            self.add_page()

        self.set_font("Helvetica", "I", 10)
        self.set_text_color(100, 100, 100)
        self.cell(0, 7, sanitize(f"[Screenshot: {label}]"), new_x="LMARGIN", new_y="NEXT")
        self.ln(1)

        x = self.l_margin
        y = self.get_y()
        w = self.w - self.l_margin - self.r_margin
        h = height

        # Dashed border
        self.set_draw_color(160, 160, 160)
        self.set_line_width(0.3)
        self.dashed_line(x, y, x + w, y, 3, 2)
        self.dashed_line(x + w, y, x + w, y + h, 3, 2)
        self.dashed_line(x + w, y + h, x, y + h, 3, 2)
        self.dashed_line(x, y + h, x, y, 3, 2)

        # Center text
        self.set_y(y + h / 2 - 5)
        self.set_font("Helvetica", "I", 11)
        self.set_text_color(170, 170, 170)
        self.cell(0, 10, "< Paste your screenshot here >", align="C")

        self.set_y(y + h + 5)
        self.ln(3)


def build_pdf(output_name: str = "Chaudhary_HW2.pdf"):
    pdf = HW2PDF(orientation="P", unit="mm", format="A4")
    pdf.alias_nb_pages()
    pdf.set_auto_page_break(auto=True, margin=20)
    pdf.set_left_margin(15)
    pdf.set_right_margin(15)

    # ════════════════════════════════════════════════════════
    # COVER PAGE
    # ════════════════════════════════════════════════════════
    pdf.add_page()
    pdf.ln(50)
    pdf.set_font("Helvetica", "B", 28)
    pdf.set_text_color(21, 101, 192)
    pdf.cell(0, 15, "DATA-236 Homework 2", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(5)
    pdf.set_font("Helvetica", "", 14)
    pdf.set_text_color(80, 80, 80)
    pdf.cell(0, 10, "HTML/CSS, FastAPI & LangGraph Agent", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(15)
    pdf.set_font("Helvetica", "", 12)
    pdf.set_text_color(60, 60, 60)
    pdf.cell(0, 8, "Viraat Chaudhary", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 8, "Section 21 & 71", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(10)
    pdf.set_font("Helvetica", "I", 10)
    pdf.set_text_color(130, 130, 130)
    pdf.cell(0, 8, "February 2026", align="C", new_x="LMARGIN", new_y="NEXT")

    # ════════════════════════════════════════════════════════
    # PART 1 – HTML & CSS
    # ════════════════════════════════════════════════════════
    pdf.add_page()
    pdf.section_title("Part 1: HTML & CSS (4 points) - Artist Liberty")

    pdf.body_text(
        "The frontend is a single-page Book Management application built with "
        "semantic HTML5 and custom CSS. It features a blue-accent colour palette, "
        "card-based layout for action sections, and a responsive data table."
    )

    pdf.sub_title("index.html")
    pdf.code_block(read(FILES["index.html"]), "static/index.html")

    pdf.sub_title("styles.css")
    pdf.code_block(read(FILES["styles.css"]), "static/css/styles.css")

    pdf.sub_title("Output — Landing Page")
    pdf.screenshot_placeholder("Part 1 — Landing page showing the Book Management UI with 3 initial books", 100)

    # ════════════════════════════════════════════════════════
    # PART 2 – FastAPI
    # ════════════════════════════════════════════════════════
    pdf.add_page()
    pdf.section_title("Part 2: FastAPI (8 points)")

    pdf.body_text(
        "The backend is a FastAPI REST API that provides CRUD operations on an "
        "in-memory list of books. The frontend JavaScript calls these endpoints "
        "and refreshes the table after each operation."
    )

    # ── main.py (full code) ────────────────────────────────
    pdf.sub_title("Server Code — main.py")
    pdf.code_block(read(FILES["main.py"]), "main.py")

    # ── app.js (full code) ─────────────────────────────────
    pdf.sub_title("Frontend Logic — app.js")
    pdf.code_block(read(FILES["app.js"]), "static/js/app.js")

    # ── Q1 ─────────────────────────────────────────────────
    pdf.add_page()
    pdf.sub_title("Question 1 — Add a New Book (2 pts)")
    pdf.body_text(
        "The user enters a Book Title and Author Name. On submission the book "
        "is added via POST /api/books and the home view refreshes to show the "
        "updated list of books."
    )
    pdf.body_text(
        "Relevant code: POST /api/books endpoint in main.py (create_book function) "
        "and createBook() in app.js."
    )
    pdf.screenshot_placeholder("Q1 — Adding a new book and seeing it in the list", 100)

    # ── Q2 ─────────────────────────────────────────────────
    pdf.sub_title('Question 2 — Update Book ID 1 (2 pts)')
    pdf.body_text(
        'Update the book with ID 1 to title "Harry Potter", Author "J.K. Rowling". '
        "After submitting, the home view shows the updated data in the list."
    )
    pdf.body_text(
        "Relevant code: PUT /api/books/{book_id} endpoint in main.py (update_book "
        "function) and updateBook() in app.js."
    )
    pdf.screenshot_placeholder('Q2 — Book ID 1 updated to "Harry Potter" by "J.K. Rowling"', 100)

    # ── Q3 ─────────────────────────────────────────────────
    pdf.sub_title("Question 3 — Delete the Highest-ID Book (2 pts)")
    pdf.body_text(
        "Clicking the delete button removes the book with the highest ID. "
        "The endpoint DELETE /api/books/highest identifies and removes it, "
        "then the home view refreshes."
    )
    pdf.body_text(
        "Relevant code: DELETE /api/books/highest endpoint in main.py "
        "(delete_highest_book function) and deleteHighestBook() in app.js."
    )
    pdf.screenshot_placeholder("Q3 — After deleting the highest-ID book", 100)

    # ── Q4 ─────────────────────────────────────────────────
    pdf.sub_title("Question 4 — Search by Title (2 pts)")
    pdf.body_text(
        "The user types a search term and the list updates to show only books "
        "whose title contains the query (case-insensitive). The endpoint "
        "GET /api/books?search=... handles the filtering."
    )
    pdf.body_text(
        "Relevant code: GET /api/books endpoint with optional search query param "
        "in main.py (get_books function) and searchBooks() in app.js."
    )
    pdf.screenshot_placeholder("Q4 — Searching for a book by title", 100)

    # ════════════════════════════════════════════════════════
    # PART 3 – Stateful Agent Graph
    # ════════════════════════════════════════════════════════
    pdf.add_page()
    pdf.section_title("Part 3: Stateful Agent Graph (LangGraph)")

    pdf.body_text(
        "This section refactors a sequential agent pipeline into a stateful, "
        "graph-based workflow using the langgraph library. The supervisor pattern "
        "dynamically routes tasks between a Planner and Reviewer, with a "
        "correction loop that sends rejected proposals back for revision."
    )
    pdf.body_text(
        "Note: LLM responses are simulated so the graph runs locally without "
        "requiring an OpenAI API key. The graph structure, state management, "
        "routing logic, and correction loop are fully functional."
    )

    # ── Step 1 ─────────────────────────────────────────────
    pdf.sub_title("Step 1 — Install langgraph")
    pdf.body_text(
        "The langgraph package is listed in requirements.txt and installed "
        "inside the project's virtual environment."
    )
    pdf.code_block(read(FILES["state.py"]).split("from")[0].strip() + "\n\n" +
                   "# requirements.txt (relevant line):\n# langgraph>=0.2.0",
                   "requirements.txt")
    pdf.screenshot_placeholder("Step 1 — pip install output showing langgraph installed", 70)

    # ── Step 2 ─────────────────────────────────────────────
    pdf.add_page()
    pdf.sub_title("Step 2 — Setting Up the AgentState")
    pdf.body_text(
        "The AgentState TypedDict acts as the shared memory for all nodes. "
        "It holds the initial inputs (title, content, email, strict, task, llm), "
        "agent outputs (planner_proposal, reviewer_feedback), and a turn_count "
        "to prevent infinite loops."
    )
    pdf.code_block(read(FILES["state.py"]), "realtygraph/state.py")

    # ── Step 3 ─────────────────────────────────────────────
    pdf.add_page()
    pdf.sub_title("Step 3 — Creating the Agent Nodes")
    pdf.body_text(
        "Each agent is a standalone function that accepts AgentState and returns "
        "a dict with the keys it wants to update. The planner_node generates a "
        "structured proposal; the reviewer_node inspects it and flags issues "
        "or approves."
    )
    pdf.code_block(read(FILES["nodes.py"]), "realtygraph/nodes.py")

    # ── Step 4 ─────────────────────────────────────────────
    pdf.add_page()
    pdf.sub_title("Step 4 — Building the Supervisor (Router Logic)")
    pdf.body_text(
        "The supervisor is split into two parts: (1) supervisor_node increments "
        "the turn counter, and (2) router_logic reads the state and returns "
        '"planner", "reviewer", or "END" to direct the flow.'
    )
    pdf.body_text(
        "The supervisor_node is defined at the bottom of nodes.py (shown above). "
        "The router_logic is in router.py:"
    )
    pdf.code_block(read(FILES["router.py"]), "realtygraph/router.py")

    # ── Step 5 ─────────────────────────────────────────────
    pdf.add_page()
    pdf.sub_title("Step 5 — Assembling the Graph")
    pdf.body_text(
        "The three nodes (supervisor, planner, reviewer) are wired together "
        "using LangGraph's StateGraph. The supervisor is the entry point. "
        "Conditional edges from the supervisor use router_logic to decide the "
        "next node. Planner and reviewer both route back to the supervisor."
    )
    pdf.code_block(read(FILES["workflow.py"]), "realtygraph/workflow.py")

    # ── Step 6 ─────────────────────────────────────────────
    pdf.add_page()
    pdf.sub_title("Step 6 — Running and Testing")
    pdf.body_text(
        "The run_graph.py script builds the compiled graph, creates the initial "
        "state, and uses .stream() to print the output from each step. "
        "The correction loop is demonstrated: the reviewer rejects the first "
        "proposal, the planner revises it, and the reviewer then approves."
    )
    pdf.code_block(read(FILES["run_graph.py"]), "run_graph.py")

    pdf.sub_title("Output — Graph Execution (.stream())")
    pdf.body_text("The terminal output below shows the full correction loop:")
    pdf.screenshot_placeholder(
        "Step 6 -- Terminal output of python run_graph.py showing:\n"
        "  Supervisor -> Planner (initial) -> Supervisor -> Reviewer (REJECTS) ->\n"
        "  Supervisor -> Planner (revised) -> Supervisor -> Reviewer (APPROVES) -> END",
        120,
    )

    # ════════════════════════════════════════════════════════
    # SAVE
    # ════════════════════════════════════════════════════════
    out_path = os.path.join(BASE, output_name)
    pdf.output(out_path)
    print(f"\n✅  PDF saved to: {out_path}")
    print(f"    Pages: {pdf.page_no()}")
    return out_path


if __name__ == "__main__":
    build_pdf()
