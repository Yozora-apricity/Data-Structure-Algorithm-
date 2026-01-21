import tkinter as tk
from tkinter import messagebox
import os
import sys
import subprocess

class ParkingMenu:
    """Sub-menu triggered by the Main Menu for parking options."""
    def __init__(self, parent):
        self.window = tk.Toplevel(parent)
        self.window.title("Parking System Selection")
        self.window.geometry("600x500")
        
        # --- Color Palette ---
        self.bg_white = "#FFFFFF"
        self.fg_navy = "#1A237E"
        self.fg_slate = "#2C3E50"
        self.btn_bg = "#FFFFFF"
        self.accent_blue = "#E3F2FD"
        
        self.window.configure(bg=self.bg_white)
        self.center_window(600, 500)
        
        # --- Header ---
        tk.Label(
            self.window,
            text="PARKING SYSTEM SELECTION",
            font=("Georgia", 24, "bold"),
            fg=self.fg_navy,
            bg=self.bg_white
        ).pack(pady=40)
        
        tk.Label(
            self.window,
            text="Choose Parking Implementation",
            font=("Georgia", 10, "italic"),
            bg=self.bg_white,
            fg=self.fg_slate
        ).pack(pady=(0, 30))
        
        # --- Button Style ---
        btn_style = {
            "font": ("Georgia", 13, "bold"),
            "bg": self.btn_bg,
            "fg": self.fg_slate,
            "activebackground": self.accent_blue,
            "activeforeground": self.fg_navy,
            "width": 30,
            "height": 2,
            "bd": 6,
            "relief": "raised",
            "cursor": "hand2"
        }
        
        # --- Parking Options ---
        self.create_button("Queue Parking (FIFO)", lambda: self.launch_parking_module("queue_ui.py"), btn_style)
        self.create_button("Stack Parking (LIFO)", lambda: self.launch_parking_module("stack_ui.py"), btn_style)
        
        # Back Button
        btn_back = tk.Button(
            self.window,
            text="BACK TO MAIN MENU",
            command=self.window.destroy,
            font=("Georgia", 11, "bold"),
            bg="#90A4AE",
            fg="white",
            width=25,
            height=2,
            bd=5,
            relief="raised"
        )
        btn_back.pack(pady=40)
    
    def create_button(self, text, command, style):
        btn = tk.Button(self.window, text=text, command=command, **style)
        btn.pack(pady=8)
        btn.bind("<Enter>", lambda e: btn.config(bg=self.accent_blue))
        btn.bind("<Leave>", lambda e: btn.config(bg=self.btn_bg))
    
    def center_window(self, width, height):
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        self.window.geometry(f'{width}x{height}+{x}+{y}')
    
    def launch_parking_module(self, filename):
        # Updated path to include the user_interface folder
        work_dir = os.path.join("car_parking_simulation", "user_interface")
        script_path = os.path.join(work_dir, filename)
        
        # Check if the file exists in the specific sub-folder
        if not os.path.exists(script_path):
            messagebox.showwarning(
                "Access Alert", 
                f"Module '{filename}' is unavailable.\nPath checked: {script_path}"
            )
            return
            
        try:
            # Launch using the correct working directory
            if os.name == 'nt':  # Windows
                # Use shell=True and cwd to ensure Python finds the file
                subprocess.Popen([sys.executable, filename], cwd=work_dir, shell=True)
            else:  # macOS/Linux
                subprocess.Popen([sys.executable, filename], cwd=work_dir)
        except Exception as e:
            messagebox.showerror("Execution Error", f"Failed to launch module:\n{e}")

class MainMenu:
    def __init__(self, root):
        self.root = root
        self.root.title("System Control Interface")
        self.root.geometry("600x750")
        
        self.bg_white = "#FFFFFF"
        self.fg_navy = "#1A237E"
        self.fg_slate = "#2C3E50"
        self.btn_bg = "#FFFFFF"
        self.accent_blue = "#E3F2FD"
        self.exit_red = "#B71C1C"
        
        self.root.configure(bg=self.bg_white)
        self.center_window(600, 750)
        
        # --- Header ---
        tk.Label(self.root, text="________________________________________________", 
                 fg="#CFD8DC", bg=self.bg_white, font=("Arial", 10)).pack(pady=(30, 0))

        tk.Label(self.root, text="COMMAND CENTER", font=("Georgia", 36, "bold"), 
                 fg=self.fg_navy, bg=self.bg_white).pack(pady=10)

        tk.Label(self.root, text="Select Module to Initialize", font=("Georgia", 10, "italic"), 
                 bg=self.bg_white, fg=self.fg_slate).pack(pady=(0, 40))
        
        # --- Button Style ---
        btn_style = {
            "font": ("Georgia", 13, "bold"),
            "bg": self.btn_bg,
            "fg": self.fg_slate,
            "activebackground": self.accent_blue,
            "activeforeground": self.fg_navy,
            "width": 30,
            "height": 2,
            "bd": 6,
            "relief": "raised",
            "cursor": "hand2"
        }

        # --- Module Buttons ---
        self.create_button("Car Parking Simulation", self.launch_parking_sim, btn_style)
        self.create_button("Tower of Hanoi", lambda: self.launch_script("recursion.py"), btn_style)
        self.create_button("Binary Tree Logic", lambda: self.launch_script("binary_tree.py"), btn_style)
        self.create_button("Binary Search Tree", lambda: self.launch_script("binary_search_tree.py"), btn_style)

        # Exit
        tk.Button(self.root, text="TERMINATE SESSION", command=self.root.quit, 
                  font=("Georgia", 11, "bold"), bg=self.exit_red, fg="white", 
                  width=25, height=2, bd=5, relief="raised").pack(pady=60)

    def create_button(self, text, command, style):
        btn = tk.Button(self.root, text=text, command=command, **style)
        btn.pack(pady=8)
        btn.bind("<Enter>", lambda e: btn.config(bg=self.accent_blue)) 
        btn.bind("<Leave>", lambda e: btn.config(bg=self.btn_bg))

    def center_window(self, width, height):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        
    def launch_script(self, filename):
        if not os.path.exists(filename):
            messagebox.showwarning("Access Alert", f"Module '{filename}' not found.")
            return
        subprocess.Popen([sys.executable, filename])
        self.root.destroy()
            
    def launch_parking_sim(self):
        # Instead of launching a script directly, open the sub-menu class
        ParkingMenu(self.root)
        self.root.withdraw()  # Hide main window instead of destroying it
        self.root.after(500, lambda: self.root.destroy() if not self.root.winfo_exists() else None)  # Close after parking menu closes

if __name__ == "__main__":
    root = tk.Tk()
    app = MainMenu(root)
    root.mainloop()