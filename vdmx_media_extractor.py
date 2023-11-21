'''
This script was created by ProjectileObjects for the VDMX community.  

It was tested on a homebrewed installed version of Python 3.8 with the assistance of ChatGPT (for debugging).

Installation
1. Ensure you have Python 3.8 or higher installed.
2. Download or clone this repository to your local machine.
3. [Any additional setup steps].

Dependencies
- Tkinter (usually comes with Python 3. If not, [instructions to install]).

Usage
Run the script from the command line:
```bash
python vdmx_media_extractor.py [optional arguments]


For communication: 
@ProjectileObjects 
ProjectileObjects@gmail.com

MIT License Copyright (c) ProjectileObjects LLC. 2023

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

import os
import shutil
import xml.etree.ElementTree as ET
from tkinter import filedialog, Tk, messagebox

def init_tk():
    root = Tk()
    root.withdraw()
    return root

def select_file(root):
    print("Prompting for VDMX file selection...")
    file_path = filedialog.askopenfilename(parent=root, title="Select a VDMX file", filetypes=[("VDMX files", "*.vdmx5")])
    print(f"Selected file: {file_path}")
    return file_path

def select_output_folder(root):
    print("Prompting for output folder selection...")
    folder_path = filedialog.askdirectory(parent=root, title="Select Output Folder")
    print(f"Selected output folder: {folder_path}")
    return folder_path

def copy_media_files(vdmx_file, output_folder):
    print(f"Starting to process file: {vdmx_file}")
    try:
        tree = ET.parse(vdmx_file)
        root = tree.getroot()
        print("XML parsed successfully")

        previous_elem = None

        for elem in root.iter():
            if previous_elem is not None and previous_elem.tag == 'key' and previous_elem.text == 'mediaPath':
                if elem.tag == 'string':
                    media_path = elem.text
                    print(f"Found media path: {media_path}")

                    if media_path and os.path.exists(media_path):
                        file_name = os.path.basename(media_path)
                        output_file = os.path.join(output_folder, file_name)
                        print(f"Preparing to copy {file_name}")

                        if not os.path.exists(output_file):
                            shutil.copy2(media_path, output_folder)
                            print(f"Copied: {file_name}")
                        else:
                            print(f"File already exists: {file_name}")
                    else:
                        print(f"Media path is not valid or file does not exist: {media_path}")

            previous_elem = elem

    except ET.ParseError as e:
        print(f"Error parsing the file: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def main():
    root = init_tk()

    vdmx_file = select_file(root)
    if not vdmx_file:
        print("No file selected, exiting...")
        root.destroy()
        return

    output_folder = select_output_folder(root)
    if not output_folder:
        print("No output folder selected, exiting...")
        root.destroy()
        return

    root.destroy()
    copy_media_files(vdmx_file, output_folder)
    messagebox.showinfo("Complete", "Search and copy complete.")

if __name__ == "__main__":
    main()
