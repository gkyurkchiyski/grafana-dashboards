import requests
import json
import os

# Configuration
GRAFANA_URL = "http://localhost:3000"  # Replace with your Grafana URL
API_KEY = "YOUR_GRAFANA_API_KEY"       # Replace with your Grafana API key
OUTPUT_DIR = "grafana_dashboards"      # Directory to save the exported JSON files

# Functions
def get_all_dashboards(grafana_url, api_key):
    """Fetches a list of all dashboards from Grafana."""
    headers = {"Authorization": f"Bearer {api_key}"}
    url = f"{grafana_url}/api/search"
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for bad status codes
        dashboards = response.json()
        return dashboards
    except requests.exceptions.RequestException as e:
        print(f"Error fetching dashboards: {e}")
        return None

def get_dashboard_by_uid(grafana_url, api_key, uid, output_dir):
    """Fetches a specific dashboard by UID and saves it as a JSON file."""
    headers = {"Authorization": f"Bearer {api_key}"}
    url = f"{grafana_url}/api/dashboards/uid/{uid}"
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        dashboard_data = response.json()
        title = dashboard_data['dashboard'].get('title', 'untitled').replace(" ", "_")
        filename = os.path.join(output_dir, f"{title}_{uid}.json")
        with open(filename, 'w') as f:
            json.dump(dashboard_data, f, indent=4)
        print(f"Dashboard '{title}' (UID: {uid}) exported to '{filename}'")
        return True
    except requests.exceptions.RequestException as e:
        print(f"Error fetching dashboard with UID '{uid}': {e}")
        return False

def main():
    """Main function to fetch and export Grafana dashboards."""
    if not API_KEY or API_KEY == "YOUR_GRAFANA_API_KEY":
        print("Error: Please replace 'YOUR_GRAFANA_API_KEY' with your actual Grafana API key.")
        return

    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        print(f"Created output directory: {OUTPUT_DIR}")

    all_dashboards = get_all_dashboards(GRAFANA_URL, API_KEY)

    if all_dashboards:
        print(f"Found {len(all_dashboards)} dashboards. Starting export...")
        for dashboard in all_dashboards:
            uid = dashboard.get('uid')
            if uid:
                get_dashboard_by_uid(GRAFANA_URL, API_KEY, uid, OUTPUT_DIR)
            else:
                print(f"Warning: Dashboard found without a UID: {dashboard.get('title', 'unknown')}")
        print("Dashboard export complete.")
    else:
        print("No dashboards found or an error occurred while fetching the dashboard list.")

if __name__ == "__main__":
    main()
