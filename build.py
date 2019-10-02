import subprocess
import os
import zipfile

CERT_PASSWORD = "P@ssw0rd"
CERT_THUMBPRING = "D09DE3BE9BF2B03450A07ACED4E022F1617D7371"

def buildUwp():
    passwordParameter = "/p:PackageCertificatePassword=" + CERT_PASSWORD

    # thumbprint needs to be fetched from the generated certificate through PowerShell
    thumbPrintParameter = "/p:PackageCertificateThumbprint=" + CERT_THUMBPRING

    # create the output directory
    cmakeMakeDirectoryCmd = ["cmake", "-E" ,"make_directory", "output"]
    retCode = subprocess.check_call(cmakeMakeDirectoryCmd, shell=True)

    # generate the solution
    cmakeGenerateCmd = ["cmake", "-E", "chdir", "./output/", "cmake", "-DCMAKE_SYSTEM_NAME=WindowsStore", "-DCMAKE_SYSTEM_VERSION=10.0", "-G", "Visual Studio 16" ,".."]
    retCode = subprocess.check_call(cmakeGenerateCmd, shell=True)

    # build and sign the appx/msix
    cmakeBuildCmd = ["cmake", "-E", "chdir", "./output/", "cmake", "--build", ".", "--", "/p:UapAppxPackageBuildMode=StoreUpload", thumbPrintParameter, "/p:PackageCertificateKeyFile=../CoderoxTestCertificate.pfx", passwordParameter]
    retCode = subprocess.check_call(cmakeBuildCmd, shell=True)

def findFilesInFolder(path, pathList, extension, subFolders = True):
    try: 
        for entry in os.scandir(path):
            if entry.is_file() and entry.path.endswith(extension):
                pathList.append(entry.path)
            elif entry.is_dir() and subFolders:
                pathList = findFilesInFolder(entry.path, pathList, extension, subFolders)
    except OSError:
        print('Cannot access ' + path)

    return pathList

def zipOutputFiles():
    dir_name = r'./output/AppPackages'

    pathList = []
    pathList = findFilesInFolder(dir_name, pathList, '.msix', True)
    if len(pathList) == 0:
        pathList = findFilesInFolder(dir_name, pathList, '.appx', True)

    if len(pathList) != 1:
        print("Should only find one .msix or .appx!")
        print("Found:")
        for filename in pathList:
            print(filename)
        return

    outputname = os.path.basename(pathList[0])[:-5] + ".appxupload"
    pathList = findFilesInFolder(dir_name, pathList, '.appxsym', True)
    if len(pathList) != 2:
        print("Should only find one .appxsym")
        print("Found:")
        for filename in pathList:
            print(filename)
        return
        
    my_zipfile = zipfile.ZipFile(outputname, mode='w', compression=zipfile.ZIP_DEFLATED)
    for filename in pathList:
        my_zipfile.write(filename, os.path.basename(filename))   
 
    my_zipfile.close()

if __name__ == '__main__':
    buildUwp()
    zipOutputFiles()