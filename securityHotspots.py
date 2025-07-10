import re
from cliColors import info, success, warning, error, prompt

def fetch_security_hotspots(session, projectKey, sonar_url):
    info(f"Fetching security hotspots for project '{projectKey}'...")
    url = f"{sonar_url}/api/hotspots/search"
    page = 1
    hotspots = []

    while True:
        params = {"projectKey": projectKey, "ps": 500, "p": page}
        response = session.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        for h in data["hotspots"]:
            hotspots.append({
                "Vulnerability Name": h.get("message"),
                "File": h.get("component"),
                "Line": h.get("line")
            })

        if page * 500 >= data["paging"]["total"]:
            break
        page += 1

    success(f"Retrieved {len(hotspots)} security hotspots.")
    return hotspots


def fetch_security_hotspots_full(session, projectKey, sonar_url):
    url = f"{sonar_url}/api/hotspots/search"
    page = 1
    hotspots = []
    while True:
        params = {"projectKey": projectKey, "ps": 500, "p": page}
        response = session.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        for h in data["hotspots"]:
            from_line = 1 if h.get("line") < 11 else h.get("line") - 10
            to_line = h.get("line") + 10 
            lines_params = {"key": h.get("component"), "from": from_line, "to": to_line}
            lines_response = session.get(f"{sonar_url}/api/sources/lines", params=lines_params)
            hotspot_line = []
            for line in lines_response.json().get("sources"):
                # Remove only <span ...> and </span> tags, keep the inner code
                clean_code = re.sub(r'</?span.*?>', '', line.get("code"))
                hotspot_line.append(clean_code)
            hotspots.append({
                "Vulnerability Name": h.get("message"),
                "File": h.get("component"),
                "Line": h.get("line"),
                "Code Snippet": "\n".join(hotspot_line)
            })

        if page * 500 >= data["paging"]["total"]:
            break
        page += 1

    success(f"Retrieved {len(hotspots)} security hotspots.")
    return hotspots
