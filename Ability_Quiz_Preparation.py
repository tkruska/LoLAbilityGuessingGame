# PART 1
import requests
import json
from tqdm.auto import tqdm

# PART 2
import tarfile
import os
import shutil

# PART 3
import pandas as pd


### PART 1 - DATA DRAGON DOWNLOADER BELOW ###


print("\nLeague of Legends - DataDragonDownloader\n\n\nChecking Version...\n")

while True:
    versions_url = "https://ddragon.leagueoflegends.com/api/versions.json"
    r = requests.get(versions_url)
    versions = r.json()
    newest_version = versions[0]

    try:
        with open("latest.txt", "r") as f:
            current_version = f.read()
    except:
        current_version = ""

    if current_version == "":
        print("Previous version: No previous version found.")
        print("New version available: " + newest_version)
        with open("latest.txt", "w") as f:
            f.write(newest_version)
        break
    elif current_version != newest_version:
        print("Previous version: " + current_version)
        print("New version available: " + newest_version)
        with open("latest.txt", "w") as f:
            f.write(newest_version)
        old_dragon_file = "dragontail-" + current_version + ".tgz"
        print("Removing older version...")
        try:
            os.remove(old_dragon_file)
            print("Older version removed.")
        except:
            print("No older version found.")
        break
    else:
        print("No new version available.\nCurrent version: " +
              current_version + "\n")
        break


while True:
    newest_url = (
        "https://ddragon.leagueoflegends.com/cdn/dragontail-" + newest_version + ".tgz"
    )
    dragon_file = newest_url.split("/")[-1]
    if dragon_file in os.listdir():
        print("\nData Dragon Archive already downloaded.")
        break
    print("\nDownloading newest Data Dragon Archive: " + dragon_file + "...")
    response = requests.get(newest_url, stream=True)
    with tqdm.wrapattr(
        open(dragon_file, "wb"),
        "write",
        miniters=1,
        total=int(response.headers.get("content-length", 0)),
        desc=dragon_file,
    ) as fout:
        for chunk in response.iter_content(chunk_size=4096):
            fout.write(chunk)
    fout.close()
    print("\nDownload successfully finished.")
    break


### DATA DRAGON DOWNLOADER DONE ###

### TGZ-EXTRACTOR BELOW ###

# TO DO: USE INPUT FOR LANGUAGE SETTINGS ...

while True:
    tar_file = dragon_file
    print("\nExtracting archive...")
    with tarfile.open(tar_file) as tar:
        subdir_and_files = [
            tarinfo
            for tarinfo in tar.getmembers()
            if tarinfo.name.startswith(newest_version + r"/data/en_US/champion")
        ]
        for member in tqdm(subdir_and_files):
            # Extract member
            tar.extract(member=member)
    print("\nArchive succesfully extracted.")
    break


champ_folder_dir = os.getcwd() + "\\" + "\\" + newest_version + \
    r"\data\en_US\champion"
print("\nMoving champion folder to prepare JSON creation...")
if "champion" in os.listdir():
    shutil.rmtree(os.getcwd() + r"\champion")
shutil.move(champ_folder_dir, os.getcwd())


###

### PART 3 - JSON CREATOR BELOW ###


# START OF PROGRAM
base_dir = os.getcwd() + r"\champion"
categories = ["Champion", "Passive", "Q", "W", "E", "R"]
champs = []
print("\nCreating dataframe for all champions...")
for file in tqdm(os.listdir(base_dir)):
    champ = {}
    json_path = os.path.join(base_dir, file)
    json_data = pd.read_json(json_path)
    champName = file.split(".")[0]
    if champName == "MonkeyKing":
        champ["Champion"] = "Wukong"
    else:
        champ["Champion"] = champName
    champ["P"] = json_data["data"][champName]["passive"]["name"]
    spells_list = json_data["data"][champName]["spells"]
    champ["Q"] = spells_list[0]["name"]
    champ["W"] = spells_list[1]["name"]
    champ["E"] = spells_list[2]["name"]
    champ["R"] = spells_list[3]["name"]
    champs.append(champ)
df = pd.DataFrame(champs)
df = df.sort_values(by=["Champion"])


# PREPARE OUTPUT
output_dict = {}
print("\nCreating dictionary based on dataframe...")
for index, row in df.iterrows():
    single_champ = {
        "P": row["P"],
        "Q": row["Q"],
        "W": row["W"],
        "E": row["E"],
        "R": row["R"],
    }
    output_dict[row["Champion"]] = single_champ

# OUTPUT FILE
out_dir = os.getcwd()
print("\nWriting dictionary to JSON file...")
with open(os.path.join(out_dir, "ChampData.json"), "w") as outfile:
    json.dump(output_dict, outfile)
print("\nJSON file succesfully created.")
remove = 0
while remove != "Y" or remove != "N":
    remove = input(
        "Do you want to remove the downloaded / extracted files? Y/N?: ").upper()
    if remove == "Y" or remove == "N":
        break
    else:
        continue


def closing_words():
    print("\nEverything is prepared.")
    print("You can now start LoL Spell Quiz.")
    input("Press any key to close...  There will be cake.\n")


def cleanup():
    print("\nRemoving extracted archive...")
    shutil.rmtree(os.getcwd() + "\\" + newest_version)
    print("\nRemoving dragontail...")
    os.remove(os.getcwd() + "\\" + dragon_file)
    print("\nRemoving champion folder...")
    shutil.rmtree(os.getcwd() + r"\champion")


if remove == "Y":
    cleanup()
    closing_words()
else:
    closing_words()
