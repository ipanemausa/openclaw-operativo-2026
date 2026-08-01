import urllib.request
import json
import re

# Inspect dist/assets/index-qW1DgnYA.js for syntax errors or broken imports
js_path = r"C:\openclaw\hb-jewelry\dist\assets\index-qW1DgnYA.js"
with open(js_path, "r", encoding="utf-8") as f:
    code = f.read()

print(f"JS Bundle Size: {len(code)} bytes")
# Check if there are any obvious undefined references or missing exports
undefined_matches = re.findall(r"(\w+)\s*is not defined", code)
print(f"Potential issues: {undefined_matches}")
