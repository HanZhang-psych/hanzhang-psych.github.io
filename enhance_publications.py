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

def format_author_names_apa(entry):
    """Format author names from BibTeX entry according to APA-7 style"""
    author_field = entry.get('author', '')
    if not author_field:
        return None
    
    # Split authors by " and "
    authors = [author.strip() for author in author_field.split(' and ')]
    
    if not authors:
        return None
    
    # Format each author name
    formatted_authors = []
    for author in authors:
        # Author is already in "Last, First" format from BibTeX
        # We just need to convert "Han Zhang" to "admin" for highlighting
        if author.strip() == "Zhang, Han":
            formatted_authors.append("admin")
        else:
            formatted_authors.append(author)
    
    return formatted_authors

def convert_author_names(authors_list):
    """Convert plain text author names to author profile references"""
    if not authors_list:
        return authors_list
    
    converted_authors = []
    for author in authors_list:
        # Convert "Han Zhang" to "admin" for author highlighting
        if author.strip() == "Han Zhang":
            converted_authors.append("admin")
        else:
            converted_authors.append(author)
    
    return converted_authors

def format_doi_url(entry):
    """Format DOI and URL according to APA-7 style"""
    doi = entry.get('doi', '')
    url = entry.get('url', '')
    
    if doi:
        # Clean DOI - remove any existing "doi:" prefix
        doi = doi.replace('doi:', '').strip()
        if not doi.startswith('http'):
            doi = f"https://doi.org/{doi}"
        return doi
    elif url:
        return url
    
    return None

def format_publication_field(entry):
    """Format publication field according to APA-7 style"""
    entry_type = entry.get('ENTRYTYPE', '').lower()
    
    if entry_type == 'article':
        # Journal article: *Journal Name*, Volume(Issue), pages
        journal = entry.get('journal', '')
        volume = entry.get('volume', '')
        number = entry.get('number', '')
        pages = entry.get('pages', '')
        
        if journal:
            pub_field = f"*{journal}*"
            
            # Add volume and issue
            if volume:
                if number:
                    pub_field += f", *{volume}*({number})"
                else:
                    pub_field += f", *{volume}*"
            
            # Add pages
            if pages:
                # Convert LaTeX page ranges (--) to en-dash
                pages = pages.replace('--', '-')
                pub_field += f", {pages}"
            
            return pub_field
    
    elif entry_type == 'inproceedings':
        # Conference paper: *Conference Name*
        booktitle = entry.get('booktitle', '')
        if booktitle:
            return f"*{booktitle}*"
    
    elif entry_type == 'incollection':
        # Book chapter: In *Book Title*
        booktitle = entry.get('booktitle', '')
        if booktitle:
            return f"In *{booktitle}*"
    
    elif entry_type == 'book':
        # Book: *Book Title*. Publisher
        title = entry.get('title', '')
        publisher = entry.get('publisher', '')
        if title and publisher:
            return f"*{title}*. {publisher}"
        elif title:
            return f"*{title}*"
        elif publisher:
            return f"*{publisher}*"
    
    elif entry_type == 'phdthesis' or entry_type == 'mastersthesis':
        # Thesis: *Title* (Doctoral dissertation/Master's thesis). University
        title = entry.get('title', '')
        school = entry.get('school', '')
        thesis_type = "Doctoral dissertation" if entry_type == 'phdthesis' else "Master's thesis"
        
        if title and school:
            return f"*{title}* ({thesis_type}). {school}"
        elif title:
            return f"*{title}* ({thesis_type})"
    
    elif entry_type == 'techreport':
        # Technical report: *Title* (Report No. X). Publisher
        title = entry.get('title', '')
        number = entry.get('number', '')
        institution = entry.get('institution', '')
        
        if title and number and institution:
            return f"*{title}* (Report No. {number}). {institution}"
        elif title and institution:
            return f"*{title}*. {institution}"
        elif title:
            return f"*{title}*"
    
    elif entry_type == 'misc':
        # Miscellaneous: *Title*. Publisher/Organization
        title = entry.get('title', '')
        howpublished = entry.get('howpublished', '')
        
        if title and howpublished:
            return f"*{title}*. {howpublished}"
        elif title:
            return f"*{title}*"
    
    # Default fallback
    journal = entry.get('journal', '')
    booktitle = entry.get('booktitle', '')
    publisher = entry.get('publisher', '')
    title = entry.get('title', '')
    
    if journal:
        return f"*{journal}*"
    elif booktitle:
        return f"*{booktitle}*"
    elif title and publisher:
        return f"*{title}*. {publisher}"
    elif title:
        return f"*{title}*"
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
                                    # Normalize both names for comparison (replace underscores and hyphens)
                                    normalized_bib_id = bib_id.lower().replace('_', '-').replace('-', '')
                                    normalized_folder = folder_name.lower().replace('_', '-').replace('-', '')
                                    
                                    # Try multiple matching strategies
                                    if (bib_id.lower() in folder_name.lower() or 
                                        normalized_bib_id in normalized_folder or
                                        folder_name.lower() in bib_id.lower()):
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
                                    
                                    # Add DOI/URL if available
                                    doi_url = format_doi_url(matching_entry)
                                    if doi_url:
                                        data['doi'] = doi_url
                                    
                                    # Format author names according to APA-7 style
                                    apa_authors = format_author_names_apa(matching_entry)
                                    if apa_authors:
                                        data['authors'] = apa_authors
                                    elif 'authors' in data:
                                        # Fallback to existing authors if no BibTeX author data
                                        data['authors'] = convert_author_names(data['authors'])
                                     
                                    # Write back the file
                                    new_front_matter = yaml.dump(data, default_flow_style=False, allow_unicode=True)
                                    new_content = f"---\n{new_front_matter}---{body}"
                                     
                                    with open(index_file, 'w', encoding='utf-8') as f:
                                        f.write(new_content)
                                     
                                    enhanced_count += 1
                                    print(f"Enhanced: {pub_folder.name}")
                                else:
                                    # Even if no matching BibTeX entry, still convert author names
                                    if 'authors' in data:
                                        data['authors'] = convert_author_names(data['authors'])
                                        
                                        # Write back the file with converted authors
                                        new_front_matter = yaml.dump(data, default_flow_style=False, allow_unicode=True)
                                        new_content = f"---\n{new_front_matter}---{body}"
                                        
                                        with open(index_file, 'w', encoding='utf-8') as f:
                                            f.write(new_content)
                                        
                                        enhanced_count += 1
                                        print(f"Enhanced authors: {pub_folder.name}")
                                    else:
                                        print(f"No matching BibTeX entry found for: {pub_folder.name}")
                            
                            except yaml.YAMLError as e:
                                print(f"YAML error in {index_file}: {e}")
                
                except Exception as e:
                    print(f"Error processing {index_file}: {e}")
    
    print(f"Enhanced {enhanced_count} publications with complete metadata!")

if __name__ == "__main__":
    enhance_publication_files()
