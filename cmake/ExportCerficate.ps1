$pwd = ConvertTo-SecureString -String P@ssw0rd -Force -AsPlainText 
Export-PfxCertificate -cert "Cert:\CurrentUser\My\E9C033A02253C30E6A72A624281AD484F5E5007B" -FilePath CoderoxTestCertificate.pfx -Password $pwd

#Export-PfxCertificate -cert "Cert:\CurrentUser\My\2B68A8444311CB43069C9C921DA80CDCAB00CA7B" -FilePath CoderoxTestCertificate.pfx -ProtectTo 