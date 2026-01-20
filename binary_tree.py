import tkinter as tk
from tkinter import ttk
import random
import string

# --- BINARY TREE LOGIC ---
class BinaryTreeNode:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

def ltr(node): # In-order
    if node is None:
        return []
    else:
        left_node = ltr(node.left)
        current_node = [node.value] if node.value != " " else []
        right_node = ltr(node.right)
        return left_node + current_node + right_node

def tlr(node): # Pre-order
    if node is None:
        return []
    else:
        current_node = [node.value] if node.value != " " else []
        left_node = tlr(node.left)
        right_node = tlr(node.right)
        return current_node + left_node + right_node

def lrt(node): # Post-Order
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
        nodes = [BinaryTreeNode(v) for v in values]
        for i in range(len(nodes)):
            left_idx = 2 * i + 1
            right_idx = 2 * i + 2
            if left_idx < len(nodes):
                nodes[i].left = nodes[left_idx] # type: ignore
            if right_idx < len(nodes):
                nodes[i].right = nodes[right_idx] # type: ignore
        self.root = nodes[0]

# --- BINARY TREE  UI ---
class BinaryTreeUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Binary Tree")
        self.root.geometry("1000x650")
        self.root.configure(bg="#f8fafc")

        self.main_frame = tk.Frame(self.root, bg="#f8fafc")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.root.bind("<Escape>", lambda e: self.root.quit())
        self.root.bind("<Tab>", lambda e: self.main_menu_screen())
        self.main_menu_screen()

    def clear_screen(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def main_menu_screen(self):
        self.clear_screen()

        tk.Label(
            self.main_frame,
            text="BINARY TREE",
            font=("Arial", 40, "bold"),
            bg="#f8fafc",
            fg="#1e293b"
        ).pack(pady=200)

        tk.Label(
            self.main_frame,
            text="Press ENTER to Start",
            font=("Arial", 14),
            bg="#f8fafc",
            fg="#64748b"
        ).pack()

        self.root.bind("<Return>", lambda e: self.ask_binary_tree_levels())
    
    def ask_binary_tree_levels(self):
        self.clear_screen()
        self.root.unbind("<Return>")

        center_frame = tk.Frame(self.main_frame, bg="#f8fafc")
        center_frame.pack(expand=True)

        tk.Label(
            center_frame,
            text="How many levels would you like?",
            font=("Arial", 24, "bold"),
            bg="#f8fafc",
            fg="#1e293b"
        ).pack(pady=10)

        tk.Label(
            center_frame,
            text="(Maximum: 5)",
            font=("Arial", 14),
            bg="#f8fafc",
            fg="#64748b"
        ).pack(pady=5)

        self.level_entry = tk.Entry(
            center_frame,
            font=("Arial", 15),
            width=7,
            justify="center"
        )
        self.level_entry.pack(pady=15)
        self.level_entry.focus_set()

        button_frame = tk.Frame(center_frame, bg="#f8fafc")
        button_frame.pack(pady=10)

        tk.Button(
            button_frame,
            text="CONFIRM",
            font=("Arial", 10, "bold"),
            command=self.confirm_level
        ).pack(side=tk.LEFT, padx=10)

        tk.Button(
            button_frame,
            text="RANDOM",
            font=("Arial", 10, "bold"),
            command=self.random_level
        ).pack(side=tk.LEFT, padx=10)

        self.feedback_label = tk.Label(
            center_frame,
            text="",
            font=("Arial", 12),
            bg="#f8fafc"
        )
        self.feedback_label.pack(pady=10)

        self.root.bind("<Return>", lambda e: self.confirm_level())

    def confirm_level(self):
        value = self.level_entry.get()

        if value.isdigit() and 1 <= int(value) <= 5:
            level = int(value)
            self.feedback_label.config(
                text=f"Level {level} selected!",
                fg="#16a34a"
            )
            self.root.after(800, lambda: self.start_binary_tree_page(level))
        else:
            self.feedback_label.config(
                text="Invalid input! Please enter a number from 1 to 5 only.",
                fg="#dc2626"
            )

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

        header = tk.Frame(
            self.main_frame,
            bg="#0f172a",
            height=40
        )
        header.pack(fill=tk.X)

        self.node_count_lbl = tk.Label(
            header,
            text=f"Level {level} | Node: 0/{self.max_nodes}",
            fg="white",
            bg="#0f172a",
            font=("Arial", 11, "bold")
        )
        self.node_count_lbl.pack(side=tk.LEFT, padx=15)

        menu_choices = tk.Label(
            header,
            text="ESC: Quit | Ctrl: Reset | Tab: Menu | Enter: Insert | Spacebar: Emopty node",
            fg="#94a3b8",
            bg="#0f172a",
            font=("Arial", 10)
        )
        menu_choices.pack(side=tk.RIGHT,padx=15)

        input_container = tk.Frame(
            self.main_frame,
            bg="#f8fafc"
        )
        input_container.pack(pady=(15, 5))

        self.input_entry = ttk.Entry(
            input_container,
            width=15,
            font=("Arial", 12)
        )
        self.input_entry.pack(side=tk.LEFT, padx=5)
        self.input_entry.focus_set()

        ttk.Button(
            input_container, 
            text="Insert", 
            command=self.handle_input
        ).pack(side=tk.LEFT, padx=5)

        ttk.Button(
            input_container, 
            text="Random", 
            command=self.handle_random_insert
        ).pack(side=tk.LEFT, padx=5)

        self.game_feedback = tk.Label(
            self.main_frame, 
            text="", 
            bg="#f8fafc", 
            font=("Arial", 12, "bold")
        )
        self.game_feedback.pack(pady=5)

        self.canvas = tk.Canvas(
            self.main_frame, 
            bg="white", 
            height=400, 
            highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True, padx=40, pady=(0, 10))

        self.traversal_container = tk.Frame(
            self.main_frame, 
            bg="#f8fafc"
        )
        self.traversal_container.pack(fill=tk.X, padx=40, pady=10)

        self.tlr_lbl = tk.Label(
            self.traversal_container, 
            text="TLR: ", 
            font=("Arial", 11, "bold"), 
            bg="#f8fafc"
        )
        self.tlr_lbl.pack(anchor="w")

        self.ltr_lbl = tk.Label(
            self.traversal_container, 
            text="LTR: ", 
            font=("Arial", 11, "bold"), 
            bg="#f8fafc")
        self.ltr_lbl.pack(anchor="w")

        self.lrt_lbl = tk.Label(
            self.traversal_container, 
            text="LRT: ", 
            font=("Arial", 11, "bold"), 
            bg="#f8fafc"
        )
        self.lrt_lbl.pack(anchor="w")

        self.input_entry.bind("<Return>", lambda e: self.handle_input())
        self.root.bind("<Control_L>", lambda e: self.reset_game())

    def handle_input(self):
        if len(self.tree_logic.nodes_list) >= self.max_nodes: return
        char = self.input_entry.get()

        if char == "" or char == " ":
            char = " "
        self.tree_logic.tree_level_value(char)
        self.input_entry.delete(0, tk.END)
        self.update_view(char, mode="insert")
    
    def handle_random_insert(self):
        if len(self.tree_logic.nodes_list) >= self.max_nodes: return

        if random.choice([True, False]):
            char = str(random.randint(0, 1000))
        else:
            char = random.choice(string.ascii_lowercase + string.digits)
        self.tree_logic.tree_level_value(char)
        self.update_view(char, mode="random")

    def reset_game(self):
        self.start_binary_tree_page(self.target_level)
    
    def update_view(self, value=None, mode=None):
        count = len(self.tree_logic.nodes_list)
        self.node_count_lbl.config(text=f"Level {self.target_level} | Node: {count}/{self.max_nodes}")
        
        node_feedback_text = ""
        if value is not None:
            if mode == "insert":
                node_feedback_text = f"Node {value} added to the tree!"
            elif mode == "random":
                node_feedback_text = f"Node {value} generated!"

        if count == self.max_nodes:
            self.game_feedback.config(text="Binary Tree completed!", fg="#16a34a")
        else:
            self.game_feedback.config(text=node_feedback_text, fg="#1e293b")

        self.canvas.delete("all")
        if self.tree_logic.root:
            self.root.update_idletasks()
            canvas_width = self.canvas.winfo_width()
            self.draw_tree(self.tree_logic.root, canvas_width // 2, 50, canvas_width // 4)

        self.tlr_lbl.config(text=f"TLR (Pre-order):  {' '.join(tlr(self.tree_logic.root))}")
        self.ltr_lbl.config(text=f"LTR (In-order):   {' '.join(ltr(self.tree_logic.root))}")
        self.lrt_lbl.config(text=f"LRT (Post-order): {' '.join(lrt(self.tree_logic.root))}")

    def draw_tree(self, node, x, y, offset):
        r = 18
        if node.left:
            self.canvas.create_line(
                x, 
                y, 
                x - offset, y + 70, 
                fill="#cbd5e1", 
                width=2
            )
            self.draw_tree(node.left, x - offset, y + 70, offset // 2)
        if node.right:
            self.canvas.create_line(
                x, 
                y, 
                x + offset, y + 70, 
                fill="#cbd5e1", 
                width=2
            )
            self.draw_tree(node.right, x + offset, y + 70, offset // 2)
        if node.value != " ":
            self.canvas.create_oval(
                x-r, 
                y-r, 
                x+r, 
                y+r, 
                fill="#3b82f6", 
                outline="#1d4ed8", 
                width=2
            )
            self.canvas.create_text(x, y, text=str(node.value), fill="white", font=("Arial", 10, "bold"))

if __name__ == "__main__":
    root = tk.Tk()
    app = BinaryTreeUI(root)
    root.mainloop()