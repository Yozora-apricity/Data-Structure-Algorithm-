import tkinter as tk
from tkinter import ttk, messagebox
import random
import time
import sys  # Added for safe exit

# --- INTERNAL LOGIC ---

class Car:
    def __init__(self, plate_number=None):
        if plate_number:
            self.plate_number = plate_number
        else:
            self.plate_number = f"{random.randint(100, 999)}-{random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')}{random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')}"
        
        self.arrivals = 0
        self.departures = 0

    def __str__(self):
        return f"Car({self.plate_number})"

class Stack:
    def __init__(self):
        self.stack = []

    def push(self, car):
        self.stack.append(car)

    def pop(self):
        if not self.isEmpty():
            return self.stack.pop()
        return None

    def peek(self):
        if not self.isEmpty():
            return self.stack[-1]
        return None

    def isEmpty(self):
        return len(self.stack) == 0

    def size(self):
        return len(self.stack)

# --- UI CODE ---

class StackUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Stack Parking Simulation (LIFO)")
        
        # --- FULL SCREEN SETTINGS ---
        self.root.attributes('-fullscreen', True)
        self.root.bind("<Escape>", self.exit_app) # Press ESC to quit
        self.root.protocol("WM_DELETE_WINDOW", self.exit_app)
        
        self.running = True # Flag to track if app is running

        # --- FORMAL LIGHT PALETTE ---
        self.bg_main = "#F0F2F5"    # Soft Light Grey
        self.bg_white = "#FFFFFF"   # Pure White
        self.fg_navy = "#1A237E"    # Deep Navy
        self.fg_slate = "#2C3E50"   # Dark Slate
        
        self.root.configure(bg=self.bg_main)

        # Initialize Stacks
        self.stack = Stack()       # Main Parking Lane
        self.temp_stack = Stack()  # Auxiliary/Temporary Lane
        self.MAX_CAPACITY = 10

        # --- Main Layout Container ---
        self.main_container = tk.Frame(self.root, bg=self.bg_main)
        self.main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # --- Left Panel (Visualization & Controls) ---
        self.left_panel = tk.Frame(self.main_container, bg=self.bg_main)
        self.left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 20))

        # --- Right Panel (Dashboard) ---
        self.right_panel = tk.Frame(self.main_container, bg=self.bg_white, width=400, relief=tk.RIDGE, bd=1)
        self.right_panel.pack(side=tk.RIGHT, fill=tk.Y)
        self.right_panel.pack_propagate(False) 

        # ==========================================
        # LEFT PANEL CONTENT
        # ==========================================

        # Title
        tk.Label(
            self.left_panel, 
            text="LIFO STACK PARKING SIMULATION", 
            font=("Georgia", 24, "bold"), 
            bg=self.bg_main,
            fg=self.fg_navy
        ).pack(pady=20)

        # --- Controls Frame ---
        control_frame = tk.Frame(self.left_panel, bg=self.bg_white, padx=15, pady=15, bd=1, relief="ridge")
        control_frame.pack(fill=tk.X, padx=20, pady=10)
        
        # Button Style
        btn_style = {
            "font": ("Georgia", 10, "bold"),
            "bg": self.bg_white,
            "fg": self.fg_slate,
            "bd": 4,
            "relief": "raised",
            "cursor": "hand2"
        }

        # Row 1: Push Operations
        row1 = tk.Frame(control_frame, bg=self.bg_white)
        row1.pack(anchor="center", pady=5)
        
        tk.Label(row1, text="Plate:", bg=self.bg_white, font=("Georgia", 12), fg=self.fg_slate).pack(side=tk.LEFT, padx=5)
        self.plate_entry = tk.Entry(row1, width=15, font=("Georgia", 12), bd=2)
        self.plate_entry.pack(side=tk.LEFT, padx=5)
        
        tk.Button(row1, text="Arrive (Manual)", command=self.push_manual, **btn_style).pack(side=tk.LEFT, padx=5)
        tk.Button(row1, text="Arrive (Random)", command=self.push_random, **btn_style).pack(side=tk.LEFT, padx=5)

        # Row 2: Pop/Remove Operations
        row2 = tk.Frame(control_frame, bg=self.bg_white)
        row2.pack(anchor="center", pady=5)

        tk.Button(row2, text="Depart (Pop Top)", command=self.pop_car, **btn_style).pack(side=tk.LEFT, padx=5)
        
        tk.Label(row2, text="Remove Plate:", bg=self.bg_white, font=("Georgia", 12), fg=self.fg_slate).pack(side=tk.LEFT, padx=5)
        self.remove_entry = tk.Entry(row2, width=15, font=("Georgia", 12), bd=2)
        self.remove_entry.pack(side=tk.LEFT, padx=5)
        tk.Button(row2, text="Remove Specific (Animate)", command=self.remove_specific_animated, **btn_style).pack(side=tk.LEFT, padx=5)

        # Row 3: Info Display
        self.info_label = tk.Label(
            control_frame, 
            text=f"Total Cars: 0 / {self.MAX_CAPACITY}", 
            bg=self.bg_white, 
            fg=self.fg_navy,
            font=("Georgia", 12, "italic")
        )
        self.info_label.pack(anchor="center", pady=5)

        # --- Canvas for Visualization ---
        self.canvas = tk.Canvas(
            self.left_panel, 
            bg=self.bg_white, 
            highlightthickness=1, 
            highlightbackground=self.fg_slate
        )
        self.canvas.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        
        self.canvas.bind("<Configure>", lambda event: self.update_display())

        # ==========================================
        # RIGHT PANEL CONTENT (DASHBOARD)
        # ==========================================

        tk.Label(
            self.right_panel, 
            text="PARKING DASHBOARD", 
            font=("Georgia", 16, "bold"), 
            bg=self.bg_white,
            fg=self.fg_navy
        ).pack(pady=(20, 15))

        tk.Label(
            self.right_panel, 
            text="Press ESC to Exit Full Screen", 
            font=("Georgia", 10, "italic"), 
            bg=self.bg_white,
            fg="red"
        ).pack(pady=(0, 10))

        # Treeview Styles
        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Georgia", 11, "bold"))
        style.configure("Treeview", font=("Georgia", 11), rowheight=28)

        # Dashboard Table
        columns = ("Slot", "Plate", "Arrivals", "Departures")
        self.dashboard_tree = ttk.Treeview(self.right_panel, columns=columns, show="headings", selectmode="none")
        
        # Define Columns
        self.dashboard_tree.heading("Slot", text="Slot")
        self.dashboard_tree.column("Slot", width=50, anchor="center")
        
        self.dashboard_tree.heading("Plate", text="Plate Number")
        self.dashboard_tree.column("Plate", width=120, anchor="center")
        
        self.dashboard_tree.heading("Arrivals", text="Arr")
        self.dashboard_tree.column("Arrivals", width=50, anchor="center")

        self.dashboard_tree.heading("Departures", text="Dep")
        self.dashboard_tree.column("Departures", width=50, anchor="center")

        # Scrollbar for Dashboard
        dash_scroll = ttk.Scrollbar(self.right_panel, orient="vertical", command=self.dashboard_tree.yview)
        self.dashboard_tree.configure(yscrollcommand=dash_scroll.set)
        
        self.dashboard_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(10, 0), pady=10)
        dash_scroll.pack(side=tk.RIGHT, fill=tk.Y, padx=(0, 10), pady=10)

    # ==========================================
    # LOGIC
    # ==========================================
    
    def exit_app(self, event=None):
        """Safely exits the application."""
        self.running = False
        try:
            self.root.destroy()
        except tk.TclError:
            pass
        sys.exit(0)

    def draw_car(self, car, x_center, y_bottom, car_width=200, car_height=50):
        if car_height < 5: return

        start_x = x_center - (car_width // 2)
        y_pos = y_bottom - car_height 
        
        body_color = "#1976D2"   
        cabin_color = "#BBDEFB"
        
        cabin_h = car_height * 0.4
        body_h = car_height * 0.6
        cabin_margin = car_width * 0.2

        try:
            # Cabin
            cabin_coords = [
                start_x + cabin_margin, y_pos,                          
                start_x + car_width - cabin_margin, y_pos,              
                start_x + car_width - (cabin_margin/2), y_pos + cabin_h, 
                start_x + (cabin_margin/2), y_pos + cabin_h             
            ]
            self.canvas.create_polygon(cabin_coords, fill=cabin_color, outline=self.fg_slate)

            # Body
            body_y_start = y_pos + cabin_h
            self.canvas.create_rectangle(
                start_x, body_y_start,
                start_x + car_width, body_y_start + body_h,
                fill=body_color, outline=self.fg_slate
            )

            # Wheels
            wheel_radius = min(10, car_height * 0.2)
            wheel_y_center = body_y_start + body_h
            self.canvas.create_oval(start_x + 30 - wheel_radius, wheel_y_center - wheel_radius, 
                                    start_x + 30 + wheel_radius, wheel_y_center + wheel_radius, fill="black")
            self.canvas.create_oval(start_x + car_width - 30 - wheel_radius, wheel_y_center - wheel_radius, 
                                    start_x + car_width - 30 + wheel_radius, wheel_y_center + wheel_radius, fill="black")
            
            # Text
            if car_height > 20:
                info_text = f"{car.plate_number} | A:{car.arrivals} D:{car.departures}"
                font_size = max(7, int(car_height * 0.25))
                self.canvas.create_text(x_center, body_y_start + (body_h / 2), text=info_text, 
                                        fill="white", font=("Arial", font_size, "bold"))
        except tk.TclError:
            pass # Suppress drawing errors if window closed

    def draw_lane_structure(self, x_center, bottom_y, width, height, label):
        try:
            c_left = x_center - (width // 2) - 10
            c_right = x_center + (width // 2) + 10
            c_top = bottom_y - height - 10
            
            self.canvas.create_line(
                c_left, c_top, c_left, bottom_y, c_right, bottom_y, c_right, c_top,
                width=5, fill="#555555", capstyle="round"
            ) # type: ignore
            self.canvas.create_text(x_center, bottom_y + 20, text=label, fill="#555555", font=("Arial", 10, "bold"))
        except tk.TclError:
            pass

    def update_dashboard(self):
        try:
            for item in self.dashboard_tree.get_children():
                self.dashboard_tree.delete(item)
            
            current_size = self.stack.size()
            for i, car in enumerate(reversed(self.stack.stack)):
                slot_number = current_size - i
                self.dashboard_tree.insert("", "end", values=(slot_number, car.plate_number, car.arrivals, car.departures))
        except tk.TclError:
            pass

    def update_display(self):
        if not self.running: return

        try:
            self.canvas.delete("all")
            self.info_label.config(text=f"Total Cars: {self.stack.size()} / {self.MAX_CAPACITY}")
            
            # Update Dashboard
            self.update_dashboard()

            w = self.canvas.winfo_width()
            h = self.canvas.winfo_height()
            
            if h < 100: h = 500
            if w < 100: w = 860

            # Dynamic Scaling
            top_margin = 40
            bottom_margin = 60
            available_height = h - top_margin - bottom_margin

            default_car_h = 50
            default_gap = 15
            
            required_height_per_car = default_car_h + default_gap
            total_required_height = self.MAX_CAPACITY * required_height_per_car

            if available_height < total_required_height:
                scale_factor = available_height / total_required_height
                car_h = int(default_car_h * scale_factor)
                gap = int(default_gap * scale_factor)
                
                if car_h < 25: car_h = 25
                if gap < 2: gap = 2
            else:
                car_h = default_car_h
                gap = default_gap

            car_w = 200 
            stack_height_pixels = self.MAX_CAPACITY * (car_h + gap)
            lane_bottom_y = h - bottom_margin
            
            center_main = w * 0.33  
            center_temp = w * 0.66  

            self.draw_lane_structure(center_main, lane_bottom_y, car_w, stack_height_pixels, "MAIN PARKING (LIFO)")
            
            for i, car in enumerate(self.stack.stack):
                y_loc = lane_bottom_y - (i * (car_h + gap)) - 5 
                self.draw_car(car, center_main, y_loc, car_width=car_w, car_height=car_h)

            self.draw_lane_structure(center_temp, lane_bottom_y, car_w, stack_height_pixels, "AUXILIARY / TEMP")

            for i, car in enumerate(self.temp_stack.stack):
                y_loc = lane_bottom_y - (i * (car_h + gap)) - 5
                self.draw_car(car, center_temp, y_loc, car_width=car_w, car_height=car_h)

            if self.stack.isEmpty() and self.temp_stack.isEmpty():
                self.canvas.create_text(center_main, h/2, text=" BAY EMPTY", fill="gray", font=("Georgia", 14, "italic"))
        
        except tk.TclError:
            pass # Ignore errors if updates happen while closing

    def push_manual(self):
        if self.stack.size() >= self.MAX_CAPACITY:
            messagebox.showwarning("Parking Full", f"The parking lot is full.")
            return

        plate = self.plate_entry.get().strip().upper()
        if not plate:
            messagebox.showwarning("Input Error", "Enter a plate number.")
            return
        
        new_car = Car(plate)
        new_car.arrivals += 1 
        self.stack.push(new_car)
        self.plate_entry.delete(0, tk.END)
        self.update_display()

    def push_random(self):
        if self.stack.size() >= self.MAX_CAPACITY:
            messagebox.showwarning("Parking Full", "Parking lot is full.")
            return
        new_car = Car() 
        new_car.arrivals += 1
        self.stack.push(new_car)
        self.update_display()

    def pop_car(self):
        car = self.stack.pop()
        if car:
            car.departures += 1
            messagebox.showinfo("Departed", f"Car {car.plate_number} departed.")
            self.update_display()
        else:
            messagebox.showinfo("Info", "No cars to depart.")

    def remove_specific_animated(self):
        target = self.remove_entry.get().strip().upper()
        if not target:
            messagebox.showwarning("Input", "Enter plate to remove.")
            return
        
        if self.stack.isEmpty():
            messagebox.showinfo("Info", "Lane is empty.")
            return

        found = False
        
        # Phase 1: Search and move to temp
        while not self.stack.isEmpty():
            if not self.running: return # Safety Check

            top_car = self.stack.peek()
            if top_car is None: break
            
            if top_car.plate_number == target:
                found = True
                break 
            else:
                moving_car = self.stack.pop()
                if moving_car: 
                    moving_car.departures += 1
                    self.temp_stack.push(moving_car)
                
                self.update_display()
                try:
                    self.root.update() 
                except tk.TclError:
                    return
                time.sleep(0.5)    

        # Phase 2: Remove Target or Restore
        if found:
            if not self.running: return
            removed_car = self.stack.pop()
            if removed_car:
                removed_car.departures += 1
                messagebox.showinfo("Found", f"Car {removed_car.plate_number} is leaving now.")
            
            self.update_display()
            try:
                self.root.update()
            except tk.TclError:
                return
            time.sleep(0.5)
        else:
            messagebox.showerror("Not Found", f"Car {target} not found. Moving cars back.")

        # Phase 3: Restore from temp
        while not self.temp_stack.isEmpty():
            if not self.running: return

            return_car = self.temp_stack.pop()
            if return_car: 
                return_car.arrivals += 1
                self.stack.push(return_car)
            
            self.update_display()
            try:
                self.root.update()
            except tk.TclError:
                return
            time.sleep(0.5)
        
        self.remove_entry.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = StackUI(root)
    root.mainloop()