#!/usr/bin/env python3
"""
Extract and parse JSON from code files where bracket counting fails.

Usage:
    python3 extract-embedded-json.py <file> <search_pattern> <close_pattern>

Examples:
    python3 extract-embedded-json.py js/app.js '"reports":' '// === Estado ==='
    python3 extract-embedded-json.py code.py 'data = {' '# End'

Outputs parsed JSON to stdout.
"""
import sys
import json
import re

def find_matching_bracket(raw, open_char, close_char):
    """Find position of matching close_char, ignoring inside quoted strings."""
    depth = 1
    in_string = False
    escape = False
    for i, c in enumerate(raw):
        if escape:
            escape = False
            continue
        if c == '\\':
            escape = True
            continue
        if c == '"':
            in_string = not in_string
            continue
        if in_string:
            continue
        if c == open_char:
            depth += 1
        elif c == close_char:
            depth -= 1
            if depth == 0:
                return i
    return -1

def parse_individual_objects(raw):
    """Parse individual JSON objects from a string, skipping non-JSON content."""
    objects = []
    depth_obj = 0
    in_str = False
    esc = False
    obj_start = None

    for i, c in enumerate(raw):
        if esc:
            esc = False
            continue
        if c == '\\':
            esc = True
            continue
        if c == '"':
            in_str = not in_str
            continue
        if in_str:
            continue
        if c == '{':
            if depth_obj == 0:
                obj_start = i
            depth_obj += 1
        elif c == '}':
            depth_obj -= 1
            if depth_obj == 0 and obj_start is not None:
                obj_str = raw[obj_start:i+1]
                objects.append(obj_str)
                obj_start = None

    return objects

def main():
    if len(sys.argv) < 4:
        print("Usage: extract-embedded-json.py <file> <search_pattern> <close_pattern>")
        print("  search_pattern: text before the JSON array/object opening")
        print("  close_pattern: text after the JSON closing (used for regex boundary)")
        sys.exit(1)

    filepath = sys.argv[1]
    search_pattern = sys.argv[2]
    close_pattern = sys.argv[3]

    with open(filepath, 'r') as f:
        content = f.read()

    # Find search pattern
    search_pos = content.find(search_pattern)
    if search_pos == -1:
        print(f"Error: Could not find '{search_pattern}' in {filepath}")
        sys.exit(1)

    # Find opening bracket
    open_pos = content.find('[', search_pos)
    if open_pos == -1:
        print(f"Error: Could not find '[' after '{search_pattern}'")
        sys.exit(1)

    # Find close position using regex
    close_pos_match = re.search(close_pattern, content[search_pos:])
    if close_pos_match:
        close_pos = search_pos + close_pos_match.start()
    else:
        # Fallback: find matching bracket
        raw = content[open_pos + 1:]
        bracket_end = find_matching_bracket(raw, '[', ']')
        if bracket_end == -1:
            print("Error: Could not find matching ]")
            sys.exit(1)
        close_pos = open_pos + 1 + bracket_end

    # Extract array content
    array_raw = content[open_pos + 1:close_pos]

    # Try json.loads
    try:
        data = json.loads(array_raw)
        print(json.dumps(data, indent=2, ensure_ascii=False))
        sys.exit(0)
    except json.JSONDecodeError:
        pass

    # Try wrapping
    try:
        wrapped = '[' + array_raw + ']'
        data = json.loads(wrapped)
        print(json.dumps(data, indent=2, ensure_ascii=False))
        sys.exit(0)
    except json.JSONDecodeError:
        pass

    # Fallback: parse individual objects
    objects = parse_individual_objects(array_raw)
    parsed = []
    for obj_str in objects:
        try:
            obj = json.loads(obj_str)
            parsed.append(obj)
        except json.JSONDecodeError:
            continue

    if parsed:
        print(json.dumps(parsed, indent=2, ensure_ascii=False))
        print(f"\n# Parsed {len(parsed)}/{len(objects)} objects", file=sys.stderr)
        sys.exit(0)

    print("Error: Could not parse any JSON from file", file=sys.stderr)
    sys.exit(1)

if __name__ == '__main__':
    main()
