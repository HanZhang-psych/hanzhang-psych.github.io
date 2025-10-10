import os
import yaml
from pathlib import Path

def convert_author_names(authors_list):
    """Convert author names to highlight Han Zhang with bold formatting or asterisk for shared authorship"""
    if not authors_list:
        return authors_list
    
    # Check if Han Zhang is the first author (for bold formatting)
    # or if there are multiple authors (for asterisk formatting)
    han_zhang_found = False
    first_author = False
    total_authors = len(authors_list)
    
    for i, author in enumerate(authors_list):
        if author.strip() == "Han Zhang":
            han_zhang_found = True
            first_author = (i == 0)
            break
    
    if not han_zhang_found:
        return authors_list
    
    # Convert author names
    converted_authors = []
    for i, author in enumerate(authors_list):
        if author.strip() == "Han Zhang":
            if first_author and total_authors == 1:
                # Single author - bold
                converted_authors.append("**Han Zhang**")
            elif first_author and total_authors > 1:
                # First author with co-authors - bold
                converted_authors.append("**Han Zhang**")
            else:
                # Co-author - add asterisk
                converted_authors.append("Han Zhang*")
        else:
            converted_authors.append(author)
    
    return converted_authors

def write_publication_file(data, body, index_file):
    """Write publication data back to markdown file"""
    new_front_matter = yaml.dump(data, default_flow_style=False, allow_unicode=True)
    new_content = f"---\n{new_front_matter}---{body}"
    
    with open(index_file, 'w', encoding='utf-8') as f:
        f.write(new_content)

def enhance_publication_files():
    """Enhance all publication markdown files with author highlighting"""
    pub_dir = Path('content/publication')
    if not pub_dir.exists():
        print("No publication directory found!")
        return
    
    enhanced_count = 0
    
    # Process all markdown files recursively
    for markdown_file in pub_dir.rglob('index.md'):
        try:
            # Read the markdown file
            with open(markdown_file, 'r', encoding='utf-8') as f:
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
                        
                        # Convert author names for highlighting
                        if 'authors' in data:
                            data['authors'] = convert_author_names(data['authors'])
                            
                            # Write back the file
                            write_publication_file(data, body, markdown_file)
                             
                            enhanced_count += 1
                            print(f"Enhanced authors: {markdown_file.parent.name}")
                        else:
                            print(f"No authors field found in: {markdown_file.parent.name}")
                    
                    except yaml.YAMLError as e:
                        print(f"YAML error in {markdown_file}: {e}")
        
        except Exception as e:
            print(f"Error processing {markdown_file}: {e}")
    
    print(f"Enhanced {enhanced_count} publications with author highlighting!")

if __name__ == "__main__":
    enhance_publication_files()