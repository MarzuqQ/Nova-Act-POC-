"""
File utilities for Nova Act automation
"""
import os
import shutil
import logging
from pathlib import Path
from typing import List, Optional, Tuple
import mimetypes

logger = logging.getLogger(__name__)

class FileUtils:
    """Utility class for file operations"""
    
    # Supported file types and their maximum sizes (in bytes)
    SUPPORTED_TYPES = {
        '.json': 1024 * 1024,      # 1MB
        '.pdf': 10 * 1024 * 1024,  # 10MB
        '.csv': 2 * 1024 * 1024,   # 2MB
        '.xml': 1024 * 1024,       # 1MB
        '.txt': 1024 * 1024,       # 1MB
    }
    
    @staticmethod
    def validate_file(file_path: str) -> Tuple[bool, str]:
        """
        Validate if a file is suitable for upload
        Returns (is_valid, error_message)
        """
        try:
            file_path = Path(file_path)
            
            # Check if file exists
            if not file_path.exists():
                return False, f"File not found: {file_path}"
            
            # Check if it's a file (not directory)
            if not file_path.is_file():
                return False, f"Path is not a file: {file_path}"
            
            # Check file extension
            extension = file_path.suffix.lower()
            if extension not in FileUtils.SUPPORTED_TYPES:
                supported = ', '.join(FileUtils.SUPPORTED_TYPES.keys())
                return False, f"Unsupported file type: {extension}. Supported: {supported}"
            
            # Check file size
            file_size = file_path.stat().st_size
            max_size = FileUtils.SUPPORTED_TYPES[extension]
            if file_size > max_size:
                return False, f"File too large: {file_size} bytes (max {max_size} bytes for {extension})"
            
            # Check if file is readable
            if not os.access(file_path, os.R_OK):
                return False, f"File is not readable: {file_path}"
            
            return True, "File is valid"
            
        except Exception as e:
            return False, f"Error validating file: {e}"
    
    @staticmethod
    def get_file_info(file_path: str) -> dict:
        """Get detailed information about a file"""
        try:
            file_path = Path(file_path)
            
            if not file_path.exists():
                return {"error": "File not found"}
            
            stat = file_path.stat()
            mime_type, _ = mimetypes.guess_type(str(file_path))
            
            return {
                "name": file_path.name,
                "path": str(file_path.absolute()),
                "size": stat.st_size,
                "extension": file_path.suffix.lower(),
                "mime_type": mime_type,
                "created": stat.st_ctime,
                "modified": stat.st_mtime,
                "is_readable": os.access(file_path, os.R_OK),
                "is_writable": os.access(file_path, os.W_OK)
            }
            
        except Exception as e:
            return {"error": f"Error getting file info: {e}"}
    
    @staticmethod
    def prepare_upload_file(source_path: str, upload_dir: str = "temp_uploads") -> str:
        """
        Prepare a file for upload by copying it to a temporary directory
        Returns the path to the prepared file
        """
        try:
            source_path = Path(source_path)
            upload_dir = Path(upload_dir)
            
            # Validate source file
            is_valid, error_msg = FileUtils.validate_file(str(source_path))
            if not is_valid:
                raise ValueError(error_msg)
            
            # Create upload directory
            upload_dir.mkdir(exist_ok=True)
            
            # Generate unique filename
            from datetime import datetime
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            new_name = f"{timestamp}_{source_path.name}"
            dest_path = upload_dir / new_name
            
            # Copy file
            shutil.copy2(source_path, dest_path)
            
            logger.info(f"Prepared file for upload: {source_path} -> {dest_path}")
            return str(dest_path)
            
        except Exception as e:
            logger.error(f"Error preparing file for upload: {e}")
            raise
    
    @staticmethod
    def cleanup_temp_files(upload_dir: str = "temp_uploads") -> None:
        """Clean up temporary upload files"""
        try:
            upload_dir = Path(upload_dir)
            
            if not upload_dir.exists():
                return
            
            # Remove all files in the upload directory
            for file_path in upload_dir.glob("*"):
                if file_path.is_file():
                    file_path.unlink()
                    logger.debug(f"Removed temp file: {file_path}")
            
            # Remove directory if empty
            if not any(upload_dir.iterdir()):
                upload_dir.rmdir()
                logger.debug(f"Removed empty temp directory: {upload_dir}")
            
        except Exception as e:
            logger.error(f"Error cleaning up temp files: {e}")
    
    @staticmethod
    def find_files_by_pattern(directory: str, pattern: str) -> List[str]:
        """Find files matching a pattern in a directory"""
        try:
            directory = Path(directory)
            
            if not directory.exists():
                return []
            
            files = []
            for file_path in directory.glob(pattern):
                if file_path.is_file():
                    files.append(str(file_path))
            
            return sorted(files)
            
        except Exception as e:
            logger.error(f"Error finding files: {e}")
            return []
    
    @staticmethod
    def get_sample_files(sample_dir: str = "sample_data") -> List[dict]:
        """Get information about available sample files"""
        try:
            sample_dir = Path(sample_dir)
            
            if not sample_dir.exists():
                return []
            
            sample_files = []
            
            for file_path in sample_dir.glob("*.json"):
                if file_path.is_file():
                    info = FileUtils.get_file_info(str(file_path))
                    if "error" not in info:
                        sample_files.append(info)
            
            return sorted(sample_files, key=lambda x: x['name'])
            
        except Exception as e:
            logger.error(f"Error getting sample files: {e}")
            return []
    
    @staticmethod
    def backup_file(file_path: str, backup_dir: str = "backups") -> Optional[str]:
        """Create a backup of a file"""
        try:
            file_path = Path(file_path)
            backup_dir = Path(backup_dir)
            
            if not file_path.exists():
                return None
            
            # Create backup directory
            backup_dir.mkdir(exist_ok=True)
            
            # Generate backup filename
            from datetime import datetime
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_name = f"{file_path.stem}_{timestamp}{file_path.suffix}"
            backup_path = backup_dir / backup_name
            
            # Copy file
            shutil.copy2(file_path, backup_path)
            
            logger.info(f"Created backup: {file_path} -> {backup_path}")
            return str(backup_path)
            
        except Exception as e:
            logger.error(f"Error creating backup: {e}")
            return None

def main():
    """Test file utilities"""
    file_utils = FileUtils()
    
    # Test validation
    test_files = [
        "sample_data/shipment_data.json",
        "sample_data/nested_shipment_data.json",
        "sample_data/alternative_format.json"
    ]
    
    for file_path in test_files:
        is_valid, message = file_utils.validate_file(file_path)
        print(f"{file_path}: {'✓' if is_valid else '✗'} {message}")
        
        if is_valid:
            info = file_utils.get_file_info(file_path)
            print(f"  Size: {info['size']} bytes")
            print(f"  Type: {info['mime_type']}")
    
    # Test finding sample files
    sample_files = file_utils.get_sample_files()
    print(f"\nFound {len(sample_files)} sample files:")
    for file_info in sample_files:
        print(f"  {file_info['name']} ({file_info['size']} bytes)")

if __name__ == "__main__":
    main() 