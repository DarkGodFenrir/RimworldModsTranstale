import os
import tkinter as tk
import tkinter.ttk as ttk

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.grid()
        self.create_widgets()

    def create_widgets(self):
        self.nodes = {}

        # Канвас слева с полем ввода и кнопкой
        self.left_canvas = tk.Canvas(self, width=200)
        self.left_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.input_label = tk.Label(self.left_canvas, text="Введите путь к папке:")
        self.input_label.grid(row=0, column=0)

        self.input_field = tk.Entry(self.left_canvas, width=30)
        self.input_field.grid(row=1, column=0)

        self.button_canvas = tk.Canvas(self.left_canvas, width=200)

        self.input_button = tk.Button(self.button_canvas, text="Вставить", command=self.input_text)
        self.input_button.pack(side=tk.LEFT)

        self.search_button = tk.Button(self.button_canvas, text="Поиск", command=self.display_treeview)
        self.search_button.pack(side=tk.RIGHT)

        self.button_canvas.grid(row=2, column=0)

        self.treeview = ttk.Treeview(self.left_canvas, height=20)
        ysb = ttk.Scrollbar(self.left_canvas, orient=tk.VERTICAL,
                            command=self.treeview.yview)
        self.treeview.configure(yscrollcommand=ysb.set)

        self.treeview.column("#0", width=200)
        self.treeview.heading("#0", text="Имя")
        self.treeview.grid(row=3, column=0, sticky=tk.W)
        ysb.grid(row=3, column=1, sticky=tk.N + tk.S)
        # self.treeview.bind("<>", self.open_node)
            # .pack(side="top", fill="both", expand=True)

        # Канвас справа с деревом содержимого папки
        self.right_canvas = tk.Canvas(self, width=600, height=500)
        self.right_canvas.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    def input_text(self):
        self.input_field.delete(0, 'end')
        self.input_field.insert(tk.INSERT, root.clipboard_get())

    def display_treeview(self):
        path = self.input_field.get()
        self.treeview.delete(*self.treeview.get_children())
        for entry in os.listdir(path):
            entry_path = os.path.join(path, entry)
            node = self.treeview.insert("", tk.END, text=entry, open=False)
            if os.path.isdir(entry_path):
                self.nodes[node] = entry_path
                self.treeview.insert(node, tk.END)

    def open_node(self, event):
        item = self.treeview.focus()
        abspath = self.nodes.pop(item, False)
        if abspath:
            children = self.treeview.get_children(item)
            self.treeview.delete(children)
            self.display_treeview(item, abspath)

root = tk.Tk()
app = Application(master=root)
app.mainloop()