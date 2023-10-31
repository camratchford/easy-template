
# Compiling

## Linux

- Make sure you have the python & python-dev >= 3.8 installed
- Create a virtual environment
- Install the package

```shell
cd ./EasyTemplate
python3 -m venv venv
source venv/bin/activate
pip install .
```

- Compile

```shell
cd ./compilation
bash ./compile.sh
```

- Copy it somewhere in $PATH

```shell
cp ./build/ezt /usr/bin/ezt
```

## Windows

- Make sure Python >= 3.8 is installed
- (for some reason) Install pyinstaller to your system Python interpreter's library

```powershell
pip install pyinstaller
```

- Run the PowerShell script

```powershell
cd .\EasyTemplate\compilation\
# It will create the venv and test the program
.\compile.ps1
```