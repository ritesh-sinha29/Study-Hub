import re
import glob
import os

headers = [
    r'IMPORTANT RULE:',
    r'HOW IT WORKS:',
    r'HOW IT WORKS INTERNALLY:',
    r'WHY \*\*IMMUTABLE\*\*\?',
    r'WHY IMMUTABLE\?',
    r'WHAT IS [A-Z ]+\?',
    r'Rule \d+:',
    r'KEY INSIGHT:',
    r'WHY USE THEM\?',
    r'WHY ARE THESE IMPORTANT\?',
    r'HOW PYTHON [A-Z ]+:',
    r'HOW THEY DIFFER AT RUNTIME:',
    r'WHY LANGGRAPH USES [A-Za-z]+:',
    r'\.env FILE SECURITY:',
    r'BUFFERING:',
    r'STACKING ORDER:',
    r'PARAMETERIZED DECORATORS:',
    r'PROTOCOL DESIGN:',
    r'REAL-WORLD USE CASES:',
    r'Method \d+:?',
    r'Example \d+:?',
    r'PART \d+:?'
]

pattern_str = r'(?<!\*\*)([ \t]*)(' + '|'.join(headers) + r')'
pattern = re.compile(pattern_str)

def format_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    new_lines = []
    changed = False
    
    for i, line in enumerate(lines):
        # Remove [!IMPORTANT]
        if '# > [!IMPORTANT]\n' in line:
            changed = True
            continue # Just drop the line
            
        if not line.strip().startswith('#'):
            new_lines.append(line)
            continue
            
        match = pattern.search(line)
        if match:
            text_start = line.find('#') + 1
            text_part = line[text_start:]
            
            text_match = pattern.search(text_part)
            if text_match:
                prefix = text_part[:text_match.start()]
                header = text_match.group(2)
                suffix = text_part[text_match.end():]
                
                header_clean = header.replace('**', '')
                
                if prefix.strip():
                    new_lines.append('#' + prefix.rstrip() + '\n')
                    new_lines.append('#\n')
                    new_lines.append(f'# **{header_clean}**{suffix}')
                else:
                    if len(new_lines) > 0 and new_lines[-1].strip() != '#':
                        new_lines.append('#\n')
                    new_lines.append(f'# **{header_clean}**{suffix}')
                changed = True
                continue
                
        new_lines.append(line)
        
    if changed:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)

def main():
    # Execute formatting
    base_dir = os.path.join(os.path.dirname(__file__), '../src/content/learning/python')
    files = glob.glob(os.path.join(base_dir, '**/*.py'), recursive=True)
    
    # We will bold words like IMMUTABLE, NEVER, ALWAYS, BRAND NEW, FIRST-CLASS
    bold_words = [
        "IMMUTABLE", "BRAND NEW", "NEVER", "ALWAYS", "UNIQUE", "HASHABLE", "EVERYTHING", "FIRST", "AUTOMATICALLY", "SUPPRESSED", "FIRST-CLASS"
    ]
    
    for filepath in files:
        # First fix headers
        format_file(filepath)
        
        # Then bold specific important words
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        original_content = content
        for word in bold_words:
            # Only replace if not already bolded
            word_pattern = r'(?<!\*\*)(' + word + r')(?!\*\*)'
            content = re.sub(word_pattern, r'**\1**', content)
            
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
                
    print("Formatting applied to Python codebase successfully.")

if __name__ == '__main__':
    main()
