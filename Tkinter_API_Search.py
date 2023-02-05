import tkinter as tk
from tkinter import ttk
import requests

# place_id = results["place_id"]
# phone_number = get_business_number(place_id, api_key)
# # Some results may not have a phone number, so check if it exists
# phone = result.get('formatted_phone_number', "N/A")
# results_phone.insert(tk.END, phone)


def get_business_number(place_id, api_key):
    detail_parameters = {
        "place_id": place_id,
        "key": api_key
    }
    detail_response = requests.get("https://maps.googleapis.com/maps/api/place/details/json", params=detail_parameters)
    data = detail_response.json()
    phone_number = None
    if "formatted_phone_number" in data["result"]:
        phone_number = data["result"]["formatted_phone_number"]
        return phone_number
    else:
        return "n/a"


def get_places():
    api_key = api_key_entry.get()
    location = location_entry.get()
    radius = radius_entry.get()
    query = query_entry.get()
    num_results = int(num_results_entry.get())

    # API request to get places
    response = requests.get(
        f'https://maps.googleapis.com/maps/api/place/textsearch/json?query={query}&location={location}&radius={radius}&key={api_key}')
    data = response.json()

    # Get the first num_results results
    results = data['results'][:num_results]

    print(f"Results = {results}")

# # Clear previous results
# results_name.delete(0, tk.END)
# results_address.delete(0, tk.END)
# results_phone.delete(0, tk.END)
# ^^^ optimized to: vvv
# If you ever need to add more Listbox widgets for displaying results, you can simply add them
# to the result_widgets list, and they will be cleared automatically when the button is clicked.
    result_widgets = [results_name, results_address, results_phone]
    for widget in result_widgets:
        widget.delete(0, tk.END)

# Insert new results into the listbox
# for result in results:
#     results_name.insert(tk.END, result['name'])
# for result in results:
#     results_address.insert(tk.END, result['name'])
# for result in results:
#     results_phone.insert(tk.END, result['name'])
# ^^^ Optimized to vvv
    for result in results:
        results_name.insert(tk.END, result['name'])
        results_address.insert(tk.END, result['formatted_address'])
        place_id = result["place_id"]
        phone = get_business_number(place_id, api_key)
        # Some results may not have a phone number, so check if it exists
        # phone = result.get('formatted_phone_number', "N/A")
        results_phone.insert(tk.END, phone)

        # place_id = results["place_id"]
        # phone_number = get_business_number(place_id, api_key)

i = 1
# Open the file in write mode
with open(f"{query}_in_{location}.txt", "w") as file:
    for result in searchdata["results"]:
        name = result["name"]
        address = result["formatted_address"]
        place_id = result["place_id"]
        phone_number = get_business_number(place_id)
        print_to_console(name, address, phone_number)
        file.write(f"{i}\nName:      {name}\nAddress:   {address}\nPhone:     {phone_number}\n")
        i = i + 1

root = tk.Tk()
root.title("Google Maps Business Search")

api_key_label = tk.Label(root, text="API Key:")
api_key_label.grid(row=0, column=0, padx=10, pady=10)

api_key_entry = tk.Entry(root, width=40)
api_key_entry.grid(row=0, column=1, padx=10, pady=10)

location_label = tk.Label(root, text="Location:")
location_label.grid(row=1, column=0, padx=10, pady=10)

location_entry = tk.Entry(root, width=40)
location_entry.grid(row=1, column=1, padx=10, pady=10)

radius_label = tk.Label(root, text="Radius:")
radius_label.grid(row=2, column=0, padx=10, pady=10)

radius_entry = tk.Entry(root, width=40)
radius_entry.grid(row=2, column=1, padx=10, pady=10)

query_label = tk.Label(root, text="Query:")
query_label.grid(row=3, column=0, padx=10, pady=10)

query_entry = tk.Entry(root, width=40)
query_entry.grid(row=3, column=1, padx=10, pady=10)

num_results_label = tk.Label(root, text="Number of Results:")
num_results_label.grid(row=4, column=0, padx=10, pady=10)

num_results_entry = tk.Entry(root, width=40)
num_results_entry.grid(row=4, column=1, padx=10, pady=10)

search_button = tk.Button(root, width=25, text="Search", bg="#00FF00", command=get_places)
search_button.grid(row=2, column=2, padx=10, pady=10)  # , columnspan=2

results_label_Col1 = tk.Label(root, text="Business Name:")
results_label_Col1.grid(row=6, column=1, padx=10, pady=10)

results_label_Col2 = tk.Label(root, text="Address:")
results_label_Col2.grid(row=6, column=2, padx=10, pady=10)

results_label_Col3 = tk.Label(root, text="Phone Number:")
results_label_Col3.grid(row=6, column=3, padx=10, pady=10)

results_label = tk.Label(root, text="Results:")
results_label.grid(row=7, column=0, padx=10, pady=10)

results_name = tk.Listbox(root, width=50, height=40)
results_name.grid(row=7, column=1, padx=10, pady=10)

results_address = tk.Listbox(root, width=50, height=40)
results_address.grid(row=7, column=2, padx=10, pady=10)

results_phone = tk.Listbox(root, width=50, height=40)
results_phone.grid(row=7, column=3, padx=10, pady=10)

root.mainloop()
