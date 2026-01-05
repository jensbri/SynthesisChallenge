import json
import os
from markdownify import markdownify as md

INPUT_FILE = "input/chat_history.txt"
OUTPUT_FILE = "docs/chat_history_formatted.md"

def format_chat():
    print(f"Reading {INPUT_FILE}...")
    
    # Read the file content
    with open(INPUT_FILE, 'r') as f:
        content = f.read()
    
    # The file might be a list of JSON objects, or a JSON array. 
    # The file content seems to be a sequence of objects separated by commas, e.g. {...}, {...}
    # This is not valid JSON on its own. We need to wrap it in [ ... ]
    try:
        data = json.loads(content)
    except json.JSONDecodeError:
        print("Standard JSON parse failed. Trying to wrap in [...]...")
        try:
            # Wrap in brackets
            wrapped_content = f"[{content}]"
            data = json.loads(wrapped_content)
        except json.JSONDecodeError as e:
            print(f"Wrapped JSON parse failed: {e}")
            # The file might end with incomplete data like "},{". 
            # We should try to trim to the last closing brace '}'.
            last_brace_index = content.rfind('}')
            if last_brace_index != -1:
                print("Trimming content to last closing brace '}'...")
                trimmed_content = content[:last_brace_index+1]
                wrapped_content = f"[{trimmed_content}]"
                try:
                    data = json.loads(wrapped_content)
                except json.JSONDecodeError as e2:
                    print(f"Trimmed JSON parse failed: {e2}")
                    raise e
            else:
                raise

    # The export seems to be in reverse chronological order (newest first)?
    # "time": "2026-01-02T08:26:45.359Z" (first item)
    # "time": "2026-01-01T19:48:23.508Z" (last item)
    # So we should reverse it to make it read like a chat.
    data.sort(key=lambda x: x.get('time', ''))

    markdown_output = "# Gemini Chat History\n\n"
    markdown_output += "> **Note**: This chat history was automatically formatted from a JSON export.\n\n"

    for turn in data:
        # Extract User Prompt
        title = turn.get('title', '')
        if title.startswith("Prompted "):
            user_text = title[9:] # Remove "Prompted "
        else:
            user_text = title
        
        # Extract Model Response
        # usually in safeHtmlItem[0]['html']
        model_html = ""
        if 'safeHtmlItem' in turn and len(turn['safeHtmlItem']) > 0:
            model_html = turn['safeHtmlItem'][0].get('html', '')
        
        # Convert HTML to Markdown
        model_markdown = md(model_html, heading_style="ATX")
        
        # Clean up some common conversion artifacts if needed
        model_markdown = model_markdown.replace("\n\n\n", "\n\n")

        # Append to output
        markdown_output += f"## User\n{user_text}\n\n"
        markdown_output += f"## Gemini\n{model_markdown}\n\n"
        markdown_output += "---\n\n"

    # Write to file
    with open(OUTPUT_FILE, 'w') as f:
        f.write(markdown_output)
    
    print(f"Successfully formatted chat to {OUTPUT_FILE}")

if __name__ == "__main__":
    format_chat()
