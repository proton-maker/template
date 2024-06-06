from bs4 import BeautifulSoup
import re

# Fungsi untuk memfilter aturan CSS berdasarkan kelas dan ID yang digunakan di index.html
def filter_css(css_content, classes, ids):
    filtered_css = []
    inside_rule = False
    current_rule = []
    add_rule = False

    for line in css_content.splitlines():
        if '{' in line:
            inside_rule = True
            current_rule.append(line)
            # Periksa apakah aturan mengandung salah satu kelas atau ID
            if any(f'.{cls}' in line for cls in classes) or any(f'#{id_}' in line for id_ in ids):
                add_rule = True
        elif '}' in line:
            current_rule.append(line)
            inside_rule = False
            if add_rule:
                filtered_css.extend(current_rule)
                filtered_css.append('\n')  # Tambahkan spasi antara aturan untuk kejelasan
            current_rule = []
            add_rule = False
        elif inside_rule:
            current_rule.append(line)

    return '\n'.join(filtered_css)

# Fungsi untuk validasi dan perbaikan otomatis CSS
def validate_and_fix_css(css_content):
    errors = []
    fixed_lines = []
    lines = css_content.splitlines()
    inside_rule = False

    for i, line in enumerate(lines):
        # Simple validation for hex color
        hex_colors = re.findall(r'#[0-9a-fA-F]{3,6}', line)
        for color in hex_colors:
            if len(color) not in [4, 7]:
                errors.append(f"Invalid hex color '{color}' on line {i + 1}")

        # Detect rule start and end
        if '{' in line:
            inside_rule = True
        if '}' in line:
            inside_rule = False

        # Validate CSS property and add missing semicolon
        if inside_rule and ':' in line and ';' not in line and not line.strip().endswith('}') and not line.strip().startswith('@'):
            fixed_lines.append(line + ';')
            errors.append(f"Missing semicolon in line {i + 1}: {line}")
        else:
            fixed_lines.append(line)

    return '\n'.join(fixed_lines), errors

# Load index.html content
index_file_path = 'C:/Users/rizky/Downloads/sky/index.html'
with open(index_file_path, 'r', encoding='utf-8') as file:
    index_content = file.read()

# Parse index.html content using BeautifulSoup
soup = BeautifulSoup(index_content, 'html.parser')

# Extract all class and id names used in index.html
classes = set()
ids = set()

for element in soup.find_all(class_=True):
    classes.update(element['class'])

for element in soup.find_all(id=True):
    ids.add(element['id'])

# Load combined.css content
combined_css_file_path = 'C:/Users/rizky/Downloads/sky/combined.css'
with open(combined_css_file_path, 'r', encoding='utf-8') as file:
    combined_css_content = file.read()

# Filter CSS rules based on usage in index.html
filtered_css_content = filter_css(combined_css_content, classes, ids)

# Validate and fix filtered CSS
fixed_css_content, css_errors = validate_and_fix_css(filtered_css_content)

# Path for the error log file
error_log_file_path = 'C:/Users/rizky/Downloads/sky/css_errors.log'

if css_errors:
    # Write error messages to the log file
    with open(error_log_file_path, 'w', encoding='utf-8') as log_file:
        for error in css_errors:
            log_file.write(error + '\n')
    print(f"Errors found and fixed where possible. Check the log file at {error_log_file_path} for details.")

# Write the filtered and fixed CSS content to a new file
filtered_css_file_path = 'C:/Users/rizky/Downloads/sky/filtered_combined.css'
with open(filtered_css_file_path, 'w', encoding='utf-8') as file:
    file.write(fixed_css_content)

print(f"Filtered and fixed CSS content has been written to {filtered_css_file_path}")
