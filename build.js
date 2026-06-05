```javascript
const fs = require('fs');
const path = require('path');
const { marked } = require('marked');

// --- Configuration ---
const ROOT_DIR = __dirname;
const OUT_DIR = path.join(ROOT_DIR, 'site');
const OUT_FILE = path.join(OUT_DIR, 'index.html');

// Directories to ignore when scanning for markdown files
const EXCLUDE_DIRS = new Set(['node_modules', 'site', '.git', '.github']);

// --- File Discovery ---
function findMarkdownFiles(dir, fileList = []) {
    const items = fs.readdirSync(dir, { withFileTypes: true });
    
    for (const item of items) {
        const fullPath = path.join(dir, item.name);
        
        if (item.isDirectory()) {
            // Recursively search allowed directories
            if (!EXCLUDE_DIRS.has(item.name) && !item.name.startsWith('.')) {
                findMarkdownFiles(fullPath, fileList);
            }
        } else if (item.isFile() && item.name.startsWith('_') && item.name.endsWith('.md')) {
            // Find files like _FolderName.md
            fileList.push(fullPath);
        }
    }
    
    return fileList;
}

// --- Content Processing ---
function processFiles(files) {
    const sections = [];
    
    for (const file of files) {
        const content = fs.readFileSync(file, 'utf-8');
        
        // Convert Markdown to HTML
        const htmlContent = marked.parse(content);
        
        // Extract a clean name for the ID and Title
        // Example: _10_QiAccess.md -> 10_QiAccess -> 10 QiAccess
        const fileName = path.basename(file, '.md');
        const cleanName = fileName.replace(/^_+/, ''); // Remove leading underscore
        const title = cleanName.replace(/_/g, ' ');    // Replace remaining underscores with spaces
        const id = cleanName.toLowerCase().replace(/[^a-z0-9]+/g, '-'); // Create URL-safe ID

        sections.push({
            id,
            title,
            htmlContent,
            sourceFile: file,
            originalName: cleanName // Used for sorting
        });
    }
    
    // Sort sections alphabetically by their original name (ensures 10_ comes before 20_)
    sections.sort((a, b) => a.originalName.localeCompare(b.originalName));
    
    return sections;
}

// --- HTML Generation ---
function generateHTML(sections) {
    // Generate Navigation Links
    const navLinks = sections.map(section => 
        `<li><a href="#${section.id}">${section.title}</a></li>`
    ).join('\n');

    // Generate Content Sections
    const contentSections = sections.map(section => `
        <section id="${section.id}" class="doc-section">
            ${section.htmlContent}
        </section>
    `).join('\n');

    // Complete HTML5 Template with embedded CSS
    return `<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Documentation</title>
    <style>
        :root {
            --bg-color: #ffffff;
            --text-main: #334155;
            --text-heading: #0f172a;
            --sidebar-bg: #f8fafc;
            --sidebar-border: #e2e8f0;
            --accent: #2563eb;
            --accent-hover: #1d4ed8;
            --code-bg: #f1f5f9;
        }

        * { box-sizing: border-box; }

        html { 
            scroll-behavior: smooth; 
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        }

        body {
            margin: 0;
            padding: 0;
            display: flex;
            color: var(--text-main);
            background-color: var(--bg-color);
            line-height: 1.6;
        }

        /* Sidebar Navigation */
        nav {
            width: 280px;
            height: 100vh;
            position: fixed;
            top: 0;
            left: 0;
            background-color: var(--sidebar-bg);
            border-right: 1px solid var(--sidebar-border);
            overflow-y: auto;
            padding: 2rem 1.5rem;
        }

        nav h1 {
            font-size: 1.25rem;
            color: var(--text-heading);
            margin-top: 0;
            margin-bottom: 1.5rem;
            padding-bottom: 1rem;
            border-bottom: 1px solid var(--sidebar-border);
        }

        nav ul {
            list-style: none;
            padding: 0;
            margin: 0;
        }

        nav li {
            margin-bottom: 0.5rem;
        }

        nav a {
            text-decoration: none;
            color: var(--text-main);
            font-size: 0.95rem;
            display: block;
            padding: 0.4rem 0.5rem;
            border-radius: 4px;
            transition: all 0.2s;
        }

        nav a:hover {
            background-color: #e2e8f0;
            color: var(--accent);
        }

        /* Main Content Area */
        main {
            margin-left: 280px;
            padding: 3rem 4rem;
            width: 100%;
            max-width: 900px;
        }

        .doc-section {
            margin-bottom: 4rem;
            padding-bottom: 2rem;
            border-bottom: 1px solid var(--sidebar-border);
            scroll-margin-top: 2rem; /* Offsets anchor jumps so headers aren't stuck at the top edge */
        }

        .doc-section:last-child {
            border-bottom: none;
        }

        /* Typography & Markdown Styling */
        h1, h2, h3, h4 {
            color: var(--text-heading);
            margin-top: 2rem;
            margin-bottom: 1rem;
            font-weight: 600;
            line-height: 1.25;
        }

        h1 { font-size: 2.25rem; }
        h2 { font-size: 1.5rem; border-bottom: 1px solid var(--sidebar-border); padding-bottom: 0.5rem; }
        h3 { font-size: 1.25rem; }

        a { color: var(--accent); text-decoration: none; }
        a:hover { text-decoration: underline; }

        code {
            background-color: var(--code-bg);
            padding: 0.2em 0.4em;
            border-radius: 3px;
            font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
            font-size: 0.9em;
        }

        pre {
            background-color: var(--code-bg);
            padding: 1.25rem;
            border-radius: 6px;
            overflow-x: auto;
        }

        pre code {
            background-color: transparent;
            padding: 0;
        }

        blockquote {
            border-left: 4px solid var(--sidebar-border);
            margin: 0;
            padding-left: 1rem;
            color: #64748b;
        }

        table {
            width: 100%;
            border-collapse: collapse;
            margin: 1.5rem 0;
        }
        
        th, td {
            border: 1px solid var(--sidebar-border);
            padding: 0.75rem;
            text-align: left;
        }
        
        th { background-color: var(--sidebar-bg); }

        /* Mobile Responsiveness */
        @media (max-width: 768px) {
            body { flex-direction: column; }
            
            nav {
                width: 100%;
                height: auto;
                position: relative;
                border-right: none;
                border-bottom: 1px solid var(--sidebar-border);
                padding: 1.5rem;
            }

            main {
                margin-left: 0;
                padding: 1.5rem;
            }
        }
    </style>
</head>
<body>

    <nav>
        <h1>Documentation</h1>
        <ul>
            ${navLinks}
        </ul>
    </nav>

    <main>
        ${contentSections}
    </main>

</body>
</html>`;
}

// --- Main Execution ---
function build() {
    console.log('🚀 Starting documentation build...');
    
    // 1. Ensure output directory exists
    if (!fs.existsSync(OUT_DIR)) {
        fs.mkdirSync(OUT_DIR, { recursive: true });
    }

    // 2. Find files
    const mdFiles = findMarkdownFiles(ROOT_DIR);
    if (mdFiles.length === 0) {
        console.warn('⚠️ No markdown files matching "_*.md" were found.');
    } else {
        console.log(`📄 Found ${mdFiles.length} documentation files.`);
    }

    // 3. Process markdown into structured data
    const sections = processFiles(mdFiles);

    // 4. Generate final HTML
    const finalHtml = generateHTML(sections);

    // 5. Write to file
    fs.writeFileSync(OUT_FILE, finalHtml);
    console.log(`✅ Build complete! Site generated at: ${OUT_FILE}`);
}

build();

```
