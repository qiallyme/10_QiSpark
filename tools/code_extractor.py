import os
from datetime import datetime

# PDF processing imports (with fallback if not installed)
try:
    from pdf2image import convert_from_path
    from pdf2image.exceptions import PDFInfoNotInstalledError
    PDF2IMAGE_AVAILABLE = True
except ImportError:
    PDF2IMAGE_AVAILABLE = False
    print("Warning: pdf2image not available. PDF to image conversion will be skipped.")
    print("Install with: pip install pdf2image")
    print("Also requires poppler: https://github.com/oschwartz10612/poppler-windows/releases/")

try:
    import pdfplumber
    PDFPLUMBER_AVAILABLE = True
except ImportError:
    PDFPLUMBER_AVAILABLE = False
    try:
        import PyPDF2
        PYPDF2_AVAILABLE = True
    except ImportError:
        PYPDF2_AVAILABLE = False
        print("Warning: Neither pdfplumber nor PyPDF2 available. PDF text extraction will be limited.")
        print("Install with: pip install pdfplumber (recommended) or pip install PyPDF2")

def should_ignore_directory(dir_name):
    """Check if directory should be ignored."""
    ignore_dirs = [
        'node_modules', 'dist', 'build', '.git', '$recycle.bin', 'tree-maker', '__pycache__',
        'venv', 'env', '.venv', '.env', 'virtualenv', 'envs',  # Python virtual environments
        'site-packages', '.pytest_cache', '.mypy_cache',  # Python caches
        'bower_components', '.sass-cache', '.cache',  # Frontend
        'target', 'out', 'bin', 'obj', '.idea', '.vscode',  # Build/IDE
        'lib', 'libs', 'library', 'libraries',  # Library directories
        'scripts', 'script', 'tools', 'utils', 'utilities',  # Script directories
        'vendor', 'packages',  # Package directories
    ]
    return dir_name.lower() in [d.lower() for d in ignore_dirs]

def is_pdf_file(file_name):
    """Check if file is a PDF."""
    return os.path.splitext(file_name)[1].lower() == '.pdf'

def is_text_file(file_name):
    """Check if file is a text file we want to extract."""
    # PDFs are handled separately - don't treat them as text files
    if is_pdf_file(file_name):
        return False
    
    # File extensions to explicitly exclude (binary/image files)
    binary_extensions = {
        '.ico', '.svg', '.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp',
        '.mp4', '.avi', '.mov', '.wmv', '.flv', '.webm', '.mkv',
        '.mp3', '.wav', '.flac', '.aac', '.ogg', '.wma',
        '.zip', '.rar', '.7z', '.tar', '.gz', '.bz2',
        '.exe', '.dll', '.so', '.dylib', '.bin',
        '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx',  # PDF removed - handled separately
        '.db', '.sqlite', '.sqlite3', '.mdb', '.accdb',
        '.log', '.tmp', '.temp', '.cache', '.lock',
        '.pyc', '.pyo', '.pyd', '.whl', '.egg'
    }
    
    # Files to explicitly ignore
    ignore_files = {
        'package-lock.json', 'yarn.lock', 'pnpm-lock.yaml',
        'composer.lock', 'Gemfile.lock', 'Pipfile.lock'
    }
    
    if file_name in ignore_files:
        return False
    
    # Check if it's a binary file
    ext = os.path.splitext(file_name)[1].lower()
    if ext in binary_extensions:
        return False
    
    # File extensions to include (text files only)
    text_extensions = {
        '.py', '.js', '.jsx', '.ts', '.tsx', '.html', '.css', '.scss', '.sass',
        '.json', '.xml', '.yaml', '.yml', '.md', '.txt', '.sh', '.bat', '.ps1',
        '.vue', '.php', '.java', '.cpp', '.c', '.h', '.hpp', '.cs', '.rb',
        '.go', '.rs', '.swift', '.kt', '.scala', '.r', '.sql', '.pl', '.lua',
        '.toml', '.ini', '.cfg', '.conf', '.env', '.gitignore'
    }
    
    # Check extension
    if ext in text_extensions:
        return True
    
    # Check for config files without extensions
    config_files = {
        'dockerfile', 'makefile', 'gemfile', 'procfile',
        'webpack.config.js', 'vite.config.js', 'rollup.config.js',
        'tsconfig.json', 'jsconfig.json', 'package.json'
    }
    return file_name.lower() in config_files

