import json
import os
from datetime import datetime
import re
import shutil  

def load_sample(path: str) -> list[str]:
    with open(path, 'r', encoding='utf-8') as file:
        resultat = file.readlines()
        resultat = [line.strip() for line in resultat]  
    return resultat

def generate_json(lines: list[str]) -> dict:

    result = {}
    for line in lines:
        parts = line.strip().split()
        name = parts[0]
        montant_str = parts[2]
        montant_num = re.sub(r'[^\d.]', '', montant_str)  
        montant = float(montant_num)  
        if name in result:
            result[name]['total_sent'] += montant
        else:
            result[name] = {
                'name': name,
                'total_sent': montant
            }
    return result

def save_result(path: str, result: dict) -> None:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"result_sample_{timestamp}.json"
    full_path = os.path.join(path, filename)

    with open(full_path, 'w', encoding='utf-8') as file:
        json.dump(result, file, indent=4, ensure_ascii=False)

def archive_file(file_path: str, archive_path: str) -> None:
    if not os.path.exists(archive_path):
        os.makedirs(archive_path)
    
    shutil.move(file_path, os.path.join(archive_path, os.path.basename(file_path)))


def process_files(source_dir: str, result_dir: str, archive_dir: str) -> None:
    if not os.path.exists(result_dir):
        os.makedirs(result_dir)
    if not os.path.exists(archive_dir):
        os.makedirs(archive_dir)

    for filename in os.listdir(source_dir):
        if filename.endswith('.txt'):  
            file_path = os.path.join(source_dir, filename)

            data_lines = load_sample(file_path)

            result_dict = generate_json(data_lines)

            save_result(result_dir, result_dict)

            archive_file(file_path, archive_dir)

if __name__ == '__main__':
    source_dir = './source'  
    result_dir = './result' 
    archive_dir = './archived'  

    
    process_files(source_dir, result_dir, archive_dir)
