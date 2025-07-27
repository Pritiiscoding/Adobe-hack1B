#!/usr/bin/env python3
"""
Multi-Collection PDF Analyzer for Adobe India Hackathon - Challenge 1b

This script processes PDF files from multiple collections, extracts relevant content
based on specific personas and use cases, and generates structured JSON output.
"""

import json
import os
import sys
import argparse
from pathlib import Path
from datetime import datetime, timezone
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from PyPDF2 import PdfReader

# Base directory for the project
BASE_DIR = Path(__file__).parent.absolute()

# Collection configurations
COLLECTIONS = {
    1: {
        'name': 'Travel Planning',
        'persona': 'Travel Planner',
        'task': 'Plan a 4-day trip for 10 college friends to South of France',
        'input_dir': BASE_DIR / 'Collection1',  # PDFs are directly in Collection1
        'output_file': BASE_DIR / 'output' / 'challenge1b_output_1.json'
    },
    2: {
        'name': 'Adobe Acrobat Learning',
        'persona': 'HR Professional',
        'task': 'Create and manage fillable forms for onboarding and compliance',
        'input_dir': BASE_DIR / 'Collection2',  # PDFs are directly in Collection2
        'output_file': BASE_DIR / 'output' / 'challenge1b_output_2.json'
    },
    3: {
        'name': 'Recipe Collection',
        'persona': 'Food Contractor',
        'task': 'Prepare vegetarian buffet-style dinner menu for corporate gathering',
        'input_dir': BASE_DIR / 'Collection3',  # PDFs are directly in Collection3
        'output_file': BASE_DIR / 'output' / 'challenge1b_output_3.json'
    }
}

@dataclass
class DocumentSection:
    """Represents a section extracted from a PDF document."""
    document: str
    section_title: str
    importance_rank: int
    page_number: int

@dataclass
class SubsectionAnalysis:
    """Represents analysis of a subsection of a document."""
    document: str
    refined_text: str
    page_number: int

def extract_sections(pdf_path: Path, collection_id: int) -> List[Dict[str, Any]]:
    """Extract sections from a PDF file based on the collection type."""
    try:
        with open(pdf_path, 'rb') as file:
            reader = PdfReader(file)
            filename = pdf_path.name
            sections = []
            
            # Extract document outline/sections if available
            if reader.outline:
                for i, item in enumerate(reader.outline, 1):
                    if hasattr(item, 'title'):
                        try:
                            page_num = reader.get_destination_page_number(item) + 1
                            sections.append({
                                "document": filename,
                                "section_title": item.title.strip(),
                                "importance_rank": i,
                                "page_number": page_num
                            })
                        except Exception as e:
                            print(f"Error processing outline item in {filename}: {e}")
            
            # If no outline, create a basic section for the whole document
            if not sections:
                sections.append({
                    "document": filename,
                    "section_title": "Document Content",
                    "importance_rank": 1,
                    "page_number": 1
                })
            
            return sections
            
    except Exception as e:
        print(f"Error processing {pdf_path}: {e}")
        return []

def analyze_content(pdf_path: Path, collection_id: int) -> List[Dict[str, Any]]:
    """Analyze the content of a PDF file based on the collection type."""
    try:
        with open(pdf_path, 'rb') as file:
            reader = PdfReader(file)
            filename = pdf_path.name
            analysis = []
            
            # Simple text extraction from first few pages for demonstration
            # In a real implementation, this would include more sophisticated analysis
            max_pages = min(3, len(reader.pages))  # Analyze first 3 pages or fewer
            
            for page_num in range(max_pages):
                page = reader.pages[page_num]
                text = page.extract_text()
                if text:
                    # Simple text refinement - in a real implementation, this would be more sophisticated
                    refined_text = ' '.join(text.split()[:200])  # First 200 words
                    analysis.append({
                        "document": filename,
                        "refined_text": refined_text,
                        "page_number": page_num + 1
                    })
            
            return analysis
            
    except Exception as e:
        print(f"Error analyzing {pdf_path}: {e}")
        return []

def process_collection(collection_id: int) -> Dict[str, Any]:
    """Process a single collection of PDFs."""
    if collection_id not in COLLECTIONS:
        raise ValueError(f"Invalid collection ID: {collection_id}")
    
    config = COLLECTIONS[collection_id]
    input_dir = config['input_dir']
    
    if not input_dir.exists():
        raise FileNotFoundError(f"Input directory not found: {input_dir}")
    
    # Find all PDF files in the input directory
    pdf_files = list(input_dir.glob('*.pdf'))
    if not pdf_files:
        raise FileNotFoundError(f"No PDF files found in {input_dir}")
    
    # Prepare the output structure
    output = {
        "metadata": {
            "collection_id": collection_id,
            "collection_name": config['name'],
            "persona": config['persona'],
            "job_to_be_done": config['task'],
            "input_documents": [f.name for f in pdf_files],
            "processing_timestamp": datetime.utcnow().isoformat()
        },
        "extracted_sections": [],
        "subsection_analysis": []
    }
    
    # Process each PDF file
    for pdf_file in pdf_files:
        # Extract sections
        sections = extract_sections(pdf_file, collection_id)
        output["extracted_sections"].extend(sections)
        
        # Analyze content
        analysis = analyze_content(pdf_file, collection_id)
        output["subsection_analysis"].extend(analysis)
    
    return output

def save_output(output: Dict[str, Any], output_path: Path) -> None:
    """Save the output to a JSON file."""
    try:
        # Create output directory if it doesn't exist
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Write the output to a JSON file
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(output, f, indent=2, ensure_ascii=False)
        
        print(f"Successfully saved output to {output_path}")
    except Exception as e:
        print(f"Error saving output to {output_path}: {e}")

def main():
    """Main function to process all collections or a specific one."""
    parser = argparse.ArgumentParser(description='Process PDF collections for Challenge 1b')
    parser.add_argument('--collection', type=int, choices=[1, 2, 3], 
                       help='Process a specific collection (1, 2, or 3)')
    parser.add_argument('--all', action='store_true',
                       help='Process all collections')
    
    args = parser.parse_args()
    
    if not args.collection and not args.all:
        print("Please specify either --collection <1|2|3> or --all")
        return
    
    collections_to_process = [args.collection] if args.collection else [1, 2, 3]
    
    for collection_id in collections_to_process:
        try:
            print(f"\nProcessing Collection {collection_id}: {COLLECTIONS[collection_id]['name']}")
            output = process_collection(collection_id)
            output_path = COLLECTIONS[collection_id]['output_file']
            save_output(output, output_path)
        except Exception as e:
            print(f"Error processing collection {collection_id}: {e}")

if __name__ == "__main__":
    main()
