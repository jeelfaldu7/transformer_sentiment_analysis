import json
import os

def fix_notebook_widgets(notebook_path=None):
    """Fix widget metadata in a single notebook or auto-detect current notebook"""
    
    # If no path provided, try to auto-detect the current notebook
    if notebook_path is None:
        try:
            # Try to get the notebook name from IPython
            from IPython import get_ipython
            ipython = get_ipython()
            
            # Check if running in Jupyter/Colab
            if ipython and hasattr(ipython, 'kernel'):
                # Try to get notebook name from various sources
                try:
                    import ipykernel
                    connection_file = ipykernel.get_connection_file()
                    kernel_id = connection_file.split('-', 1)[1].split('.')[0]
                    
                    # Look for notebook file
                    import glob
                    notebooks = glob.glob("*.ipynb")
                    
                    if len(notebooks) == 1:
                        notebook_path = notebooks[0]
                    else:
                        # Try multiple notebooks
                        for nb in notebooks:
                            try:
                                with open(nb, 'r', encoding='utf-8') as f:
                                    data = json.load(f)
                                    if 'metadata' in data and 'widgets' in data['metadata']:
                                        notebook_path = nb
                                        break
                            except:
                                continue
                except:
                    # Fallback: find all notebooks in directory
                    import glob
                    notebooks = glob.glob("*.ipynb")
                    if notebooks:
                        print(f"Found {len(notebooks)} notebook(s). Fixing all with widget issues...\n")
                        fixed_count = 0
                        for nb in notebooks:
                            if fix_single_notebook(nb):
                                fixed_count += 1
                        print(f"\n✓ Fixed {fixed_count} notebook(s)")
                        return fixed_count
        except:
            pass
    
    # If still no path, try to find notebooks in current directory
    if notebook_path is None:
        import glob
        notebooks = glob.glob("*.ipynb")
        
        if not notebooks:
            print("❌ No notebooks found in current directory")
            return 0
        
        print(f"Found {len(notebooks)} notebook(s). Fixing all with widget issues...\n")
        fixed_count = 0
        for nb in notebooks:
            if fix_single_notebook(nb):
                fixed_count += 1
        
        print(f"\n✓ Fixed {fixed_count} notebook(s)")
        return fixed_count
    
    # Fix the specified notebook
    return 1 if fix_single_notebook(notebook_path) else 0

def fix_single_notebook(notebook_path):
    """Fix widget metadata in a specific notebook file"""
    try:
        with open(notebook_path, 'r', encoding='utf-8') as f:
            notebook = json.load(f)
        
        if 'metadata' in notebook and 'widgets' in notebook['metadata']:
            print(f"Fixing {notebook_path}...")
            del notebook['metadata']['widgets']
            
            with open(notebook_path, 'w', encoding='utf-8') as f:
                json.dump(notebook, f, indent=2)
            
            print(f"  ✓ Fixed {notebook_path}")
            return True
        else:
            print(f"  ○ {notebook_path} - no widget metadata issues")
            return False
            
    except Exception as e:
        print(f"  ✗ Error fixing {notebook_path}: {e}")
        return False

# Auto-run when imported/executed
if __name__ == "__main__" or True:
    fix_notebook_widgets()