# Operations Runbook: Build Local Site

This document outlines how to execute the static site compiler.

## Prerequisites
Ensure the virtual environment is active or invoke python directly from the `.venv`:
```powershell
# Path to environment python
c:\QiLabs\.venv\Scripts\python.exe
```

## Running the Build

### Standard Dry Run/Verify:
```powershell
c:\QiLabs\.venv\Scripts\python.exe C:\QiLabs\10_QiSpark\build_site.py
```

### Compile Including Active Files (Dev Mode):
```powershell
c:\QiLabs\.venv\Scripts\python.exe C:\QiLabs\10_QiSpark\build_site.py --allow-active
```

### Override Output Path:
```powershell
c:\QiLabs\.venv\Scripts\python.exe C:\QiLabs\10_QiSpark\build_site.py --dist C:\QiLabs\10_QiSpark\10_site_preview
```
