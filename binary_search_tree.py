import tkinter as tk
from tkinter import ttk
import random
from tkinter import messagebox

# ---------------- BST LOGIC ---------------- #
class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None


class BST:
    def __init__(self):
        self.root = None

    def insert(self, value):
        self.root = self._insert(self.root, value)

    def _insert(self, node, value):
        if not node:
            return Node(value)
        if value > node.value:
            node.right = self._insert(node.right, value)
        else:
            node.left = self._insert(node.left, value)
        return node

    # ---------- SEARCH ----------
    def search(self, node, value):
        if not node:
            return False
        if node.value == value:
            return True
        if value < node.value:
            return self.search(node.left, value)
        return self.search(node.right, value)

    # ---------- DELETE ----------
    def delete(self, node, value):
        if not node:
            return None

        if value < node.value:
            node.left = self.delete(node.left, value)
        elif value > node.value:
            node.right = self.delete(node.right, value)
        else:
            # Case 1 & 2: no child or one child
            if not node.left:
                return node.right
            if not node.right:
                return node.left

            # Case 3: two children
            successor = self._min_value(node.right)
            node.value = successor.value
            node.right = self.delete(node.right, successor.value)

        return node

    def _min_value(self, node):
        current = node
        while current.left:
            current = current.left
        return current

    # ---------- TRAVERSALS ----------
    def ltr(self, node, result):
        if node:
            self.ltr(node.left, result)
            result.append(node.value)
            self.ltr(node.right, result)

    def tlr(self, node, result):
        if node:
            result.append(node.value)
            self.tlr(node.left, result)
            self.tlr(node.right, result)

    def lrt(self, node, result):
        if node:
            self.lrt(node.left, result)
            self.lrt(node.right, result)
            result.append(node.value)


