from cliColors import info, success, warning, error, prompt
from colorama import Fore, Style

def fetch_project_keys(session, sonar_url):
    info("Fetching project keys from SonarQube...")
    project_keys = []
    page = 1

    while True:
        params = {'p': page, 'ps': 100}
        response = session.get(f"{sonar_url}/api/projects/search", params=params)
        response.raise_for_status()
        data = response.json()

        for project in data.get("components", []):
            project_keys.append({"name": project.get("name"), "key": project.get("key")})

        if page * 100 >= data["paging"]["total"]:
            break
        page += 1

    success(f"Found {len(project_keys)} projects.")
    return project_keys

def choose_project_key(session, sonar_url):
    projects = fetch_project_keys(session, sonar_url)
    if not projects:
        error("No projects found.")
        raise Exception("No projects available.")

    print("\nAvailable Projects:")
    for i, proj in enumerate(projects, 1):
        print(f"  {Fore.YELLOW}{i}. {proj['name']} ({proj['key']}){Style.RESET_ALL}")

    while True:
        choice = prompt("Select a project by number:")
        if choice.isdigit():
            index = int(choice)
            if 1 <= index <= len(projects):
                return projects[index - 1]['key']
        warning("Invalid selection. Please try again.")
