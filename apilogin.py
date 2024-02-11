import requests
import threading
import tkinter as tk
from tkinter import messagebox

def login_action():
    email = email_entry.get()
    password = password_entry.get()

    data = {
    'email': email,
    'pass': password,
    }
    #     data = {
    #     'email': 'jugalnaik14@gmail.com',
    #     'pass': 'thispasswordisverystrong',
    #   }

    try:
        response = requests.post('https://ezalts.shop/wp-json/api/buff', data=data)
        if(response.status_code==200):
            if(response.text=='true'):
                # print("Allowed to access") #Is a user and has panel
                messagebox.showinfo("Success","Logged in successfully.")
            else:
                # print("Not allowed") #Is a user and does not have panel
                messagebox.showerror("Error","You do not have an EZALTS.SHOP BUFF163 BOT.\nBuy it now from www.ezalts.shop")
        elif(response.status_code==403):
            # print("Wrong username/password!") #Incorrect details
            messagebox.showerror("Error","Incorrect username/password!")
        elif(response.status_code==404): #other
            raise Exception
        else:
            raise Exception
    except Exception as e: #Exception
        # print("An error occured! Could not connect to the server!")
        messagebox.showerror("Error","An error occcured!\nCould not connect to the server!")
    loginroot.after(0, lambda: login_button.config(state=tk.NORMAL))
    

def login_action_thread():
    # Disable the login button
    login_button.config(state=tk.DISABLED)
    # Start the login process in a new thread
    login_thread = threading.Thread(target=login_action)
    login_thread.start()

# Create the main window
loginroot = tk.Tk()
loginroot.title("EZALTS.SHOP BUFF BOT")
loginroot.geometry("400x250")
loginroot.minsize(400,250)

# Create the title label for EZALTS.SHOP BUFF BOT
title_label = tk.Label(loginroot, text="EZALTS.SHOP BUFF163 BOT", font=("Arial", 16, "bold"))
title_login_label = tk.Label(loginroot, text="USER LOGIN", font=("Arial", 12))
title_label.pack(pady=(20, 0))
title_login_label.pack(pady=(10, 0))

# Create a frame for the login components
login_frame = tk.LabelFrame(loginroot, padx=10, pady=10)
login_frame.pack(padx=10, pady=10)

# Email label and entry
email_label = tk.Label(login_frame, text="Email:")
email_label.grid(row=0, column=0, sticky="e", padx=5)
email_entry = tk.Entry(login_frame, width=30)
email_entry.grid(row=0, column=1, padx=5)

# Password label and entry
password_label = tk.Label(login_frame, text="Password:")
password_label.grid(row=1, column=0, sticky="e", padx=5)
password_entry = tk.Entry(login_frame, show="*", width=30)
password_entry.grid(row=1, column=1, padx=5)

# Login button
login_button = tk.Button(login_frame, text="Login", command=login_action_thread)
login_button.grid(row=2, column=0, columnspan=2, pady=5)

loginroot.mainloop()
