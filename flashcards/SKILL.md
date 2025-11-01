---
name: flashcards
description: Create printable PDF flashcards optimized for double-sided printing with a 2x5 grid layout. Use when users request to create flashcards, study cards, or memory cards for any subject. Supports both duplex printers and manual printing workflows.
---

# Flashcards

## Overview

This skill enables creating professional PDF flashcards with a 2x5 grid layout (10 cards per sheet) optimized for efficient double-sided printing. The skill automatically handles proper alignment between front and back sides, adds cutting guides, and supports both automatic duplex printing and manual printing workflows.

## When to Use This Skill

Use this skill when users request:
- "Create flashcards for [topic]"
- "Make study cards for [subject]"
- "Generate flashcards from this content"
- "Help me make printable flashcards"
- Any request involving creating physical or printable study materials

## Quick Start

To create flashcards, set up a Python virtual environment with reportlab, then use the `add_flashcards()` function:

```python
from scripts.create_flashcards import add_flashcards

# Define flashcards as a list of dictionaries
flashcards = [
    {"front": "Question 1", "back": "Answer 1"},
    {"front": "Question 2", "back": "Answer 2"},
    # ... up to any number of cards
]

# Generate PDF
add_flashcards(flashcards, "output.pdf")
```

## Setup Requirements

Install the required dependency (reportlab) using a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install reportlab
```

## Creating Flashcards

### Basic Usage

```python
from scripts.create_flashcards import add_flashcards

cards = [
    {"front": "7 × 8 = ?", "back": "56"},
    {"front": "What is Python?", "back": "A programming language"},
]

add_flashcards(cards, "my_flashcards.pdf")
```

### For Duplex Printers (Default)

Generate a single PDF with alternating front/back pages:

```python
add_flashcards(flashcards, "flashcards.pdf", separate_pdfs=False)
```

**Printer settings to look for:**
- "Two-Sided" or "Duplex Printing"
- "Long-Edge binding" or "Flip on Long Edge"
- "Automatic 2-Sided"

### For Printers Without Duplex Support

Generate separate PDFs for fronts and backs:

```python
add_flashcards(flashcards, "flashcards.pdf", separate_pdfs=True)
```

This creates:
- `flashcards_fronts.pdf` - Print first
- `flashcards_backs.pdf` - Print after flipping the stack

**Printing instructions:**
1. Print all pages from `_fronts.pdf`
2. Take the printed stack and flip it over
3. Reinsert into printer tray (blank side up)
4. Print all pages from `_backs.pdf`
5. Cut along the dotted lines

## Layout Specifications

- **Grid**: 2 columns × 5 rows = 10 cards per sheet
- **Card size**: Approximately 3.5" × 1.9" (calculated based on page size and margins)
- **Margins**: 0.5 inch on all edges for safe printing
- **Spacing**: 0.2 inch between cards
- **Cutting guides**: Dotted lines centered between cards
- **Back alignment**: Automatically mirrored for proper alignment with fronts

## Workflow

1. **Gather content**: Collect or generate the questions and answers
2. **Format data**: Structure as list of dictionaries with "front" and "back" keys
3. **Choose printing mode**: Decide between single PDF (duplex) or separate PDFs (manual)
4. **Generate PDF(s)**: Call `add_flashcards()` with appropriate parameters
5. **Print**: Follow instructions based on printer capabilities
6. **Cut**: Use dotted lines as guides to separate individual cards

## Resources

### scripts/create_flashcards.py

The main Python script for generating flashcard PDFs. Contains the `add_flashcards()` function which handles:
- PDF generation using reportlab
- 2x5 grid layout calculation
- Front/back page alignment (mirroring for proper double-sided printing)
- Cutting guide generation
- Both single PDF and separate PDF modes

**Key function:**
```python
add_flashcards(flashcards_data, output_filename="my_flashcards.pdf", separate_pdfs=False)
```

**Parameters:**
- `flashcards_data`: List of dicts with 'front' and 'back' keys
- `output_filename`: Name of output PDF file
- `separate_pdfs`: If True, creates separate files for fronts and backs

The script is self-contained and can be executed directly or imported as a module.
