import sys
import argparse
import math 
import xml.etree.ElementTree as ET
from xml.dom import minidom

# ---- Этап 3: Интерпретатор и операции с памятью ----

OP_CODES_MAP = {
    32: 'LOAD_CONST',
    54: 'READ_MEM',
    52: 'WRITE_MEM',
    31: 'SQRT'
}

SHIFT_B = 6
MEM_SIZE = 1024

def execute_program(bytecode):

    memory = [0] * MEM_SIZE
    stack = []
    pc = 0
    file_len = len(bytecode)
    
    print(f"--- Запуск интерпретации (Размер программы: {file_len} байт) ---")
    
    while pc < file_len:
        chunk = bytecode[pc:pc+3]
        if len(chunk) < 3:
            break
        
        val = int.from_bytes(chunk, byteorder='little')
        
        opcode = val & 0x3F
        operand_b = (val >> SHIFT_B) & 0x1FFF
        
        op_name = OP_CODES_MAP.get(opcode, "UNKNOWN")
        pc += 3
        
        if op_name == 'LOAD_CONST':
            stack.append(operand_b)
            
        elif op_name == 'READ_MEM':
            if operand_b >= MEM_SIZE:
                print(f"Ошибка: Чтение за границами памяти (Адрес: {operand_b})")
                sys.exit(1)
            stack.append(memory[operand_b])
            
        elif op_name == 'WRITE_MEM':
            if len(stack) < 2:
                print("Ошибка: Стек пуст для операции WRITE_MEM (нужны Адрес и Значение)")
                sys.exit(1)
            
            base_addr = stack.pop()
            value = stack.pop()
            
            target_addr = base_addr + operand_b
            
            if target_addr >= MEM_SIZE:
                print(f"Ошибка: Запись за границами памяти (Адрес: {target_addr})")
                sys.exit(1)
            
            memory[target_addr] = value
            
        elif op_name == 'SQRT':
            # ---- Этап 3: Реализация арифметико-логического устройства (АЛУ) ----
            
            if operand_b >= MEM_SIZE:
                print(f"Ошибка: SQRT по адресу {operand_b} вне памяти")
                sys.exit(1)
            
            mem_val = memory[operand_b]
            
            res = int(math.isqrt(mem_val))
            
            stack.append(res)
            
        else:
            print(f"Предупреждение: Неизвестный опкод {opcode}")
            
    return memory

def dump_memory_xml(memory, path, start_addr, end_addr):
    root = ET.Element("memory_dump")
    
    for i in range(start_addr, end_addr + 1):
        if i < len(memory):
            cell = ET.SubElement(root, "cell")
            cell.set("address", str(i))
            cell.text = str(memory[i])
    
    xml_str = minidom.parseString(ET.tostring(root)).toprettyxml(indent="  ")
    
    try:
        with open(path, "w", encoding="utf-8") as f:
            f.write(xml_str)
    except IOError as e:
        print(f"Ошибка записи дампа: {e}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Interpreter for UVM (Variant 7)")
    parser.add_argument('binary', help="Путь к бинарному файлу")
    parser.add_argument('result', help="Путь к файлу результата (XML)")
    parser.add_argument('range', help="Диапазон памяти для дампа (формат: start-end)")
    
    args = parser.parse_args()
    
    try:
        start, end = map(int, args.range.split('-'))
    except ValueError:
        print("Ошибка: Неверный формат диапазона. Используйте формат start-end (например, 0-20)")
        sys.exit(1)

    try:
        with open(args.binary, 'rb') as f:
            bytecode = f.read()
    except FileNotFoundError:
        print(f"Ошибка: Бинарный файл '{args.binary}' не найден.")
        sys.exit(1)
        
    memory_state = execute_program(bytecode)
    
    dump_memory_xml(memory_state, args.result, start, end)
    print(f"Интерпретация завершена. Дамп памяти сохранен в '{args.result}'.")

if __name__ == '__main__':
    main()
    