import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import random
import string
import os
import sys

# --- BINARY TREE LOGIC ---
class BinaryTreeNode:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

def ltr(node): # In-order traversal
    if node is None:
        return []
    else:
        left_node = ltr(node.left)
        current_node = [node.value] if node.value != " " else []
        right_node = ltr(node.right)
        return left_node + current_node + right_node

def tlr(node): # Pre-order traversal
    if node is None:
        return []
    else:
        current_node = [node.value] if node.value != " " else []
        left_node = tlr(node.left)
        right_node = tlr(node.right)
        return current_node + left_node + right_node

def lrt(node): # Post-order traversal
    if node is None:
        return []
    else:
        left_node = lrt(node.left)
        right_node = lrt(node.right)
        current_node = [node.value] if node.value != " " else []
        return left_node + right_node + current_node

class BinaryTreeOrder:
    def __init__(self):
        self.root = None
        self.nodes_list = []

    def tree_level_value(self, char_val):
        self.nodes_list.append(char_val)
        self.tree_level_order(self.nodes_list)

    def tree_level_order(self, values):
        if not values:
            self.root = None
            return
        
        reserved = set()
        for i in range(len(values)):
            if values[i] == " ":
                left_child = 2 * i + 1
                right_child = 2 * i + 2
                reserved.add(left_child)
                reserved.add(right_child)
        
        nodes = [BinaryTreeNode(v) if i not in reserved else None for i, v in enumerate(values)]
        
        for i in range(len(nodes)):
            if nodes[i] is None or values[i] == " ":
                continue
            
            left_idx = 2 * i + 1
            right_idx = 2 * i + 2
            if left_idx < len(nodes):
                nodes[i].left = nodes[left_idx]
            if right_idx < len(nodes):
                nodes[i].right = nodes[right_idx]
        self.root = nodes[0]

