#!/usr/bin/env python3
"""
Filter ICS file to include only dates and titles.
Reads an ICS file and generates a new one with only DTSTART, DTEND, and SUMMARY fields.
"""

import sys
import re

def filter_ics(input_file, output_file):
    """
    Filter ICS file to include only essential calendar structure and dates/titles.
    
    Args:
        input_file: Path to input ICS file
        output_file: Path to output ICS file
    """
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    lines = content.split('\n')
    filtered_lines = []
    in_vevent = False
    current_event = []
    keep_continuation = False
    
    for line in lines:
        # Always keep VCALENDAR structure
        if line.startswith('BEGIN:VCALENDAR'):
            filtered_lines.append(line)
        elif line.startswith('PRODID:'):
            filtered_lines.append(line)
        elif line.startswith('VERSION:'):
            filtered_lines.append(line)
        elif line.startswith('CALSCALE:'):
            filtered_lines.append(line)
        elif line.startswith('METHOD:'):
            filtered_lines.append(line)
        elif line.startswith('X-WR-CALNAME:'):
            filtered_lines.append(line)
        elif line.startswith('X-WR-TIMEZONE:'):
            filtered_lines.append(line)
        elif line.startswith('BEGIN:VEVENT'):
            in_vevent = True
            current_event = [line]
            keep_continuation = False
        elif line.startswith('END:VEVENT'):
            current_event.append(line)
            # Add the complete event to filtered lines
            filtered_lines.extend(current_event)
            current_event = []
            in_vevent = False
            keep_continuation = False
        elif in_vevent:
            # Check if this is a continuation line (starts with space)
            if line.startswith(' '):
                if keep_continuation:
                    current_event.append(line)
            else:
                # This is a new field line
                if (line.startswith('UID:') or 
                    line.startswith('DTSTART') or 
                    line.startswith('DTEND') or 
                    line.startswith('SUMMARY:')):
                    current_event.append(line)
                    keep_continuation = True
                else:
                    keep_continuation = False
        elif line.startswith('END:VCALENDAR'):
            filtered_lines.append(line)
    
    # Write filtered content
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(filtered_lines))

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: filter_ics.py <input_file> <output_file>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    filter_ics(input_file, output_file)
    print(f"Filtered ICS file created: {output_file}")
