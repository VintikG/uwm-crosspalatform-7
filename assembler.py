import sys
import yaml
import argparse

# ---- Этап 1: Перевод программы в промежуточное представление ----

OP_CODES = {
    'LOAD_CONST': 32,
    'READ_MEM':   54,
    'WRITE_MEM':  52,
    'SQRT':       31
}

SHIFT_B = 6

def parse_yaml(source_path):
    with open(source_path, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
        if not data or 'program' not in data:
            return []
        return data.get('program', [])

def to_ir(instructions):
    ir = []
    for i, instr in enumerate(instructions):
        cmd_name = instr.get('cmd')
        
        if cmd_name not in OP_CODES:
            print(f"Ошибка: Неизвестная команда '{cmd_name}' в строке {i+1}")
            sys.exit(1)
        
        opcode = OP_CODES[cmd_name]
        entry = {'op': cmd_name, 'A': opcode, 'B': 0}

        try:
            if cmd_name == 'LOAD_CONST':
                entry['B'] = int(instr.get('value', 0))
            elif cmd_name == 'READ_MEM':
                entry['B'] = int(instr.get('addr', 0))
            elif cmd_name == 'WRITE_MEM':
                entry['B'] = int(instr.get('offset', 0))
            elif cmd_name == 'SQRT':
                entry['B'] = int(instr.get('addr', 0))
        except ValueError:
            print(f"Ошибка: Неверный формат аргумента в строке {i+1}")
            sys.exit(1)
            
        ir.append(entry)
    return ir

# ---- Этап 2: Формирование машинного кода ----

def serialize_cmd(cmd_ir):
    a = cmd_ir['A'] & 0x3F        
    b = cmd_ir['B'] & 0x1FFF 
    
    value = (b << SHIFT_B) | a
    
    return value.to_bytes(3, byteorder='little')

def assemble_to_bin(ir):
    binary = bytearray()
    hex_log = []
    
    for item in ir:
        chunk = serialize_cmd(item)
        binary.extend(chunk)
    
        hex_str = ", ".join(f"0x{b:02X}" for b in chunk)
        hex_log.append(f"{item['op']:<12}: {hex_str}")
        
    return binary, hex_log

def print_test_mode(ir, hex_log):

    print("\n--- [Этап 1] Внутреннее представление ---")
    for item in ir:
        print(f"Команда {item['op']:<12}: A={item['A']}, B={item['B']}")
        
    print("\n--- [Этап 2] Результат ассемблирования ---")
    for line in hex_log:
        print(line)

def main():
    parser = argparse.ArgumentParser(description="Assembler for UVM (Variant 7)")
    parser.add_argument('source', help="Путь к исходному файлу (.yaml)")
    parser.add_argument('output', help="Путь к двоичному файлу-результату")
    parser.add_argument('--test', action='store_true', help="Режим тестирования")
    
    args = parser.parse_args()

    raw_instructions = parse_yaml(args.source)
    ir = to_ir(raw_instructions)
    
    binary_data, hex_log = assemble_to_bin(ir)
    
    try:
        with open(args.output, 'wb') as f:
            f.write(binary_data)
    except IOError as e:
        print(f"Ошибка записи файла: {e}")
        sys.exit(1)

    print(f"Размер двоичного файла: {len(binary_data)} байт.")

    if args.test:
        print_test_mode(ir, hex_log)

if __name__ == '__main__':
    main()
