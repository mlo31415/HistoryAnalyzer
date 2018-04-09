import xml.etree.ElementTree as ET
import os


# The purpose of this program is to analyze the downloaded Fancy3 history data
    # Is anything missing? (Look for skipped versions numbers)
    # Who did how much? (Build table of edits by user ID)

historyDirectory="I:\Fancyclopedia History"

userCounts={}   # a dictionary indexed by user ID and counting edits

# Walk the history directory looking at each page folder
mainDirList=[f.path for f in os.scandir(historyDirectory) if f.is_dir()]
for dir1 in mainDirList:
    dir1List=[f.path for f in os.scandir(dir1) if f.is_dir()]
    for dir2 in dir1List:
        pageDirList=[f.path for f in os.scandir(dir2) if f.is_dir()]
        for pageDir in pageDirList:
            verNameList=[f.name for f in os.scandir(pageDir) if f.is_dir()]

            # Step 1: Make sure all the directories are present.
            # Directory names are of the form Vnnnn, beginning with V0000
            # To check to see if there are no gaps, remove the directories fromt he list starting at V0000. We should empty the list exactly when we reach the end.
            i=0
            while len(verNameList) > 0:
                vname="V"+("0000"+str(i))[-4:]
                if vname not in verNameList:
                    print("*** "+pageDir+ " is missing "+vname)
                else:
                    verNameList.remove(vname)
                i=i+1

            # Now go through the directories and read the metadata.xml file to figure out who did the edit.
            verDirList=[f.path for f in os.scandir(pageDir) if f.is_dir()]
            for ver in verDirList:
                tree=ET.parse(os.path.join(ver, "metadata.xml"))
                id=tree.find("name").text.strip()
                if id in userCounts:
                    userCounts[id]=userCounts[id]+1
                else:
                    userCounts[id]=1

# Convert the dictionary into a list of tuples and then sort the list on the count
listOfTuples=sorted([(v, k) for k, v in userCounts.items()], reverse=True)

for count, id in listOfTuples:
    print(id+": "+str(count))
i=0