import os
import stat
import time
import argparse
from PIL import Image

import magic


def extract_file_metadata(file_path):
    try:
        # Get file metadata using os.stat
        file_stat = os.stat(file_path)
        
        # Extract relevant file metadata
        creation_time = file_stat.st_ctime
        modification_time = file_stat.st_mtime
        access_time = file_stat.st_atime
        size = file_stat.st_size

        # Get file type
        mime = magic.Magic()
        file_type = mime.from_file(file_path)

        # Initialize other metadata variables
        author = None
        owner = file_stat.st_uid
        permissions = oct(stat.S_IMODE(file_stat.st_mode))
        tags = None
        gps_coordinates = None
        camera_settings = None
        audio_bitrate = None
        video_resolution = None

        # Convert timestamps to human-readable format
        creation_time_str = time.ctime(creation_time)
        modification_time_str = time.ctime(modification_time)
        access_time_str = time.ctime(access_time)

        # For images (JPEG, PNG, etc.)
        if file_type.startswith("image"):
            with Image.open(file_path) as img:
                exif_data = img._getexif()
                if exif_data:
                    author = exif_data.get(315, None)  # 315 is the EXIF tag for Author/Artist
                    gps_coordinates = exif_data.get(34853, None)  # 34853 is the EXIF tag for GPS Info

        # For PDF files
        if file_type == "application/pdf":
            with open(file_path, "rb") as pdf_file:
                pdf_reader = PdfFileReader(pdf_file)
                author = pdf_reader.getDocumentInfo().author

        # For audio files (MP3, etc.)
        if file_type.startswith("audio"):
            # You may use a specialized library to extract audio metadata
            pass

        # For video files
        if file_type.startswith("video"):
            # You may use a specialized library to extract video metadata
            pass

        # Print extracted metadata
        print("---File Meta Data Extractor ~by JUDE---")
        print()
        print(f"File: {file_path}")
        print(f"File Type: {file_type}")
        print(f"Size: {size} bytes")
        print(f"Creation Time: {creation_time_str}")
        print(f"Modification Time: {modification_time_str}")
        print(f"Access Time: {access_time_str}")
        print(f"Author: {author}")
        print(f"Owner (User ID): {owner}")
        print(f"Permissions: {permissions}")
        print(f"Tags: {tags}")
        print(f"GPS Coordinates: {gps_coordinates}")
        print(f"Camera Settings: {camera_settings}")
        print(f"Audio Bitrate: {audio_bitrate}")
        print(f"Video Resolution: {video_resolution}")
        print()
        print("*** For more details and Tools visit our GitHub page 'CyberMystic-Jude' ***")
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except Exception as e:
        print(f"Error extracting metadata: {str(e)}")
       

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="File Metadata Extractor -by Jude",
        epilog="Example: python MetaDataExtract.py -f '/path/to/your/file.txt'  # Extract metadata for a specific file"
    )
    parser.add_argument("-f", "--file", required=True, help="Path to the file for which you want to extract metadata ")

    args = parser.parse_args()

    file_path = args.file
    extract_file_metadata(file_path)

