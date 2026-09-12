import urllib.parse
import requests

# Base MapQuest API endpoint from Lab 4.9.2
MAIN_API_URL = "https://www.mapquestapi.com/directions/v2/route?"
API_KEY = "EGVIJZBu6OlzjazQolRueK1VFVfoi30D"

def get_user_input():
    """Prompt user for locations and unit preference, handling exit commands."""
    orig = input("\nStarting Location: ").strip()
    if orig.lower() in ["quit", "q"]:
        return None, None, None
        
    dest = input("Destination: ").strip()
    if dest.lower() in ["quit", "q"]:
        return None, None, None

    print("Select Unit System:")
    print("  1. Metric (Kilometers / Liters)")
    print("  2. Imperial (Miles / Gallons)")
    choice = input("Choice (1 or 2, default 1): ").strip()
    unit = "m" if choice == "2" else "k"
    
    return orig, dest, unit

def fetch_route(orig, dest, unit):
    """Build URL request using urllib.parse and execute GET call via requests module."""
    # MapQuest default returns miles; pass unit parameter when requested
    params = {"key": API_KEY, "from": orig, "to": dest}
    url = MAIN_API_URL + urllib.parse.urlencode(params)
    print(f"\nConstructed URL: {url}")
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"\n[ERROR] Network failure: {e}")
        return None

def display_directions(json_data, unit):
    """Parse JSON payload and print trip summary and maneuvers table."""
    status_code = json_data["info"]["statuscode"]
    
    # MapQuest Status Code Handling from Lab 4.9.2
    if status_code == 402:
        print("\n************************************************************************")
        print("Status Code: 402; Invalid user inputs for one or both locations.")
        print("************************************************************************")
        return
    elif status_code == 611:
        print("\n************************************************************************")
        print("Status Code: 611; Missing an entry for one or both locations.")
        print("************************************************************************")
        return
    elif status_code != 0:
        print(f"\nFor Status Code: {status_code}; Refer to:")
        print("https://developer.mapquest.com/documentation/directions-api/status-codes")
        return

    print(f"\nAPI Status: {status_code} = A successful route call.")
    route = json_data["route"]
    
    # Calculate values based on user unit choice (Lab 4.9.2 metric conversion ratios)
    raw_dist = route["distance"]
    raw_fuel = route["fuelUsed"]
    
    if unit == "k":
        dist_val = raw_dist * 1.61
        fuel_val = raw_fuel * 3.78
        dist_unit, fuel_unit = "km", "Ltr"
    else:
        dist_val = raw_dist
        fuel_val = raw_fuel
        dist_unit, fuel_unit = "Miles", "Gal"

    # Trip Summary Output
    print("=" * 65)
    print(f" Directions from {route['locations'][0]['adminArea5']} to {route['locations'][1]['adminArea5']}")
    print("=" * 65)
    print(f" Trip Duration : {route['formattedTime']}")
    print(f" Distance      : {dist_val:.2f} {dist_unit}")
    print(f" Fuel Used     : {fuel_val:.2f} {fuel_unit}")
    print("=" * 65)
    
    # Format maneuvers list from json_data['route']['legs'][0]['maneuvers']
    print(f" {'#':<3} | {'Step Directions':<45} | {'Distance':<10}")
    print("-" * 65)
    
    maneuvers = route["legs"][0]["maneuvers"]
    for idx, step in enumerate(maneuvers, start=1):
        narrative = step["narrative"]
        step_dist = step["distance"] * (1.61 if unit == "k" else 1.0)
        print(f" {idx:<3} | {narrative:<45} | {step_dist:.2f} {dist_unit}")
        
    print("=" * 65 + "\n")

def main():
    print("--- MapQuest Direction Application (DEVASC Refactored) ---")
    while True:
        orig, dest, unit = get_user_input()
        if orig is None or dest is None:
            print("Exiting application. Goodbye!")
            break
            
        json_data = fetch_route(orig, dest, unit)
        if json_data:
            display_directions(json_data, unit)

if __name__ == "__main__":
    main()