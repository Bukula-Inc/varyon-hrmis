import os

root_dir = './'

for root, dirs, files in os.walk(root_dir):
    for file in files:
        file_path = os.path.join(root, file)
        try:
            file_size_mb = os.path.getsize(file_path) / (1024 * 1024)
            if file_size_mb > 1:
                print(f"{file_path}: {file_size_mb:.2f} MB")
        except FileNotFoundError:
            pass  # Skip non-existent files
        except Exception as e:
            print(f"Error processing {file_path}: {e}")