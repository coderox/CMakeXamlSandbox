$pwd = ConvertTo-SecureString -String P@ssw0rd -Force -AsPlainText 

New-SelfSignedCertificate -Type Custom -Subject "CN=coderox" -KeyUsage DigitalSignature -FriendlyName "Self signed test certificate" -CertStoreLocation "Cert:\CurrentUser\My" -TextExtension @("2.5.29.37={text}1.3.6.1.5.5.7.3.3", "2.5.29.19={text}") -OutVariable selfSignedCertificateOutput

$certificatePath = -join("Cert:\CurrentUser\My\",$selfSignedCertificateOutput.Thumbprint)
Export-PfxCertificate -cert $certificatePath -FilePath CoderoxTestCertificate.pfx -Password $pwd

$cert = (Get-ChildItem -Path $certificatePath)
Export-Certificate -Cert $cert -FilePath .\CoderoxTestCertificate.cer