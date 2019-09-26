import subprocess

clearTextPwd = "P@ssw0rd"
passwordParameter = "/p:PackageCertificatePassword=" + clearTextPwd

# thumbprint needs to be fetched from the generated certificate through PowerShell
thumbPrint="4DE9A23607C871CFCD1E85CFD009C17DE358A641"
thumbPrintParameter = "/p:PackageCertificateThumbprint=" + thumbPrint

# create the output directory
cmakeMakeDirectoryCmd = ["cmake", "-E" ,"make_directory", "output"]
retCode = subprocess.check_call(cmakeMakeDirectoryCmd, shell=True)

# generate the solution
cmakeGenerateCmd = ["cmake", "-E", "chdir", "./output/", "cmake", "-DCMAKE_SYSTEM_NAME=WindowsStore", "-DCMAKE_SYSTEM_VERSION=10.0", "-G", "Visual Studio 16" ,".."]
retCode = subprocess.check_call(cmakeGenerateCmd, shell=True)

# build and sign the appx/msix
cmakeBuildCmd = ["cmake", "-E", "chdir", "./output/", "cmake", "--build", ".", "--", "/p:UapAppxPackageBuildMode=StoreUpload", thumbPrintParameter, "/p:PackageCertificateKeyFile=../CoderoxTestCertificate.pfx",passwordParameter]
retCode = subprocess.check_call(cmakeBuildCmd, shell=True)