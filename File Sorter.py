import os
import time

# ===============================================================================
# Functions
# ===============================================================================

def exitCheck(exitStr): # closing the program
    exitKeywords = ["exit"]
    if exitStr in exitKeywords:
            print("Closing Program...")
            time.sleep(0.5) # sleep for 0.5 seconds
            exit()
    return True

def getPath(): # get full path to target directory
    while True:
        path = input("Enter the target directory: ")
        exitCheck(path)

        if os.path.exists(path):
            title = os.path.basename(path)
            print(f"Directory: {path}")
            print(f"title: {title}")
            confirmation = input(f"Enter 'y' to continue with directory {path}\n : ")
            if confirmation == 'y':
                return path, title
        elif path == "":
            print("Please enter a directory...")
        else:
            print("No such directory found! Please enter a valid directory\n")

def addCustomDir(path, existDir):
    while True:
        c = input("Add custom new directories? (Y/N): ")
        if c == "Y":
            while True:
                name = input("Add a directory: ")
                if name == "":
                    print(f"New current directories: {existDir}")
                    return existDir
                elif name not in existDir:
                    existDir.append(name)
                    os.mkdir(os.path.join(path, name))
                    print(f"New directory '{name}' is added!\n")
                else:
                    print(f"Directory '{name}' already exists!")
        elif c == "N":
            return existDir

def sortDir(path, title):
    existDir = [] # All existing folders in this directory
    newfCheck = {} # Checklist to determine new folders to be created
    while True:
        addTitleCheck = input(f"Append title '{title}'to all files? (y/n): ")
        if addTitleCheck in ['y', 'n']:
            break

    for file in os.listdir(path):
            # Check for existing folders
            if os.path.isdir(os.path.join(path, file)):
                existDir.append(file)
                continue
            
            # for creating new directories
            if file.split('_')[0] != title:
                if file.split('_')[0] in existDir:
                    pass
                elif file.split('_')[0] not in newfCheck: 
                    newfCheck[file.split('_')[0]] = 1
                else:
                    newfCheck[file.split('_')[0]] += 1
                if addTitleCheck == "y":
                    f = '_'.join([title, file])
                    # Prepend files with parent folder's name (Title)
                    os.rename(os.path.join(path, file), os.path.join(path, f))
            else:
                if file.split('_')[0] in existDir:
                    pass
                elif file.split('_')[1] not in newfCheck: 
                    newfCheck[file.split('_')[1]] = 1
                else:
                    newfCheck[file.split('_')[1]] += 1
    # add custom dirs
    existDir = addCustomDir(path, existDir)
    # output current dirs
    print("================================================")
    print(f"dirs in current directory: {existDir}\n")


    dirNewGrp = [v for v in newfCheck if newfCheck[v] > 1]
    for name in dirNewGrp: # Create new folders for common name
        if name in existDir:
            continue
        os.mkdir(os.path.join(path, name))
        existDir.append(name)
    return existDir

# sorting based on common names
def fileToDir(path, file, existDir):
    f = file.rsplit(".", 1)[0] # remove extensions from a file name
    f = f.split("_")[1]
    print(f[1])
    if f in existDir:
        os.rename(os.path.join(path, file), os.path.join(path, f, file))
        print(f"\"{file}\" is moved into \"{f}\"")
        return True
    return False

# sorting based on file types
def fileSorting(path, file, dirname):
    if not os.path.exists(os.path.join(path, dirname)):
        os.mkdir(os.path.join(path, dirname))
    os.rename(os.path.join(path, file), os.path.join(path, dirname, file))
    print(f"\"{file}\" is moved into \"{dirname}\"")

def priSort(path, existDir):
    print("================================================")
    for file in os.listdir(path):
            # skip all directories
            if os.path.isdir(os.path.join(path, file)):
                # print(f"\"{file}\"" + " is a directory")
                continue

            # for files that has their respective folders
            if fileToDir(path, file, existDir):
                continue

            # for all PDF
            elif file.endswith((".pdf", ".PDF")):
                fileSorting(path, file, "PDF")
            
            # for all slides
            elif file.endswith((".ppt", ".pptx")):
                fileSorting(path, file, "Slides")
            
            # for all excel data files
            elif file.endswith((".xls", ".xlsx", ".csv")):
                fileSorting(path, file, "CSV/Excel")
            
            # for all other images
            elif file.endswith((".png",".PNG", ".jpeg", ".JPEG", ".jpg", ".JPG")):
                fileSorting(path, file, "Images")

            # for all other txt files
            elif file.endswith((".txt", ".TXT")):
                fileSorting(path, file, "Notes")
            
            else:
                fileSorting(path, file, "Others")

            # elif file.endswith("[extensions]"):
            #    fileSorting(path, file, "[fileName]")
    print("================================================")

#def secSort(path, title, existDir): 
    
    #for folder in existDir:
        #existDirInside = sortDir(os.path.join(path, folder), title)
        #priSort(os.path.join(path, folder), existDir)


# ===============================================================================

def main():
    
    while True:
        print("================================================")
        print("Simple File Sorter")
        print("================================================")

        path, title = getPath()
        existDir = sortDir(path, title)
        priSort(path, existDir)
        #secSort(path, title, existDir)
        exitCheck(input("Press Enter to continue/Enter 'exit' to end the program: "))
main()