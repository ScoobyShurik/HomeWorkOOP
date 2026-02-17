import os


def merge_files(folder_path, output_file='result.txt'):
    files_data = []
    for filename in os.listdir(folder_path):
        if filename.endswith('.txt'):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.readlines()
            files_data.append({
                'name': filename,
                'line_count': len(content),
                'content': content
            })
    files_data.sort(key=lambda x: x['line_count'])
    with open(output_file, 'w', encoding='utf-8') as f:
        for file_info in files_data:
            f.write(f"{file_info['name']}\n")
            f.write(f"{file_info['line_count']}\n")
            for line in file_info['content']:
                f.write(line)
            f.write('\n')
    print(f"Файл '{output_file}' успешно создан!")


if __name__ == "__main__":
    merge_files('files')