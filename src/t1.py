import os

def get_directory_size_and_file_count(aDir):
    total_size = 0
    total_files = 0

    for Root, Dirs, Files in os.walk(aDir):
        for xFile in Files:
            file_path = os.path.join(Root, xFile)
            total_size += os.path.getsize(file_path)
            total_files += 1

    return total_size, total_files

# Example usage
directory_path = "Data/img/product/1"
size, file_count = get_directory_size_and_file_count(directory_path)

print()
print(f"Total Size: {size} bytes")
print(f"Total Files: {file_count}")
