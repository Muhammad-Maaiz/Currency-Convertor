import requests
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import ImageTk, Image

def get_exchange_rates(api_key):
    base_url = 'https://open.er-api.com/v6/latest'
    try:
        response = requests.get(f'{base_url}?api_key={api_key}')
        response.raise_for_status()  # Raise an HTTPError for bad responses
        return response.json()['rates']
    except requests.exceptions.RequestException as e:
        print(f"Error fetching exchange rates: {e}")
        return None

def convert_currency():
    amount = amount_entry.get()
    if not amount:
        messagebox.showerror("Error", "Please enter an amount.")
        return
    
    try:
        amount = float(amount)
    except ValueError:
        messagebox.showerror("Error", "Invalid amount entered.")
        return

    from_currency = from_currency_var.get().upper()
    to_currency = to_currency_var.get().upper()

    if from_currency in exchange_rates and to_currency in exchange_rates:
        rate_from = exchange_rates[from_currency]
        rate_to = exchange_rates[to_currency]
        converted_amount = amount * (rate_to / rate_from)
        result_entry.config(state="normal")  # Enable the entry for writing
        result_entry.delete(0, tk.END)  # Clear previous result
        result_entry.insert(0, f"{amount} {from_currency} = {converted_amount:.2f} {to_currency}")
        result_entry.config(state="readonly")  # Disable the entry for editing
    else:
        messagebox.showerror("Error", "Invalid currency code entered.")

api_key = '84eeba3e1a6945ceafc925b8bb01127b'
exchange_rates = get_exchange_rates(api_key)

if exchange_rates:
    root = tk.Tk()
    root.title("Currency Converter")
    root.geometry('800x600')

    # Load the background image
    image_path = r"C:\Users\HS LAPTOP\Desktop\Python Project\image3.jpeg"
    background_image = Image.open(image_path)
    background_image = ImageTk.PhotoImage(background_image.resize((1365, 1200)))

    # Set the background image
    background_label = tk.Label(root, image=background_image)
    background_label.place(relwidth=1, relheight=1)

    # Light Blue Frame
    frame_width = 400  # Set the width of the frame
    frame_height = 600  # Set the height of the frame
    frame_converter = ttk.Frame(root, style="TFrame", width=frame_width, height=frame_height)
    frame_converter.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    # Welcome Label
    label_welcome = ttk.Label(frame_converter, text="Currency Converter", font=('Helvetica', 16, 'bold'), style="TLabel")
    label_welcome.grid(row=0, column=0, columnspan=2, pady=20)

    # Labels
    label_amount = ttk.Label(frame_converter, text="Enter Amount:", style="TLabel")
    label_amount.grid(row=1, column=0, padx=10, pady=10)

    label_from_currency = ttk.Label(frame_converter, text="From Currency:", style="TLabel")
    label_from_currency.grid(row=2, column=0, padx=10, pady=10)

    label_to_currency = ttk.Label(frame_converter, text="To Currency:", style="TLabel")
    label_to_currency.grid(row=3, column=0, padx=10, pady=10)

    # Entry
    amount_entry = ttk.Entry(frame_converter, style="TEntry")
    amount_entry.grid(row=1, column=1, padx=10, pady=10)

    from_currency_var = tk.StringVar()
    from_currency_combobox = ttk.Combobox(frame_converter, textvariable=from_currency_var, values=list(exchange_rates.keys()), style="TEntry")
    from_currency_combobox.grid(row=2, column=1, padx=10, pady=10)

    to_currency_var = tk.StringVar()
    to_currency_combobox = ttk.Combobox(frame_converter, textvariable=to_currency_var, values=list(exchange_rates.keys()), style="TEntry")
    to_currency_combobox.grid(row=3, column=1, padx=10, pady=10)

    # Button
    convert_button = ttk.Button(frame_converter, text="Convert", command=convert_currency, style="TButton")
    convert_button.grid(row=4, column=0, pady=10, columnspan=2)

    # Result Entry
    result_entry = ttk.Entry(frame_converter, style="TEntry", state="readonly", width=30)
    result_entry.grid(row=5, column=0, columnspan=2, pady=(10, 20))  # Adding bottom padding

    # Style
    style = ttk.Style()
    style.theme_create("fancy", parent="alt", settings={
        "TButton": {
            "configure": {
                "background": "blue",  # blue button background
                "foreground": "white",
                "padding": 10,
                "font": ('Helvetica', 12),
            },
            "map": {
                "background": [("active", "dark blue")],  # Dark blue on click
            },
        },
        "TLabel": {
            "configure": {
                "font": ('Helvetica', 12, 'bold'),  # Bold and larger font
                "background": "aqua",  # Aqua label background
                "foreground": "dark blue",  # Dark blue text color
            },
        },
        "TEntry": {
            "configure": {
                "font": ('Helvetica', 12),
            },
        },
        "TFrame": {
            "configure": {
                "background": "aqua",  # Aqua frame background
            },
        },
    })

    style.theme_use("fancy")

    # Main loop
    root.mainloop()
else:
    print("Failed to fetch exchange rates. Please check your API key or try again later.")