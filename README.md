# Multi-Collection PDF Analysis

## Overview
This project is a solution for Adobe India Hackathon - Challenge 1b. It processes multiple document collections and extracts relevant content based on specific personas and use cases.

## Project Structure
```
Challenge_1b/
├── Collection1/                    # Travel Planning
│   ├── input/                     # South of France guides
│   └── output/                    # Analysis results
├── Collection2/                   # Adobe Acrobat Learning
│   ├── input/                     # Acrobat tutorials
│   └── output/                    # Analysis results
├── Collection3/                   # Recipe Collection
│   ├── input/                     # Cooking guides
│   └── output/                    # Analysis results
├── pdf_analyzer.py               # Main script
├── requirements.txt              # Python dependencies
└── README.md                     # This file
```

## Collections

### Collection 1: Travel Planning
- **Persona**: Travel Planner
- **Task**: Plan a 4-day trip for 10 college friends to South of France
- **Documents**: 7 travel guides

### Collection 2: Adobe Acrobat Learning
- **Persona**: HR Professional
- **Task**: Create and manage fillable forms for onboarding and compliance
- **Documents**: 15 Acrobat guides

### Collection 3: Recipe Collection
- **Persona**: Food Contractor
- **Task**: Prepare vegetarian buffet-style dinner menu for corporate gathering
- **Documents**: 9 cooking guides

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd Challenge_1b
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Process a specific collection:
```bash
python pdf_analyzer.py --collection 1  # Process Collection 1 (Travel Planning)
python pdf_analyzer.py --collection 2  # Process Collection 2 (Adobe Acrobat Learning)
python pdf_analyzer.py --collection 3  # Process Collection 3 (Recipe Collection)
```

### Process all collections:
```bash
python pdf_analyzer.py --all
```

## Output Format

The script generates JSON output files in the respective collection's output directory with the following structure:

```json
{
  "metadata": {
    "collection_id": 1,
    "collection_name": "Travel Planning",
    "persona": "Travel Planner",
    "job_to_be_done": "Plan a 4-day trip for 10 college friends to South of France",
    "input_documents": ["file1.pdf", "file2.pdf"],
    "processing_timestamp": "2025-01-01T12:00:00.000000"
  },
  "extracted_sections": [
    {
      "document": "file1.pdf",
      "section_title": "Introduction",
      "importance_rank": 1,
      "page_number": 1
    }
  ],
  "subsection_analysis": [
    {
      "document": "file1.pdf",
      "refined_text": "Extracted text content...",
      "page_number": 1
    }
  ]
}
```

## Features

- **Persona-based Analysis**: Content extraction tailored to specific user personas
- **Multi-Collection Support**: Process multiple document collections with different purposes
- **Structured Output**: Well-formatted JSON output with metadata and extracted content
- **Error Handling**: Robust error handling and logging

## Dependencies

- Python 3.7+
- PyPDF2
- typing-extensions

## License

This project is part of the Adobe India Hackathon 2025.
