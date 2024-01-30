import tkinter as tk
from tkinter import messagebox,PhotoImage
import json
import settings
import os
import Logger
import VPN_COMMANDS
def show_info():
    # Placeholder for info messagebox
    messagebox.showinfo("Info", "EZALTS BUFF163 BOT.\nWebsite Link : www.ezalts.shop")

def delete_cookies():
    delete_cookies_response=messagebox.askquestion("Cookies", "Do you want to delete cookies?\n(NOTE:This will log you out of steam from the bot)",icon="warning") 
    if(delete_cookies_response=="yes"):
        if os.path.exists(settings.cookies_path):
            os.remove(settings.cookies_path)
            messagebox.showinfo("Cookies", "Cookies deleted successfully.") 
        else:
            messagebox.showerror("Cookies", "Error: Could not find cookies in the directory!")

def exit_app():
    root.destroy()

def start_vpn_menu():
    VPN_COMMANDS.START_VPN()

def stop_vpn_menu():
    VPN_COMMANDS.STOP_VPN()

def restart_vpn_menu():
    VPN_COMMANDS.RESTART_VPN()

print(f"------EZALTS.SHOP BUFF163 BOT {settings.VERSION_NO}------")
print("-DEBUG LOG-")


# Create the main window
root = tk.Tk()
root.title("EZALTS.SHOP BUFF163 BOT")
root.geometry("500x400")
root.minsize(305, 350)

icon_rel_path='assets/ezaltsicon.ico'
icon_path=os.path.normpath(os.path.join(settings.abs_path, icon_rel_path))
root.iconbitmap(icon_path)

settings_json_rel_path='settings.json'
settings_json_path=os.path.normpath(os.path.join(settings.abs_path, settings_json_rel_path))

with open(settings_json_path, 'r') as file:
    data = json.load(file)
    ITEM_LINK = data['LINK']
    ITEM_MIN_FLOAT = data['MIN_FLOAT']
    ITEM_MAX_FLOAT=data['MAX_FLOAT']
    ITEM_MAX_PRICE = data['MAX_PRICE']

# Create a menubar
menubar = tk.Menu(root)
root.config(menu=menubar)

# Create a 'File' menu
file_menu = tk.Menu(menubar, tearoff=0)
file_menu.add_command(label="Delete Cookies",command=delete_cookies)
file_menu.add_command(label="Exit", command=exit_app)
menubar.add_cascade(label="File", menu=file_menu)

# Create a 'VPN' menu
vpn_menu=tk.Menu(menubar,tearoff=0)
vpn_menu.add_command(label="Restart VPN",command=restart_vpn_menu)
vpn_menu.add_command(label="Start VPN",command=start_vpn_menu)
vpn_menu.add_command(label="Stop VPN",command=stop_vpn_menu)
menubar.add_cascade(label="VPN",menu=vpn_menu)

# Create an 'About' menu
about_menu = tk.Menu(menubar, tearoff=0)
about_menu.add_command(label="Info", command=show_info)
menubar.add_cascade(label="About", menu=about_menu)


# Create and pack the heading
heading_label = tk.Label(root, text="EZALTS.SHOP BUFF163 BOT", font=("Helvetica 16 bold"))
subheading_label = tk.Label(root, text=settings.VERSION_NO, font=("Helvetica 10 "))
heading_label.pack(pady=(20, 0))
subheading_label.pack(pady=5)

# Create and pack the labels and entry widgets for the Item Link, Max Float, and Max Price
entries = {}
for label_text in ["Item Link:","Min Float:", "Max Float:", "Max Price:"]:
    frame = tk.Frame(root)
    frame.pack(fill='x', padx=10, pady=10)

    label = tk.Label(frame, text=label_text, width=10, anchor='w')
    label.pack(side='left')

    entry = tk.Entry(frame)
    entry.pack(side='right', expand=True, fill='x')
    entries[label_text] = entry

# Create and pack the Start Bot button
start_button = tk.Button(root, text="Start Bot",font=("Helvetica 10 bold"), command=lambda: start_bot(entries),padx=8,pady=8)
start_button.pack(pady=20)

entries["Item Link:"].insert(0, ITEM_LINK)
entries["Min Float:"].insert(0, ITEM_MIN_FLOAT)
entries["Max Float:"].insert(0, ITEM_MAX_FLOAT)
entries["Max Price:"].insert(0, ITEM_MAX_PRICE)

def start_bot(entries):
    # This function will be called when the Start Bot button is clicked
    item_link = entries["Item Link:"].get()
    min_float = entries["Min Float:"].get()
    max_float = entries["Max Float:"].get()
    max_price = entries["Max Price:"].get()
    # Modify the JSON data
    data['LINK'] = item_link  
    data['MIN_FLOAT'] = min_float
    data['MAX_FLOAT'] = max_float 
    data['MAX_PRICE'] = max_price  

    # Writing the modified data back to the JSON file
    with open(settings_json_path, 'w') as file:
        json.dump(data, file, indent=4)

    settings.URL=item_link
    settings.min_float=min_float
    settings.max_float=max_float
    settings.max_price=max_price
    root.destroy()

    import buff_bot as BUFF_BOT
    BUFF_BOT.initiate_buff_bot()
    BUFF_BOT.start_buff_bot()

# Start the Tkinter event loop
root.mainloop()