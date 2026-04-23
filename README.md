# Data Structures & Algorithms Visualizer

A comprehensive collection of interactive Python visualizations for fundamental data structures and algorithms. This project utilizes **Tkinter** and **Pygame** to demonstrate concepts such as Queues, Stacks, Recursion, and Trees in a graphical user interface.

## 👤 Author
* **Gerald Tan**

## 👥 Collaborators
* **[Francisco Pedrigal III](https://github.com/Fabongita)**
* **[Samantha Angel Valderama](https://github.com/samvalderama29)**
* **[Aira Villarito](https://github.com/ventyunquarters)**

---

## 🚀 Project Overview

This system allows users to interact with and visualize the logic behind the following computer science concepts:

### 1. Car Parking Simulation (Queue & Stack)
A simulation of a parking management system demonstrating two distinct data structures:
* **FIFO Queue (First-In, First-Out):** visualized as a drive-through parking lane where cars exit in the order they arrived.
* **LIFO Stack (Last-In, First-Out):** visualized as a single-entry parking lane where the last car to enter must be the first to leave.
* **Features:** Manual/Random car arrival, plate number generation, animated entry/exit, and a real-time dashboard.

### 2. Tower of Hanoi (Recursion)
A Pygame-based visualization of the classic recursive problem.
* **Features:** Solves the puzzle for 3 to 8 disks. Includes controls for animation speed (Slow, Normal, Fast, Turbo), a move counter, and a "Skip to Result" option.

### 3. Binary Tree Logic
An educational tool for understanding Binary Trees.
* **Features:** Construct trees level-by-level (up to 5 levels), input custom node values, and visualize Pre-order, In-order, and Post-order traversals.

### 4. Binary Search Tree (BST)
A fully interactive BST visualizer.
* **Features:** Insert nodes, generate random trees, search for specific values, delete nodes, and view traversal paths (LTR, TLR, LRT) dynamically.

---

## 🛠️ Technologies Used
* **Python 3.x**
* **Tkinter:** Built-in Python GUI library (used for Menus, Data Visual, and Trees).
* **Pygame:** Library for multimedia applications (used for Tower of Hanoi).

---

## 📦 Installation & Setup

1.  **Clone or Download** the repository to your local machine.
2.  **Install Dependencies:**
    Most modules use `tkinter` (included with Python), but the Tower of Hanoi module requires `pygame`.
    ```bash
    pip install pygame
    ```
3.  **Directory Structure:**
    Ensure your folders are organized as follows so the scripts can find their dependencies:
    ```text
    /Project_Root
    │── main_menu.py
    │── recursion.py
    │── binary_tree.py
    │── binary_search_tree.py
    │── README.md
    │
    └── /car_parking_simulation
        │── plate_number_generator.py
        │── car_park_queue.py
        │── car_park_stack.py
        └── /user_interface
            │── queue_ui.py
            └── stack_ui.py
    ```

---

##  ▶️ How to Run

To start the application, run the **Main Menu**. This acts as the command center to launch all other modules.

```bash
python main_menu.py
