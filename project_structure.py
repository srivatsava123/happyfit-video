import os

# Folders to ignore
IGNORE = {'venv', '__pycache__', 'static', 'media', 'migrations', '.git', '.idea', '.vscode', 'node_modules'}

def print_tree(start_path='.', prefix='', depth=0, max_depth=3):
    if depth > max_depth:
        return
    items = sorted(os.listdir(start_path))
    for item in items:
        if item in IGNORE or item.endswith('.pyc'):
            continue
        path = os.path.join(start_path, item)
        print(f"{prefix}|-- {item}")
        if os.path.isdir(path):
            print_tree(path, prefix + '    ', depth + 1, max_depth)

print("📁 Project Structure:\n")
print_tree('.')
