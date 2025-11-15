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

def get_project_tasks(project_id):
    """Get all tasks in a project"""
    url = f"{API_BASE}/project/{project_id}/data"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error getting project tasks: {response.text}")
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
        print(f"  + Added: {title}")
        return task.get('id')
    else:
        print(f"  X Failed: {title}")
        print(f"    Error: {response.text}")
        return None

# The project ID for Tivaleo (from the previous run)
TIVALEO_PROJECT_ID = "69176ea48f080c72d1c389d9"

# We'll need to find the Special Considerations parent task ID
# For now, we'll add these as standalone tasks and you can move them later
# Or we can try to get the task list through another method

print("Note: Adding missing tasks. If parent task info is unavailable,")
print("they will be added as regular tasks that you can organize manually.")
print()

# Try to get the parent task ID by creating a test query
# If it fails, we'll add tasks without parent
special_considerations_parent = None

# List of missing tasks from the failed section
# Adding prefix to make them easy to find and move under Special Considerations
missing_tasks = [
    '[Special Considerations] Build "Shop the Look" features',
    '[Special Considerations] Use product videos',
    '[Special Considerations] Set up easy returns/exchanges',
    '[Special Considerations] Create detailed size guides',
    '[Special Considerations] Provide material information',
    '[Special Considerations] Add styling suggestions',
    '[Special Considerations] Set up quick customer support',
    '[Special Considerations] Track best sellers',
    '[Special Considerations] Manage supplier relationships',
    '[Special Considerations] Plan restock schedules',
    '[Special Considerations] Do seasonal inventory planning',
    '[Special Considerations] Make trend-based buying decisions',
    '[Special Considerations] Research competitive pricing',
    '[Special Considerations] Create price tiers (Budget Rs 199-499, Mid-range Rs 500-999, Premium Rs 1000+)',
    '[Special Considerations] Create bundle deals',
    '[Special Considerations] Plan seasonal discounts',
    '[Special Considerations] Do regular market research',
    '[Special Considerations] Collect customer feedback',
    '[Special Considerations] Do seasonal trend analysis',
    '[Special Considerations] Do competitor analysis',
    '[Special Considerations] Maintain supplier relationships'
]

print(f"\nAdding {len(missing_tasks)} missing tasks...")
print("="*60)

added = 0
failed = 0

for task_title in missing_tasks:
    task_id = create_task(task_title, TIVALEO_PROJECT_ID, parent_id=special_considerations_parent)
    if task_id:
        added += 1
    else:
        failed += 1
    time.sleep(2)  # Much longer delay to avoid rate limiting

print("="*60)
print(f"\nResults:")
print(f"  Successfully added: {added}")
print(f"  Failed: {failed}")
print(f"  Total: {len(missing_tasks)}")
