#
#   Written by:  Mark W Kiehl
#   http://mechatronicsolutionsllc.com/
#   http://www.savvysolutions.info/savvycodesolutions/

# Copyright (C) Mechatroinc Solutions LLC 2025
# License:  MIT


# Define the script version in terms of Semantic Versioning (SemVer)
# when Git or other versioning systems are not employed.
__version__ = "0.0.0"
from pathlib import Path
print("'" + Path(__file__).stem + ".py'  v" + __version__)
# v0.0.0    Initial release


"""
This script will be packaged into a container and configured to run as a Cloud Run Job.
A Cloud Storage volume mount is used to create a bridge between the Cloud Storage bucket
and the Cloud Run container's file system.
Volume mounts allow a container (this script) to access files stored in persistent disks or NFS shares as if they were local.
The feature leverages Cloud Storage FUSE to provide this file system interface.  

The script writes a UTF-8 text file with 5 lines of random characters, and then attempts to read them back. 

"""

import os
from pathlib import Path


# ---------------------------------------------------------------------------
# Helpful tools

def savvy_get_os(verbose=False):
    """
    Returns the following OS descriptions depending on what OS the Python script is running in:
        "Windows"
        "Linux"
        "macOS"

    os_name = savvy_get_os()
    """

    import platform

    if platform.system() == "Windows":
        return "Windows"
    elif platform.system() == "Linux":
        return "Linux"
    elif platform.system() == "Darwin":
        return "macOS"
    else:
        raise Exception("Unknown OS: ", platform.system())


def gcp_json_credentials_exist(verbose=False):
    """
    Returns TRUE if the Application Default Credentials (ADC) file "application_default_credentials.json" is found.

    Works with both Windows and Linux OS.

    https://cloud.google.com/docs/authentication/application-default-credentials#personal
    """

    from pathlib import Path

    if savvy_get_os() == "Windows":
        # Windows: %APPDATA%\gcloud\application_default_credentials.json
        path_gcloud = Path(Path.home()).joinpath("AppData\\Roaming\\gcloud")
        if not path_gcloud.exists():
            if verbose: print("WARNING:  Google CLI folder not found: " + str(path_gcloud))
            #raise Exception("Google CLI has not been installed!")
            return False
        if verbose: print(f"path_gcloud: {path_gcloud}")
        path_file_json = path_gcloud.joinpath("application_default_credentials.json")
        if not path_file_json.exists() or not path_file_json.is_file():
            if verbose: print("WARNING: Application Default Credential JSON file missing: "+ str(path_file_json))
            #raise Exception("File not found: " + str(path_file_json))
            return False
        
        if verbose: print(str(path_file_json))
        return True
    else:
        # Linux, macOS: 
        # $HOME/.config/gcloud/application_default_credentials.json
        # //root/.config/gcloud/application_default_credentials.json
        path_gcloud = Path(Path.home()).joinpath(".config/gcloud/")
        if not path_gcloud.exists():
            if verbose: 
                print("Path.home(): ", str(Path.home()))
                print("WARNING:  Google CLI folder not found: " + str(path_gcloud))
            # WARNING:  Google CLI folder not found: /.config/gcloud
            #raise Exception("Google CLI has not been installed!")
            return False
        if verbose: print(f"path_gcloud: {path_gcloud}")

        path_file_json = path_gcloud.joinpath("application_default_credentials.json")
        if not path_file_json.exists() or not path_file_json.is_file():
            if verbose: print("WARNING: Application Default Credential JSON file missing: "+ str(path_file_json))
            # /root/.config/gcloud/application_default_credentials.json
            #os.environ['GOOGLE_APPLICATION_CREDENTIALS'] ='$HOME/.config/gcloud/application_default_credentials.json'
            #raise Exception("File not found: " + str(path_file_json))
            return False
        
        if verbose: print(str(path_file_json))
        # /root/.config/gcloud/application_default_credentials.json
        return True




if __name__ == '__main__':

    print(f"\nOperating system: {savvy_get_os()}")

    adc_json_file_found = gcp_json_credentials_exist()
    print(f"Application Default Credentials (ADC) file 'application_default_credentials.json' found: {adc_json_file_found}\n")

    if adc_json_file_found:
        # This script is running locally, either directly, or from within a Docker container with a blind volume for the Google SDK folder, but not via Google Run or similar.
        print(f"The script is running locally, either directly OR from within a local Docker container with a blind volume created for the Google SDK folder.")

    else:
        # gcp_json_credentials_exist() == False
        # This script is running from a Docker container via Google Run Jobs.
        print(f"This script is running from a Docker container via Google Run.")

        # Get the Google Storage bucket mount path from the OS environment variable, or assign a default.
        bucket_mount_path = os.environ.get('MOUNT_PATH', '/mnt/storage')
        print(f"bucket_mount_path: {bucket_mount_path}")

        # Create the folder 'bucket_mount_path' if it doesn't exist using pathlib
        path_bucket_mount = Path(bucket_mount_path)
        #print(f"path_bucket_mount.is_dir(): {path_bucket_mount.is_dir()}")
        if not path_bucket_mount.is_dir:  path_bucket_mount.mkdir()
        if not path_bucket_mount.is_dir: raise Exception(f"Unable to create folder {path_bucket_mount}")

        # Define the text filename to write/read to.
        path_file = path_bucket_mount.joinpath("text_file_utf8.txt")
        print(f"path_file: {path_file}")
        if path_file.is_file():  path_file.unlink()     # Delete the file if it already exists
        if path_file.is_file(): raise Exception(f"Unable to delete file {path_file}")

        # Generate random strings and write them to path_file
        import random
        import string
        length = 40
        characters = string.ascii_letters + string.digits
        
        # Write the file
        print(f"Writing line by line utf-8 text file: {path_file}")
        with open(file=path_file, mode="w", encoding='utf-8') as f:
            for l in range(0, 5):
                rnd_str = ''.join(random.choice(characters) for i in range(length))
                f.write(rnd_str + "\n")
        
        # Read the file
        if not path_file.is_file(): raise Exception(f"File not found {path_file}")
        print(f"Reading line by line utf-8 text file: {path_file}")
        i = 0
        with open(file=path_file, mode="r", encoding='utf-8') as f:
            for line in f.readlines():
                i += 1
                # Only process lines that are not blank by using: if len(line.strip()) > 0:
                if len(line.strip()) > 0: print(f"{i}  {line.strip()}")        # .strip() removes \n


