import tkinter as tk
from tkinter import ttk, messagebox
import random
import time

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
        self.root.geometry("1200x750")

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
        self.main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # --- Left Panel (Visualization & Controls) ---
        self.left_panel = tk.Frame(self.main_container, bg=self.bg_main)
        self.left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

        # --- Right Panel (Dashboard) ---
        self.right_panel = tk.Frame(self.main_container, bg=self.bg_white, width=350, relief=tk.RIDGE, bd=1)
        self.right_panel.pack(side=tk.RIGHT, fill=tk.Y)
        self.right_panel.pack_propagate(False)

        # ==========================================
        # LEFT PANEL CONTENT
        # ==========================================

        # Title
        tk.Label(
            self.left_panel,
            text="FIFO QUEUE PARKING SIMULATION",
            font=("Georgia", 20, "bold"),
            bg=self.bg_main,
            fg=self.fg_navy
        ).pack(pady=10)

        # Controls
        control_frame = tk.Frame(self.left_panel, bg=self.bg_white, padx=10, pady=10, bd=1, relief="ridge")
        control_frame.pack(fill=tk.X, padx=20, pady=10)

        # Button Style Config
        btn_config = {
            "font": ("Georgia", 9, "bold"),
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

        tk.Label(inner_row1, text="Plate:", bg=self.bg_white, font=("Georgia", 10), fg=self.fg_slate).pack(side=tk.LEFT, padx=2)
        self.plate_entry = tk.Entry(inner_row1, width=15, font=("Georgia", 10), bd=2)
        self.plate_entry.pack(side=tk.LEFT, padx=2)

        tk.Button(inner_row1, text="Arrive (Manual)", command=self.push_manual, **btn_config).pack(side=tk.LEFT, padx=2)
        tk.Button(inner_row1, text="Arrive (Random)", command=self.push_random, **btn_config).pack(side=tk.LEFT, padx=2)

        row2 = tk.Frame(control_frame, bg=self.bg_white)
        row2.pack(fill=tk.X, pady=5)

        inner_row2 = tk.Frame(row2, bg=self.bg_white)
        inner_row2.pack()

        tk.Label(inner_row2, text="Remove Plate:", bg=self.bg_white, font=("Georgia", 10), fg=self.fg_slate).pack(
            side=tk.LEFT, padx=2)
        self.remove_entry = tk.Entry(inner_row2, width=15, font=("Georgia", 10), bd=2)
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
            font=("Georgia", 10, "italic")
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
            font=("Georgia", 14, "bold"),
            bg=self.bg_white,
            fg=self.fg_navy
        ).pack(pady=(20, 15))

        # Treeview Styles
        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Georgia", 10, "bold"))
        style.configure("Treeview", font=("Georgia", 10), rowheight=25)

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
    # DRAWING & UPDATE LOGIC
    # ===============================

    def draw_car(self, car, x_center, y_bottom, car_width=200, car_height=50):
        start_x = x_center - car_width // 2
        y_top = y_bottom - car_height
        cabin_h, body_h = car_height * 0.4, car_height * 0.6
        cabin_margin = car_width * 0.2

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
        wheel_y = y_top + cabin_h + body_h
        for dx in (30, car_width - 30):
            self.canvas.create_oval(
                start_x + dx - 10, wheel_y - 10,
                start_x + dx + 10, wheel_y + 10,
                fill="black"
            )

        self.canvas.create_text(
            x_center,
            y_top + cabin_h + body_h / 2,
            text=f"{car.plate_number} | A:{car.arrivals} D:{car.departures}",
            fill="white",
            font=("Georgia", 9, "bold")
        )

    def draw_lane(self, x_center, bottom_y, width, height):
        left, right = x_center - width // 2 - 10, x_center + width // 2 + 10
        top = bottom_y - height - 10
        self.canvas.create_line(left, top, left, bottom_y, width=5, fill=self.fg_slate)
        self.canvas.create_line(right, top, right, bottom_y, width=5, fill=self.fg_slate)

    def update_dashboard(self):
        # Updates the Treeview in the right panel with current queue data.
        for item in self.dashboard_tree.get_children():
            self.dashboard_tree.delete(item)
        
        # Populate with current queue items
        # Slot 1 corresponds to the front of the queue (Index 0)
        for i, car in enumerate(self.queue.queue):
            slot_number = i + 1
            self.dashboard_tree.insert("", "end", values=(slot_number, car.plate_number, car.arrivals, car.departures))

    def update_display(self):
        self.canvas.delete("all")
        self.info_label.config(text=f"Total Cars: {self.queue.size()} / {self.MAX_CAPACITY}")
        
        # Updates the Dashboard
        self.update_dashboard()

        w = max(self.canvas.winfo_width(), 860)
        h = max(self.canvas.winfo_height(), 500)

        car_w, car_h, gap = 200, 50, 15
        bottom_y = h - 40
        lane_height = self.MAX_CAPACITY * (car_h + gap)

        center_x = w // 2

        self.draw_lane(center_x, bottom_y, car_w, lane_height)

        for i, car in enumerate(self.queue.queue):
            y = bottom_y - i * (car_h + gap) - 5
            self.draw_car(car, center_x, y)

        if self.queue.is_empty():
            self.canvas.create_text(
                center_x, h / 2,
                text="BAY EMPTY",
                fill="gray",
                font=("Georgia", 14, "italic")
            )

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

        while not self.queue.is_empty():
            car = self.queue.dequeue()
            self.update_display()
            self.root.update()
            time.sleep(0.5)

            if car.plate_number == target: # type: ignore
                messagebox.showinfo("Removed", f"Car {car.plate_number} permanently departs.") # type: ignore
                break
            else:
                departed.append(car)

        for car in departed:
            self.queue.enqueue(car)
            self.update_display()
            self.root.update()
            time.sleep(0.5)

        self.remove_entry.delete(0, tk.END)
# main
if __name__ == "__main__":
    root = tk.Tk()
    QueueUI(root)
    root.mainloop()