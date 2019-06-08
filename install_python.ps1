
Add-Type -AssemblyName System.IO.Compression.FileSystem

function DownloadURL
{
    param([string]$url, [string]$outpath)
    
    New-Item -ItemType File -Force -Path $outpath | Out-Null # safety creation of folder
    
    echo "Downloading $url to $outpath"
    
    [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
    $down = New-Object System.Net.WebClient
    $down.DownloadFile($url, $outpath)
}


$PYTHON_VERSION = "3.7.3"
$PYTHON_VERSION_CLEAN = $PYTHON_VERSION.replace(".", "").Substring(0,2)
$PYTHON_DOWNLOAD_URL = "https://www.python.org/ftp/python/$PYTHON_VERSION/python-$PYTHON_VERSION.exe"
$PYTHON_DOWNLOAD_EXE = "C:\python\python-$PYTHON_VERSION.exe"
$PYTHON_INSTALL_DIR = "C:\python\python$PYTHON_VERSION_CLEAN"


echo "Installing Python $PYTHON_VERSION - $PYTHON_DOWNLOAD_URL"
DownloadURL $PYTHON_DOWNLOAD_URL $PYTHON_DOWNLOAD_EXE

# Set the PATH environment variable for the entire machine (that is, for all users) to include the Python install dir
echo "Setting Environment PATH to $PYTHON_INSTALL_DIR"
New-Item -ItemType Directory -Force -Path $PYTHON_INSTALL_DIR | Out-Null # safety creation of folder
[Environment]::SetEnvironmentVariable("PATH", "${env:path};${PYTHON_INSTALL_DIR}", "Machine") | Out-Null

echo "Starting Installer $PYTHON_DOWNLOAD_EXE ..."
& $PYTHON_DOWNLOAD_EXE /quiet InstallAllUsers=1 PrependPath=0 Include_test=0 Include_pip=1 TargetDir=$PYTHON_INSTALL_DIR

cmd /c pause | out-null
