import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import random
import string
import os
import sys

# --- BINARY TREE LOGIC ---
class BinaryTreeNode:
    def __init__(self, value, index=None):
        self.value = value
        self.left = None
        self.right = None
        self.index = index
        self.parent = None

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
        
        nodes = [BinaryTreeNode(v, i) if i not in reserved else None for i, v in enumerate(values)]
        
        for i in range(len(nodes)):
            if nodes[i] is None or values[i] == " ":
                continue
            
            left_idx = 2 * i + 1
            right_idx = 2 * i + 2
            if left_idx < len(nodes):
                nodes[i].left = nodes[left_idx] # type: ignore
                if nodes[left_idx]:
                    nodes[left_idx].parent = nodes[i] # type: ignore
            if right_idx < len(nodes):
                nodes[i].right = nodes[right_idx] # type: ignore
                if nodes[right_idx]:
                    nodes[right_idx].parent = nodes[i] # type: ignore
        self.root = nodes[0]

# --- BINARY TREE  UI ---
class BinaryTreeUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Binary Tree")
        self.root.geometry("1200x900")
        
        # --- Formal Light Palette ---
        self.bg_white = "#FFFFFF"          
        self.bg_grey = "#F0F2F5"           
        self.fg_navy = "#1A237E"           
        self.fg_slate = "#2C3E50"          
        self.btn_bg = "#FFFFFF"            
        self.accent_blue = "#E3F2FD"       
        self.exit_red = "#B71C1C"          
        
        self.selected_node = None
        self.node_coords = {}
        self.current_traversal = None
        
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
        self.selected_node = None
        self.node_coords = {}
        self.current_traversal = None

        # Header Status Bar
        status_bar = tk.Frame(self.main_frame, bg=self.bg_grey, height=45)
        status_bar.pack(fill=tk.X)
        status_bar.pack_propagate(False)

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

        self.message_container = tk.Frame(self.main_frame, bg=self.bg_white)
        self.message_container.pack(fill=tk.X, pady=(15, 10))

        self.completion_lbl = tk.Label(
            self.message_container,
            text="System Initialized...",
            font=("Georgia", 14, "bold"),
            bg=self.bg_white,
            fg=self.fg_navy,
            justify="center"
        )
        self.completion_lbl.pack(expand=True)

        # --- MAIN CONTENT ---
        container = tk.Frame(self.main_frame, bg=self.bg_white)
        container.pack(fill=tk.BOTH, expand=True, padx=20, pady=(5, 20))

        # LEFT: CANVAS + TRAVERSAL RESULTS
        left_section = tk.Frame(container, bg=self.bg_white)
        left_section.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        canvas_border = tk.Frame(left_section, bg=self.fg_slate, bd=2)
        canvas_border.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        self.canvas = tk.Canvas(canvas_border, bg="white", highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        self.canvas.bind("<Button-1>", self.on_canvas_click)
        self.canvas.bind("<Configure>", lambda e: self.on_canvas_resize())

        # Traversal Results Display
        result_frame = tk.Frame(left_section, bg=self.bg_grey, bd=6, relief="sunken")
        result_frame.pack(fill=tk.X, pady=(0, 0))
        tk.Label(result_frame, text="Traversal Result:", font=("Georgia", 10, "bold"), bg=self.bg_grey, fg=self.fg_navy).pack(anchor="w", padx=10, pady=(10, 5))
        
        self.result_display = tk.Text(result_frame, height=3, bg=self.bg_grey, fg=self.fg_slate, font=("Georgia", 11), wrap=tk.WORD, relief=tk.FLAT, bd=0)
        self.result_display.pack(fill=tk.X, padx=10, pady=(5, 10))
        
        # Configure text tags for bold
        self.result_display.tag_config("bold", font=("Georgia", 11, "bold"), foreground=self.fg_navy)
        self.result_display.tag_config("normal", font=("Georgia", 11), foreground=self.fg_navy)

        # RIGHT: SIDEBAR
        sidebar = tk.Frame(container, bg=self.bg_white, width=300)
        sidebar.pack(side=tk.RIGHT, fill=tk.BOTH, expand=False, padx=(20, 0))

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
        box3.pack(fill=tk.X, pady=(0, 20))
        
        btn_traversal = tk.Frame(box3, bg=self.bg_grey)
        btn_traversal.pack(fill=tk.X, padx=5, pady=10)
        
        tk.Button(btn_traversal, text="Pre-order", font=("Georgia", 9, "bold"), bd=4, relief="raised", bg="#00FF00", command=lambda: self.show_traversal("preorder")).pack(fill=tk.X, pady=3)
        tk.Button(btn_traversal, text="Inorder", font=("Georgia", 9, "bold"), bd=4, relief="raised", bg="#FFA500", command=lambda: self.show_traversal("inorder")).pack(fill=tk.X, pady=3)
        tk.Button(btn_traversal, text="Post-order", font=("Georgia", 9, "bold"), bd=4, relief="raised", bg="#FF1493", command=lambda: self.show_traversal("postorder")).pack(fill=tk.X, pady=3)

        # Box 4: Selected Node
        tk.Label(sidebar, text="Ⅳ. SELECTED NODE", font=("Georgia", 10, "bold"), bg=self.bg_white).pack(anchor="w")
        box4 = tk.Frame(sidebar, **box_style)
        box4.pack(fill=tk.BOTH, expand=True)

        info_frame = tk.Frame(box4, bg=self.bg_grey)
        info_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        tk.Label(info_frame, text="Node Information", font=("Georgia", 10, "bold"), bg=self.bg_grey, fg=self.fg_navy).pack(pady=(5, 10))

        self.node_index_lbl = tk.Label(info_frame, text="Node Index:        ?", font=("Georgia", 10), bg=self.bg_grey, fg=self.fg_slate, anchor="w")
        self.node_index_lbl.pack(fill=tk.X, padx=10, pady=3)

        self.node_value_lbl = tk.Label(info_frame, text="Node Value:        ?", font=("Georgia", 10), bg=self.bg_grey, fg=self.fg_slate, anchor="w")
        self.node_value_lbl.pack(fill=tk.X, padx=10, pady=3)

        self.node_parent_lbl = tk.Label(info_frame, text="Parent:              ?", font=("Georgia", 10), bg=self.bg_grey, fg=self.fg_slate, anchor="w")
        self.node_parent_lbl.pack(fill=tk.X, padx=10, pady=3)

        self.node_left_lbl = tk.Label(info_frame, text="Left Child:         ?", font=("Georgia", 10), bg=self.bg_grey, fg=self.fg_slate, anchor="w")
        self.node_left_lbl.pack(fill=tk.X, padx=10, pady=3)

        self.node_right_lbl = tk.Label(info_frame, text="Right Child:       ?", font=("Georgia", 10), bg=self.bg_grey, fg=self.fg_slate, anchor="w")
        self.node_right_lbl.pack(fill=tk.X, padx=10, pady=10)

        self.input_entry.bind("<Return>", lambda e: self.handle_input())
        self.root.bind("<Control_L>", lambda e: self.reset_game())

    def handle_input(self):
        if len(self.tree_logic.nodes_list) >= self.max_nodes: return
        char = self.input_entry.get()
        display_char = char if char and char != "." else "EMPTY" #
        if char == "" or char == " " or char == ".": char = " "
        self.tree_logic.tree_level_value(char)
        self.input_entry.delete(0, tk.END)
        self.completion_lbl.config(text=f"Node '{display_char}' added to system", fg=self.fg_navy) #
        self.update_view()

    def handle_random(self):
        if len(self.tree_logic.nodes_list) >= self.max_nodes: return
        char = str(random.randint(0, 99)) if random.random() > 0.5 else random.choice(string.ascii_uppercase)
        self.tree_logic.tree_level_value(char)
        self.completion_lbl.config(text=f"Node '{char}' added to system", fg=self.fg_navy)
        self.update_view()

    def reset_game(self):
        self.start_binary_tree_page(self.target_level)

    def show_traversal(self, traversal_type):
        self.current_traversal = traversal_type
        
        if not self.tree_logic.root:
            self.result_display.config(state=tk.NORMAL)
            self.result_display.delete("1.0", tk.END)
            self.result_display.insert("1.0", "No tree to traverse")
            self.result_display.config(state=tk.DISABLED, foreground=self.exit_red)
            return
        
        if traversal_type == "preorder":
            result = tlr(self.tree_logic.root)
            method_name = "Pre-order"
            description = "(Root-Left-Right)"
        elif traversal_type == "inorder":
            result = ltr(self.tree_logic.root)
            method_name = "In-order"
            description = "(Left-Root-Right)"
        elif traversal_type == "postorder":
            result = lrt(self.tree_logic.root)
            method_name = "Post-order"
            description = "(Left-Right-Root)"
        else:
            return
        
        result_str = " → ".join(str(x) for x in result) if result else "Empty"
        
        # Update Text widget with formatted text
        self.result_display.config(state=tk.NORMAL)
        self.result_display.delete("1.0", tk.END)
        self.result_display.insert("1.0", method_name, "bold")
        self.result_display.insert(tk.END, f" {description}\n", "normal")
        self.result_display.insert(tk.END, result_str, "normal")
        self.result_display.config(state=tk.DISABLED)

    def on_canvas_resize(self):
        if self.tree_logic.root:
            self.root.update_idletasks()
            self.canvas.delete("all")
            self.node_coords = {}
            w = self.canvas.winfo_width()
            self.draw_tree(self.tree_logic.root, w//2, 60, w//4)

    def on_canvas_click(self, event):
        clicked = False
        for tag, (x, y, r, node) in self.node_coords.items():
            # Check if click is within the node circle
            if (event.x - x) ** 2 + (event.y - y) ** 2 <= r ** 2:
                self.selected_node = node
                self.update_node_info()
                self.update_view()
                clicked = True
                break
        
        if not clicked:
            self.selected_node = None
            self.update_node_info()
            self.update_view()

    def update_node_info(self):
        if self.selected_node is None:
            self.node_index_lbl.config(text="Node Index:        ?")
            self.node_value_lbl.config(text="Node Value:        ?")
            self.node_parent_lbl.config(text="Parent:              ?")
            self.node_left_lbl.config(text="Left Child:          ?")
            self.node_right_lbl.config(text="Right Child:       ?")
        else:
            index_val = self.selected_node.index if self.selected_node.index is not None else "?"
            value_val = self.selected_node.value
            parent_val = self.selected_node.parent.value if self.selected_node.parent else "None"
            left_val = self.selected_node.left.value if self.selected_node.left and self.selected_node.left.value != " " else "None"
            right_val = self.selected_node.right.value if self.selected_node.right and self.selected_node.right.value != " " else "None"
            
            self.node_index_lbl.config(text=f"Node Index:        {index_val}")
            self.node_value_lbl.config(text=f"Node Value:        {value_val}")
            self.node_parent_lbl.config(text=f"Parent:              {parent_val}")
            self.node_left_lbl.config(text=f"Left Child:          {left_val}")
            self.node_right_lbl.config(text=f"Right Child:       {right_val}")

    def update_view(self):
        count = len(self.tree_logic.nodes_list)
        self.node_count_lbl.config(text=f"Level {self.target_level} | Node: {count}/{self.max_nodes}")
        
        if count == self.max_nodes:
            self.completion_lbl.config(text="BINARY TREE COMPLETED", fg="green", font=("Georgia", 14, "bold"))

        self.canvas.delete("all")
        self.node_coords = {}
        if self.tree_logic.root:
            self.root.update_idletasks()
            w = self.canvas.winfo_width()
            self.draw_tree(self.tree_logic.root, w//2, 60, w//4)

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
            color = "#FFE082" if node == self.selected_node else self.accent_blue
            self.canvas.create_oval(x-r, y-r, x+r, y+r, fill=color, outline=self.fg_navy, width=2, tags=(f"node_{node.index}",))
            self.canvas.create_text(x, y, text=str(node.value), fill=self.fg_navy, font=("Georgia", 10, "bold"))
            self.node_coords[f"node_{node.index}"] = (x, y, r, node)

if __name__ == "__main__":
    root = tk.Tk()
    app = BinaryTreeUI(root)
    root.mainloop()