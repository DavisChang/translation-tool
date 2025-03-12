import json
import os
import re

def escape_android_string(value):
    """Escapes special characters for Android XML strings."""
    return (value.replace("'", "\\'")  # Escape single quotes
                 .replace("&", "&amp;") # Escape ampersands
                 .replace("<", "&lt;")  # Escape <
                 .replace(">", "&gt;")  # Escape >
                 .replace('"', "&quot;")) # Escape double quotes

def convert_web_placeholders(value):
    """Converts {name} to {{name}} for Web compatibility (Vue, React, Angular)."""
    return re.sub(r'\{(\w+)\}', r'{{\1}}', value)

def convert_android_placeholders(value):
    """Converts {name} to %1$s for Android XML compatibility."""
    placeholders = re.findall(r'\{(\w+)\}', value)
    for index, placeholder in enumerate(placeholders):
        value = value.replace(f"{{{placeholder}}}", f"%{index + 1}$s")
    return value

def convert_windows_placeholders(value):
    """Converts {name} to {0} for Windows RESX compatibility."""
    placeholders = re.findall(r'\{(\w+)\}', value)
    for index, placeholder in enumerate(placeholders):
        value = value.replace(f"{{{placeholder}}}", f"{{{index}}}")
    return value

def json_to_android(xml_path, json_path):
    """Converts JSON to Android XML format."""
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    xml_content = '<?xml version="1.0" encoding="utf-8"?>\n<resources>\n'

    def process_object(obj, parent_key=""):
        for key, value in obj.items():
            full_key = f"{parent_key}_{key}" if parent_key else key
            if isinstance(value, dict):
                process_object(value, full_key)  # Recursively process nested objects
            else:
                formatted_value = escape_android_string(str(value))
                formatted_value = convert_android_placeholders(formatted_value)  # Convert placeholders
                xml_content_list.append(f'    <string name="{full_key}">{formatted_value}</string>\n')

    xml_content_list = []
    process_object(data)
    
    xml_content += "".join(xml_content_list) + "</resources>\n"
    
    with open(xml_path, "w", encoding="utf-8") as f:
        f.write(xml_content)

    print(f"✅ Successfully generated Android XML: {xml_path}")

def json_to_resx(resx_path, json_path):
    """Converts JSON to Windows RESX format."""
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    resx_content = '<?xml version="1.0" encoding="utf-8"?>\n<root>\n'

    def process_object(obj, parent_key=""):
        for key, value in obj.items():
            full_key = f"{parent_key}_{key}" if parent_key else key
            if isinstance(value, dict):
                process_object(value, full_key)  # Recursively process nested objects
            else:
                formatted_value = convert_windows_placeholders(str(value))  # Convert placeholders
                resx_content_list.append(f'    <data name="{full_key}" xml:space="preserve">\n')
                resx_content_list.append(f'        <value>{formatted_value}</value>\n')
                resx_content_list.append('    </data>\n')

    resx_content_list = []
    process_object(data)
    
    resx_content += "".join(resx_content_list) + "</root>\n"
    
    with open(resx_path, "w", encoding="utf-8") as f:
        f.write(resx_content)

    print(f"✅ Successfully generated Windows RESX: {resx_path}")

def json_to_web_dict(web_path, json_path):
    """Converts JSON to a Web-friendly dictionary file with dot-separated keys."""
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    def flatten_dict(d, parent_key=""):
        items = {}
        for key, value in d.items():
            new_key = f"{parent_key}.{key}" if parent_key else key
            if isinstance(value, dict):
                items.update(flatten_dict(value, new_key))  # Recursively flatten nested objects
            else:
                formatted_value = convert_web_placeholders(str(value))  # Convert placeholders
                items[new_key] = formatted_value
        return items

    flat_dict = flatten_dict(data)
    
    # Sort keys alphabetically
    sorted_dict = {k: flat_dict[k] for k in sorted(flat_dict)}

    with open(web_path, "w", encoding="utf-8") as f:
        json.dump(sorted_dict, f, indent=2, ensure_ascii=False)

    print(f"✅ Successfully generated Web dictionary: {web_path}")

# Process translations for all languages
languages = ["en", "zh"]
for lang in languages:
    json_to_android(f"locales/android/strings_{lang}.xml", f"locales/{lang}.json")
    json_to_resx(f"locales/windows/resx_{lang}.resx", f"locales/{lang}.json")
    json_to_web_dict(f"locales/web/{lang}_web.json", f"locales/{lang}.json")
