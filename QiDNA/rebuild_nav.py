import os
import yaml
from pathlib import Path
import re

def clean_name(name):
    """Remove numeric prefixes like '00_' or '10_' and format the name cleanly."""
    # Remove prefix like "00_" or "10_"
    clean = re.sub(r'^\d+_', '', name)
    # Remove extensions if it's a file
    clean = re.sub(r'\.md$', '', clean)
    # Handle specific names
    clean = clean.replace('.workspace', '')
    # Convert underscores/hyphens to spaces and title case if it doesn't look camelCased
    if '_' in clean or '-' in clean:
        clean = clean.replace('_', ' ').replace('-', ' ').title()
    return clean

def build_nav(docs_dir="docs"):
    """Builds a navigation list based on the directories in docs."""
    docs_path = Path(docs_dir)
    nav = []
    
    # Always put Home first
    if (docs_path / "index.md").exists():
        nav.append({"Home": "index.md"})
    
    # Sort items based on their names to respect the 00_, 10_ prefixes
    items = sorted(docs_path.iterdir(), key=lambda x: x.name)
    
    for item in items:
        # Skip the root index.md as it's already added
        if item.name == "index.md":
            continue
            
        if item.is_dir():
            # Find the main index file for the directory
            index_file = None
            if (item / "index.md").exists():
                index_file = "index.md"
            elif (item / "_index.md").exists():
                index_file = "_index.md"
            elif (item / "README.md").exists():
                index_file = "README.md"
                
            if index_file:
                # Add the directory to nav
                display_name = clean_name(item.name)
                rel_path = f"{item.name}/{index_file}"
                nav.append({display_name: rel_path})
                
        elif item.is_file() and item.name.endswith(".md"):
            display_name = clean_name(item.name)
            nav.append({display_name: item.name})
            
    return nav

def update_mkdocs_yaml(yaml_path="mkdocs.yml"):
    """Update the nav section in mkdocs.yml."""
    if not os.path.exists(yaml_path):
        print(f"Error: {yaml_path} not found.")
        return

    with open(yaml_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    try:
        # Load the YAML safely preserving order where possible
        data = yaml.safe_load(content)
        
        # Generate new nav
        new_nav = build_nav()
        
        # Update nav
        data['nav'] = new_nav
        
        # Dump back to yaml
        yaml_output = yaml.dump(data, sort_keys=False, allow_unicode=True, default_flow_style=False)
        
        with open(yaml_path, 'w', encoding='utf-8') as f:
            f.write(yaml_output)
            
        print("Successfully rebuilt navigation indexes in mkdocs.yml!")
        
    except Exception as e:
        print(f"Error parsing mkdocs.yml: {e}")

if __name__ == "__main__":
    update_mkdocs_yaml()
