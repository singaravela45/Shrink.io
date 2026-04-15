import subprocess
import os
import shutil

def compress_pdf(input_path, output_path, level):
    level = level.strip()
    gs_bin = shutil.which("gs")
    if not gs_bin:
        raise Exception("The 'gs' executable was not found. Try: sudo apt install ghostscript")
    if level == "Extreme Compression":
        quality = "/screen"  
    elif level == "Recommended Compression":
        quality = "/ebook"
    else:
        quality = "/prepress" 
    input_path = os.path.abspath(input_path)
    output_path = os.path.abspath(output_path)
    command = [
        gs_bin,
        "-sDEVICE=pdfwrite",
        "-dCompatibilityLevel=1.4",
        f"-dPDFSETTINGS={quality}",
        "-dNOPAUSE",
        "-dBATCH",
        "-dQUIET",
        f"-sOutputFile={output_path}",
        input_path
    ]
    try:
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        if not os.path.exists(output_path) or os.path.getsize(output_path) == 0:
            raise Exception("Ghostscript ran but created an empty or missing file.")            
        return output_path

    except subprocess.CalledProcessError as e:
        print(f"--- GS DEBUG START ---")
        print(f"STDOUT: {e.stdout}")
        print(f"STDERR: {e.stderr}")
        print(f"--- GS DEBUG END ---")
        raise Exception(f"Ghostscript Error: {e.stderr}")