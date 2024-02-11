import tkinter as tk
from tkinter import messagebox
import threading

def perform_login():
    # Simulate a delay for the login process
    # This is where you would add your actual authentication logic
    email = email_entry.get()
    password = password_entry.get()
    
    # Simulate a response delay
    import time
    time.sleep(2)  # Simulate time-consuming operations
    
    # After the operation, re-enable the login button
    # Since we are modifying the GUI from another thread, we need to use root.after
    loginroot.after(0, lambda: login_button.config(state=tk.NORMAL))
    
    # Placeholder for actual login logic
    messagebox.showinfo("Login Info", "Login attempted with:\nEmail: {}\nPassword: {}".format(email, password))

def login_action():
    # Disable the login button
    login_button.config(state=tk.DISABLED)
    # Start the login process in a new thread
    login_thread = threading.Thread(target=perform_login)
    login_thread.start()

# Create the main window
loginroot = tk.Tk()
loginroot.title("EZALTS.SHOP BUFF BOT")
loginroot.geometry("400x250")
loginroot.minsize(400,250)

# Create the title label for EZALTS.SHOP BUFF BOT
title_label = tk.Label(loginroot, text="EZALTS.SHOP BUFF163 BOT", font=("Arial", 16, "bold"))
title_login_label = tk.Label(loginroot, text="LOGIN", font=("Arial", 12))
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
login_button = tk.Button(login_frame, text="Login", command=login_action)
login_button.grid(row=2, column=0, columnspan=2, pady=5)

loginroot.mainloop()