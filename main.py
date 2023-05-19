import os
import tkinter as tk
import tkinter.ttk as ttk
import xml.etree.ElementTree as ET


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
        self.treeview.bind("<Double-1>", self.onDoubleClick)

        # Канвас справа с деревом содержимого папки
        self.right_canvas = tk.Canvas(self, width=600, height=500)
        self.right_canvas.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.menu_canvas = tk.Canvas(self.right_canvas)
        self.menu_canvas.pack(side=tk.TOP, fill=tk.BOTH)
        self.path_label = tk.Label(self.menu_canvas, text="Путь к файлу:")
        self.path_label.grid(row=0, column=0)

        self.input_field_name = tk.Entry(self.menu_canvas, width=60)
        self.input_field_name.grid(row=0, column=1)

        self.text_row = tk.Label(self.menu_canvas, text="Строка: ")
        self.text_row.grid(row=0, column=2)

        self.text_tecRow = tk.Label(self.menu_canvas, text="0")
        self.text_tecRow.grid(row=0, column=3)

        self.text_mRow = tk.Label(self.menu_canvas, text="/")
        self.text_mRow.grid(row=0, column=4)

        self.text_maxRow = tk.Label(self.menu_canvas, text="0")
        self.text_maxRow.grid(row=0, column=5)

        self.button_next = tk.Button(self.menu_canvas, text=">>>", command=self.display_treeview)
        self.button_next.grid(row=1, column=5)

        self.button_prev = tk.Button(self.menu_canvas, text="<<<", command=self.display_treeview)
        self.button_prev.grid(row=1, column=3)

        self.originText_convas = tk.Canvas(self.right_canvas)
        self.originText_convas.pack(fill=tk.BOTH)

        self.originText_label = tk.Label(self.originText_convas, text="Оригинальный текст")
        self.originText_label.pack()

        self.originText_entry = tk.Text(self.originText_convas, height=10)
        self.originText_entry.pack(fill=tk.BOTH)

        self.perevText_label = tk.Label(self.originText_convas, text="Переведенный текст текст")
        self.perevText_label.pack()

        self.perevText_entry = tk.Text(self.originText_convas, height=10)
        self.perevText_entry.pack(fill=tk.BOTH)

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
                for subentry in os.listdir(entry_path):
                    self.treeview.insert(node, tk.END, text=subentry)

    def onDoubleClick(self, event):
        item = self.treeview.selection()[0]
        parant_item = self.treeview.parent(item)
        mem_path = self.input_field.get()
        mem_path = os.path.join(mem_path, self.treeview.item(parant_item, "text"))
        mem_path = os.path.join(mem_path, self.treeview.item(item, "text"))
        # print("Путь к файлу", mem_path)
        self.input_field_name.delete(0, 'end')
        self.input_field_name.insert(tk.INSERT, mem_path)

        # print(count_xml_lines(mem_path))
        get_xml = count_xml_lines(mem_path)
        self.text_maxRow.configure(text=get_xml[0])

        self.originText_entry.delete(1.0, 'end')
        self.originText_entry.insert(tk.INSERT, get_xml[1])

    def get_next_row(self):
        xml_path = self.input_field_name.get()
        xml_tree = ET.parse(xml_path)
        xml_root = xml_tree.getroot()
        next_row = self.text_tecRow

def count_xml_lines(filepath):
    with open(filepath, "r", encoding='utf-8-sig') as file:
        xml_tree = ET.parse(file)
        xml_root = xml_tree.getroot()

        # print(list(xml_root.iter()))

        return len(list(xml_root.iter())), list(xml_root.iter())[0].text


def get_xml_line_text(file_path, line_number):
    xml_tree = ET.parse(file_path)
    xml_root = xml_tree.getroot()

    # Находим все элементы "row"
    row_elements = xml_root.findall(".//row")

    # Получаем элемент с указанным номером строки
    line_element = row_elements[line_number - 1]

    # Получаем текст элемента
    line_text = line_element.text

    return line_text


root = tk.Tk()
app = Application(master=root)
app.mainloop()
