from os import system as osExec
from hashlib import pbkdf2_hmac as hash
from mfrc522 import SimpleMFRC522 as RFID
from subprocess import check_output as outExec

rfid = RFID()

# Verify if the card is an authorized card
def VerifCard(id=0):
    try:
        default = True
        if (id == 0):
            default = False
            print("Verify card")
            print('Waiting for tag ...')
            id, c = rfid.read()
        
        TagList = ((outExec("cat ValidTags", shell=True)).decode('UTF-8')).split("\n")
        
        CardIsValid = False
        for Tag in TagList:
            if (Tag == str(id)):
                CardIsValid = True
        
        if (default):
            print((f"The Tag is NOT valid", f"The tag is valid") [CardIsValid])
        return CardIsValid

    except Exception as e:
        print(str(e))


# Add a new card to the authorized cards
def AddCard():
    try:
        print("Add card")
        print("Waiting for tag")
        id, c = rfid.read()
        
        if (VerifCard(id)):
            print("The card already exist")
            return
        
        validation = osExec(f"echo {id} >> ValidTags")
        
        print(("An error occured while adding the tag", "The tag was added sucessfully") [validation==0])
        
    except Exception as e:
        print(str(e))
    
# Print the main menu
def msg():
    print("Choose mode\n--------------------\n 1 : Verify card\n 2 : Add new card")
    

# Main execution
msg()
while True:
    i = input()
    code = 0

    if (i == '1'):
        if (VerifCard()):
            code = osExec("sudo python3 HttpAndRouter.py")

            # Error code :
            # 0 (000) = no error
            # 1 (001) = server proxy error
            # 2 (010) = router proxy error
            # 3 (011) = server and router proxy error
            # 4 (100) = http error
            # 5 (101) = http and wifi error
            # 6 (110) = http and dhcp error
            # 7 (111) = http and dhcp and wifi error

            if (code == 0):
                print("Successfull ! Starting main controller and closing ..")

                if (osExec("python3 main.py & pid=$!; ps | grep $pid | grep python3") == 0):
                    exit(0)
                else:
                    raise Exception("The main controller couldn't be started..\n\ttype 'python3 main.py' to start it manually")
            
            errorList = []

            for i in range(1, 4):
                message = (["Wifi Access Point", "DHCP server", "HTTP server"][i-1], "")[code & (1, 10, 100)[i - 1] == i]
                if (message != "") : errorList.append(message)

            for error in errorList:
                print("There was a problem while starting the " + error)

        msg()

    elif (i == '2'):

        print("Enter your password :")

        for i in range(3):
            P = input()

            if hash('sha256', P.encode('utf-8'), b"MC4ele67#a#S2", 100000) == b'\xbd\xfc\xbd\xd4l>\x14\x9d\xcb5\xefR\x912=\xaf\xa3I\x96\xc4T\xaf\xe8\x87\t\x9bd\x9d\x05\xad9r':
                AddCard()
                break
            else:
                print((f"Bad password please try again ..", f"Too many bad try !") [i==2])

        msg()
    else:
        print("please enter 1 or 2")
