import requests
import json
import time

# Load the access token
with open("ticktick_token.json", "r") as f:
    token_data = json.load(f)

ACCESS_TOKEN = token_data["access_token"]

# TickTick API endpoint
API_BASE = "https://api.ticktick.com/open/v1"
headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Content-Type": "application/json"
}

def create_project(name):
    """Create a new project/list in TickTick"""
    url = f"{API_BASE}/project"
    data = {"name": name}
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        project = response.json()
        print(f"Created project: {name} (ID: {project['id']})")
        return project['id']
    else:
        print(f"Error creating project {name}: {response.text}")
        return None

def create_task(title, project_id, parent_id=None):
    """Create a task in TickTick"""
    url = f"{API_BASE}/task"
    data = {
        "title": title,
        "projectId": project_id
    }

    if parent_id:
        data["parentId"] = parent_id

    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        task = response.json()
        return task.get('id')
    else:
        print(f"Error creating task '{title}': {response.text}")
        return None

def parse_and_add_tasks(file_path, project_name):
    """Parse the task file and add tasks to TickTick with parent-child structure"""
    print(f"\n{'='*60}")
    print(f"Processing: {project_name}")
    print(f"{'='*60}")

    # Create project
    project_id = create_project(project_name)
    if not project_id:
        print(f"Failed to create project. Skipping {project_name}")
        return

    # Read the file
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    current_parent_task_id = None
    current_section = None
    tasks_added = 0
    subtasks_added = 0

    for line in lines:
        line = line.strip()

        # Skip empty lines
        if not line:
            continue

        # Skip the main title line
        if line.endswith("- Shopify Setup Tasks"):
            continue

        # Check if it's a phase header (single #)
        if line.startswith("# ") and not line.startswith("## "):
            # Phase headers are just printed, not added as tasks
            phase_name = line.replace("#", "").strip()
            print(f"\n{phase_name}")
            current_parent_task_id = None
            continue

        # Check if it's a section header (##)
        if line.startswith("## "):
            current_section = line.replace("##", "").strip()
            print(f"\n  Section: {current_section}")

            # Create parent task for this section
            parent_task_id = create_task(current_section, project_id, parent_id=None)
            if parent_task_id:
                current_parent_task_id = parent_task_id
                tasks_added += 1
                print(f"    + Created parent task: {current_section}")
                time.sleep(0.1)
            continue

        # Check if it's a subtask (starts with -)
        if line.startswith("-"):
            task_title = line[1:].strip()

            # Create subtask under current parent
            if current_parent_task_id:
                subtask_id = create_task(task_title, project_id, parent_id=current_parent_task_id)
                if subtask_id:
                    subtasks_added += 1
                    print(f"      - {task_title}")
                    time.sleep(0.1)
            else:
                # No parent, create as regular task
                task_id = create_task(task_title, project_id, parent_id=None)
                if task_id:
                    tasks_added += 1
                    print(f"    + {task_title}")
                    time.sleep(0.1)

    print(f"\n+ Total parent tasks added: {tasks_added}")
    print(f"+ Total subtasks added: {subtasks_added}")
    print(f"+ Grand total: {tasks_added + subtasks_added}")

# Main execution
print("Starting TickTick task import...")
print(f"Using access token: {ACCESS_TOKEN[:20]}...")

# Add Swadha Bangles tasks
parse_and_add_tasks(
    "swadha/shopify/ticktick_swadha_bangles.txt",
    "Shopify - Swadha Bangles"
)

# Add Tivaleo tasks
parse_and_add_tasks(
    "swadha/shopify/ticktick_tivaleo.txt",
    "Shopify - Tivaleo by Swadha"
)

print("\n" + "="*60)
print("All tasks imported successfully!")
print("="*60)
