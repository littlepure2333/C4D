#!/usr/bin/env python3
"""
Video compression script using ffmpeg
"""

import subprocess
import os
import sys
from pathlib import Path


def compress_video(input_file, output_file=None, quality='medium', scale=None):
    """
    Compress video file using ffmpeg
    
    Args:
        input_file (str): Path to input video file
        output_file (str): Path to output video file (optional)
        quality (str): Compression quality - 'low' (smaller), 'medium', 'high' (better quality)
        scale (str): Resize video, e.g., '1280:720' or '50%'
    
    Returns:
        bool: True if successful, False otherwise
    """
    
    # Check if input file exists
    if not os.path.exists(input_file):
        print(f"Error: Input file '{input_file}' not found!")
        return False
    
    # Set output filename if not provided
    if output_file is None:
        path = Path(input_file)
        output_file = str(path.parent / f"{path.stem}_compressed.mp4")
    
    # CRF (Constant Rate Factor) values: 0-51, lower = better quality
    # Default is 23
    crf_values = {
        'low': '28',      # More compression, lower quality
        'medium': '23',   # Default, balanced
        'high': '18'      # Less compression, higher quality
    }
    crf = crf_values.get(quality, '23')
    
    # Build ffmpeg command
    cmd = [
        'ffmpeg',
        '-i', input_file,
        '-c:v', 'libx264',           # Video codec
        '-crf', crf,                  # Quality (lower = better)
        '-c:a', 'aac',                # Audio codec
        '-b:a', '128k',               # Audio bitrate
    ]
    
    # Add scaling if specified
    if scale:
        cmd.extend(['-vf', f'scale={scale}'])
    
    cmd.append(output_file)
    
    # Get file sizes
    input_size = os.path.getsize(input_file) / (1024 * 1024)  # MB
    
    print(f"Compressing video...")
    print(f"Input: {input_file} ({input_size:.2f} MB)")
    print(f"Output: {output_file}")
    print(f"Quality: {quality} (CRF={crf})")
    if scale:
        print(f"Scale: {scale}")
    print()
    
    try:
        # Run ffmpeg
        subprocess.run(cmd, check=True)
        
        # Get output file size
        output_size = os.path.getsize(output_file) / (1024 * 1024)  # MB
        compression_ratio = (1 - output_size / input_size) * 100
        
        print(f"\n✅ Compression successful!")
        print(f"Output size: {output_size:.2f} MB")
        print(f"Compression ratio: {compression_ratio:.1f}%")
        
        return True
    
    except subprocess.CalledProcessError as e:
        print(f"❌ Error during compression: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False


if __name__ == '__main__':
    # Example usage
    if len(sys.argv) < 2:
        print("Usage: python compress_video.py <input_file> [output_file] [quality] [scale]")
        print()
        print("Examples:")
        print("  python compress_video.py video.mp4")
        print("  python compress_video.py video.mp4 compressed.mp4 medium")
        print("  python compress_video.py video.mp4 compressed.mp4 low 1280:720")
        print()
        print("Quality options: low (smaller), medium (default), high (better)")
        print("Scale examples: 1280:720, 50%, 1920:1080")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    quality = sys.argv[3] if len(sys.argv) > 3 else 'medium'
    scale = sys.argv[4] if len(sys.argv) > 4 else None
    
    compress_video(input_file, output_file, quality, scale)
