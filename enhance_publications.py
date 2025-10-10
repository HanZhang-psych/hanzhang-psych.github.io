import os
import yaml
import bibtexparser
from pathlib import Path
from citeproc import CitationStylesStyle, CitationStylesBibliography, Citation, CitationItem
from citeproc.source.json import CiteProcJSON

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

def convert_bibtex_to_csl(bib_entry):
    """Convert a BibTeX entry to CSL JSON format"""
    entry_type = bib_entry.get('ENTRYTYPE', '').lower()
    
    # Map BibTeX entry types to CSL types
    type_mapping = {
        'article': 'article-journal',
        'book': 'book',
        'inproceedings': 'paper-conference',
        'incollection': 'chapter',
        'phdthesis': 'thesis',
        'mastersthesis': 'thesis',
        'techreport': 'report',
        'misc': 'article'
    }
    
    csl_type = type_mapping.get(entry_type, 'article')
    
    # Convert authors
    authors = []
    if 'author' in bib_entry:
        author_string = bib_entry['author']
        # Split by " and " and parse each author
        for author in author_string.split(' and '):
            author = author.strip()
            if ',' in author:
                # Format: "Last, First"
                last, first = author.split(',', 1)
                authors.append({
                    'family': last.strip(),
                    'given': first.strip()
                })
            else:
                # Format: "First Last" - try to split
                parts = author.split()
                if len(parts) >= 2:
                    authors.append({
                        'family': parts[-1],
                        'given': ' '.join(parts[:-1])
                    })
                else:
                    authors.append({
                        'family': author,
                        'given': ''
                    })
    
    # Build CSL entry
    csl_entry = {
        'id': bib_entry.get('ID', ''),
        'type': csl_type,
        'title': bib_entry.get('title', ''),
        'author': authors
    }
    
    # Add publication-specific fields
    if entry_type == 'article':
        csl_entry.update({
            'container-title': str(bib_entry.get('journal', '')),
            'volume': str(bib_entry.get('volume', '')),
            'issue': str(bib_entry.get('number', '')),
            'page': str(bib_entry.get('pages', '')),
            'DOI': str(bib_entry.get('doi', '')),
            'URL': str(bib_entry.get('url', ''))
        })
    elif entry_type in ['inproceedings', 'incollection']:
        csl_entry.update({
            'container-title': str(bib_entry.get('booktitle', '')),
            'publisher': str(bib_entry.get('publisher', '')),
            'page': str(bib_entry.get('pages', '')),
            'DOI': str(bib_entry.get('doi', '')),
            'URL': str(bib_entry.get('url', ''))
        })
    elif entry_type == 'book':
        csl_entry.update({
            'publisher': str(bib_entry.get('publisher', '')),
            'publisher-place': str(bib_entry.get('address', '')),
            'page': str(bib_entry.get('pages', '')),
            'DOI': str(bib_entry.get('doi', '')),
            'URL': str(bib_entry.get('url', ''))
        })
    elif entry_type in ['phdthesis', 'mastersthesis']:
        csl_entry.update({
            'publisher': str(bib_entry.get('school', '')),
            'genre': 'Doctoral dissertation' if entry_type == 'phdthesis' else 'Master\'s thesis'
        })
    
    # Add common fields
    if 'year' in bib_entry:
        try:
            year = int(bib_entry['year'])
            csl_entry['issued'] = {'date-parts': [[year]]}
        except (ValueError, TypeError):
            # If year is not a valid integer, skip it
            pass
    else:
        # Ensure issued field exists even without year
        csl_entry['issued'] = {'date-parts': [[]]}
    
    if 'doi' in bib_entry and bib_entry['doi']:
        csl_entry['DOI'] = str(bib_entry['doi'])
    if 'url' in bib_entry and bib_entry['url']:
        csl_entry['URL'] = str(bib_entry['url'])
    
    return csl_entry

