from django.shortcuts import render
from hashcat.models import Hash, CrackingTask
# Create your views here.
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_http_methods
from django.core import serializers
from django.forms.models import model_to_dict
################################
import sys, re, os
from subprocess import PIPE, Popen
from threading  import Thread, Event
################################
import channels.layers
from asgiref.sync import async_to_sync
################################

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORKING_DIR = os.path.join(BASE_DIR, 'work_folder')
WORDLISTS_DIR = os.path.join(WORKING_DIR, 'wordlists')
HASHES_DIR = os.path.join(WORKING_DIR, 'hash_files')

STARTED_EVENT = Event()

SEPARATOR = "|"

Status, Speed, recoveredHashes, totalLoadedHashes, triedPasswords, totalPasswords, progressPercent, estimatedTime = 0, 0, 0, 0, 0, 0, 0, 0

def sendUpdate(taskId ,data):
    channel_layer = channels.layers.get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        str(taskId),
        {
            'type': 'send_status_update',
            'status_update': data
        }
    )

def analyseOutput(output, crackTaskId):
    STARTED_EVENT.clear()
    REGEX_UNIQUE_DIGESTS = "\; (\d*) unique digests"
    REGEX_TOTAL_PASSWORDS = "\* Passwords.: (\d*)"

    REGEX_Status="STATUS\t(\d*)"
    REGEX_Speed="SPEED\t(\d*)\t(\d*)"
    REGEX_Progress="PROGRESS\t(\d*)\t(\d*)"
    REGEX_Recovered="RECHASH\t(\d*)\t(\d*)"
    REGEX_Recovered_Password = "\r(.*)\|(.*)\n"
# Check Passowrd regex and cross ref the hash with the database to verify.
# Whenever there is a new password cracked, add it the default wordlist that will always be used with the command line in addition to the wordlist specified by the user.
    
    crackTask = CrackingTask.objects.get(pk=crackTaskId)

    ## The following two REGEX searches are here to initialize the loaded digests and total passwords upon starting up hashcat
    StartingUniqueHashes = re.search(REGEX_UNIQUE_DIGESTS, output, re.IGNORECASE)
    if StartingUniqueHashes:
        StartingUniqueHashes = StartingUniqueHashes.group(1)
        crackTask.totalLoadedHashes = int(StartingUniqueHashes)
        crackTask.save()
        pass

    StartingTotalPasswords = re.search(REGEX_TOTAL_PASSWORDS, output, re.IGNORECASE)
    if StartingTotalPasswords:
        StartingTotalPasswords = StartingTotalPasswords.group(1)
        crackTask.totalPasswords = int(StartingTotalPasswords)
        crackTask.save()
        STARTED_EVENT.set()
        pass
    ## End of initializer

    Recovered_Password = re.search(REGEX_Recovered_Password, output, re.IGNORECASE)
    if Recovered_Password:
        hashText = Recovered_Password.group(1)
        Recovered_Password = Recovered_Password.group(2)
        print(Recovered_Password)
        try:
            recoveredHash = crackTask.hash_set.filter(hashText__exact=hashText.strip())

        except Exception as e:
            print(e)
            pass
        else:
            hash_ids = recoveredHash.values_list('id', flat=True)
            sendUpdate(crackTaskId, {'type':'password', 'password':Recovered_Password, 'hash_ids':list(hash_ids)})
            recoveredHash.update(password=Recovered_Password)
            

    Status = re.search(REGEX_Status, output, re.IGNORECASE)
    if Status:
        Status = Status.group(1)
        crackTask.status = int(Status)

    Speed = re.search(REGEX_Speed, output, re.IGNORECASE)
    if Speed:
        Speed = Speed.group(1)
        crackTask.speed = int(Speed)


    Recovered = re.search(REGEX_Recovered, output, re.IGNORECASE)
    if Recovered:
        recoveredHashes, totalLoadedHashes = Recovered.group(1), Recovered.group(2)
        crackTask.recoveredHashes = int(recoveredHashes)
        crackTask.totalLoadedHashes = int(totalLoadedHashes)
        

    Progress = re.search(REGEX_Progress, output, re.IGNORECASE)
    if Progress:
        triedPasswords, totalPasswords = Progress.group(1), Progress.group(2)
        crackTask.triedPasswords = int(triedPasswords)
        crackTask.totalPasswords = int(totalPasswords)

    crackTask.save()
    statusDict = {
        'status':crackTask.status,
        'statusText':crackTask.statusText(),
        'speed':crackTask.speed,
        'recoveredHashes':crackTask.recoveredHashes,
        'triedPasswords':crackTask.triedPasswords,
        'estimatedTime':crackTask.estimatedTime(),
        'progressPercent':crackTask.progressPercent()
    }
    sendUpdate(crackTaskId, {'id':crackTaskId, 'type':'status', 'dict':statusDict})
    sendUpdate(0, {'id':crackTaskId, 'type':'status', 'dict':statusDict})


