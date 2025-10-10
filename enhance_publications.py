import os
import yaml
from pathlib import Path

def convert_author_names(authors_list):
    """Convert 'Han Zhang' to 'admin' for Hugo Blox author highlighting"""
    if not authors_list:
        return authors_list
    
    # Convert author names
    converted_authors = []
    for author in authors_list:
        # Check for "Han Zhang" in various formats and convert to "admin"
        clean_author = author.strip().replace('**', '').replace('*', '').replace('<strong>', '').replace('</strong>', '')
        if clean_author == "Han Zhang":
            converted_authors.append("admin")
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