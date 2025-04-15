import tkinter as tk
from tkinter import messagebox, filedialog, StringVar, OptionMenu, Text, ttk, simpledialog
import webbrowser
import time
import json  # Import the json module
import speech_recognition as sr  # Import speech_recognition


class DorkNetTool:
    def __init__(self, root):
        self.root = root
        self.root.title("DorkNet - Google Dorks Search Tool")
        self.root.geometry("1000x900")

        self.theme = "dark"
        self.bg_color = '#000000'
        self.fg_color = '#00ff00'

        self.root.configure(bg=self.bg_color)

        self.show_startup_animation()
        self.dorks = self.initialize_dorks()
        self.create_widgets()
        self.load_osint_data("osint_data.json")  # Load OSINT data from JSON

    def show_startup_animation(self):
        splash = tk.Toplevel(self.root)
        splash.geometry("600x400")
        splash.configure(bg="black")
        splash.overrideredirect(True)

        label = tk.Label(splash, text="DorkNet", font=("Courier", 36, "bold"), fg="#00ff00", bg="black")
        label.pack(expand=True)

        self.root.update()
        splash.after(2000, splash.destroy)  # Show for 2 seconds
        self.root.wait_window(splash)

    def toggle_theme(self):
        if self.theme == "dark":
            self.theme = "light"
            self.bg_color = "#ffffff"
            self.fg_color = "#0000ff"
        else:
            self.theme = "dark"
            self.bg_color = "#000000"
            self.fg_color = "#00ff00"

        self.root.configure(bg=self.bg_color)
        self.update_theme()

    def update_theme(self):
        self.theme_btn_canvas.configure(bg=self.bg_color)
        self.theme_btn_canvas.itemconfig(self.theme_btn_circle, fill=self.fg_color, outline=self.fg_color)
        self.theme_btn_canvas.itemconfig(self.theme_btn_text, fill=self.bg_color)

        for widget in self.root.winfo_children():
            if isinstance(widget, (tk.Frame, tk.Label, tk.Button, Text, tk.Entry, OptionMenu)):
                try:
                    widget.configure(bg=self.bg_color, fg=self.fg_color)
                except:
                    pass

        for tab in self.category_frames.values():
            tab.configure(bg=self.bg_color)

        for listbox in self.dork_listboxes.values():
            listbox.configure(bg=self.bg_color, fg=self.fg_color)

        self.terminal.configure(bg=self.bg_color, fg=self.fg_color)

    def animate_toggle(self, event):
        self.toggle_theme()

    def initialize_dorks(self):
        return {
            "Sensitive Directories": [
                "intitle:index.of",
                "inurl:backup",
                "inurl:db",
                "inurl:config",
                "inurl:logs",
                "inurl:phpinfo",
                "inurl:ftp",
            ],
            "File Types": [
                "filetype:pdf",
                "filetype:xls",
                "filetype:doc",
                "filetype:docx",
                "filetype:csv",
                "filetype:xml",
                "filetype:sql",
                "filetype:json",
            ],
            "Error Messages": [
                "intext:sql syntax error",
                "intext:Warning: mysql_connect()",
                "intext:Warning: pg_connect()",
                "intext:Warning: include()",
                "intext:Warning: require()",
            ],
            "Credentials and Keys": [
                "intext:username",
                "intext:password",
                "inurl:env",
                "inurl:git",
                "intext:API key",
                "inurl:credentials",
            ],
            "Cameras and IoT": [
                "inurl:/view/index.shtml",
                "intitle:Live View / AXIS",
                "intitle:Live View / Network Camera",
                "inurl:axis-cgi",
                "inurl:viewerframe?mode=motion",
                "intitle:Network Camera",
            ],
            "Vulnerable Servers": [
                "inurl:phpmyadmin",
                "inurl:wp-admin",
                "intitle:phpMyAdmin",
                "intext:wp-config.php",
                "inurl:sql",
            ],
            "Other Sensitive Information": [
                "intext:ssn",
                "intext:credit card",
                "intext:CVV",
                "intext:passport",
                "intext:confidential",
                "intext:proprietary",
            ],
            "Exploit Specific": [
                "inurl:/proc/self/cwd",
                "inurl:/etc/passwd",
                "inurl:cmd.exe",
                "inurl:wp-login.php",
                "inurl:phpinfo.php",
                "inurl:/cgi-bin/",
            ],
            "Public BBH": [
                "inurl:/bug bounty",
                "inurl:/security",
                "inurl:/responsible disclosure",
                "inurl:/responsible-disclosure/reward",
                "inurl:/responsible-disclosure/swag",
                "inurl:/responsible-disclosure/bounty",
                "inurl:'/responsible disclosure' hoodie",
                "responsible disclosure swag r=h:com",
                "responsible disclosure:sites",
                "responsible disclosure r=h:nl",
                "site:*.gov.* 'responsible disclosure'",
            ],
            "Daily purpose": [],
            "People needs": [],
        }

    def create_widgets(self):
        # 🌙 Circular Theme Button
        self.theme_btn_canvas = tk.Canvas(self.root, width=80, height=80, bg=self.bg_color, highlightthickness=0)
        self.theme_btn_canvas.place(x=10, y=10)
        self.theme_btn_circle = self.theme_btn_canvas.create_oval(10, 10, 70, 70, fill=self.fg_color, outline=self.fg_color)
        self.theme_btn_text = self.theme_btn_canvas.create_text(40, 40, text="Theme", font=("Courier", 10, "bold"), fill=self.bg_color)
        self.theme_btn_canvas.tag_bind(self.theme_btn_circle, "<Button-1>", self.animate_toggle)
        self.theme_btn_canvas.tag_bind(self.theme_btn_text, "<Button-1>", self.animate_toggle)

        # Title in the middle top
        title_label = tk.Label(self.root, text="DorkNet", font=("Courier", 28, "bold"), bg=self.bg_color, fg=self.fg_color)
        title_label.pack(pady=(20, 5))
        subtitle_label = tk.Label(self.root, text="(The ultimate searcher tool)", font=("Courier", 14), bg=self.bg_color, fg=self.fg_color)
        subtitle_label.pack(pady=(0, 10))

        top_frame = tk.Frame(self.root, bg=self.bg_color)
        top_frame.pack(pady=10, padx=20, fill='x')

        tk.Label(top_frame, text="Enter search term:", font=("Courier", 14), bg=self.bg_color, fg=self.fg_color).pack(side="left", padx=10)
        self.entry = tk.Entry(top_frame, width=40, font=("Courier", 14), borderwidth=2, relief="flat")
        self.entry.pack(side="left", padx=10)

        self.browser_var = StringVar(value="default")
        tk.Label(top_frame, text="Browser:", font=("Courier", 14), bg=self.bg_color, fg=self.fg_color).pack(side="left", padx=10)
        browser_menu = OptionMenu(top_frame, self.browser_var, "default", "chrome", "firefox", "brave")
        browser_menu.config(font=("Courier", 12), bg=self.fg_color, fg='black')
        browser_menu.pack(side="left", padx=10)

        tk.Label(top_frame, text="Search dork:", font=("Courier", 14), bg=self.bg_color, fg=self.fg_color).pack(side="left", padx=10)
        self.dork_search_entry = tk.Entry(top_frame, width=30, font=("Courier", 14), borderwidth=2, relief="flat")
        self.dork_search_entry.pack(side="left", padx=10)
        self.dork_search_entry.bind("<KeyRelease>", self.filter_dorks)

        self.tabs = ttk.Notebook(self.root)
        self.tabs.pack(pady=10, padx=20, fill='both', expand=True)

        self.category_frames = {}
        self.dork_listboxes = {}

        for category in self.dorks.keys():
            frame = tk.Frame(self.tabs, bg=self.bg_color)
            self.tabs.add(frame, text=category)

            self.category_frames[category] = frame

            listbox = tk.Listbox(frame, selectmode=tk.MULTIPLE, font=("Courier", 12), bg=self.bg_color, fg=self.fg_color, height=15)
            listbox.pack(fill='both', expand=True, padx=10, pady=10)

            for dork in self.dorks[category]:
                listbox.insert(tk.END, dork)

            self.dork_listboxes[category] = listbox

        # Button Frame
        button_frame = tk.Frame(self.root, bg=self.bg_color)
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="Delete Dork", width=15, height=2, font=("Courier", 12), bg=self.fg_color, fg='black', command=self.delete_dork).pack(side="left", padx=5)
        tk.Button(button_frame, text="Voice Search", width=15, height=2, font=("Courier", 12), bg=self.fg_color, fg='black', command=self.voice_search).pack(side="left", padx=5)
        tk.Button(button_frame, text="Add More Dork", width=15, height=2, font=("Courier", 12), bg=self.fg_color, fg='black', command=self.add_more_dork).pack(side="left", padx=5)
        tk.Button(self.root, text="Perform Search", width=20, height=2, font=("Courier", 12), bg=self.fg_color, fg='black', command=self.perform_search).pack(pady=10)

        # OSINT Search Section
        osint_frame = tk.Frame(self.root, bg=self.bg_color)
        osint_frame.pack(pady=10, padx=20)

        tk.Label(osint_frame, text="OSINT Query:", font=("Courier", 14), bg=self.bg_color, fg=self.fg_color).pack(side="left", padx=10)
        self.osint_entry = tk.Entry(osint_frame, width=40, font=("Courier", 14), borderwidth=2, relief="flat")
        self.osint_entry.pack(side="left", padx=10)

        tk.Button(osint_frame, text="OSINT Search", width=20, height=2, font=("Courier", 12), bg=self.fg_color, fg='black', command=self.osint_search).pack(side="left", padx=10)

        terminal_frame = tk.Frame(self.root, bg=self.bg_color)
        terminal_frame.pack(pady=10, padx=20, fill='both', expand=True)

        tk.Label(terminal_frame, text="Terminal Output:", font=("Courier", 14), bg=self.bg_color, fg=self.fg_color).pack(pady=10)

        self.terminal = Text(terminal_frame, font=("Courier", 12), bg=self.bg_color, fg=self.fg_color, height=15)
        self.terminal.pack(fill='both', expand=True)

    def filter_dorks(self, event):
        search_text = self.dork_search_entry.get().lower()
        for category, listbox in self.dork_listboxes.items():
            listbox.delete(0, tk.END)
            for dork in self.dorks[category]:
                if search_text in dork.lower():
                    listbox.insert(tk.END, dork)

    def delete_dork(self):
        category = self.tabs.tab(self.tabs.select(), "text")
        listbox = self.dork_listboxes[category]
        selected_indices = listbox.curselection()

        if not selected_indices:
            messagebox.showwarning("Selection Error", "Please select a dork to delete.")
            return

        for index in reversed(selected_indices):  # Delete from the end to avoid index shifting
            dork_to_delete = self.dorks[category][index]
            del self.dorks[category][index]
            listbox.delete(index)
            self.log_to_terminal(f"Deleted dork from {category}: {dork_to_delete}")

    def voice_search(self):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            self.log_to_terminal("Say your search query!")
            audio = r.listen(source)

        try:
            query = r.recognize_google(audio)
            self.log_to_terminal(f"You said: {query}")
            self.entry.delete(0, tk.END)  # Clear the entry field
            self.entry.insert(0, query)  # Insert the voice query
        except sr.UnknownValueError:
            self.log_to_terminal("Google Speech Recognition could not understand audio")
            messagebox.showerror("Error", "Could not understand audio. Please try again.")
        except sr.RequestError as e:
            self.log_to_terminal(f"Could not request results from Google Speech Recognition service; {e}")
            messagebox.showerror("Error", f"Could not request results from Google Speech Recognition service; {e}")

    def add_more_dork(self):
        category = simpledialog.askstring("Add Dork", "Enter the category (e.g., Daily purpose, People needs, Public BBH, Other Sensitive Info, etc.):")
        if not category or category not in self.dorks:
            messagebox.showerror("Error", "Invalid category! Please enter a valid category.")
            return

        new_dork = simpledialog.askstring("Add Dork", "Enter the new dork:")
        if not new_dork:
            messagebox.showerror("Error", "Dork cannot be empty.")
            return

        self.dorks[category].append(new_dork)
        self.dork_listboxes[category].insert(tk.END, new_dork)
        self.log_to_terminal(f"Added new dork to {category}: {new_dork}")

    def perform_search(self):
        user_input = self.entry.get().strip()
        if not user_input:
            messagebox.showwarning("Input Error", "Please enter a search term.")
            return

        selected_queries = []
        for category, listbox in self.dork_listboxes.items():
            selected_indices = listbox.curselection()
            selected_queries += [f"{self.dorks[category][i]} {user_input}" for i in selected_indices]

        if not selected_queries:
            messagebox.showwarning("Selection Error", "Please select at least one dork.")
            return

        urls = [f"https://www.google.com/search?q={query}" for query in selected_queries]
        for url in urls:
            self.open_url(url)
            self.log_to_terminal(f"Opening URL: {url}")

    def open_url(self, url):
        browser = self.browser_var.get()
        try:
            if browser == "chrome":
                chrome_path = "C:/Program Files/Google/Chrome/Application/chrome.exe %s"
                webbrowser.get(chrome_path).open_new_tab(url)
            elif browser == "firefox":
                firefox_path = "C:/Program Files/Mozilla Firefox/firefox.exe %s"
                webbrowser.get(firefox_path).open_new_tab(url)
            elif browser == "brave":
                brave_path = "C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe %s"
                webbrowser.get(brave_path).open_new_tab(url)
            else:
                webbrowser.open_new_tab(url)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open browser: {e}")

    def log_to_terminal(self, message):
        self.terminal.insert(tk.END, f"{message}\n")
        self.terminal.see(tk.END)

    def load_osint_data(self, filename):
        try:
            with open(filename, 'r') as f:
                self.osint_data = json.load(f)
            self.log_to_terminal(f"OSINT data loaded from {filename}")
        except FileNotFoundError:
            self.osint_data = {}
            self.log_to_terminal(f"OSINT data file {filename} not found.  Starting with empty data.")
        except json.JSONDecodeError:
            self.osint_data = {}
            self.log_to_terminal(f"Error decoding JSON from {filename}. Starting with empty data.")

    def osint_search(self):
        query = self.osint_entry.get().strip().lower()  # Convert query to lowercase for case-insensitive matching

        if not query:
            messagebox.showwarning("Input Error", "Please enter a query for OSINT search.")
            return

        if query in self.osint_data:
            result = self.osint_data[query]
            self.log_to_terminal(f"OSINT Result for '{query}': {result}")
            messagebox.showinfo("OSINT Result", result)  # Display the result in a message box
        else:
            self.log_to_terminal(f"No OSINT data found for '{query}'")
            messagebox.showinfo("OSINT Result", f"No data found for '{query}' in the OSINT database.")

if __name__ == "__main__":
    root = tk.Tk()
    app = DorkNetTool(root)
    root.mainloop()
