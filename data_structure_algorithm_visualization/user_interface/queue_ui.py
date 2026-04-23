import tkinter as tk
from tkinter import ttk, messagebox
import random
import time
import sys

# ===============================
# INTERNAL LOGIC
# ===============================

class Car:
    def __init__(self, plate_number=None):
        self.plate_number = (
            plate_number
            if plate_number
            else f"{random.randint(100, 999)}-"
                 f"{random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')}"
                 f"{random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')}"
        )
        self.arrivals = 0
        self.departures = 0

    def __repr__(self):
        return self.plate_number


class Queue:
    def __init__(self):
        self.queue = []

    def enqueue(self, car):
        self.queue.append(car)
        car.arrivals += 1

    def dequeue(self):
        if self.is_empty():
            return None
        car = self.queue.pop(0)
        car.departures += 1
        return car

    def peek(self):
        return None if self.is_empty() else self.queue[0]

    def is_empty(self):
        return len(self.queue) == 0

    def size(self):
        return len(self.queue)


# queue UI

class QueueUI:
    def __init__(self, root):
        self.root = root
        self.root.title("System Control Interface - Parking Module")
        
        # --- FULL SCREEN SETTINGS ---
        self.root.attributes('-fullscreen', True)
        self.root.bind("<Escape>", self.exit_app)
        self.root.protocol("WM_DELETE_WINDOW", self.exit_app)
        self.running = True

        # --- FORMAL THEME COLORS ---
        self.bg_main = "#F0F2F5"  # Soft Light Grey
        self.bg_white = "#FFFFFF"  # Pure White
        self.fg_navy = "#1A237E"  # Deep Navy
        self.fg_slate = "#2C3E50"  # Dark Slate

        self.root.configure(bg=self.bg_main)

        self.queue = Queue()
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
            text="FIFO QUEUE PARKING SIMULATION",
            font=("Georgia", 24, "bold"),
            bg=self.bg_main,
            fg=self.fg_navy
        ).pack(pady=20)

        # Controls
        control_frame = tk.Frame(self.left_panel, bg=self.bg_white, padx=15, pady=15, bd=1, relief="ridge")
        control_frame.pack(fill=tk.X, padx=20, pady=10)

        # Button Style Config
        btn_config = {
            "font": ("Georgia", 10, "bold"),
            "bg": self.bg_white,
            "fg": self.fg_slate,
            "bd": 4,
            "relief": "raised",
            "cursor": "hand2"
        }

        row1 = tk.Frame(control_frame, bg=self.bg_white)
        row1.pack(fill=tk.X, pady=5)

        inner_row1 = tk.Frame(row1, bg=self.bg_white)
        inner_row1.pack()

        tk.Label(inner_row1, text="Plate:", bg=self.bg_white, font=("Georgia", 12), fg=self.fg_slate).pack(side=tk.LEFT, padx=2)
        self.plate_entry = tk.Entry(inner_row1, width=15, font=("Georgia", 12), bd=2)
        self.plate_entry.pack(side=tk.LEFT, padx=2)

        tk.Button(inner_row1, text="Arrive (Manual)", command=self.push_manual, **btn_config).pack(side=tk.LEFT, padx=2)
        tk.Button(inner_row1, text="Arrive (Random)", command=self.push_random, **btn_config).pack(side=tk.LEFT, padx=2)

        row2 = tk.Frame(control_frame, bg=self.bg_white)
        row2.pack(fill=tk.X, pady=5)

        inner_row2 = tk.Frame(row2, bg=self.bg_white)
        inner_row2.pack()

        tk.Label(inner_row2, text="Remove Plate:", bg=self.bg_white, font=("Georgia", 12), fg=self.fg_slate).pack(
            side=tk.LEFT, padx=2)
        self.remove_entry = tk.Entry(inner_row2, width=15, font=("Georgia", 12), bd=2)
        self.remove_entry.pack(side=tk.LEFT, padx=2)

        tk.Button(
            inner_row2,
            text="Remove Specific (Animate)",
            command=self.remove_specific_animated,
            **btn_config
        ).pack(side=tk.LEFT, padx=2)

        self.info_label = tk.Label(
            control_frame,
            text=f"Total Cars: 0 / {self.MAX_CAPACITY}",
            bg=self.bg_white,
            fg=self.fg_navy,
            font=("Georgia", 12, "italic")
        )
        self.info_label.pack(anchor="center", pady=5)

        # Canvas
        self.canvas = tk.Canvas(
            self.left_panel,
            bg=self.bg_white,
            highlightthickness=1,
            highlightbackground=self.fg_slate
        )
        self.canvas.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        self.canvas.bind("<Configure>", lambda _: self.update_display())

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

    # ===============================
    # LOGIC & UTILS
    # ===============================
    
    def exit_app(self, event=None):
        self.running = False
        try:
            self.root.destroy()
        except tk.TclError:
            pass
        sys.exit(0)

    # ===============================
    # DRAWING & UPDATE LOGIC
    # ===============================

    def draw_car(self, car, x_center, y_bottom, car_width=200, car_height=50):
        if car_height < 5: return

        start_x = x_center - car_width // 2
        y_top = y_bottom - car_height
        cabin_h, body_h = car_height * 0.4, car_height * 0.6
        cabin_margin = car_width * 0.2

        try:
            # Cabin
            self.canvas.create_polygon(
                start_x + cabin_margin, y_top,
                start_x + car_width - cabin_margin, y_top,
                start_x + car_width - cabin_margin / 2, y_top + cabin_h,
                start_x + cabin_margin / 2, y_top + cabin_h,
                fill="#BBDEFB", outline=self.fg_slate
            )

            # Body
            self.canvas.create_rectangle(
                start_x, y_top + cabin_h,
                         start_x + car_width, y_top + cabin_h + body_h,
                fill="#1976D2", outline=self.fg_slate
            )

            # Wheels
            wheel_r = min(10, car_height * 0.2)
            wheel_y = y_top + cabin_h + body_h
            
            for dx in (30, car_width - 30):
                self.canvas.create_oval(
                    start_x + dx - wheel_r, wheel_y - wheel_r,
                    start_x + dx + wheel_r, wheel_y + wheel_r,
                    fill="black"
                )

            # Text
            if car_height > 20:
                font_size = max(7, int(car_height * 0.25))
                self.canvas.create_text(
                    x_center,
                    y_top + cabin_h + body_h / 2,
                    text=f"{car.plate_number} | A:{car.arrivals} D:{car.departures}",
                    fill="white",
                    font=("Georgia", font_size, "bold")
                )
        except tk.TclError:
            pass

    def draw_lane(self, x_center, bottom_y, width, height):
        try:
            left, right = x_center - width // 2 - 10, x_center + width // 2 + 10
            top = bottom_y - height - 10
            self.canvas.create_line(left, top, left, bottom_y, width=5, fill=self.fg_slate)
            self.canvas.create_line(right, top, right, bottom_y, width=5, fill=self.fg_slate)
        except tk.TclError:
            pass

    def update_dashboard(self):
        try:
            for item in self.dashboard_tree.get_children():
                self.dashboard_tree.delete(item)
            
            for i, car in enumerate(self.queue.queue):
                slot_number = i + 1
                self.dashboard_tree.insert("", "end", values=(slot_number, car.plate_number, car.arrivals, car.departures))
        except tk.TclError:
            pass

    def update_display(self):
        if not self.running: return

        try:
            self.canvas.delete("all")
            self.info_label.config(text=f"Total Cars: {self.queue.size()} / {self.MAX_CAPACITY}")
            self.update_dashboard()

            w = max(self.canvas.winfo_width(), 860)
            h = max(self.canvas.winfo_height(), 500)

            # --- DYNAMIC SCALING ---
            top_margin = 40
            bottom_margin = 40
            available_height = h - top_margin - bottom_margin

            default_car_h = 50
            default_gap = 15
            
            required_height = self.MAX_CAPACITY * (default_car_h + default_gap)
            
            if available_height < required_height:
                scale = available_height / required_height
                car_h = int(default_car_h * scale)
                gap = int(default_gap * scale)
                if car_h < 25: car_h = 25
                if gap < 2: gap = 2
            else:
                car_h = default_car_h
                gap = default_gap

            car_w = 200
            bottom_y = h - bottom_margin
            lane_height = self.MAX_CAPACITY * (car_h + gap)

            center_x = w // 2

            self.draw_lane(center_x, bottom_y, car_w, lane_height)

            for i, car in enumerate(self.queue.queue):
                y = bottom_y - i * (car_h + gap) - 5
                self.draw_car(car, center_x, y, car_width=car_w, car_height=car_h)

            if self.queue.is_empty():
                self.canvas.create_text(
                    center_x, h / 2,
                    text="BAY EMPTY",
                    fill="gray",
                    font=("Georgia", 14, "italic")
                )
        except tk.TclError:
            pass

    # ===============================
    # QUEUE OPERATIONS
    # ===============================

    def push_manual(self):
        if self.queue.size() >= self.MAX_CAPACITY:
            messagebox.showwarning("Full", "Parking is full.")
            return

        plate = self.plate_entry.get().strip().upper()
        if not plate:
            messagebox.showwarning("Input Error", "Enter plate number.")
            return

        car = Car(plate)
        self.queue.enqueue(car)
        self.plate_entry.delete(0, tk.END)
        self.update_display()

    def push_random(self):
        if self.queue.size() >= self.MAX_CAPACITY:
            messagebox.showwarning("Full", "Parking is full.")
            return
        self.queue.enqueue(Car())
        self.update_display()

    def remove_specific_animated(self):
        target = self.remove_entry.get().strip().upper()
        if not target:
            messagebox.showwarning("Input", "Enter plate to remove.")
            return
        if self.queue.is_empty():
            messagebox.showinfo("Info", "Queue is empty.")
            return

        departed = []

        # Phase 1: Depart
        while not self.queue.is_empty():
            if not self.running: return

            car = self.queue.dequeue()
            self.update_display()
            try:
                self.root.update()
            except tk.TclError:
                return
            time.sleep(0.5)

            if car.plate_number == target: # type: ignore
                messagebox.showinfo("Removed", f"Car {car.plate_number} permanently departs.") # type: ignore
                break
            else:
                departed.append(car)

        # Phase 2: Re-Enter
        for car in departed:
            if not self.running: return
            self.queue.enqueue(car)
            self.update_display()
            try:
                self.root.update()
            except tk.TclError:
                return
            time.sleep(0.5)

        self.remove_entry.delete(0, tk.END)
# main
if __name__ == "__main__":
    root = tk.Tk()
    QueueUI(root)
    root.mainloop()