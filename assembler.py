import sys
import yaml
import argparse

# ---- Перевод программы в промежуточное представление ----

OP_CODES = {
    'LOAD_CONST': 32,
    'READ_MEM':   54,
    'WRITE_MEM':  52,
    'SQRT':       31
}

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

def print_test_mode(ir):
    print(">>> Тестовый режим: Внутреннее представление <<<")
    for item in ir:
        print(f"Команда {item['op']:<12}: A={item['A']}, B={item['B']}")

def main():
    parser = argparse.ArgumentParser(description="Assembler for UVM (Variant 7) - Stage 1")
    parser.add_argument('source', help="Путь к исходному файлу (.yaml)")
    parser.add_argument('output', help="Путь к файлу-результату (заглушка для этапа 1)")
    parser.add_argument('--test', action='store_true', help="Режим тестирования (вывод IR)")
    
    args = parser.parse_args()

    raw_instructions = parse_yaml(args.source)
    
    ir = to_ir(raw_instructions)

    if args.test:
        print_test_mode(ir)
    else:
        print(f"Трансляция завершена. Сформировано {len(ir)} инструкций.")
        print("Генерация бинарного файла будет реализована на Этапе 2.")

if __name__ == '__main__':
    main()
