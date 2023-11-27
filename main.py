from tkinter import *
from tkinter import messagebox, simpledialog
import json
import hashlib
from random import choice, randint, shuffle
import pyperclip


# ---------------------------- PASSWORD GENERATOR ------------------------------- #

# Password Generator Project
def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letters = [choice(letters) for _ in range(randint(8, 10))]
    password_symbols = [choice(symbols) for _ in range(randint(2, 4))]
    password_numbers = [choice(numbers) for _ in range(randint(2, 4))]

    password_list = password_letters + password_symbols + password_numbers
    shuffle(password_list)

    password = "".join(password_list)
    password_entry.delete(0, END)  # Clear previous content
    password_entry.insert(0, password)
    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #

# Variable to store the master password
master_password = "your_default_master_password"  # Change this to a secure default master password


# Function to check the master password
def check_master_password():
    entered_password = simpledialog.askstring("Master Password", "Enter Master Password:", show='*')
    hashed_entered_password = hashlib.sha256(entered_password.encode()).hexdigest()

    if hashed_entered_password == hashlib.sha256(master_password.encode()).hexdigest():
        messagebox.showinfo("Access Granted", "Master Password correct. Access granted.")
        return True
    else:
        messagebox.showerror("Access Denied", "Incorrect Master Password. Access denied.")
        return False


# Function to save the password
def save():
    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()
    new_data = {
        website: {
            "email": email,
            "password": password,
        }
    }

    if len(website) == 0 or len(password) == 0:
        messagebox.showinfo(title="Oops", message="Please make sure you haven't left any fields empty.")
    else:
        try:
            with open("data.json", "r") as data_file:
                # Reading old data
                data = json.load(data_file)
        except FileNotFoundError:
            with open("data.json", "w") as data_file:
                # Saving updated data
                json.dump(new_data, data_file, indent=4)
        else:
            # Updating old data with new data
            data.update(new_data)
            with open("data.json", "w") as data_file:
                json.dump(data, data_file, indent=4)
        finally:
            website_entry.delete(0, END)
            password_entry.delete(0, END)


# Function to find and display the password
def find_password():
    website = website_entry.get()

    # Check master password only when searching
    if check_master_password():
        try:
            with open("data.json") as data_file:
                data = json.load(data_file)
        except FileNotFoundError:
            messagebox.showinfo(title="ERROR", message="No Data File Found")
        else:
            if website in data:
                email = data[website]["email"]
                password = data[website]["password"]
                messagebox.showinfo(title=website, message=f"Email: {email}\nPassword: {password}")
            else:
                messagebox.showinfo(title=website, message=f"No details for {website} exists.")


# Toggle Dark Mode
def toggle_dark_mode():
    # You can customize the color values for your dark mode
    dark_mode_background = "#282c35"
    dark_mode_text = "#ffffff"

    current_bg = window.cget("background")
    if current_bg == dark_mode_background:
        # Switch to light mode
        window.configure(background="#ffffff")
        website_label.configure(bg="#ffffff", fg="#000000")
        email_label.configure(bg="#ffffff", fg="#000000")
        password_label.configure(bg="#ffffff", fg="#000000")
        search_button.configure(bg="#ffffff", fg="#000000")
        generate_password_button.configure(bg="#ffffff", fg="#000000")
        add_button.configure(bg="#ffffff", fg="#000000")
    else:
        # Switch to dark mode
        window.configure(background=dark_mode_background)
        website_label.configure(bg=dark_mode_background, fg=dark_mode_text)
        email_label.configure(bg=dark_mode_background, fg=dark_mode_text)
        password_label.configure(bg=dark_mode_background, fg=dark_mode_text)
        search_button.configure(bg=dark_mode_background, fg=dark_mode_text)
        generate_password_button.configure(bg=dark_mode_background, fg=dark_mode_text)
        add_button.configure(bg=dark_mode_background, fg=dark_mode_text)


# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Password Manager - Itai Markovetzky")
window.config(padx=50, pady=50, background="#ffffff")  # Set initial background color

canvas = Canvas(height=200, width=200, bg="#ffffff")
logo_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_img)
canvas.grid(row=0, column=1)

# Labels
website_label = Label(text="Website:", bg="#ffffff", fg="#000000")
website_label.grid(row=1, column=0)
email_label = Label(text="Email/Username:", bg="#ffffff", fg="#000000")
email_label.grid(row=2, column=0, padx=10)
password_label = Label(text="Password:", bg="#ffffff", fg="#000000")
password_label.grid(row=3, column=0)

# Entries
website_entry = Entry(width=40)
website_entry.grid(row=1, column=1, columnspan=1)
website_entry.focus()
email_entry = Entry(width=40)
email_entry.grid(row=2, column=1, columnspan=1)
email_entry.insert(0, "yourmail@gmail.com")
password_entry = Entry(width=40)
password_entry.grid(row=3, column=1)

# Buttons
search_button = Button(text="Search", width=13, command=find_password, bg="#ffffff", fg="#000000")
search_button.grid(row=1, column=2, pady=10, padx=10)
generate_password_button = Button(text="Generate Password", command=generate_password, bg="#ffffff", fg="#000000")
generate_password_button.grid(row=3, column=2, pady=10, padx=10)
add_button = Button(text="Add", width=50, command=save, bg="#ffffff", fg="#000000")
add_button.grid(row=4, column=1, columnspan=1, pady=15)

# Toggle Dark Mode Button
dark_mode_button = Button(text="Toggle Dark Mode", command=toggle_dark_mode, bg="#ffffff", fg="#000000")
dark_mode_button.grid(row=5, column=1, pady=10)

window.mainloop()
