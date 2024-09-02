import os


def get_files_directory():
    return os.path.join(os.getcwd(), 'local_disk/files')


def create_directories():
    os.makedirs(get_files_directory(), exist_ok=True)
