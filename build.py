#------------------------------------------------------------
import os
import io
import re
import shutil
import pycdlib
import subprocess
from sys import platform
from tools.setup_linux import *
from PIL import Image, ImageDraw, ImageFont
from translation.translate import translate, Injector
#------------------------------------------------------------
iso_dir = "iso"
asm_src_dir = "source"
build_dir = "build"
assets = "assets"
quests_dir = "quests"
release_dir = "release"
#------------------------------------------------------------
armips = os.path.join("tools", "armips.exe")
umd_replace = os.path.join("tools", "UMD-replace.exe")
xdelta = os.path.join("tools", "xdelta.exe")
mhff = os.path.join("tools", "mhff", "psp", "data.py")
pspdecrypt = os.path.join("tools", "pspdecrypt.exe")
#------------------------------------------------------------
if not os.path.exists(mhff):
    installMHFF()

if platform == "linux" or platform == "linux2":
    armips = os.path.join("tools", "armips", "build", "armips")
    umd_replace = os.path.join("tools", "UMD-replace")
    xdelta = "xdelta3"
    if not os.path.exists(armips):
        installArmips()
    if not os.path.exists(umd_replace):
        installUMDReplace()
        
games = []

def createFolder(folder):
    if os.path.exists(folder):
        shutil.rmtree(folder)
    os.makedirs(folder, exist_ok=True)

def createPatches():
    for folder in games:
        print(f"Creating xdelta patch for {folder}.iso...")
        unmodified = os.path.join(iso_dir, f"{folder}.iso")
        modified = os.path.join(build_dir, folder, f"{folder}.iso")
        patch = os.path.join(build_dir, folder, f"{folder}.xdelta")
        subprocess.run(
            [xdelta, "-e", "-s", unmodified, modified, patch],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.STDOUT
        )
        if folder == "ULJM05156":
               release = os.path.join(release_dir, "ULJM05156.xdelta")
            
        if os.path.exists(release):
            os.remove(release)
        os.rename(patch, release)

def patchISOs():
    for folder in games:
        iso = os.path.join(build_dir, folder, f"{folder}.iso")
        print(f"Patching DATA.BIN for {folder}.iso...")
        subprocess.run(
            [umd_replace, iso, "/PSP_GAME/USRDIR/DATA.BIN", os.path.join(build_dir, folder, "DATA.BIN")],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.STDOUT
        )
        print(f"Patching EBOOT.BIN for {folder}.iso...")
        subprocess.run(
            [umd_replace, iso, "/PSP_GAME/SYSDIR/EBOOT.BIN", os.path.join(build_dir, folder, "EBOOT.BIN")],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.STDOUT
        )
        PIC0 = os.path.join(assets, "PIC0.PNG")
        subprocess.run(
            [umd_replace, iso, "/PSP_GAME/PIC0.PNG", PIC0],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.STDOUT
        )
 
def extractData():
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
            if not (game_id == "ULJM05156"):
                continue
            dir = os.path.join(build_dir, game_id)
            createFolder(dir)
            print(f"Extracting DATA.BIN from {file}...")
            with open(os.path.join(dir, "DATA.BIN"), "wb") as data_bin:
                iso.get_file_from_iso_fp(data_bin, iso_path="/PSP_GAME/USRDIR/DATA.BIN")
            print(f"Extracting EBOOT.BIN from {file}...")
            with open(os.path.join(dir, "EBOOT.BIN"), "wb") as eboot_bin:
                iso.get_file_from_iso_fp(eboot_bin, iso_path="/PSP_GAME/SYSDIR/EBOOT.BIN")
            iso.close()
            shutil.copyfile(os.path.join(iso_dir, file), os.path.join(build_dir, game_id, f"{game_id}.iso"))
            os.rename(os.path.join(iso_dir, file), os.path.join(iso_dir, f"{game_id}.iso"))
            print(f"Decrypting EBOOT.BIN for {file}...")
            subprocess.run(
                [pspdecrypt, os.path.join(dir, "EBOOT.BIN")],
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.STDOUT
            )
            os.remove(os.path.join(dir, "EBOOT.BIN"))
            os.rename(os.path.join(dir, "EBOOT.BIN.dec"), os.path.join(dir, "EBOOT.BIN"))
            
            games.append(game_id)
            
 
if __name__ == "__main__":
    createFolder(build_dir)
    
    extractData()
    translate(build_dir)
    patchISOs()
    createPatches()
        
    print("Done!")
