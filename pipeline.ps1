# CREATE CERTIFICATES
$pwd = ConvertTo-SecureString -String P@ssw0rd -Force -AsPlainText 

New-SelfSignedCertificate -Type Custom -Subject "CN=coderox" -KeyUsage DigitalSignature -FriendlyName "Self signed test certificate" -CertStoreLocation "Cert:\CurrentUser\My" -TextExtension @("2.5.29.37={text}1.3.6.1.5.5.7.3.3", "2.5.29.19={text}") -OutVariable selfSignedCertificateOutput

$certificatePath = -join("Cert:\CurrentUser\My\",$selfSignedCertificateOutput.Thumbprint)
Export-PfxCertificate -cert $certificatePath -FilePath CoderoxTestCertificate.pfx -Password $pwd

$cert = (Get-ChildItem -Path $certificatePath)
Export-Certificate -Cert $cert -FilePath .\CoderoxTestCertificate.cer

& cmake -E make_directory output

# GENERATE
& cmake -E chdir ./output/ cmake -DCMAKE_SYSTEM_NAME="WindowsStore" -DCMAKE_SYSTEM_VERSION="10.0" -G "Visual Studio 16" ..

# BUILD
$msbuildparameters = -join("/p:UapAppxPackageBuildMode=StoreUpload /p:PackageCertificateThumbprint=",$selfSignedCertificateOutput.Thumbprint, " /p:PackageCertificateKeyFile=../CoderoxTestCertificate.pfx /p:PackageCertificatePassword=", $pwd)
# & cmake -E chdir ./output/ cmake --build . -- /p:AppxPackageSigningEnabled=false
& cmake -E chdir ./output/ cmake --build . -- $msbuildparameters