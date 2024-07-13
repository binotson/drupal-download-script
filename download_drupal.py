"""
Script to download, extract, and move the latest Drupal version to the htdocs directory.
"""

import os
import tarfile
import shutil
import requests
from requests.exceptions import Timeout

# Step 1: Download Drupal
DRUPAL_URL = 'https://www.drupal.org/download-latest/tar.gz'
DOWNLOAD_FOLDER = os.path.expanduser('~/Downloads')
DOWNLOAD_PATH = os.path.join(DOWNLOAD_FOLDER, 'drupal.tar.gz')
TIMEOUT = 120  # Increased timeout

def download_drupal(url, path, timeout, retries=3):
    """
    Downloads a file from the specified URL to the given path with a specified timeout.
    Retries the download if it times out.

    Parameters:
    url (str): The URL to download the file from.
    path (str): The local path to save the downloaded file.
    timeout (int): The timeout duration in seconds.
    retries (int): The number of retry attempts in case of timeout. Default is 3.

    Returns:
    bool: True if the download was successful, False otherwise.
    """
    for attempt in range(retries):
        try:
            response = requests.get(url, stream=True, timeout=timeout)
            with open(path, 'wb') as file:
                shutil.copyfileobj(response.raw, file)
            print(f"Drupal downloaded to {path}")
            return True
        except Timeout:
            print(f"Attempt {attempt + 1} of {retries} timed out.")
    print("Failed to download Drupal after several attempts.")
    return False

# Download Drupal
if not download_drupal(DRUPAL_URL, DOWNLOAD_PATH, TIMEOUT):
    raise RuntimeError(
        "Failed to download Drupal. Please check your internet connection and try again."
    )

# Step 2: Extract Drupal
EXTRACTED_FOLDER = os.path.join(DOWNLOAD_FOLDER, 'drupal-extracted')
if not os.path.exists(EXTRACTED_FOLDER):
    os.makedirs(EXTRACTED_FOLDER)

# Attempt extraction with proper error handling for permissions
try:
    with tarfile.open(DOWNLOAD_PATH, 'r:gz') as tar:
        tar.extractall(path=EXTRACTED_FOLDER)
    print(f"Drupal extracted to {EXTRACTED_FOLDER}")
except PermissionError as e:
    raise PermissionError(
        "Permission denied. Please run the script with administrator privileges."
    ) from e

# Find the extracted Drupal folder (usually drupal-x.x.x)
EXTRACTED_DRUPAL_FOLDER = None
for root, dirs, files in os.walk(EXTRACTED_FOLDER):
    for directory in dirs:
        if directory.startswith('drupal-'):
            EXTRACTED_DRUPAL_FOLDER = os.path.join(root, directory)
            break
    if EXTRACTED_DRUPAL_FOLDER:
        break

if not EXTRACTED_DRUPAL_FOLDER:
    raise FileNotFoundError("Extracted Drupal folder not found")

# Step 3: Copy to htdocs
HTDOCS_FOLDER = r'C:\xampp\htdocs'  # Change this to your actual htdocs path for Windows
# HTDOCS_FOLDER = '/var/www/html'  # Uncomment this for Linux with Apache

DESTINATION_FOLDER = os.path.join(HTDOCS_FOLDER, 'drupal')

if os.path.exists(DESTINATION_FOLDER):
    shutil.rmtree(DESTINATION_FOLDER)  # Remove the existing directory if it exists
shutil.copytree(EXTRACTED_DRUPAL_FOLDER, DESTINATION_FOLDER)
print(f"Drupal copied to {DESTINATION_FOLDER}")
