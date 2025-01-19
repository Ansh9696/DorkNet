import tkinter as tk
from tkinter import messagebox, filedialog, StringVar, OptionMenu, Text, ttk, simpledialog
import webbrowser


class DorkNetTool:
    def __init__(self, root):
        self.root = root
        self.root.title("DorkNet - Google Dorks Search Tool")
        self.root.geometry("1000x900")
        self.root.configure(bg='#000000')

        self.dorks = self.initialize_dorks()
        self.create_widgets()

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
        }

    def create_widgets(self):
        top_frame = tk.Frame(self.root, bg='#000000')
        top_frame.pack(pady=10, padx=20, fill='x')

        tk.Label(top_frame, text="Enter search term:", font=("Courier", 14), bg='#000000', fg='white').pack(side="left", padx=10)
        self.entry = tk.Entry(top_frame, width=40, font=("Courier", 14), borderwidth=2, relief="flat")
        self.entry.pack(side="left", padx=10)

        self.browser_var = StringVar(value="default")
        tk.Label(top_frame, text="Browser:", font=("Courier", 14), bg='#000000', fg='white').pack(side="left", padx=10)
        browser_menu = OptionMenu(top_frame, self.browser_var, "default", "chrome", "firefox", "brave")
        browser_menu.config(font=("Courier", 12), bg='#00ff00', fg='black')
        browser_menu.pack(side="left", padx=10)

        tk.Label(top_frame, text="Search dork:", font=("Courier", 14), bg='#000000', fg='white').pack(side="left", padx=10)
        self.dork_search_entry = tk.Entry(top_frame, width=30, font=("Courier", 14), borderwidth=2, relief="flat")
        self.dork_search_entry.pack(side="left", padx=10)
        self.dork_search_entry.bind("<KeyRelease>", self.filter_dorks)

        self.tabs = ttk.Notebook(self.root)
        self.tabs.pack(pady=10, padx=20, fill='both', expand=True)

        self.category_frames = {}
        self.dork_listboxes = {}

        for category in self.dorks.keys():
            frame = tk.Frame(self.tabs, bg='#000000')
            self.tabs.add(frame, text=category)

            self.category_frames[category] = frame

            listbox = tk.Listbox(frame, selectmode=tk.MULTIPLE, font=("Courier", 12), bg='#000000', fg='#00ff00', height=15)
            listbox.pack(fill='both', expand=True, padx=10, pady=10)

            for dork in self.dorks[category]:
                listbox.insert(tk.END, dork)

            self.dork_listboxes[category] = listbox

        tk.Button(self.root, text="Add More Dork", width=20, height=2, font=("Courier", 12), bg='#00ff00', fg='black', command=self.add_more_dork).pack(pady=10)
        tk.Button(self.root, text="Perform Search", width=20, height=2, font=("Courier", 12), bg='#00ff00', fg='black', command=self.perform_search).pack(pady=10)

        terminal_frame = tk.Frame(self.root, bg='#000000')
        terminal_frame.pack(pady=10, padx=20, fill='both', expand=True)

        tk.Label(terminal_frame, text="Terminal Output:", font=("Courier", 14), bg='#000000', fg='white').pack(pady=10)

        self.terminal = Text(terminal_frame, font=("Courier", 12), bg='#000000', fg='#00ff00', height=15)
        self.terminal.pack(fill='both', expand=True)

    def filter_dorks(self, event):
        search_text = self.dork_search_entry.get().lower()
        for category, listbox in self.dork_listboxes.items():
            listbox.delete(0, tk.END)
            for dork in self.dorks[category]:
                if search_text in dork.lower():
                    listbox.insert(tk.END, dork)

    def add_more_dork(self):
        category = simpledialog.askstring("Add Dork", "Enter the category (e.g., Site, InURL, Document):")
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


if __name__ == "__main__":
    root = tk.Tk()
    app = DorkNetTool(root)
    root.mainloop()