def format_with_csl(bib_entry, csl_file_path='apa-cv.csl'):
    """Format a BibTeX entry using CSL style"""
    try:
        # Convert BibTeX to CSL format
        csl_entry = convert_bibtex_to_csl(bib_entry)
        
        # Create CSL JSON source - CiteProcJSON expects a list of items
        csl_data = [csl_entry]
        
        # Load CSL style
        style = CitationStylesStyle(csl_file_path, validate=False)
        
        # Create bibliography source - pass the data directly, not as JSON string
        bib_source = CiteProcJSON(csl_data)
        
        # Create bibliography formatter
        bibliography = CitationStylesBibliography(style, bib_source)
        
        # Add citation
        citation = Citation([CitationItem(csl_entry['id'])])
        bibliography.register(citation)
        
        # Render bibliography
        for item in bibliography.bibliography():
            formatted = str(item)
            # Clean up HTML entities and LaTeX formatting
            formatted = clean_csl_output(formatted)
            return formatted
            
    except Exception as e:
        print(f"Error formatting with CSL: {e}")
        return None

def clean_csl_output(text):
    """Clean up CSL output by removing HTML entities and LaTeX formatting"""
    import re
    
    # Replace HTML entities
    text = text.replace('&amp;', '&')
    text = text.replace('&lt;', '<')
    text = text.replace('&gt;', '>')
    text = text.replace('&quot;', '"')
    text = text.replace('&#39;', "'")
    
    # Remove LaTeX curly braces around single words (but preserve them for multi-word phrases)
    # This regex matches {word} but not {multiple words}
    text = re.sub(r'\{([A-Za-z]+)\}', r'\1', text)
    
    # Clean up any remaining formatting issues
    text = text.replace('  ', ' ')  # Remove double spaces
    text = text.strip()
    
    return text

def convert_author_names(authors_list):
    """Convert plain text author names to author profile references"""
    if not authors_list:
        return authors_list
    
    # Convert "Han Zhang" to "admin" for author highlighting
    return ["admin" if author.strip() == "Han Zhang" else author for author in authors_list]

def write_publication_file(data, body, index_file):
    """Write publication data back to markdown file"""
    new_front_matter = yaml.dump(data, default_flow_style=False, allow_unicode=True)
    new_content = f"---\n{new_front_matter}---{body}"
    
    with open(index_file, 'w', encoding='utf-8') as f:
        f.write(new_content)

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
    
    # Create subdirectories for different publication types
    type_dirs = {
        'article-journal': 'journal-articles',
        'preprint': 'preprints'
    }
    
    for type_dir in type_dirs.values():
        type_path = pub_dir / type_dir
        type_path.mkdir(exist_ok=True)
    
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
                                    # Format using CSL (if CSL file exists)
                                    if os.path.exists('apa-cv.csl'):
                                        try:
                                            csl_formatted = format_with_csl(matching_entry)
                                            if csl_formatted:
                                                data['publication'] = csl_formatted
                                                # Clear authors and title fields since CSL formatting includes both
                                                if 'authors' in data:
                                                    del data['authors']
                                                if 'title' in data:
                                                    del data['title']
                                                print(f"CSL formatted: {pub_folder.name}")
                                            else:
                                                print(f"CSL formatting returned empty for: {pub_folder.name}")
                                        except Exception as e:
                                            print(f"CSL formatting failed for {pub_folder.name}: {e}")
                                    else:
                                        print(f"CSL file not found, skipping formatting for: {pub_folder.name}")
                                    
                                    # Only convert author names if we don't have CSL formatting
                                    if 'authors' in data:
                                        data['authors'] = convert_author_names(data['authors'])
                                     
                                    # Write back the file
                                    write_publication_file(data, body, index_file)
                                     
                                    enhanced_count += 1
                                    print(f"Enhanced: {pub_folder.name}")
                                else:
                                    # Even if no matching BibTeX entry, still convert author names
                                    if 'authors' in data:
                                        data['authors'] = convert_author_names(data['authors'])
                                        write_publication_file(data, body, index_file)
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
