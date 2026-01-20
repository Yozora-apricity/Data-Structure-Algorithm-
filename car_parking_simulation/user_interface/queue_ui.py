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
            else f"{random.randint(100,999)}-"
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
        self.root.title("Queue Parking Simulation (FIFO)")
        self.root.geometry("900x750")
        self.root.configure(bg="#f0f0f0")

        self.queue = Queue()
        self.MAX_CAPACITY = 8

        # Title
        tk.Label(
            self.root,
            text="FIFO Queue Parking Simulation",
            font=("Arial", 20, "bold"),
            bg="#f0f0f0"
        ).pack(pady=10)

        # Controls
        control_frame = tk.Frame(self.root, bg="#d9d9d9", padx=10, pady=10)
        control_frame.pack(fill=tk.X, padx=20, pady=10)

        row1 = tk.Frame(control_frame, bg="#d9d9d9")
        row1.pack(fill=tk.X, pady=5)

        tk.Label(row1, text="Plate:", bg="#d9d9d9").pack(side=tk.LEFT)
        self.plate_entry = ttk.Entry(row1, width=15)
        self.plate_entry.pack(side=tk.LEFT, padx=5)

        ttk.Button(row1, text="Arrive (Manual)", command=self.push_manual).pack(side=tk.LEFT, padx=5)
        ttk.Button(row1, text="Arrive (Random)", command=self.push_random).pack(side=tk.LEFT, padx=5)

        row2 = tk.Frame(control_frame, bg="#d9d9d9")
        row2.pack(fill=tk.X, pady=5)

        tk.Label(row2, text="Remove Plate:", bg="#d9d9d9").pack(side=tk.LEFT)
        self.remove_entry = ttk.Entry(row2, width=15)
        self.remove_entry.pack(side=tk.LEFT, padx=5)

        ttk.Button(
            row2,
            text="Remove Specific (Animate)",
            command=self.remove_specific_animated
        ).pack(side=tk.LEFT, padx=5)

        self.info_label = tk.Label(
            control_frame,
            text=f"Total Cars: 0 / {self.MAX_CAPACITY}",
            bg="#d9d9d9",
            font=("Arial", 10)
        )
        self.info_label.pack(anchor="w", pady=5)

        # Canvas
        self.canvas = tk.Canvas(
            self.root,
            bg="white",
            highlightthickness=1,
            highlightbackground="black"
        )
        self.canvas.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        self.canvas.bind("<Configure>", lambda e: self.update_display())
        #drawing

    def draw_car(self, car, x_center, y_bottom, car_width=200, car_height=50):
        start_x = x_center - car_width // 2
        y_top = y_bottom - car_height

        cabin_h = car_height * 0.4
        body_h = car_height * 0.6
        cabin_margin = car_width * 0.2

        # Cabin
        self.canvas.create_polygon(
            start_x + cabin_margin, y_top,
            start_x + car_width - cabin_margin, y_top,
            start_x + car_width - cabin_margin / 2, y_top + cabin_h,
            start_x + cabin_margin / 2, y_top + cabin_h,
            fill="#8abef0", outline="black"
        )

        # Body
        self.canvas.create_rectangle(
            start_x, y_top + cabin_h,
            start_x + car_width, y_top + cabin_h + body_h,
            fill="#4a90e2", outline="black"
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
            font=("Arial", 9, "bold")
        )

    def draw_lane(self, x_center, bottom_y, width, height):
        left = x_center - width // 2 - 10
        right = x_center + width // 2 + 10
        top = bottom_y - height - 10

        self.canvas.create_line(left, top, left, bottom_y, width=5, fill="#555555")
        self.canvas.create_line(right, top, right, bottom_y, width=5, fill="#555555")

    #display

    def update_display(self):
        self.canvas.delete("all")
        self.info_label.config(text=f"Total Cars: {self.queue.size()} / {self.MAX_CAPACITY}")

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
                text="Empty",
                fill="gray",
                font=("Arial", 14)
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

        car = Car()
        self.queue.enqueue(car)
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

            if car.plate_number == target:
                messagebox.showinfo("Removed", f"Car {car.plate_number} permanently departs.")
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
