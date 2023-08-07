# gui.py

import tkinter as tk
from tkinter import messagebox  # Import messagebox
from main2refactor import main  # Import the main function from main_app.py
import threading

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

        # Center the window on the screen
        window_width = self.master.winfo_reqwidth()
        window_height = self.master.winfo_reqheight()
        position_right = int(self.master.winfo_screenwidth() / 2 - window_width / 2)
        position_down = int(self.master.winfo_screenheight() / 2 - window_height / 2)
        self.master.geometry("+{}+{}".format(position_right, position_down))

        # Create a new Frame to act as the console
        self.console_frame = tk.Frame(self.master)
        # Add the console frame to the master window
        self.console_frame.pack(fill='both', expand=True)
        self.console_frame.pack_forget()  # Hide it initially

        # Create a Text widget in the console frame
        self.console_text = tk.Text(self.console_frame, state='disabled', width=30)
        self.console_text.pack()

        # Create a StringVar for the status label
        self.status_var = tk.StringVar()
        self.status_var.trace('w', self.update_console)  # Call update_console whenever the status_var changes

        self.status_label = tk.Label(self, textvariable=self.status_var)
        self.status_label.grid(row=7, column=0, columnspan=2, padx=10, pady=5)

        # Create a button to show/hide the console window
        self.console_button = tk.Button(self, text="Show Console", command=self.toggle_console)
        self.console_button.grid(row=8, column=0, columnspan=2, padx=10, pady=10)

    def toggle_console(self):
        if self.console_frame.winfo_viewable():
            self.console_frame.pack_forget()
            self.console_button.config(text="Show Console")
        else:
            self.console_frame.pack(fill='both', expand=True)
            self.console_button.config(text="Hide Console")

    def update_console(self, *args):
        # Get the latest status update
        status_update = self.status_var.get()

        # Skip "Listening" and "Processing" updates
        if status_update in ["Listening", "Processing", "Wait"]:
            return

        # Enable the Text widget, insert the text, then disable it
        # Disabling it makes it read-only for the user
        self.console_text.config(state='normal')
        self.console_text.insert('end', status_update + '\n')
        self.console_text.config(state='disabled')

    def create_widgets(self):
        font = ("Montserrat", 17)

        self.playlist_label = tk.Label(self, text="Playlist URL", font=font)
        self.playlist_label.grid(row=0, column=0, sticky="w", padx=10, pady=5)
        self.playlist_entry = tk.Entry(self, font=font)
        self.playlist_entry.grid(row=1, column=0, columnspan=2, sticky="ew", padx=10, pady=5)

        self.username_label = tk.Label(self, text="Email", font=font)
        self.username_label.grid(row=2, column=0, sticky="w", padx=10, pady=5)
        self.username_entry = tk.Entry(self, font=font)
        self.username_entry.grid(row=3, column=0, sticky="ew", padx=10, pady=5)

        # Create a Label for the email domain
        self.domain_label = tk.Label(self, text="@brandtrack.fm", fg="gray", font=font)
        self.domain_label.grid(row=3, column=1, sticky="w", padx=(0, 10), pady=5)

        self.password_label = tk.Label(self, text="Password", font=font)
        self.password_label.grid(row=4, column=0, sticky="w", padx=10, pady=5)
        self.password_entry = tk.Entry(self, show="*", font=font)
        self.password_entry.grid(row=5, column=0, sticky="ew", padx=10, pady=5)

        # Create a Checkbutton to show/hide password
        self.show_password = tk.IntVar()
        self.show_password_checkbutton = tk.Checkbutton(self, text="Show password", variable=self.show_password,
                                                        command=self.toggle_password, font=font)
        self.show_password_checkbutton.grid(row=5, column=1, sticky="w", padx=10, pady=5)

        self.start_button = tk.Button(self, text="Start", font=font, command=self.start_script)
        self.start_button.grid(row=6, column=0, columnspan=2, padx=10, pady=5)

        # Configure the column weights to ensure the entry fields stretch to fill the window
        self.grid_columnconfigure(0, weight=1)

        self.status_label = tk.Label(self, text="", font=font)
        self.status_label.grid(row=7, column=0, columnspan=2, padx=10, pady=5)

    def toggle_password(self):
        if self.show_password.get():
            self.password_entry.config(show="")
        else:
            self.password_entry.config(show="*")

    def start_script(self):
        playlist_url = self.playlist_entry.get()
        username = self.username_entry.get() + "@brandtrack.fm"
        password = self.password_entry.get()

        # Validate user input
        if not playlist_url or not username or not password:
            messagebox.showerror("Error", "All fields must be filled out")  # Show error message
            # Clear input fields
            self.playlist_entry.delete(0, tk.END)
            self.username_entry.delete(0, tk.END)
            self.password_entry.delete(0, tk.END)
            return

        # If the validation passes, hide the credential inputs
        self.username_label.grid_remove()
        self.username_entry.grid_remove()
        self.domain_label.grid_remove()
        self.password_label.grid_remove()
        self.password_entry.grid_remove()
        self.show_password_checkbutton.grid_remove()

        self.update_idletasks()  # Force the GUI to update

        # Move the window to the top right of the screen
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        window_width = self.master.winfo_reqwidth()
        window_height = self.master.winfo_reqheight()
        position_right = screen_width - window_width
        position_down = 0
        self.master.geometry("+{}+{}".format(position_right, position_down))

        try:
            # Start the main function in a new thread
            thread = threading.Thread(target=main, args=(playlist_url, username, password, self.status_var),
                                      daemon=True)
            thread.start()
        except Exception as e:
            messagebox.showerror("Error", str(e))


root = tk.Tk()
root.title("PyBrandtrack")
app = Application(master=root)
app.mainloop()
