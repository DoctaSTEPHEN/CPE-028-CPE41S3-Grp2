import urllib.parse
import requests
from colorama import init, Fore, Style
from tabulate import tabulate

init(autoreset=True)

main_api = "https://www.mapquestapi.com/directions/v2/route?"
key = "EGVIJZBu6OlzjazQolRueK1VFVfoi30D"  


def get_units():
    while True:
        choice = input("Units - type 'metric' or 'imperial': ").strip().lower()
        if choice in ("metric", "imperial"):
            return choice
        print(Fore.YELLOW + "Please type 'metric' or 'imperial'.")


units = get_units()

while True:
    orig = input("Starting Location: ")
    if orig.lower() in ("quit", "q"):
        break
    dest = input("Destination: ")
    if dest.lower() in ("quit", "q"):
        break

    url = main_api + urllib.parse.urlencode({"key": key, "from": orig, "to": dest})
    print(Fore.CYAN + "URL: " + url)

    json_data = requests.get(url).json()
    json_status = json_data["info"]["statuscode"]

    if json_status == 0:
        route = json_data["route"]
        print(Fore.GREEN + f"API Status: {json_status} = A successful route call.\n")

        if units == "metric":
            distance = route["distance"] * 1.61
            dist_label = "Kilometers"
        else:
            distance = route["distance"]
            dist_label = "Miles"

        summary = [
            ["Directions", f"{orig} -> {dest}"],
            ["Trip Duration", route["formattedTime"]],
            [dist_label, "{:.2f}".format(distance)],
        ]
        print(Style.BRIGHT + tabulate(summary, tablefmt="grid"))

        steps = []
        for i, each in enumerate(route["legs"][0]["maneuvers"], start=1):
            step_distance = each["distance"] * 1.61 if units == "metric" else each["distance"]
            unit_label = "km" if units == "metric" else "mi"
            steps.append([i, each["narrative"], f"{step_distance:.2f} {unit_label}"])

        print(tabulate(steps, headers=["#", "Direction", "Distance"], tablefmt="grid"))
        print()

    elif json_status == 402:
        print(Fore.RED + "**********************************************")
        print(Fore.RED + f"Status Code: {json_status}; Invalid user inputs for one or both locations.")
        print(Fore.RED + "**********************************************\n")

    elif json_status == 611:
        print(Fore.RED + "**********************************************")
        print(Fore.RED + f"Status Code: {json_status}; Missing an entry for one or both locations.")
        print(Fore.RED + "**********************************************\n")

    else:
        print(Fore.RED + "************************************************************************")
        print(Fore.RED + f"For Status Code: {json_status}; Refer to:")
        print(Fore.RED + "https://developer.mapquest.com/documentation/directions-api/status-codes")
        print(Fore.RED + "************************************************************************\n")