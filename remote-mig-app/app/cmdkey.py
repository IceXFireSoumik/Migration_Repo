import os
import subprocess
import logging
import socket
from azure.storage.fileshare import ShareFileClient

# Logging Configuration
LOG_DIR = os.path.join(os.getcwd(), 'logs')
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE_PATH = os.path.join(LOG_DIR, f'migration_log_{socket.gethostname()}.log')
logging.basicConfig(filename=LOG_FILE_PATH, filemode='a', format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

def test_shared_drive_access(drive_path):
    """Test if the shared drive is accessible by attempting to list its contents."""
    logging.info(f'Testing access to shared drive at {drive_path}')
    try:
        if os.path.exists(drive_path):
            logging.info(f'Successfully accessed the shared drive at {drive_path}')
            print(f'Successfully accessed the shared drive at {drive_path}')
            # List the contents as a further test
            contents = os.listdir(drive_path)
            logging.info(f'Contents of {drive_path}: {contents}')
            print(f'Contents of {drive_path}: {contents}')
        else:
            logging.error(f'Cannot access the shared drive at {drive_path}')
            print(f'Cannot access the shared drive at {drive_path}')
    except Exception as e:
        logging.error(f'Error accessing the shared drive at {drive_path}: {e}')
        print(f'Error accessing the shared drive at {drive_path}: {e}')

def download_file_from_azure(storage_account_name, file_share_name, directory_name, file_name, access_key):
    """Download a file from Azure File Share."""
    try:
        file_client = ShareFileClient(
            account_url=f"https://{storage_account_name}.file.core.windows.net/",
            share_name=file_share_name,
            file_path=f"{directory_name}/{file_name}",
            credential=access_key
        )
        with open(file_name, "wb") as file:
            file.write(file_client.download_file().readall())
        logging.info(f"File {file_name} downloaded successfully.")
        print(f"File {file_name} downloaded successfully.")
    except Exception as e:
        logging.error(f"Error downloading {file_name} from Azure: {e}")
        print(f"Error downloading {file_name} from Azure: {e}")

def run_report_app(arg1, arg2, arg3):
    """Run the report migration application."""
    exe_path = os.path.join(arg1, 'reportmigration.exe')
    exe_argument = [arg2, arg3]
    exe_command = [exe_path] + exe_argument

    if not os.path.exists(exe_path):
        logging.error(f'Executable not found at {exe_path}')
        print(f'Executable not found at {exe_path}')
        return

    try:
        logging.info(f'Executing {exe_path} with arguments {exe_argument}')
        process = subprocess.run(exe_command, capture_output=True, text=True)
        if process.returncode == 0:
            logging.info(f'{exe_path} executed successfully.')
            print(f'{exe_path} executed successfully.')
        else:
            logging.error(f'{exe_path} failed with return code {process.returncode}. Error: {process.stderr}')
            print(f'{exe_path} failed with return code {process.returncode}.')
            print(f"Error: {process.stderr}")
    except Exception as e:
        logging.error(f'Error running {exe_path}: {e}')
        print(f'Error running {exe_path}: {e}')

if __name__ == '__main__':
    # Define the shared drive path to test
    shared_drive_path = r'\\ginesystechstorage.file.core.windows.net\pgmigration'

    # Test access to the shared drive
    test_shared_drive_access(shared_drive_path)

    # Azure File Share credentials and details
    storage_account_name = 'ginesystechstorage'
    file_share_name = 'pgmigration'
    directory_name = '_PGMigrationBackup'
    file_name = 'reportmigration.exe'
    access_key = 'YourAccessKey'  # Replace with your actual access key

    # Download the reportmigration.exe file from Azure
    download_file_from_azure(storage_account_name, file_share_name, directory_name, file_name, access_key)

    # Run the report application
    backup_path = r'Z:\_PGMigrationBackup'
    run_report_app(backup_path, 'BAZH_20342', '0')
