import os

def rename_files():
    file_list = os.listdir("series/")
    print(file_list)
    saved_path = os.getcwd()
    print("Current Working Directory is " + saved_path)
    os.chdir("series/")
    # (2) for each file, rename filename
    for file_name in file_list:
        old_name = file_name
        new_name = file_name.replace("E", "")
        new_name = new_name.replace("S3", "")
        new_name = new_name.replace("S4", "")
        new_name = new_name.replace("S5", "")
        new_name = new_name.replace("S6", "")
        new_name = new_name.replace("S7", "")
        new_name = new_name.replace("S8", "")
        new_name = new_name.replace("S10", "")
        new_name = new_name.replace("  ", " ")
        new_name = new_name.replace("Tamil Dub 720p", "")
        new_name = new_name.replace("Naruto ", "")
        new_name = new_name.replace(" ", "")
        new_name = new_name.replace("E", "")
        if (new_name.startswith("0")):
            new_name = new_name[1:]
        # if newname not ends with .mp4
        if not new_name.endswith(".mp4"):
            new_name = new_name + ".mp4"
        os.rename(old_name, new_name)

    os.chdir(saved_path)

rename_files()