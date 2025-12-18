import tkinter as tk
from tkinter import scrolledtext, messagebox, filedialog
import sys
import os
import assembler
import interpreter

def run_uvm():
    source_code = editor.get("1.0", tk.END)
    
    if not source_code.strip():
        messagebox.showwarning("Внимание", "Программа пуста!")
        return

    try:
        import tempfile
        with tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix='.yaml', encoding='utf-8') as tmp:
            tmp.write(source_code)
            tmp_path = tmp.name
        
        try:
            raw_instr = assembler.parse_yaml(tmp_path)
            ir = assembler.to_ir(raw_instr)
            binary, _ = assembler.assemble_to_bin(ir)
        finally:
            os.remove(tmp_path)

        memory = interpreter.execute_program(binary)

        output_text = "Адрес\tЗначение\n" + "-"*20 + "\n"
        
        for i in range(31):
            val = memory[i]
            output_text += f"{i}\t{val}\n"
            
        output_view.config(state='normal')
        output_view.delete("1.0", tk.END) 
        output_view.insert(tk.END, output_text)
        output_view.config(state='disabled')

        status_label.config(text=f"Успешно. Размер бинарника: {len(binary)} байт", fg="green")

    except Exception as e:
        messagebox.showerror("Ошибка выполнения", str(e))
        status_label.config(text="Ошибка", fg="red")

def load_file():
    path = filedialog.askopenfilename(filetypes=[("YAML Files", "*.yaml"), ("All Files", "*.*")])
    if path:
        with open(path, 'r', encoding='utf-8') as f:
            text = f.read()
            editor.delete("1.0", tk.END)
            editor.insert(tk.END, text)

root = tk.Tk()
root.title("УВМ - Вариант 7 (GUI)")
root.geometry("800x600")

toolbar = tk.Frame(root, bd=1, relief=tk.RAISED)
toolbar.pack(side=tk.TOP, fill=tk.X)

btn_load = tk.Button(toolbar, text="Загрузить YAML", command=load_file)
btn_load.pack(side=tk.LEFT, padx=2, pady=2)

btn_run = tk.Button(toolbar, text="Ассемблировать и Запустить", command=run_uvm, bg="#ddffdd")
btn_run.pack(side=tk.LEFT, padx=2, pady=2)

status_label = tk.Label(toolbar, text="Готов", fg="grey")
status_label.pack(side=tk.RIGHT, padx=5)
\
paned = tk.PanedWindow(root, orient=tk.HORIZONTAL)
paned.pack(fill=tk.BOTH, expand=True)
\
frame_left = tk.Frame(paned)
lbl_editor = tk.Label(frame_left, text="Код программы (YAML):", font=("Arial", 10, "bold"))
lbl_editor.pack(anchor="w")
editor = scrolledtext.ScrolledText(frame_left, width=40, font=("Consolas", 10))
editor.pack(fill=tk.BOTH, expand=True)
paned.add(frame_left)
\
frame_right = tk.Frame(paned)
lbl_dump = tk.Label(frame_right, text="Дамп памяти (0-30):", font=("Arial", 10, "bold"))
lbl_dump.pack(anchor="w")
output_view = scrolledtext.ScrolledText(frame_right, width=30, font=("Consolas", 10), state='disabled', bg="#f0f0f0")
output_view.pack(fill=tk.BOTH, expand=True)
paned.add(frame_right)

default_prog = """program:
  # Пример: вычисление sqrt(64) -> 8
  - cmd: LOAD_CONST
    value: 64
  - cmd: LOAD_CONST
    value: 0
  - cmd: WRITE_MEM
    offset: 0
  - cmd: SQRT
    addr: 0
  - cmd: LOAD_CONST
    value: 5
  - cmd: WRITE_MEM
    offset: 0
"""
editor.insert(tk.END, default_prog)

root.mainloop()