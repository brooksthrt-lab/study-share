import cloudinary
import cloudinary.uploader
import os
from dotenv import load_dotenv

load_dotenv()

cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET")
)

def upload_file(file):
    original_filename = file.filename
    print(f"DEBUG - filename received: {original_filename}")  # temporary debug line
    
    result = cloudinary.uploader.upload(
        file,
        resource_type="raw",
        public_id=original_filename,
        overwrite=True
    )
    return result["secure_url"]