def print_directory_tree(root_dir, output_writer, script_path, output_base_dir, current_depth=0, prefix=''):
    """Print directory tree structure."""
    try:
        items = os.listdir(root_dir)
    except (PermissionError, FileNotFoundError):
        message = prefix + "└── [Access Denied]"
        print(message)
        output_writer.write(message + "\n")
        return

    # Get absolute paths for comparison
    script_path = os.path.abspath(script_path)
    output_base_dir_abs = os.path.abspath(output_base_dir) if output_base_dir else None

    # Filter and sort items
    directories = []
    files = []
    
    for item in items:
        if item.startswith('.'):
            continue
        
        # Skip output directories
        if item.startswith('code_extraction_'):
            continue
            
        path = os.path.join(root_dir, item)
        path_abs = os.path.abspath(path)
        
        # Skip script and output directories
        if path_abs == script_path:
            continue
        if output_base_dir_abs and path_abs.startswith(output_base_dir_abs):
            continue
            
        if os.path.isdir(path):
            if not should_ignore_directory(item):
                directories.append(item)
        else:
            # Include both text files and PDFs in the tree (but not the script itself)
            if path_abs != script_path and (is_text_file(item) or is_pdf_file(item)):
                files.append(item)
    
    # Sort alphabetically
    directories.sort(key=lambda s: s.lower())
    files.sort(key=lambda s: s.lower())
    items = directories + files

    for index, item in enumerate(items):
        path = os.path.join(root_dir, item)
        
        # Tree connector
        if index == len(items) - 1:
            connector = '└── '
            extension = '    '
        else:
            connector = '├── '
            extension = '│   '

        message = prefix + connector + item
        print(message)
        output_writer.write(message + "\n")

        # Recurse into directories
        if os.path.isdir(path):
            print_directory_tree(path, output_writer, script_path, output_base_dir, current_depth + 1, prefix + extension)

def is_binary_file(file_path):
    """Check if a file is binary by reading the first 1024 bytes."""
    try:
        with open(file_path, 'rb') as f:
            chunk = f.read(1024)
            if b'\0' in chunk:  # Null bytes indicate binary
                return True
            # Check for high ratio of non-printable characters
            try:
                chunk.decode('utf-8')
            except UnicodeDecodeError:
                return True
            return False
    except:
        return True  # If we can't read it, assume it's binary

def extract_pdf_text_pdfplumber(pdf_path):
    """Extract text from PDF using pdfplumber (best quality)."""
    text_content = []
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for i, page in enumerate(pdf.pages, 1):
                page_text = page.extract_text()
                if page_text:
                    text_content.append(f"## Page {i}\n\n{page_text}\n")
        return "\n".join(text_content)
    except Exception as e:
        return f"Error extracting text with pdfplumber: {str(e)}\n"

def extract_pdf_text_pypdf2(pdf_path):
    """Extract text from PDF using PyPDF2 (fallback)."""
    text_content = []
    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for i, page in enumerate(pdf_reader.pages, 1):
                try:
                    page_text = page.extract_text()
                    if page_text:
                        text_content.append(f"## Page {i}\n\n{page_text}\n")
                except Exception as e:
                    text_content.append(f"## Page {i}\n\n[Error extracting text: {str(e)}]\n")
        return "\n".join(text_content)
    except Exception as e:
        return f"Error extracting text with PyPDF2: {str(e)}\n"