# --- BINARY TREE  UI ---
class BinaryTreeUI:
    def __init__(self, root):
        self.root = root
        self.root.title("System Control Interface - Binary Tree")
        self.root.geometry("1200x850")
        
        # --- Formal Light Palette ---
        self.bg_white = "#FFFFFF"          
        self.bg_grey = "#F0F2F5"           
        self.fg_navy = "#1A237E"           
        self.fg_slate = "#2C3E50"          
        self.btn_bg = "#FFFFFF"            
        self.accent_blue = "#E3F2FD"       
        self.exit_red = "#B71C1C"          
        
        self.root.configure(bg=self.bg_white)
        
        self.main_frame = tk.Frame(self.root, bg=self.bg_white)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.root.bind("<Escape>", lambda e: self.root.quit())
        self.root.bind("<Tab>", lambda e: self.main_menu_screen())
        
        self.main_menu_screen()

    def clear_screen(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def main_menu_screen(self):
        self.clear_screen()
        self.root.bind("<Return>", lambda e: self.ask_binary_tree_levels())

        center_frame = tk.Frame(self.main_frame, bg=self.bg_white)
        center_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        tk.Label(
            center_frame,
            text="BINARY TREE LOGIC",
            font=("Georgia", 40, "bold"),
            bg=self.bg_white,
            fg=self.fg_navy
        ).pack()

        tk.Label(
            center_frame,
            text="Press ENTER to Start System",
            font=("Georgia", 14, "italic"),
            bg=self.bg_white,
            fg=self.fg_slate
        ).pack(pady=(10, 0))

    def ask_binary_tree_levels(self):
        self.clear_screen()
        self.root.unbind("<Return>")

        center_frame = tk.Frame(self.main_frame, bg=self.bg_white)
        center_frame.pack(expand=True)

        tk.Label(
            center_frame,
            text="SELECT LEVEL (1-5)",
            font=("Georgia", 24, "bold"),
            bg=self.bg_white,
            fg=self.fg_navy
        ).pack(pady=10)

        self.level_entry = tk.Entry(
            center_frame,
            font=("Georgia", 18),
            width=7,
            justify="center",
            bd=4,
            relief="sunken"
        )
        self.level_entry.pack(pady=15)
        self.level_entry.focus_set()

        button_frame = tk.Frame(center_frame, bg=self.bg_white)
        button_frame.pack(pady=10)

        tk.Button(
            button_frame,
            text="CONFIRM",
            font=("Georgia", 10, "bold"),
            bg=self.btn_bg,
            bd=6,
            relief="raised",
            command=self.confirm_level
        ).pack(side=tk.LEFT, padx=10)

        tk.Button(
            button_frame,
            text="RANDOM",
            font=("Georgia", 10, "bold"),
            bg=self.btn_bg,
            bd=6,
            relief="raised",
            command=self.random_level
        ).pack(side=tk.LEFT, padx=10)

        self.feedback_label = tk.Label(
            center_frame,
            text="",
            font=("Georgia", 12),
            bg=self.bg_white
        )
        self.feedback_label.pack(pady=10)

        self.root.bind("<Return>", lambda e: self.confirm_level())

    def confirm_level(self):
        value = self.level_entry.get()
        if value.isdigit() and 1 <= int(value) <= 5:
            level = int(value)
            self.feedback_label.config(text=f"Level {level} selected!", fg="#16a34a")
            self.root.after(800, lambda: self.start_binary_tree_page(level))
        else:
            self.feedback_label.config(text="Invalid input! Enter 1 to 5.", fg=self.exit_red)

    def random_level(self):
        level = random.randint(1, 5)
        self.level_entry.delete(0, tk.END)
        self.level_entry.insert(0, str(level))
        self.confirm_level()

    def start_binary_tree_page(self, level):
        self.clear_screen()
        self.root.unbind("<Return>")
        self.target_level = level
        self.max_nodes = (2 ** level) - 1
        self.tree_logic = BinaryTreeOrder()

        # Header Status Bar
        status_bar = tk.Frame(self.main_frame, bg=self.bg_grey, height=45)
        status_bar.pack(fill=tk.X)
        status_bar.pack_propagate(False)

        # UPDATED STATUS LABEL: Level {level} | Node: 0/{self.max_nodes}
        self.node_count_lbl = tk.Label(
            status_bar, 
            text=f"Level {level} | Node: 0/{self.max_nodes}", 
            font=("Georgia", 12, "bold"), 
            fg=self.fg_slate, 
            bg=self.bg_grey
        )
        self.node_count_lbl.pack(side=tk.LEFT, padx=15)

        tk.Label(
            status_bar, 
            text="ESC: Quit | Ctrl: Reset | Tab: Menu | Enter: Insert", 
            font=("Georgia", 10), 
            fg=self.fg_slate, 
            bg=self.bg_grey
        ).pack(side=tk.RIGHT, padx=15)

        # --- MAIN CONTENT ---
        container = tk.Frame(self.main_frame, bg=self.bg_white)
        container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # LEFT: CANVAS
        canvas_border = tk.Frame(container, bg=self.fg_slate, bd=2)
        canvas_border.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.canvas = tk.Canvas(canvas_border, bg="white", highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)

        # RIGHT: SIDEBAR
        sidebar = tk.Frame(container, bg=self.bg_white, width=300)
        sidebar.pack(side=tk.RIGHT, fill=tk.Y, padx=(20, 0))

        box_style = {"bg": self.bg_grey, "bd": 6, "relief": "raised"}

        # Box 1: Control
        tk.Label(sidebar, text="Ⅰ. SYSTEM CONTROL", font=("Georgia", 10, "bold"), bg=self.bg_white).pack(anchor="w")
        box1 = tk.Frame(sidebar, **box_style)
        box1.pack(fill=tk.X, pady=(0, 20))
        tk.Label(box1, text=f"Target Level: {level}", bg=self.bg_grey, font=("Georgia", 11)).pack(pady=10)
        tk.Button(box1, text="RESET ENGINE", font=("Georgia", 9, "bold"), bd=4, relief="raised", command=self.reset_game).pack(pady=5)

        # Box 2: Input
        tk.Label(sidebar, text="Ⅱ. DATA INPUT", font=("Georgia", 10, "bold"), bg=self.bg_white).pack(anchor="w")
        box2 = tk.Frame(sidebar, **box_style)
        box2.pack(fill=tk.X, pady=(0, 20))

        self.input_entry = tk.Entry(box2, width=15, font=("Georgia", 12), bd=2)
        self.input_entry.pack(pady=(10, 2))
        self.input_entry.focus_set()

        tk.Label(box2, text="Period (.) is for empty node", font=("Georgia", 8, "italic"), bg=self.bg_grey).pack(pady=(0, 5))

        btn_row = tk.Frame(box2, bg=self.bg_grey)
        btn_row.pack(pady=5)
        tk.Button(btn_row, text="Insert", font=("Georgia", 10, "bold"), bd=6, relief="raised", command=self.handle_input).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_row, text="Random", font=("Georgia", 10, "bold"), bd=6, relief="raised", command=self.handle_random).pack(side=tk.LEFT, padx=5)

        # Box 3: Traversals
        tk.Label(sidebar, text="Ⅲ. TRAVERSALS", font=("Georgia", 10, "bold"), bg=self.bg_white).pack(anchor="w")
        box3 = tk.Frame(sidebar, **box_style)
        box3.pack(fill=tk.BOTH, expand=True)
        self.tlr_lbl = tk.Label(box3, text="TLR: ", font=("Georgia", 11), bg=self.bg_grey, anchor="w", wraplength=250)
        self.tlr_lbl.pack(fill=tk.X, padx=10, pady=5)
        self.ltr_lbl = tk.Label(box3, text="LTR: ", font=("Georgia", 11), bg=self.bg_grey, anchor="w", wraplength=250)
        self.ltr_lbl.pack(fill=tk.X, padx=10, pady=5)
        self.lrt_lbl = tk.Label(box3, text="LRT: ", font=("Georgia", 11), bg=self.bg_grey, anchor="w", wraplength=250)
        self.lrt_lbl.pack(fill=tk.X, padx=10, pady=5)

        self.input_entry.bind("<Return>", lambda e: self.handle_input())
        self.root.bind("<Control_L>", lambda e: self.reset_game())

    def handle_input(self):
        if len(self.tree_logic.nodes_list) >= self.max_nodes: return
        char = self.input_entry.get()
        if char == "" or char == " " or char == ".": char = " "
        self.tree_logic.tree_level_value(char)
        self.input_entry.delete(0, tk.END)
        self.update_view()

    def handle_random(self):
        if len(self.tree_logic.nodes_list) >= self.max_nodes: return
        char = str(random.randint(0, 99)) if random.random() > 0.5 else random.choice(string.ascii_uppercase)
        self.tree_logic.tree_level_value(char)
        self.update_view()

    def reset_game(self):
        self.start_binary_tree_page(self.target_level)

    def update_view(self):
        count = len(self.tree_logic.nodes_list)
        # Maintaining the format during updates
        self.node_count_lbl.config(text=f"Level {self.target_level} | Node: {count}/{self.max_nodes}")
        self.canvas.delete("all")
        if self.tree_logic.root:
            self.root.update_idletasks()
            w = self.canvas.winfo_width()
            self.draw_tree(self.tree_logic.root, w//2, 60, w//4)
        
        self.tlr_lbl.config(text=f"TLR: {' '.join(tlr(self.tree_logic.root))}")
        self.ltr_lbl.config(text=f"LTR: {' '.join(ltr(self.tree_logic.root))}")
        self.lrt_lbl.config(text=f"LRT: {' '.join(lrt(self.tree_logic.root))}")

    def draw_tree(self, node, x, y, offset):
        r = 20
        if node.left:
            if node.left.value != " ":
                self.canvas.create_line(x, y, x - offset, y + 80, fill=self.fg_navy, width=2)
            self.draw_tree(node.left, x - offset, y + 80, offset // 2)
        if node.right:
            if node.right.value != " ":
                self.canvas.create_line(x, y, x + offset, y + 80, fill=self.fg_navy, width=2)
            self.draw_tree(node.right, x + offset, y + 80, offset // 2)
        if node.value != " ":
            self.canvas.create_oval(x-r, y-r, x+r, y+r, fill=self.accent_blue, outline=self.fg_navy, width=2)
            self.canvas.create_text(x, y, text=str(node.value), fill=self.fg_navy, font=("Georgia", 10, "bold"))

if __name__ == "__main__":
    root = tk.Tk()
    app = BinaryTreeUI(root)
    root.mainloop()