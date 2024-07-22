import os
from tinytag import TinyTag
from tkinter.filedialog import askdirectory
import re


def remove_feat(text):
    # Regularni izraz koji pronalazi dio stringa u formatu (feat. Ime)
    pattern = r"\s*\(feat\..*?\)"
    # Zamjena pronađenog dijela sa praznim stringom
    return re.sub(pattern, '', text).strip()


def rename_file(song_artist, song_title):
    new_name = song_artist + " - " + song_title
    old_name = filename[0:filename.index('.mp3')]
    new_filename = filename.replace(old_name, new_name).strip()

    old_file = os.path.join(folder_path, filename)
    new_file = os.path.join(folder_path, new_filename)
    os.rename(old_file, new_file)


# Definiranje putanje do foldera
folder_path = askdirectory(title='Select Folder')
print("folder path is ->", folder_path)

# Provjera da li folder postoji
if not os.path.exists(folder_path):
    print(f"Folder {folder_path} ne postoji.")
else:
    # Iteracija kroz sve datoteke u folderu
    for filename in os.listdir(folder_path):
        audio = TinyTag.get(folder_path + "/" + filename)

        title = audio.title
        if title is None:
            continue
        title = title.replace(" - ", " ")
        if "feat." in title:
            title = remove_feat(title)

        artist = audio.artist
        if artist is None:
            continue
        artist = artist.replace("/", ", ")

        rename_file(artist, title)

print("Preimenovanje je završeno.")
