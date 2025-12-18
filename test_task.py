import os

VECTOR_LEN = 7
IN_START = 0 
OUT_START = 10

datasets = [
    ("test_task_1", [4, 9, 16, 25, 36, 49, 64]),         
    ("test_task_2", [100, 121, 144, 169, 196, 225, 256]), 
    ("test_task_3", [0, 1, 2, 3, 5, 10, 8100])          
]

def generate_yaml(filename, data):
    lines = ["program:"]
    
    lines.append(f"# >> Инициализация входного вектора (Адреса {IN_START}-{IN_START+VECTOR_LEN-1})")
    for i, val in enumerate(data):
        addr = IN_START + i
        lines.append(f" ")
        lines.append(f"  - cmd: LOAD_CONST")
        lines.append(f"    value: {val}")
        lines.append(f"  - cmd: LOAD_CONST")
        lines.append(f"    value: {addr}")
        lines.append(f"  - cmd: WRITE_MEM")
        lines.append(f"    offset: 0")

    lines.append(f"  # >> Вычисление SQRT и запись в (Адреса {OUT_START}-{OUT_START+VECTOR_LEN-1})")
    for i in range(VECTOR_LEN):
        in_addr = IN_START + i
        out_addr = OUT_START + i

        lines.append(f" ")
        lines.append(f"  - cmd: SQRT")
        lines.append(f"    addr: {in_addr}")
        
        lines.append(f"  - cmd: LOAD_CONST")
        lines.append(f"    value: {out_addr}")
        
        lines.append(f"  - cmd: WRITE_MEM")
        lines.append(f"    offset: 0")

    filename = f"{filename}.yaml"
    with open(filename, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"Сгенерирован файл: {filename}")

for name, data in datasets:
    generate_yaml(name, data)
