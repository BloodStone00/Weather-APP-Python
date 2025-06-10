import tkinter as tk
from tkinter import messagebox
import requests
from datetime import datetime, timezone
import threading
import time

cities = []
city_windows = {}

def get_weather(city, update=False):
    api_key = "3462577ab5286a6c1ceec56aa32a28f5"
    base_url = "https://api.openweathermap.org/data/2.5/weather"
    
    params = {
        "q": city,
        "appid": api_key,
        "units": "metric"
    }
    
    response = requests.get(base_url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        
        timestamp = data["dt"]
        current_time = datetime.fromtimestamp(timestamp, tz=timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
        temperature = round(data["main"]["temp"])
        weather_description = data["weather"][0]["description"]
        
        if not update:
            city_window = tk.Toplevel(root)
            city_window.title("Weather Information")
            city_window.geometry("300x100")
            city_windows[city] = city_window
        else:
            city_window = city_windows[city]
            for widget in city_window.winfo_children():
                widget.destroy()

        tk.Label(city_window, text=city, font=("Arial", 14, "bold")).pack(pady=5)
        tk.Label(city_window, text=current_time).pack()
        tk.Label(city_window, text=f"{temperature}°C, {weather_description}").pack()

        for child in city_window.winfo_children():
            child.pack_configure(anchor='center')
    else:
        messagebox.showerror("Error", f"Error fetching weather data for {city}.")

def add_city():
    city = city_entry.get()
    if city and city not in cities:
        cities.append(city)
        get_weather(city)
        city_entry.delete(0, tk.END)

def periodic_update():
    while True:
        time.sleep(600) 
        for city in cities:
            get_weather(city, update=True)

root = tk.Tk()
root.title("Multi-City Weather App")
root.geometry("300x100")

city_label = tk.Label(root, text="Enter city name:")
city_label.pack(pady=5)

city_entry = tk.Entry(root, width=30)
city_entry.pack(pady=5)

add_city_button = tk.Button(root, text="Add City", command=add_city)
add_city_button.pack(pady=5)

threading.Thread(target=periodic_update, daemon=True).start()

root.mainloop()
