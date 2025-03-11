import json
import os

def escape_android_string(value):
    """Escapes special characters for Android XML strings."""
    return (value.replace("'", "\\'")  # Escape single quotes
                 .replace("&", "&amp;") # Escape ampersands
                 .replace("<", "&lt;")  # Escape <
                 .replace(">", "&gt;")  # Escape >
                 .replace('"', "&quot;")) # Escape double quotes

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
                escaped_value = escape_android_string(str(value))
                xml_content_list.append(f'    <string name="{full_key}">{escaped_value}</string>\n')

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
                resx_content_list.append(f'    <data name="{full_key}" xml:space="preserve">\n')
                resx_content_list.append(f'        <value>{value}</value>\n')
                resx_content_list.append('    </data>\n')

    resx_content_list = []
    process_object(data)
    
    resx_content += "".join(resx_content_list) + "</root>\n"
    
    with open(resx_path, "w", encoding="utf-8") as f:
        f.write(resx_content)

    print(f"✅ Successfully generated Windows RESX: {resx_path}")

# Process translations for all languages
languages = ["en", "zh"]
for lang in languages:
    json_to_android(f"locales/android/strings_{lang}.xml", f"locales/{lang}.json")
    json_to_resx(f"locales/windows/resx_{lang}.resx", f"locales/{lang}.json")
