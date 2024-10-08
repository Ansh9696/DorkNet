import tkinter as tk
from tkinter import messagebox, simpledialog, Scrollbar, Canvas, Frame, filedialog, StringVar, OptionMenu
import webbrowser
import os

class GoogleDorksTool:
    def __init__(self, root):
        self.root = root
        self.root.title("Google Dorks Search Tool")
        self.root.geometry("700x750")  # Increased height for additional widgets
        self.root.configure(bg='#000000')  # Dark background for hacker theme
        
        self.dorks = self.initialize_dorks()  # Initialize dorks
        self.create_widgets()
        self.update_buttons()

    def initialize_dorks(self):
        # Initial list of Google dorks
        return [
            "filetype:pdf", "inurl:admin", "site:example.com", "intitle:login", "intext:password",
            "index of", "filetype:xls", "inurl:login", "site:gov", "intext:confidential",
            "inurl:register", "filetype:doc", "intitle:index.of", "site:edu", "intext:email",
            "filetype:sql", "inurl:wp-admin", "site:org", "intext:database", "filetype:xml",
            "intitle:dashboard", "inurl:search", "intext:private", "filetype:csv", "site:mil",
            "inurl:adminlogin", "intitle:admin", "filetype:log", "inurl:secure", "intext:api",
            "site:us", "filetype:json", "inurl:account", "intitle:files", "site:uk",
            "inurl:login.php", "filetype:backup", "intitle:ftp", "site:ca", "intext:passwords",
            "filetype:db", "inurl:login.aspx", "intitle:settings", "site:au", "intext:secret",
            "filetype:bak", "inurl:admin.php", "intitle:server", "site:br", "intext:token",
        ]

    def create_widgets(self):
        # Create top frame for filter buttons
        top_frame = tk.Frame(self.root, bg='#000000')
        top_frame.pack(pady=10, padx=20, fill='x')

        # Filter buttons
        self.create_button(top_frame, "Filter Dorks", self.filter_dorks, '#ff0000')
        self.create_button(top_frame, "Show Filetype Dorks", self.show_filetype_dorks, '#ff0000')
        self.create_button(top_frame, "Show Non-Filetype Dorks", self.show_non_filetype_dorks, '#ff0000')

        # Frame for input and result display
        frame = tk.Frame(self.root, bg='#000000')
        frame.pack(pady=20, padx=20, fill='both', expand=True)

        # Input field for the user
        tk.Label(frame, text="Enter name or search term:", font=("Courier", 14), bg='#000000', fg='white').pack(pady=10)
        self.entry = tk.Entry(frame, width=60, font=("Courier", 14), borderwidth=2, relief="flat")
        self.entry.pack(pady=10)

        # Browser selection
        self.browser_var = StringVar(value="default")
        tk.Label(frame, text="Select browser:", font=("Courier", 14), bg='#000000', fg='white').pack(pady=10)
        browser_menu = OptionMenu(frame, self.browser_var, "default", "chrome", "firefox", "brave")
        browser_menu.config(font=("Courier", 12), bg='#00ff00', fg='black')
        browser_menu.pack(pady=10)

        # Canvas and scrollbar for dork buttons
        self.canvas = Canvas(frame, bg='#000000', width=700)
        self.scrollbar = Scrollbar(frame, orient="vertical", command=self.canvas.yview)
        self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.button_frame = tk.Frame(self.canvas, bg='#000000')
        self.canvas.create_window((0, 0), window=self.button_frame, anchor="nw")

        # Bind mouse wheel event to canvas
        self.root.bind_all("<MouseWheel>", self.on_mouse_wheel)

        # Button to add new dorks and upload dorks file
        self.create_button(frame, "Add Multiple Dorks", self.add_dorks, '#00ff00')
        self.create_button(frame, "Upload Dorks File", self.upload_dorks_file, '#00ff00')

        # Filter input field
        tk.Label(frame, text="Filter dorks:", font=("Courier", 14), bg='#000000', fg='white').pack(pady=10)
        self.filter_entry = tk.Entry(frame, width=60, font=("Courier", 14), borderwidth=2, relief="flat")
        self.filter_entry.pack(pady=10)

        # Result display
        self.result_label = tk.Label(frame, text="", font=("Courier", 12), fg="cyan", bg='#000000', wraplength=650)
        self.result_label.pack(pady=20)

    def create_button(self, parent, text, command, color):
        tk.Button(parent, text=text, width=20, height=2, font=("Courier", 12),
                  bg=color, fg='white', borderwidth=1, relief="flat", command=command).pack(pady=5)

    def update_buttons(self, dorks_to_display=None):
        if dorks_to_display is None:
            dorks_to_display = sorted(self.dorks)

        for widget in self.button_frame.winfo_children():
            widget.destroy()

        for dork in dorks_to_display:
            button = tk.Button(self.button_frame, text=dork, width=25, height=2, font=("Courier", 12),
                               bg='#00ff00', fg='black', borderwidth=1, relief="flat",
                               command=lambda dork_query=dork: self.perform_search(dork_query))
            button.pack(pady=5)

        # Update scroll region
        self.button_frame.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

    def perform_search(self, dork):
        user_input = self.entry.get().strip()
        if not user_input:
            messagebox.showwarning("Input Error", "Please enter a name or search term.")
            return

        query = f"{dork} {user_input}"
        url = f"https://www.google.com/search?q={query}"
        self.result_label.config(text=f"Search Query: {url}")

        # Open URL in the selected browser
        browser = self.browser_var.get()
        if browser == "chrome":
            self.open_in_chrome(url)
        elif browser == "firefox":
            self.open_in_firefox(url)
        elif browser == "brave":
            self.open_in_brave(url)
        else:
            webbrowser.open_new_tab(url)

    def open_in_chrome(self, url):
        try:
            # Update path to Chrome executable as needed
            chrome_path = "C:/Program Files/Google/Chrome/Application/chrome.exe %s"
            webbrowser.get(chrome_path).open_new_tab(url)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open Chrome: {e}")

    def open_in_firefox(self, url):
        try:
            # Update path to Firefox executable as needed
            firefox_path = "C:/Program Files/Mozilla Firefox/firefox.exe %s"
            webbrowser.get(firefox_path).open_new_tab(url)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open Firefox: {e}")

    def open_in_brave(self, url):
        try:
            # Update path to Brave executable as needed
            brave_path = "C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe %s"
            webbrowser.get(brave_path).open_new_tab(url)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open Brave: {e}")

    def add_dorks(self):
        dorks_input = simpledialog.askstring("Add Google Dorks", "Enter new Google dorks (one per line):")
        if dorks_input:
            new_dorks = [dork.strip() for dork in dorks_input.split('\n') if dork.strip()]
            existing_dorks = set(self.dorks)
            for dork in new_dorks:
                if dork and dork not in existing_dorks:
                    self.dorks.append(dork)
                    existing_dorks.add(dork)
                elif dork:
                    messagebox.showinfo("Duplicate Dork", f"The dork '{dork}' is already in the list.")
            self.dorks.sort()
            self.update_buttons()

    def upload_dorks_file(self):
        initial_dir = r"B:\database"  # Set initial directory for file dialog
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")], initialdir=initial_dir)
        if file_path:
            try:
                with open(file_path, "r") as file:
                    new_dorks = [line.strip() for line in file if line.strip()]
                existing_dorks = set(self.dorks)
                for dork in new_dorks:
                    if dork and dork not in existing_dorks:
                        self.dorks.append(dork)
                        existing_dorks.add(dork)
                    elif dork:
                        messagebox.showinfo("Duplicate Dork", f"The dork '{dork}' is already in the list.")
                self.dorks.sort()
                self.update_buttons()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to read file: {e}")

    def filter_dorks(self):
        filter_text = self.filter_entry.get().strip().lower()
        if filter_text:
            filtered_dorks = [dork for dork in self.dorks if filter_text in dork.lower()]
        else:
            filtered_dorks = self.dorks
        self.update_buttons(filtered_dorks)

    def show_filetype_dorks(self):
        filetype_dorks = [dork for dork in self.dorks if dork.startswith("filetype:")]
        self.update_buttons(filetype_dorks)

    def show_non_filetype_dorks(self):
        non_filetype_dorks = [dork for dork in self.dorks if not dork.startswith("filetype:")]
        self.update_buttons(non_filetype_dorks)

    def on_mouse_wheel(self, event):
        # Scroll canvas vertically with limits
        if event.delta > 0:
            # Scroll up
            self.canvas.yview_scroll(-1, "units")
        elif event.delta < 0:
            # Scroll down
            self.canvas.yview_scroll(1, "units")

if __name__ == "__main__":
    root = tk.Tk()
    app = GoogleDorksTool(root)
    
    # Register browsers with webbrowser module
    webbrowser.register('chrome', webbrowser.BackgroundBrowser("C:/Program Files/Google/Chrome/Application/chrome.exe %s"))
    webbrowser.register('firefox', webbrowser.BackgroundBrowser("C:/Program Files/Mozilla Firefox/firefox.exe %s"))
    webbrowser.register('brave', webbrowser.BackgroundBrowser("C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe %s"))

    root.mainloop()
