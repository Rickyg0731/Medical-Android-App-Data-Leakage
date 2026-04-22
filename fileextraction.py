import os

def get_all_code_files(directory):
    code_files = []

    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith((".java", ".kt", ".smali", ".xml")):
                code_files.append(os.path.join(root, file))

    return code_files
