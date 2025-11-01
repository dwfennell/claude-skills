from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.lib import colors

def add_flashcards(flashcards_data, output_filename="my_flashcards.pdf", separate_pdfs=False):
    """
    Creates a PDF with flashcards optimized for double-sided printing.

    Layout: 2x5 grid (10 cards per sheet)
    - Odd pages: Front sides of cards
    - Even pages: Back sides of cards (mirrored for proper alignment)

    Args:
        flashcards_data: List of dicts with 'front' and 'back' keys, and optional 'category' key
        output_filename: Name of output PDF file
        separate_pdfs: If True, creates two separate PDFs (one for fronts, one for backs)
                      This is useful for printers without duplex/double-sided printing support

    Example:
        cards = [
            {"front": "What is Python?", "back": "A programming language"},
            {"front": "What is a list?", "back": "An ordered collection", "category": "Data Structures"},
        ]
        add_flashcards(cards, "python_flashcards.pdf")

        # For printers without duplex support:
        add_flashcards(cards, "python_flashcards.pdf", separate_pdfs=True)

    To print with duplex/double-sided printing:
        - Look for "Two-Sided" or "Duplex" setting in your printer dialog
        - Common options: "Long-Edge binding" or "Flip on Long Edge"
        - Print the single PDF normally

    To print without duplex support (separate_pdfs=True):
        1. Print the "_fronts.pdf" file
        2. Take the printed pages, flip the stack over
        3. Reinsert into printer tray (blank side up)
        4. Print the "_backs.pdf" file
        5. Cut along the dotted lines
    """
    page_width, page_height = letter

    # 2x5 grid: 2 columns, 5 rows
    cols = 2
    rows = 5
    cards_per_page = cols * rows

    # Card dimensions with margins for safe printing
    margin_x = 0.5 * inch  # Left/right margins
    margin_y = 0.5 * inch  # Top/bottom margins
    spacing_x = 0.2 * inch  # Horizontal spacing between cards
    spacing_y = 0.2 * inch  # Vertical spacing between cards

    card_width = (page_width - 2 * margin_x - (cols - 1) * spacing_x) / cols
    card_height = (page_height - 2 * margin_y - (rows - 1) * spacing_y) / rows

    # Determine output file names
    if separate_pdfs:
        base_name = output_filename.rsplit('.', 1)[0]
        fronts_filename = f"{base_name}_fronts.pdf"
        backs_filename = f"{base_name}_backs.pdf"
        c_fronts = canvas.Canvas(fronts_filename, pagesize=letter)
        c_backs = canvas.Canvas(backs_filename, pagesize=letter)
    else:
        c = canvas.Canvas(output_filename, pagesize=letter)

    # Process cards in batches of 10
    for batch_start in range(0, len(flashcards_data), cards_per_page):
        batch = flashcards_data[batch_start:batch_start + cards_per_page]

        # Select the appropriate canvas for fronts
        canvas_front = c_fronts if separate_pdfs else c

        # FRONT PAGE (odd page)
        for idx, card in enumerate(batch):
            row = idx // cols
            col = idx % cols

            x = margin_x + col * (card_width + spacing_x)
            y = page_height - margin_y - (row + 1) * card_height - row * spacing_y

            # Draw card border
            canvas_front.setStrokeColor(colors.black)
            canvas_front.setLineWidth(1)
            canvas_front.rect(x, y, card_width, card_height)

            # Draw front content (centered)
            canvas_front.setFont("Helvetica", 12)
            canvas_front.setFillColor(colors.black)

            # Handle multi-line text if needed
            text = card["front"]
            text_width = canvas_front.stringWidth(text, "Helvetica", 12)

            if text_width > card_width - 20:
                # If text is too long, use smaller font
                canvas_front.setFont("Helvetica", 10)
                text_width = canvas_front.stringWidth(text, "Helvetica", 10)

            x_text = x + (card_width - text_width) / 2
            y_text = y + card_height / 2
            canvas_front.drawString(x_text, y_text, text)

        # Draw cutting guides
        canvas_front.setStrokeColor(colors.grey)
        canvas_front.setLineWidth(0.5)
        canvas_front.setDash(2, 2)

        # Vertical guides (between columns)
        for col in range(1, cols):
            x_guide = margin_x + col * card_width + (col - 0.5) * spacing_x
            canvas_front.line(x_guide, margin_y, x_guide, page_height - margin_y)

        # Horizontal guides (between rows)
        for row in range(1, rows):
            y_guide = page_height - margin_y - row * card_height - (row - 0.5) * spacing_y
            canvas_front.line(margin_x, y_guide, page_width - margin_x, y_guide)

        canvas_front.setDash()  # Reset to solid line
        canvas_front.showPage()

        # Select the appropriate canvas for backs
        canvas_back = c_backs if separate_pdfs else c

        # BACK PAGE (even page) - mirrored horizontally for proper alignment
        for idx, card in enumerate(batch):
            row = idx // cols
            # Mirror the column for back side
            col = (cols - 1) - (idx % cols)

            x = margin_x + col * (card_width + spacing_x)
            y = page_height - margin_y - (row + 1) * card_height - row * spacing_y

            # Draw card border
            canvas_back.setStrokeColor(colors.black)
            canvas_back.setLineWidth(1)
            canvas_back.rect(x, y, card_width, card_height)

            # Draw category if present (top-right corner)
            if "category" in card and card["category"]:
                category = card["category"][:50]  # Limit to 50 characters
                canvas_back.setFont("Helvetica", 8)
                canvas_back.setFillColor(colors.grey)
                category_x = x + card_width - 5 - canvas_back.stringWidth(category, "Helvetica", 8)
                category_y = y + card_height - 12
                canvas_back.drawString(category_x, category_y, category)

            # Draw back content (centered)
            canvas_back.setFont("Helvetica", 12)
            canvas_back.setFillColor(colors.black)

            # Handle multi-line text if needed
            text = card["back"]
            text_width = canvas_back.stringWidth(text, "Helvetica", 12)

            if text_width > card_width - 20:
                # If text is too long, use smaller font
                canvas_back.setFont("Helvetica", 10)
                text_width = canvas_back.stringWidth(text, "Helvetica", 10)

            x_text = x + (card_width - text_width) / 2
            y_text = y + card_height / 2
            canvas_back.drawString(x_text, y_text, text)

        # Draw cutting guides
        canvas_back.setStrokeColor(colors.grey)
        canvas_back.setLineWidth(0.5)
        canvas_back.setDash(2, 2)

        # Vertical guides (between columns)
        for col in range(1, cols):
            x_guide = margin_x + col * card_width + (col - 0.5) * spacing_x
            canvas_back.line(x_guide, margin_y, x_guide, page_height - margin_y)

        # Horizontal guides (between rows)
        for row in range(1, rows):
            y_guide = page_height - margin_y - row * card_height - (row - 0.5) * spacing_y
            canvas_back.line(margin_x, y_guide, page_width - margin_x, y_guide)

        canvas_back.setDash()  # Reset to solid line
        canvas_back.showPage()

    # Save the PDF(s)
    if separate_pdfs:
        c_fronts.save()
        c_backs.save()
        print(f"Flashcards created:")
        print(f"  Fronts: {fronts_filename}")
        print(f"  Backs: {backs_filename}")
    else:
        c.save()
        print(f"Flashcards created: {output_filename}")

    print(f"Total cards: {len(flashcards_data)}")
    num_pages = ((len(flashcards_data) + cards_per_page - 1) // cards_per_page)
    if separate_pdfs:
        print(f"Pages: {num_pages} pages per PDF")
    else:
        print(f"Pages: {num_pages * 2} total pages")

if __name__ == "__main__":
    # Example of creating custom flashcards
    my_cards = [
        {"front": "What is the capital of France?", "back": "Paris", "category": "Geography"},
        {"front": "What is 2 + 2?", "back": "4", "category": "Math"},
        {"front": "What is the largest planet?", "back": "Jupiter", "category": "Astronomy"},
        {"front": "7 × 8 = ?", "back": "56", "category": "Math"},
        {"front": "What is H2O?", "back": "Water", "category": "Chemistry"},
    ]
    add_flashcards(my_cards, "example_flashcards.pdf")
