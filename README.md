Clone the repo...

Open a powershell prompt and browse to the repository root directory.

Run:

.\cmake\CreateSelfSignedCert.ps1

This will generate the certificate required for signing, copy the outputted thumbprint value into the build.py script in the appropriate parameter field, then run:

python build.py

If everything works, you should have a installable