::Copy all files from sourcepath to destinationpath using Robocopy
::Orignally xcopy /s /d /c /y C:\Users\dev E:\backups\dev
:: cd C:\Users\dev\Documents\Repositories\job-hunting\bat
:: backup_dev.bat
::
::Switches:
::(E)mpty folders included in copy
::(R)etry each copy up to 0 times
::(W)ait 0 seconds between attempts
::(LOG) creates log file
::(NP) do not include progress txt in logfile; this keeps filesize down
::(MIR)rors a directory tree
::(V)erbose logging
::COPYALL Copy all file info
::ETA show Estimated Time of Arrival of copied files

::Source path
set sourcepath=C:\Users\dev

::Destination path
set destinationpath=E:\backups\dev

::Log path
set logpath=E:\logs\Robocopy\

::Include format yyyy-mm-dd#hh-mm-ss.ms in log filename
set filename=Backup_Job_%date:~-4,4%-%date:~-10,2%-%date:~-7,2%#%time::=-%.txt

::Run command
robocopy "%sourcepath%" "%destinationpath%" /MIR /V /ETA /R:0 /W:0 /COPYALL /LOG:"%logpath%%filename%" /NP