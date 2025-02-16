import os
from tinytag import TinyTag
from tkinter.filedialog import askdirectory
from tkinter import messagebox
import re


def remove_feat(text):
    # Regularni izraz koji pronalazi dio stringa u formatu (feat. Ime)
    pattern = r"\s*\(feat\..*?\)"
    # Zamjena pronađenog dijela sa praznim stringom
    return re.sub(pattern, '', text).strip()


def rename_file(song_artist, song_title, file_name):
    new_name = song_artist + " - " + song_title
    old_name = file_name[0:file_name.index('.mp3')]
    new_filename = file_name.replace(old_name, new_name).strip()

    old_file = os.path.join(folder_path, file_name)
    new_file = os.path.join(folder_path, new_filename)
    if old_file != new_file:
        os.rename(old_file, new_file)


def create_txt_file(file_path, song_artist, song_title):
    with open(file_path, 'a', encoding='utf-8') as file:
        file.write(f"{song_artist} - {song_title}\n")


def show_message(number_of_unsuccessful_files):
    # Function to display a message box with a custom message
    messagebox.showinfo("Info", "Broj file-ova koji nisu preimenovani je ->"
                        + str(number_of_unsuccessful_files))


def display_unsuccessful_files(unsuccessful_files):
    file_string = "\n".join(unsuccessful_files)
    messagebox.showinfo("File-ovi koji nisu preimenovani su ->", file_string)


# Definiranje putanje do foldera
folder_path = askdirectory(title='Select Folder')
print("folder path is ->", folder_path)

# Provjera da li folder postoji
if not os.path.exists(folder_path):
    print(f"Folder {folder_path} ne postoji.")
else:
    list_unsuccessful_file = []
    create_txt = messagebox.askyesno("Create TXT File", "Do you want to create a .txt file with song details?")
    txt_file_path = None

    if create_txt:
        # Prompt user to select the folder for the .txt file
        folder_path_for_txt = askdirectory(title='Select Folder for TXT file')
        # Check if the user selected a folder
        while not os.path.exists(folder_path_for_txt):
            folder_path_for_txt = askdirectory(title='Try to Select Folder for TXT file Again')

        txt_file_path = os.path.join(folder_path_for_txt, 'songs_info.txt')

    # Iteracija kroz sve datoteke u folderu
    for filename in os.listdir(folder_path):
        if not (filename.endswith('.mp3') or filename.endswith('.mp4')):
            continue

        audio = TinyTag.get(folder_path + "/" + filename)

        title = audio.title
        if title is None:
            list_unsuccessful_file.append(filename)
            continue
        title = title.replace(" - ", " ")
        if "feat." in title:
            title = remove_feat(title)

        artist = audio.artist
        if artist is None:
            list_unsuccessful_file.append(audio)
            continue
        artist = artist.replace("/", ", ")

        rename_file(artist, title, filename)
        if txt_file_path is not None:
            create_txt_file(txt_file_path, artist, title)
    if len(list_unsuccessful_file) != 0:
        show_message(list_unsuccessful_file)

print("Preimenovanje je završeno.")
