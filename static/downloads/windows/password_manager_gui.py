import tkinter as tk
from tkinter import ttk, messagebox
import json
from password_manager import PasswordManager

class PasswordManagerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("SOManager")
        self.root.geometry("600x400")
        self.root.configure(bg='#2d2d2d')
        
        self.password_manager = PasswordManager()
        self.setup_styles()
        self.create_widgets()
        
        # Start with login frame
        self.show_login_frame()

    def setup_styles(self):
        # Configure dark theme styles
        style = ttk.Style()
        style.configure('TFrame', background='#2d2d2d')
        style.configure('TLabel', background='#2d2d2d', foreground='white')
        style.configure('TButton', padding=5)
        style.configure('TEntry', padding=5)

    def create_widgets(self):
        # Login Frame
        self.login_frame = ttk.Frame(self.root)
        ttk.Label(self.login_frame, text="Enter Master Password").pack(pady=20)
        self.master_password_entry = ttk.Entry(self.login_frame, show="*")
        self.master_password_entry.pack(pady=10)
        ttk.Button(self.login_frame, text="Unlock", command=self.unlock_manager).pack(pady=10)

        # Main Frame
        self.main_frame = ttk.Frame(self.root)
        
        # Add Credentials Section
        add_frame = ttk.Frame(self.main_frame)
        add_frame.pack(pady=20, padx=20, fill='x')
        
        ttk.Label(add_frame, text="Add New Credentials").pack()
        
        site_frame = ttk.Frame(add_frame)
        site_frame.pack(fill='x', pady=5)
        ttk.Label(site_frame, text="Website:").pack(side='left', padx=5)
        self.site_entry = ttk.Entry(site_frame)
        self.site_entry.pack(side='left', expand=True, fill='x', padx=5)
        
        username_frame = ttk.Frame(add_frame)
        username_frame.pack(fill='x', pady=5)
        ttk.Label(username_frame, text="Username:").pack(side='left', padx=5)
        self.username_entry = ttk.Entry(username_frame)
        self.username_entry.pack(side='left', expand=True, fill='x', padx=5)
        
        password_frame = ttk.Frame(add_frame)
        password_frame.pack(fill='x', pady=5)
        ttk.Label(password_frame, text="Password:").pack(side='left', padx=5)
        self.password_entry = ttk.Entry(password_frame, show="*")
        self.password_entry.pack(side='left', expand=True, fill='x', padx=5)
        
        ttk.Button(add_frame, text="Save Credentials", command=self.save_credentials).pack(pady=10)
        
        # View Credentials Section
        view_frame = ttk.Frame(self.main_frame)
        view_frame.pack(pady=20, padx=20, fill='both', expand=True)
        
        ttk.Label(view_frame, text="Stored Credentials").pack()
        
        self.sites_listbox = tk.Listbox(view_frame, bg='#3d3d3d', fg='white')
        self.sites_listbox.pack(pady=10, fill='both', expand=True)
        self.sites_listbox.bind('<Double-Button-1>', self.view_credential)
        
        button_frame = ttk.Frame(view_frame)
        button_frame.pack(fill='x', pady=5)
        ttk.Button(button_frame, text="View", command=lambda: self.view_credential(None)).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Delete", command=self.delete_credential).pack(side='left', padx=5)

    def show_login_frame(self):
        self.main_frame.pack_forget()
        self.login_frame.pack(expand=True)
        self.master_password_entry.focus()

    def show_main_frame(self):
        self.login_frame.pack_forget()
        self.main_frame.pack(expand=True, fill='both')
        self.update_sites_list()

    def unlock_manager(self):
        try:
            self.password_manager.initialize(self.master_password_entry.get())
            self.show_main_frame()
        except ValueError as e:
            messagebox.showerror("Error", str(e))
        self.master_password_entry.delete(0, tk.END)

    def save_credentials(self):
        site = self.site_entry.get()
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        if not all([site, username, password]):
            messagebox.showerror("Error", "Please fill in all fields")
            return
        
        try:
            self.password_manager.add_credential(site, username, password)
            self.update_sites_list()
            self.clear_entries()
            messagebox.showinfo("Success", "Credentials saved successfully")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def view_credential(self, event):
        if not self.sites_listbox.curselection():
            messagebox.showwarning("Warning", "Please select a site")
            return
            
        site = self.sites_listbox.get(self.sites_listbox.curselection())
        try:
            cred = self.password_manager.get_credential(site)
            messagebox.showinfo("Credentials", 
                              f"Site: {site}\nUsername: {cred['username']}\nPassword: {cred['password']}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def delete_credential(self):
        if not self.sites_listbox.curselection():
            messagebox.showwarning("Warning", "Please select a site")
            return
            
        site = self.sites_listbox.get(self.sites_listbox.curselection())
        if messagebox.askyesno("Confirm", f"Delete credentials for {site}?"):
            try:
                self.password_manager.delete_credential(site)
                self.update_sites_list()
                messagebox.showinfo("Success", "Credentials deleted successfully")
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def update_sites_list(self):
        self.sites_listbox.delete(0, tk.END)
        for site in self.password_manager.list_sites():
            self.sites_listbox.insert(tk.END, site)

    def clear_entries(self):
        self.site_entry.delete(0, tk.END)
        self.username_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)

def main():
    root = tk.Tk()
    app = PasswordManagerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