def process_pdf(pdf_path, output_base_dir, root_dir):
    """Process PDF: extract text to .md file and convert pages to images."""
    pdf_name = os.path.splitext(os.path.basename(pdf_path))[0]
    
    # Preserve relative directory structure
    rel_path = os.path.relpath(pdf_path, root_dir)
    rel_dir = os.path.dirname(rel_path)
    
    # Create output directories preserving structure
    md_output_dir = os.path.join(output_base_dir, 'pdf_text_extracted')
    img_output_dir = os.path.join(output_base_dir, 'pdf_images')
    
    if rel_dir:
        md_output_dir = os.path.join(md_output_dir, rel_dir)
        img_output_dir = os.path.join(img_output_dir, rel_dir)
    
    os.makedirs(md_output_dir, exist_ok=True)
    os.makedirs(img_output_dir, exist_ok=True)
    
    # Extract text to .md file
    md_output_path = os.path.join(md_output_dir, f"{pdf_name}.md")
    
    text_content = ""
    if PDFPLUMBER_AVAILABLE:
        text_content = extract_pdf_text_pdfplumber(pdf_path)
    elif PYPDF2_AVAILABLE:
        text_content = extract_pdf_text_pypdf2(pdf_path)
    else:
        text_content = f"# PDF Text Extraction\n\n**Source:** {rel_path}\n\n*Note: PDF text extraction libraries not available. Install pdfplumber or PyPDF2.*\n"
    
    # Add header to markdown file
    markdown_content = f"""# {pdf_name}

**Source PDF:** `{rel_path}`
**Extracted:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

---

{text_content}
"""
    
    try:
        with open(md_output_path, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
        print(f"✓ Extracted PDF text to: {md_output_path}")
    except Exception as e:
        print(f"✗ Error writing PDF text: {md_output_path} - {str(e)}")
    
    # Convert PDF pages to images
    if PDF2IMAGE_AVAILABLE:
        try:
            images = convert_from_path(pdf_path, dpi=200)
            for i, image in enumerate(images, 1):
                img_output_path = os.path.join(img_output_dir, f"{pdf_name}_page_{i:03d}.png")
                image.save(img_output_path, 'PNG')
            print(f"✓ Converted PDF pages to images: {len(images)} pages in {img_output_dir}")
        except Exception as e:
            print(f"✗ Error converting PDF to images: {str(e)}")
    else:
        print(f"⚠ PDF to image conversion skipped (pdf2image not available)")
    
    return md_output_path

class ChunkedFileWriter:
    """Manages writing to multiple files, splitting at max_lines."""
    def __init__(self, base_path, max_lines=2000):
        self.base_path = base_path
        self.max_lines = max_lines
        self.current_file_num = 1
        self.current_line_count = 0
        self.current_file = None
        self.base_name = os.path.splitext(os.path.basename(base_path))[0]
        self.ext = os.path.splitext(base_path)[1]
        self.dir = os.path.dirname(base_path)
        self._open_new_file()
    
    def _open_new_file(self):
        """Close current file and open next chunk file."""
        if self.current_file:
            self.current_file.close()
        
        filename = f"{self.base_name}_part{self.current_file_num:03d}{self.ext}"
        filepath = os.path.join(self.dir, filename)
        self.current_file = open(filepath, 'w', encoding='utf-8')
        self.current_line_count = 0
        print(f"Opened new chunk file: {filename}")
        if self.current_file_num > 1:
            continuation_header = f"\n{'='*80}\nCONTINUATION FROM PREVIOUS FILE\n{'='*80}\n\n"
            self.write(continuation_header)
    
    def write(self, text):
        """Write text to current file, opening new file if needed."""
        if not self.current_file:
            self._open_new_file()
        
        # Split text into lines and write line by line to ensure we split at 2000 lines
        lines = text.split('\n')
        text_ends_with_newline = text.endswith('\n')
        
        for i, line in enumerate(lines):
            # Handle last line specially if text doesn't end with newline
            is_last_line = (i == len(lines) - 1)
            
            if is_last_line and not text_ends_with_newline:
                # Last line and text doesn't end with newline - write without adding newline
                if line or i == 0:  # Write if line has content or it's the only line
                    self.current_file.write(line)
                    self.current_line_count += 1
            else:
                # Write line with newline
                self.current_file.write(line + '\n')
                self.current_line_count += 1
            
            # Check if we need to switch files after this line
            if self.current_line_count >= self.max_lines:
                # Close current chunk and add continuation footer
                continuation_footer = f"\n{'='*80}\nFILE CONTINUES IN NEXT PART (part{self.current_file_num + 1:03d})\n{'='*80}\n"
                self.current_file.write(continuation_footer)
                self.current_file_num += 1
                self._open_new_file()
    
    def close(self):
        """Close current file."""
        if self.current_file:
            self.current_file.close()
            self.current_file = None
    
    def get_current_filepath(self):
        """Get path of current file."""
        filename = f"{self.base_name}_part{self.current_file_num:03d}{self.ext}"
        return os.path.join(self.dir, filename)

def extract_file_content(file_path, output_writer):
    """Extract and write file content."""
    try:
        # Double-check if file is binary before reading
        if is_binary_file(file_path):
            skip_msg = f"\n{'='*80}\nSKIPPED BINARY FILE: {file_path}\n{'='*80}\n\n"
            print(skip_msg)
            output_writer.write(skip_msg)
            return
        
        # File header
        header = f"\n{'='*80}\nFILE: {file_path}\n{'='*80}\n\n"
        print(header)
        output_writer.write(header)
        
        # Read and write content
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            print(content)
            output_writer.write(content)
            
        # File footer
        footer = f"\n\n{'='*80}\nEND: {file_path}\n{'='*80}\n\n"
        print(footer)
        output_writer.write(footer)
        
    except Exception as e:
        error_msg = f"\nERROR: {file_path} - {str(e)}\n"
        print(error_msg)
        output_writer.write(error_msg)

def walk_and_extract(root_dir, output_writer, output_base_dir, script_path):
    """Walk directories and extract text files in order. Process PDFs separately."""
    print(f"\n{'='*80}")
    print("EXTRACTING FILE CONTENTS")
    print(f"{'='*80}\n")
    output_writer.write(f"\n{'='*80}\nEXTRACTING FILE CONTENTS\n{'='*80}\n\n")
    
    file_count = 0
    pdf_count = 0
    
    # Get absolute paths for comparison
    script_path = os.path.abspath(script_path)
    output_base_dir_abs = os.path.abspath(output_base_dir)
    
    for root, dirs, files in os.walk(root_dir):
        # Filter directories - ignore script/library directories
        dirs[:] = [d for d in dirs if not should_ignore_directory(d) and not d.startswith('.')]
        
        # Ignore output directories
        dirs[:] = [d for d in dirs if not d.startswith('code_extraction_')]
        
        # Separate PDFs from text files
        text_files = []
        pdf_files = []
        
        for f in files:
            file_path = os.path.abspath(os.path.join(root, f))
            
            # Skip the script itself
            if file_path == script_path:
                continue
            
            # Skip files in output directory
            if file_path.startswith(output_base_dir_abs):
                continue
            
            if is_pdf_file(f):
                pdf_files.append(f)
            elif is_text_file(f):
                text_files.append(f)
        
        # Sort files
        text_files.sort(key=lambda s: s.lower())
        pdf_files.sort(key=lambda s: s.lower())
        
        # Process text files
        for file_name in text_files:
            file_path = os.path.join(root, file_name)
            extract_file_content(file_path, output_writer)
            file_count += 1
        
        # Process PDF files
        for file_name in pdf_files:
            file_path = os.path.join(root, file_name)
            print(f"\n{'='*80}")
            print(f"PROCESSING PDF: {file_path}")
            print(f"{'='*80}\n")
            output_writer.write(f"\n{'='*80}\nPDF FOUND: {file_path}\n{'='*80}\n")
            output_writer.write(f"Text extracted to .md file in pdf_text_extracted/ directory\n")
            output_writer.write(f"Images saved to pdf_images/ directory\n{'='*80}\n\n")
            
            try:
                md_path = process_pdf(file_path, output_base_dir, root_dir)
                output_writer.write(f"PDF text extracted to: {md_path}\n\n")
                pdf_count += 1
            except Exception as e:
                error_msg = f"ERROR processing PDF {file_path}: {str(e)}\n"
                print(error_msg)
                output_writer.write(error_msg)
    
    return file_count, pdf_count

def main():
    """Main function to run the code extraction."""
    # Get the directory where the script is located (not current working directory)
    script_path = os.path.abspath(__file__)
    root_dir = os.path.dirname(script_path)
    
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    
    # Create output directory structure
    output_base_dir = os.path.join(root_dir, f"code_extraction_{timestamp}")
    os.makedirs(output_base_dir, exist_ok=True)
    
    output_filename = os.path.join(output_base_dir, f"code_extraction_{timestamp}.txt")
    
    print(f"Script location: {script_path}")
    print(f"Extracting from: {root_dir}")
    print(f"Output directory: {output_base_dir}")
    print(f"Main output file: {output_filename} (will be split into chunks of 2000 lines)")
    print(f"PDF text will be saved to: {os.path.join(output_base_dir, 'pdf_text_extracted')}")
    print(f"PDF images will be saved to: {os.path.join(output_base_dir, 'pdf_images')}")
    print(f"Ignoring: node_modules, dist, build, .git, scripts, libs, venv, and output directories")
    print(f"Ignoring script itself: {os.path.basename(script_path)}")
    print(f"PDFs will be processed separately (text extracted to .md, pages converted to images)")
    print(f"{'='*80}\n")
    
    # Check for required libraries
    if not PDF2IMAGE_AVAILABLE:
        print("⚠ Warning: pdf2image not available - PDF to image conversion will be skipped")
    if not PDFPLUMBER_AVAILABLE and not PYPDF2_AVAILABLE:
        print("⚠ Warning: No PDF text extraction library available - install pdfplumber or PyPDF2")
    
    # Create chunked file writer
    output_writer = ChunkedFileWriter(output_filename, max_lines=2000)
    
    try:
        # Header
        header = f"CODE EXTRACTION - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        header += f"Script: {script_path}\n"
        header += f"Root: {root_dir}\n"
        header += f"Output Directory: {output_base_dir}\n"
        header += f"Output split into chunks of 2000 lines max\n"
        header += f"{'='*80}\n\n"
        print(header)
        output_writer.write(header)
        
        # Directory tree
        print("DIRECTORY TREE:")
        print("-" * 40)
        output_writer.write("DIRECTORY TREE:\n" + "-" * 40 + "\n")
        print_directory_tree(root_dir, output_writer, script_path, output_base_dir)
        
        # Extract files
        file_count, pdf_count = walk_and_extract(root_dir, output_writer, output_base_dir, script_path)
        
        # Footer
        footer = f"\n{'='*80}\nCOMPLETE\n"
        footer += f"Text files extracted: {file_count}\n"
        footer += f"PDFs processed: {pdf_count}\n"
        footer += f"Total output files created: {output_writer.current_file_num}\n"
        footer += f"{'='*80}\n"
        print(footer)
        output_writer.write(footer)
    finally:
        output_writer.close()
    
    print(f"\nDone!")
    print(f"Main output split into {output_writer.current_file_num} files:")
    for i in range(1, output_writer.current_file_num + 1):
        part_filename = f"{os.path.splitext(os.path.basename(output_filename))[0]}_part{i:03d}.txt"
        part_filepath = os.path.join(output_base_dir, part_filename)
        if os.path.exists(part_filepath):
            line_count = sum(1 for _ in open(part_filepath, 'r', encoding='utf-8'))
            print(f"  - {part_filename} ({line_count} lines)")
    print(f"PDF text files: {os.path.join(output_base_dir, 'pdf_text_extracted')}")
    print(f"PDF images: {os.path.join(output_base_dir, 'pdf_images')}")

if __name__ == "__main__":
    main()