def startCracking(hashType, attackMode, crackTaskId):
    env = os.environ.copy()
    # Add the PYTHONPATH using the existing python system path.
    env['PYTHONPATH'] = ":".join(sys.path)
    crackTask = CrackingTask.objects.get(pk=crackTaskId)

    process = Popen(['/usr/bin/hashcat', '--machine-readable', '--potfile-disable', '--status', '--status-time', '3', '-d', '1', '-p', SEPARATOR, '--session', str(crackTask.sessionID), '--force', '-a', str(attackMode), '-m', str(hashType), os.path.join(HASHES_DIR, str(crackTask.sessionID)), os.path.join(WORDLISTS_DIR, 'rockyou.txt')], stdout=PIPE, stdin=PIPE, stderr=PIPE, bufsize=1, close_fds=True, env=env)

    while process.poll() is None:
        # for errLine in iter(process.stderr.readline, b''):
        #     print(errLine)
        for stdOut in iter(process.stdout.readline, b''):
            print(stdOut.decode('ascii'))
            analyseOutput(stdOut.decode('ascii'), crackTaskId)
    print("Cracking done")


@require_http_methods(["GET"])
def crackTaskStatus(request, crackTaskId):
	crackTask = CrackingTask.objects.get(pk=crackTaskId)
	crackTaskDict = model_to_dict(crackTask)
	crackTaskDict['estimatedTime'] = crackTask.estimatedTime()
	crackTaskDict['progressPercent'] = crackTask.progressPercent()
	crackTaskDict['statusText'] = crackTask.statusText()

	return JsonResponse(crackTaskDict)
################################

@require_http_methods(["POST"])
def crack(request, hashType, attackMode):
    hashesWrittenInFile = 0
    postHashes = request.POST.get('hashes')
    crackTask = CrackingTask(hashType=hashType, attackMode=attackMode, status=0, speed=0, recoveredHashes=0, totalLoadedHashes=0, totalPasswords=0, triedPasswords=0)
    crackTask.save()
    
    hashesFile = open(os.path.join(HASHES_DIR, str(crackTask.sessionID)),"w+")
    for hashLine in postHashes.split('\n'):
        if hashLine.strip() != "" :
            dbHash = Hash.objects.filter(hashText__exact=hashLine.strip()).exclude(password__exact="").values_list("hashText","password").distinct()
            if dbHash:
                crackTask.hash_set.create(hashText=hashLine.strip(), password=dbHash[0][1])
            else:
                crackTask.hash_set.create(hashText=hashLine.strip())
                hashesFile.write(postHashes)
                hashesWrittenInFile += 1
    crackTask.save()
    hashesFile.close()

    if hashesWrittenInFile > 0:
        crackingThread = Thread(target=startCracking, args=(hashType, attackMode, crackTask.id))
        crackingThread.daemon = True
        crackingThread.start()
        STARTED_EVENT.wait()
    else:
        crackTask.status=6
        crackTask.save()

    return JsonResponse({'id':crackTask.id})
