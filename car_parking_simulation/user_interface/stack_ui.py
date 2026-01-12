import tkinter as tk
from tkinter import ttk, messagebox
import random
import time

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
        self.root.title("Stack Visualizer (Car Parking)")
        self.root.geometry("1200x750") 
        self.root.configure(bg="#f0f0f0")

        # Initialize Stacks
        self.stack = Stack()       # Main Parking Lane
        self.temp_stack = Stack()  # Auxiliary/Temporary Lane
        self.MAX_CAPACITY = 8 

        # --- Main Layout Container ---
        self.main_container = tk.Frame(self.root, bg="#f0f0f0")
        self.main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # --- Left Panel (Visualization & Controls) ---
        self.left_panel = tk.Frame(self.main_container, bg="#f0f0f0")
        self.left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

        # --- Right Panel (Dashboard) ---
        self.right_panel = tk.Frame(self.main_container, bg="white", width=350, relief=tk.RIDGE, bd=1)
        self.right_panel.pack(side=tk.RIGHT, fill=tk.Y)
        self.right_panel.pack_propagate(False) 

        # ==========================================
        # LEFT PANEL CONTENT
        # ==========================================

        # Title
        tk.Label(
            self.left_panel, 
            text="Stack Parking Simulation", 
            font=("Arial", 20, "bold"), 
            bg="#f0f0f0"
        ).pack(pady=10)

        # --- Controls Frame ---
        control_frame = tk.Frame(self.left_panel, bg="#d9d9d9", padx=10, pady=10)
        control_frame.pack(fill=tk.X, padx=20, pady=10)

        # Row 1: Push Operations
        row1 = tk.Frame(control_frame, bg="#d9d9d9")
        row1.pack(fill=tk.X, pady=5)
        
        tk.Label(row1, text="Plate:", bg="#d9d9d9").pack(side=tk.LEFT)
        self.plate_entry = ttk.Entry(row1, width=15)
        self.plate_entry.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(row1, text="Arrive (Manual)", command=self.push_manual).pack(side=tk.LEFT, padx=5)
        ttk.Button(row1, text="Arrive (Random)", command=self.push_random).pack(side=tk.LEFT, padx=5)

        # Row 2: Pop/Remove Operations
        row2 = tk.Frame(control_frame, bg="#d9d9d9")
        row2.pack(fill=tk.X, pady=5)

        ttk.Button(row2, text="Depart (Pop Top)", command=self.pop_car).pack(side=tk.LEFT, padx=5)
        
        self.remove_entry = ttk.Entry(row2, width=15)
        self.remove_entry.pack(side=tk.LEFT, padx=(20, 5))
        ttk.Button(row2, text="Remove Specific (Animate)", command=self.remove_specific_animated).pack(side=tk.LEFT, padx=5)

        # Row 3: Info Display
        self.info_label = tk.Label(control_frame, text=f"Total Cars: 0 / {self.MAX_CAPACITY}", bg="#d9d9d9", font=("Arial", 10))
        self.info_label.pack(anchor="w", pady=5)

        # --- Canvas for Visualization ---
        self.canvas = tk.Canvas(self.left_panel, bg="white", highlightthickness=1, highlightbackground="black")
        self.canvas.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        
        self.canvas.bind("<Configure>", lambda event: self.update_display())

        # ==========================================
        # RIGHT PANEL CONTENT (DASHBOARD)
        # ==========================================

        tk.Label(
            self.right_panel, 
            text="PARKING DASHBOARD", 
            font=("Arial", 14, "bold"), 
            bg="white",
            fg="#333"
        ).pack(pady=(20, 15))

        # Treeview Styles
        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Arial", 10, "bold"))
        style.configure("Treeview", font=("Arial", 10), rowheight=25)

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

    def draw_car(self, car, x_center, y_bottom, car_width=200, car_height=50):
        start_x = x_center - (car_width // 2)
        y_pos = y_bottom - car_height 
        
        body_color = "#4a90e2"
        cabin_color = "#8abef0"
        
        cabin_h = car_height * 0.4
        body_h = car_height * 0.6
        cabin_margin = car_width * 0.2

        # Cabin
        cabin_coords = [
            start_x + cabin_margin, y_pos,                         
            start_x + car_width - cabin_margin, y_pos,             
            start_x + car_width - (cabin_margin/2), y_pos + cabin_h, 
            start_x + (cabin_margin/2), y_pos + cabin_h            
        ]
        self.canvas.create_polygon(cabin_coords, fill=cabin_color, outline="black")

        # Body
        body_y_start = y_pos + cabin_h
        self.canvas.create_rectangle(
            start_x, body_y_start,
            start_x + car_width, body_y_start + body_h,
            fill=body_color, outline="black"
        )

        # Wheels
        wheel_radius = 10
        wheel_y_center = body_y_start + body_h
        self.canvas.create_oval(start_x + 30 - 10, wheel_y_center - 10, start_x + 30 + 10, wheel_y_center + 10, fill="black")
        self.canvas.create_oval(start_x + car_width - 30 - 10, wheel_y_center - 10, start_x + car_width - 30 + 10, wheel_y_center + 10, fill="black")
        
        # Text
        info_text = f"{car.plate_number} | A:{car.arrivals} D:{car.departures}"
        self.canvas.create_text(x_center, body_y_start + (body_h / 2), text=info_text, fill="white", font=("Arial", 9, "bold"))

    def draw_lane_structure(self, x_center, bottom_y, width, height, label):
        c_left = x_center - (width // 2) - 10
        c_right = x_center + (width // 2) + 10
        c_top = bottom_y - height - 10
        
        self.canvas.create_line(
            c_left, c_top, c_left, bottom_y, c_right, bottom_y, c_right, c_top,
            width=5, fill="#555555", capstyle="round"
        ) # type: ignore
        self.canvas.create_text(x_center, bottom_y + 20, text=label, fill="#555555", font=("Arial", 10, "bold"))

    def update_dashboard(self):
        """Updates the Treeview in the right panel with current stack data."""
        for item in self.dashboard_tree.get_children():
            self.dashboard_tree.delete(item)
        
        # Populate with current stack items
        current_size = self.stack.size()
        for i, car in enumerate(reversed(self.stack.stack)):
            slot_number = current_size - i
            self.dashboard_tree.insert("", "end", values=(slot_number, car.plate_number, car.arrivals, car.departures))

    def update_display(self):
        self.canvas.delete("all")
        self.info_label.config(text=f"Total Cars: {self.stack.size()} / {self.MAX_CAPACITY}")
        
        # Update Dashboard
        self.update_dashboard()

        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
        if h < 100: h = 500
        if w < 100: w = 860

        car_w, car_h, gap = 200, 50, 15
        bottom_margin = 40
        lane_bottom_y = h - bottom_margin
        
        center_main = w * 0.33  
        center_temp = w * 0.66  

        stack_height_pixels = self.MAX_CAPACITY * (car_h + gap)

        # --- DRAW MAIN LANE ---
        self.draw_lane_structure(center_main, lane_bottom_y, car_w, stack_height_pixels, "MAIN PARKING (LIFO)")
        
        for i, car in enumerate(self.stack.stack):
            y_loc = lane_bottom_y - (i * (car_h + gap)) - 5 
            self.draw_car(car, center_main, y_loc)

        # --- DRAW AUXILIARY LANE ---
        self.draw_lane_structure(center_temp, lane_bottom_y, car_w, stack_height_pixels, "AUXILIARY / TEMP")

        for i, car in enumerate(self.temp_stack.stack):
            y_loc = lane_bottom_y - (i * (car_h + gap)) - 5
            self.draw_car(car, center_temp, y_loc)

        if self.stack.isEmpty() and self.temp_stack.isEmpty():
             self.canvas.create_text(center_main, h/2, text="Empty", fill="gray", font=("Arial", 14))

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
            # UPDATE: Manual departure counts as a departure
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
        
        while not self.stack.isEmpty():
            top_car = self.stack.peek()
            
            if top_car is None:
                break
            
            if top_car.plate_number == target:
                found = True
                break 
            else:
                moving_car = self.stack.pop()
                if moving_car: 
                    # UPDATE: Moving to temp lane counts as physical departure
                    moving_car.departures += 1
                    self.temp_stack.push(moving_car)
                
                self.update_display()
                self.root.update() 
                time.sleep(0.5)    

        if found:
            removed_car = self.stack.pop()
            if removed_car:
                # Permanent departure
                removed_car.departures += 1
                messagebox.showinfo("Found", f"Car {removed_car.plate_number} is leaving now.")
            
            self.update_display()
            self.root.update()
            time.sleep(0.5)
        else:
            messagebox.showerror("Not Found", f"Car {target} not found. Moving cars back.")

        while not self.temp_stack.isEmpty():
            return_car = self.temp_stack.pop()
            if return_car: 
                # UPDATE: Returning to main lane counts as re-arrival
                return_car.arrivals += 1
                self.stack.push(return_car)
            
            self.update_display()
            self.root.update()
            time.sleep(0.5)
        
        self.remove_entry.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = StackUI(root)
    root.mainloop()