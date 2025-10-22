import json
import glob

# Find the notebook file in /content (where Colab stores the active notebook)
notebooks = glob.glob('/content/*.ipynb')

if notebooks:
    for notebook_path in notebooks:
        print(f"Checking: {notebook_path}")
        
        with open(notebook_path, 'r', encoding='utf-8') as f:
            nb = json.load(f)
        
        # Check if widgets metadata exists
        if 'metadata' in nb and 'widgets' in nb.get('metadata', {}):
            print(f"  → Fixing widget metadata...")
            del nb['metadata']['widgets']
            
            # Save the fixed version
            with open(notebook_path, 'w', encoding='utf-8') as f:
                json.dump(nb, f, indent=2)
            
            print(f"  ✓ Fixed! Now safe to save to GitHub")
        else:
            print(f"  ○ No widget issues")
else:
    print("No notebooks found in /content")
    print("Make sure you've saved your notebook first (Ctrl+S or Cmd+S)")