# ---------------- UI ---------------- #
class BSTVisualizer:
    def __init__(self, root):
        self.root = root
        self.root.title("BST Visualizer – LTR / TLR / LRT")
        self.root.geometry("1300x900")

        self.bst = BST()

        # ---------- MODE ----------
        mode_frame = tk.Frame(root)
        mode_frame.pack(pady=5)

        self.mode = tk.StringVar(value="manual")
        tk.Label(mode_frame, text="Input Mode:", font=("Georgia", 10)).pack(side=tk.LEFT)

        tk.Radiobutton(mode_frame, text="Manual", variable=self.mode,
                       value="manual", command=self.update_mode).pack(side=tk.LEFT)
        tk.Radiobutton(mode_frame, text="Random Tree", variable=self.mode,
                       value="random", command=self.update_mode).pack(side=tk.LEFT)

        # ---------- CONTROLS ----------
        control = tk.Frame(root)
        control.pack(pady=10)

        btn_style = {
            "font": ("Georgia", 10, "bold"),
            "bg": "#FFFFFF",
            "bd": 2,
            "relief": "raised",
            "cursor": "hand2"
        }

        self.entry = tk.Entry(control, width=8, font=("Georgia", 12))
        self.entry.pack(side=tk.LEFT, padx=4)

        tk.Button(control, text="Insert", command=self.insert_value, **btn_style).pack(side=tk.LEFT)

        tk.Label(control, text="Nodes:", font=("Georgia", 10)).pack(side=tk.LEFT, padx=4)

        self.rand_count = tk.Entry(control, width=5, font=("Georgia", 12))
        self.rand_count.pack(side=tk.LEFT)

        tk.Button(control, text="Generate", command=self.generate_random, **btn_style).pack(side=tk.LEFT, padx=4)

        tk.Button(control, text="Clear", command=self.clear_tree, fg="#B71C1C", **btn_style).pack(side=tk.LEFT, padx=4)

        # ---------- SEARCH ----------
        self.search_entry = tk.Entry(control, width=8, font=("Georgia", 12))
        self.search_entry.pack(side=tk.LEFT, padx=4)
        tk.Button(control, text="Search", command=self.search_node, **btn_style).pack(side=tk.LEFT)

        # ---------- DELETE ----------
        self.delete_entry = tk.Entry(control, width=8, font=("Georgia", 12))
        self.delete_entry.pack(side=tk.LEFT, padx=4)
        tk.Button(control, text="Delete", command=self.delete_node, fg="#B71C1C", **btn_style).pack(side=tk.LEFT)

        # ---------- TRAVERSALS ----------
        for label, cmd in [("LTR", self.show_ltr), ("TLR", self.show_tlr), ("LRT", self.show_lrt)]:
            tk.Button(control, text=label, command=cmd, **btn_style).pack(side=tk.LEFT, padx=3)

        # ---------- CANVAS ----------
        self.canvas = tk.Canvas(root, bg="white", height=450)
        self.canvas.pack(fill=tk.BOTH, expand=True, padx=20)

        # ---------- OUTPUT ----------
        self.output = tk.Label(root, text="Traversal:", font=("Georgia", 12, "bold"))
        self.output.pack(pady=15)

        self.update_mode()

    # ---------- MODE ----------
    def update_mode(self):
        state_manual = self.mode.get() == "manual"
        self.entry.config(state="normal" if state_manual else "disabled")

    # ---------- ACTIONS ----------
    def insert_value(self):
        try:
            v = int(self.entry.get())
            self.bst.insert(v)
            self.redraw()
        except ValueError:
            messagebox.showerror("Error", "Invalid integer", parent=self.root)

    def generate_random(self):
        try:
            count = int(self.rand_count.get())
            if count < 10 or count > 30:
                messagebox.showerror("Error", "Enter 10–30 nodes", parent=self.root)
                return
            for _ in range(count):
                self.bst.insert(random.randint(0, 200))
            self.redraw()
        except ValueError:
            messagebox.showerror("Error", "Invalid integer", parent=self.root)

    def search_node(self):
        try:
            v = int(self.search_entry.get())
            found = self.bst.search(self.bst.root, v)
            messagebox.showinfo("Search Result", f"{v} {'FOUND' if found else 'NOT FOUND'}", parent=self.root)
        except ValueError:
            messagebox.showerror("Error", "Invalid integer", parent=self.root)

    def delete_node(self):
        try:
            v = int(self.delete_entry.get())
            if not self.bst.search(self.bst.root, v):
                messagebox.showerror("Error", "Node not found", parent=self.root)
                return
            self.bst.root = self.bst.delete(self.bst.root, v)
            self.redraw()
        except ValueError:
            messagebox.showerror("Error", "Invalid integer", parent=self.root)

    def clear_tree(self):
        self.bst.root = None
        self.canvas.delete("all")
        self.output.config(text="Traversal:")

    # ---------- DRAW ----------
    def redraw(self):
        self.canvas.delete("all")
        self.draw_tree(self.bst.root, 650, 40, 300)

    def draw_tree(self, node, x, y, offset):
        if not node:
            return
        r = 22
        self.canvas.create_oval(x-r, y-r, x+r, y+r, fill="#3b82f6")
        self.canvas.create_text(x, y, text=str(node.value), fill="white")

        if node.left:
            self.canvas.create_line(x, y+r, x-offset, y+80-r)
            self.draw_tree(node.left, x-offset, y+80, offset//2)
        if node.right:
            self.canvas.create_line(x, y+r, x+offset, y+80-r)
            self.draw_tree(node.right, x+offset, y+80, offset//2)

    # ---------- TRAVERSALS ----------
    def show_ltr(self):
        res = []
        self.bst.ltr(self.bst.root, res)
        self.output.config(text="LTR: " + str(res))

    def show_tlr(self):
        res = []
        self.bst.tlr(self.bst.root, res)
        self.output.config(text="TLR: " + str(res))

    def show_lrt(self):
        res = []
        self.bst.lrt(self.bst.root, res)
        self.output.config(text="LRT: " + str(res))


# ---------------- RUN ---------------- #
if __name__ == "__main__":
    root = tk.Tk()
    app = BSTVisualizer(root)
    root.mainloop()
