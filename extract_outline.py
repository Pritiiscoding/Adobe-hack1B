#!/usr/bin/env python3
"""
PDF Content Extractor for Adobe India Hackathon - Challenge 1b

This script processes PDF files from the input directory and generates
structured JSON output with document metadata, extracted sections, and analysis.
"""

import json
import os
import sys
import argparse
from pathlib import Path
from datetime import datetime
from PyPDF2 import PdfReader

# Base directory for the project
BASE_DIR = Path(__file__).parent.absolute()

# Default directories
DEFAULT_INPUT_DIR = BASE_DIR / "Collection3" / "input"
DEFAULT_OUTPUT_DIR = BASE_DIR / "Collection3" / "output"

# Configure argument parser
def parse_arguments():
    parser = argparse.ArgumentParser(description='Extract content from PDF files.')
    parser.add_argument('--input-dir', type=str, default=str(DEFAULT_INPUT_DIR),
                      help=f'Input directory containing PDF files (default: {DEFAULT_INPUT_DIR})')
    parser.add_argument('--output-dir', type=str, default=str(DEFAULT_OUTPUT_DIR),
                      help=f'Output directory for JSON files (default: {DEFAULT_OUTPUT_DIR})')
    parser.add_argument('--collection', type=int, choices=[1, 2, 3], default=3,
                      help='Collection number to process (1, 2, or 3)')
    return parser.parse_args()

def extract_content(pdf_path):
    """Extract content from a PDF file."""
    try:
        with open(pdf_path, 'rb') as file:
            reader = PdfReader(file)
            filename = Path(pdf_path).name
            
            # Extract document outline/sections
            sections = []
            if reader.outline:
                for i, item in enumerate(reader.outline, 1):
                    if hasattr(item, 'title'):
                        page_num = reader.get_destination_page_number(item) + 1
                        sections.append({
                            "document": filename,
                            "section_title": item.title.strip(),
                            "importance_rank": i,
                            "page_number": page_num
                        })
            
            # Extract text content (simple extraction - can be enhanced)
            text_content = []
            for page_num, page in enumerate(reader.pages, 1):
                text = page.extract_text()
                if text:
                    text_content.append({
                        "document": filename,
                        "refined_text": text.strip(),
                        "page_number": page_num
                    })
            
            return {
                "sections": sections[:5],  # Top 5 sections
                "content": text_content[:5]  # Top 5 content items
            }
            
    except Exception as e:
        print(f"Error processing {pdf_path}: {str(e)}")
        return {"sections": [], "content": []}

def main():
    args = parse_arguments()
    
    # Set collection-specific paths and metadata
    collection_dir = BASE_DIR / f"Collection{args.collection}"
    input_dir = collection_dir / "input"
    output_dir = collection_dir / "output"
    
    # Ensure input and output directories exist
    if not input_dir.exists():
        print(f"Error: Input directory '{input_dir}' does not exist.")
        sys.exit(1)
    
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Get all PDF files from input directory
    pdf_files = list(input_dir.glob('*.pdf'))
    
    if not pdf_files:
        print(f"No PDF files found in '{input_dir}'.")
        sys.exit(0)
    
    # Collection-specific metadata
    collection_metadata = {
        1: {
            "persona": "Travel Planner",
            "job": "Plan a trip of 4 days for a group of 10 college friends."
        },
        2: {
            "persona": "HR professional",
            "job": "Create and manage fillable forms for onboarding and compliance."
        },
        3: {
            "persona": "Food Contractor",
            "job": "Prepare a vegetarian buffet-style dinner menu for a corporate gathering, including gluten-free items."
        }
    }
    
    # Initialize result structure
    result = {
        "metadata": {
            "input_documents": [f.name for f in pdf_files],
            "persona": collection_metadata[args.collection]["persona"],
            "job_to_be_done": collection_metadata[args.collection]["job"],
            "processing_timestamp": datetime.now().isoformat()
        },
        "extracted_sections": [],
        "subsection_analysis": []
    }
    
    # Process each PDF file
    for pdf_file in pdf_files:
        print(f"Processing: {pdf_file.name}")
        
        # Extract content
        content = extract_content(pdf_file)
        
        # Add to results
        result["extracted_sections"].extend(content["sections"])
        result["subsection_analysis"].extend(content["content"])
    
    # Sort sections by importance_rank
    result["extracted_sections"].sort(key=lambda x: x["importance_rank"])
    
    # Ensure we only keep top 5 sections and content items
    result["extracted_sections"] = result["extracted_sections"][:5]
    result["subsection_analysis"] = result["subsection_analysis"][:5]
    
    # Prepare output filename
    output_filename = f"collection{args.collection}_output.json"
    output_path = output_dir / output_filename
    
    # Save to JSON file
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    
    print(f"\nProcessing complete!")
    print(f"- Collection: {args.collection}")
    print(f"- Output saved to: {output_path}")
    print(f"- Total sections extracted: {len(result['extracted_sections'])}")
    print(f"- Total content items: {len(result['subsection_analysis'])}")

if __name__ == "__main__":
    main()
