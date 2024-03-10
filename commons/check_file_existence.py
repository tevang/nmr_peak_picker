import os
import shutil


# ANSI escape codes for colors
class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    CYAN = '\033[96m'
    RESET = '\033[0m'


def normalize_input(input_item):
    """
    Normalize the input to always be a list.
    """
    if input_item is None:
        return []
    if isinstance(input_item, list):
        return input_item
    return [input_item]


def check_executables_and_files(executables=None, files=None):
    """
    Check if the given executables exist in the PATH and if the given files exist.
    Handles all exceptions internally and prints appropriate messages.

    Parameters:
    - executables: A single executable name, a list of executable names, or None.
    - files: A single file path, a list of file paths, or None.
    """
    executables = normalize_input(executables)
    files = normalize_input(files)

    # Check files
    for file_path in files:
        try:
            if not os.path.exists(file_path):
                print(f"{Colors.RED}Error: The file '{file_path}' does not exist.{Colors.RESET}")
        except Exception as e:
            print(f"{Colors.RED}Error checking file {file_path}: {e}{Colors.RESET}")

    # Check executables
    path_dirs = os.environ.get("PATH", "").split(os.pathsep)
    for executable_name in executables:
        try:
            executable_found = False
            for dir in path_dirs:
                executable_path = os.path.join(dir, executable_name)
                if os.path.isfile(executable_path) and os.access(executable_path, os.X_OK):
                    executable_found = True
                    break

            if executable_found:
                print(f"{Colors.GREEN}The executable '{executable_name}' exists in the PATH.{Colors.RESET}")
            else:
                print(f"{Colors.YELLOW}The executable '{executable_name}' does not exist in the PATH.{Colors.RESET}")
                print(f"{Colors.CYAN}Please install '{executable_name}' to continue.{Colors.RESET}")
        except Exception as e:
            print(f"{Colors.RED}Error checking executable {executable_name}: {e}{Colors.RESET}")

def prepare_slice_directory(workdir, spectrum_type, dry_run=False):

    slices_dir = os.path.join(workdir, f"{spectrum_type}_slices")

    if not os.path.exists(workdir):
        os.makedirs(workdir)
        print(f"Created directory: {workdir}")

    if os.path.exists(slices_dir) and not dry_run:
        shutil.rmtree(slices_dir)
        print(f"Deleted directory: {slices_dir}")

    if not os.path.exists(slices_dir):
        os.makedirs(slices_dir)
        print(f"Created directory: {slices_dir}")

