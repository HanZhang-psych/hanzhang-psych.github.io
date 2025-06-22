import os
import re
import yaml
import bibtexparser
from pathlib import Path

def load_bibtex_data():
    """Load all BibTeX files and create a lookup dictionary"""
    bib_data = {}
    
    # List of possible bib files
    bib_files = ['journal_articles.bib', 'preprints.bib', 'conference_papers.bib', 'talks.bib', 'publications.bib']
    
    for bib_file in bib_files:
        if os.path.exists(bib_file):
            print(f"Loading {bib_file}...")
            with open(bib_file, 'r', encoding='utf-8') as f:
                try:
                    bib_database = bibtexparser.load(f)
                    for entry in bib_database.entries:
                        # Use ID as key, store full entry
                        bib_data[entry['ID']] = entry
                except Exception as e:
                    print(f"Error loading {bib_file}: {e}")
    
    return bib_data

def format_publication_field(entry):
    """Format publication field with volume, issue, pages"""
    entry_type = entry.get('ENTRYTYPE', '').lower()
    
    if entry_type == 'article':
        # Journal article
        journal = entry.get('journal', '')
        volume = entry.get('volume', '')
        number = entry.get('number', '')
        pages = entry.get('pages', '')
        
        if journal:
            pub_field = f"*{journal}*"
            
            # Add volume and issue
            if volume:
                if number:
                    pub_field += f", {volume}*({number})"
                else:
                    pub_field += f", {volume}*"
            
            # Add pages
            if pages:
                # Convert LaTeX page ranges (--) to en-dash
                pages = pages.replace('--', '-')
                pub_field += f", {pages}"
            
            return pub_field
    
    elif entry_type == 'inproceedings' or entry_type == 'incollection':
        # Conference paper or book chapter
        booktitle = entry.get('booktitle', '')
        if booktitle:
            return f"In *{booktitle}*"
    
    elif entry_type == 'book':
        # Book
        publisher = entry.get('publisher', '')
        if publisher:
            return f"*{publisher}*"
    
    # Default fallback
    journal = entry.get('journal', '')
    booktitle = entry.get('booktitle', '')
    publisher = entry.get('publisher', '')
    
    if journal:
        return f"*{journal}*"
    elif booktitle:
        return f"In *{booktitle}*"
    elif publisher:
        return f"*{publisher}*"
    
    return None

def enhance_publication_files():
    """Enhance all publication markdown files"""
    bib_data = load_bibtex_data()
    
    if not bib_data:
        print("No BibTeX data found!")
        return
    
    pub_dir = Path('content/publication')
    if not pub_dir.exists():
        print("No publication directory found!")
        return
    
    enhanced_count = 0
    
    for pub_folder in pub_dir.iterdir():
        if pub_folder.is_dir():
            index_file = pub_folder / 'index.md'
            if index_file.exists():
                try:
                    # Read the markdown file
                    with open(index_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Split front matter and body
                    if content.startswith('---'):
                        parts = content.split('---', 2)
                        if len(parts) >= 3:
                            front_matter = parts[1]
                            body = parts[2] if len(parts) > 2 else ''
                            
                            # Parse YAML front matter
                            try:
                                data = yaml.safe_load(front_matter)
                                
                                # Try to find matching BibTeX entry
                                # Look for entry by folder name or title
                                folder_name = pub_folder.name
                                title = data.get('title', '')
                                
                                matching_entry = None
                                
                                # First try to match by folder name pattern
                                for bib_id, entry in bib_data.items():
                                    if bib_id.lower() in folder_name.lower():
                                        matching_entry = entry
                                        break
                                
                                # If no match, try by title similarity
                                if not matching_entry and title:
                                    for bib_id, entry in bib_data.items():
                                        bib_title = entry.get('title', '').lower()
                                        if bib_title and title.lower() in bib_title:
                                            matching_entry = entry
                                            break
                                
                                if matching_entry:
                                    # Format the publication field
                                    new_pub_field = format_publication_field(matching_entry)
                                    
                                    if new_pub_field:
                                        # Update or add publication field
                                        data['publication'] = new_pub_field
                                        
                                        # Write back the file
                                        new_front_matter = yaml.dump(data, default_flow_style=False, allow_unicode=True)
                                        new_content = f"---\n{new_front_matter}---{body}"
                                        
                                        with open(index_file, 'w', encoding='utf-8') as f:
                                            f.write(new_content)
                                        
                                        enhanced_count += 1
                                        print(f"Enhanced: {pub_folder.name}")
                                    else:
                                        print(f"Could not format publication field for: {pub_folder.name}")
                                else:
                                    print(f"No matching BibTeX entry found for: {pub_folder.name}")
                            
                            except yaml.YAMLError as e:
                                print(f"YAML error in {index_file}: {e}")
                
                except Exception as e:
                    print(f"Error processing {index_file}: {e}")
    
    print(f"Enhanced {enhanced_count} publications with complete metadata!")

if __name__ == "__main__":
    enhance_publication_files()
