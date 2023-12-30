import os

def get_directory_info(aDir: str):
    total_size = 0
    total_files = 0
    total_dirs = 0

    Dirs = {}
    Files = []
    for Root, Dirs, Files in os.walk(aDir):
        for xFile in Files:
            file_path = os.path.join(Root, xFile)
            total_size += os.path.getsize(file_path)

        total_files += len(Files)
        total_dirs += len(Dirs)

    return total_size, total_files, total_dirs

# Example usage
directory_path = "Data/img/product/1"
size, files_count, dirs_count = get_directory_info(directory_path)

print()
print(f"Directory: {directory_path}")
print(f"Total size: {size} bytes")
print(f"Total files: {files_count}")
print(f"Total directories: {dirs_count}")
