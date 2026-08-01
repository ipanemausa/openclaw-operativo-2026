import urllib.request
import re

url = "https://hb-jewelry-cloud-2026-2dff9.web.app/"
try:
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req) as resp:
        html = resp.read().decode('utf-8')
        print("HTML Status Code:", resp.status)
        print("HTML Snippet:", html[:500])
        
        # Extract JS bundle URL
        js_match = re.search(r'src="(/assets/[^"]+\.js)"', html)
        if js_match:
            js_url = "https://hb-jewelry-cloud-2026-2dff9.web.app" + js_match.group(1)
            print("Found JS Bundle URL:", js_url)
            req_js = urllib.request.Request(js_url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req_js) as js_resp:
                js_content = js_resp.read().decode('utf-8')
                print("JS Status Code:", js_resp.status)
                print("JS Size:", len(js_content), "bytes")
                print("JS Starts with:", js_content[:200])
except Exception as e:
    print("Error fetching URL:", e)
