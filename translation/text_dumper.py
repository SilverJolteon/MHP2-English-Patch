import os
import io
import shutil
import pycdlib
import subprocess

iso_dir = os.path.join("..", "iso")
mhff = os.path.join("..", "tools", "mhff", "psp", "data.py")
build_dir = "dumped_text"

newline = "<NEWLINE>"
new_section = "<NEW SECTION>"


data = {
    "ULJM05156": {
        "0003": ["general", 1],
        "9308": ["game0", 1],
        "9309": ["game1", 1],
        "9660": ["tavern", 3],
        "9661": ["pokke", 3],
        "9662": ["farm", 3],
        "9663": ["kitchen", 3]
    },
    "ULUS10266": {
        "0003": ["general", 1],
        "9308": ["game0", 1],
        "9309": ["game1", 1],
        "9660": ["tavern", 3],
        "9661": ["pokke", 3],
        "9662": ["farm", 3],
        "9663": ["kitchen", 3]
    }
}
        
def getString(data, addr, encoding):
    return data[addr:data.find(b"\x00", addr)].decode(encoding)
    
def getOffset(data, addr):
    return int.from_bytes(data[addr:addr+4], byteorder="little", signed=False)

def dumpNPCText(key, folder, path, encoding):
    input = os.path.join(build_dir, folder, key)
    
    os.makedirs(path, exist_ok=True)
    
    print(f"Dumping strings to \"{path}\"...");
    with open(input, "rb") as fp:
        header_data = []
        data = fp.read()
        h_off = 0
        while(1):
            sec_id = getOffset(data, h_off)
            sec_off = getOffset(data, h_off+4)
            if(sec_id == 0xFFFFFFFF and sec_off == 0xFFFFFFFF):
                break;
            header_data.append([sec_id, sec_off])
            h_off += 8
            
        for i, section in enumerate(header_data):
            with open(os.path.join(path, f"string_table_{i}_{section[0]}.txt"), "w", encoding=encoding) as out:
                sec_start = section[1]
                
                s_off = getOffset(data, sec_start+4)
                
                sec_off = sec_start
                while(sec_off < sec_start + s_off):
                    str_id = getOffset(data, sec_off)
                    str_off = getOffset(data, sec_off+4)
                    str = f"{str_id}," + getString(data, sec_start+str_off, encoding).replace("\n", newline)
                    sec_off += 8
                    if(sec_off+4 < sec_start + s_off):
                        str += "\n"
                    out.write(str)
                    
    shutil.copyfile(input, os.path.join(path, key))
    os.remove(input)
    
def dumpGameText(key, folder, path, encoding):
    input = os.path.join(build_dir, folder, key)
    
    os.makedirs(path, exist_ok=True)
    
    print(f"Dumping strings to \"{path}\"...");
    with open(input, "rb") as fp:
        header_data = []
        data = fp.read()
        sec_size = getOffset(data, 0)
       
        for i in range(8, sec_size * 4 + 8, 4):
            sec_off = getOffset(data, i)
            header_data.append(sec_off)
            
        for i, section in enumerate(header_data):
            with open(os.path.join(path, f"string_table_{i}.txt"), "w", encoding=encoding) as out:
                sec_start = section
                
                s_off = getOffset(data, sec_start)
                
                sec_off = sec_start
                while(sec_off < sec_start + s_off):
                    str_off = getOffset(data, sec_off)
                    str = getString(data, sec_start+str_off, encoding).replace("\n", newline)
                    sec_off += 4
                    if(sec_off+4 < sec_start + s_off):
                        str += "\n"
                    out.write(str)
                    
    shutil.copyfile(input, os.path.join(path, key))
    os.remove(input)

def extractFiles(folder):
    path = os.path.join(build_dir, folder, "DATA.BIN")
    encoding = "utf-8"
    #if(folder == "ULJM05156" or folder == "ULUS10266"): encoding = "shift_jis_2004"
    #else: encoding = "utf-8"
    for key, value in data[folder].items():
        print(f"Extracting file \"{key}\" from {folder}.iso...");
        file = os.path.join(build_dir, folder, key)
        subprocess.run(
            ["python", mhff, "x", path, key, file],
            check=True
        )
        if(value[1] == 1):
            dumpGameText(key, folder, os.path.join(build_dir, folder, value[0]), encoding)
        if(value[1] == 3):
            dumpNPCText(key, folder, os.path.join(build_dir, folder, value[0]), encoding)

    os.remove(path)

def extractDataBin():
    for _, _, files in os.walk(iso_dir):
        for file in files:
            if not file.endswith(".iso"):
               continue
            iso = pycdlib.PyCdlib()
            iso.open(os.path.join(iso_dir, file))
            param = io.BytesIO()
            iso.get_file_from_iso_fp(param, iso_path="/PSP_GAME/PARAM.SFO")
            param.seek(0x128)
            game_id = param.read(0x0A)
            game_id = game_id.split(b"\x00", 1)[0].decode("utf-8")
            if not (game_id == "ULJM05156" or game_id == "ULUS10266" or game_id == "ULES00851"):
                continue
            dir = os.path.join(build_dir, game_id)
            if os.path.exists(dir):
                shutil.rmtree(dir)
            os.makedirs(dir, exist_ok=True)
            print(f"Extracting DATA.BIN from {file}...")
            with open(os.path.join(dir, "DATA.BIN"), "wb") as data_bin:
                iso.get_file_from_iso_fp(data_bin, iso_path="/PSP_GAME/USRDIR/DATA.BIN")
            iso.close()

if __name__ == "__main__":
    if os.path.exists(build_dir):
        shutil.rmtree(build_dir)
    os.makedirs(build_dir, exist_ok=True)
    
    extractDataBin()
    for folder in os.listdir(build_dir):
        extractFiles(folder)
    
    print("\nDone!")