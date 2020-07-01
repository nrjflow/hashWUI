import sys, re
from subprocess import PIPE, Popen
from threading  import Thread

# I dont remember why i need this file. looks like a PoC test

def analyseOutput(output):
    REGEX_Status="STATUS\t(\d*)"
    REGEX_Speed="SPEED\t(\d*)\t(\d*)"
    REGEX_Progress="PROGRESS\t(\d*)\t(\d*)"
    REGEX_Recovered="RECHASH\t(\d*)\t(\d*)"

    Status, Speed, recoveredHashes, totalHashes, triedHashes, progressPercent, estimatedTime = 0, 0, 0, 0, 0, 0, 0

    Status = re.search(REGEX_Status, output, re.IGNORECASE)
    if Status:
        Status = Status.group(1)
        print("Status is " + Status)

    Speed = re.search(REGEX_Speed, output, re.IGNORECASE)
    if Speed:
        Speed = Speed.group(1)
        print((Speed) + ' H/s')

    Recovered = re.search(REGEX_Recovered, output, re.IGNORECASE)
    if Recovered:
        recoveredHashes, totalHashes = Recovered.group(1), Recovered.group(2)
        print((recoveredHashes) + ' hashes recovered out of ' + (totalHashes))

    Progress = re.search(REGEX_Progress, output, re.IGNORECASE)
    if Progress:
        triedHashes, totalHashes = Progress.group(1), Progress.group(2)
        print((triedHashes) + ' hashes tried out of ' + (totalHashes))

def startCracking():
    process = Popen(['hashcat','--machine-readable','--status','--status-time','5','-d','1','--session','UDID','--force','-m','0','hashTes','./rockyou.txt'], stdout=PIPE, stdin=PIPE, bufsize=1, close_fds=True)
    while process.poll() is None:
        for line in iter(process.stdout.readline, b''):
            analyseOutput(line.decode('ascii'))

crackingThread = Thread(target=startCracking)
crackingThread.daemon = True
crackingThread.start()

print("Cracking done")