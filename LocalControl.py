from TankAPI import Ev3Controller as cd
from pynput import keyboard

control = cd()

#Get called when a key is press
def keyPressHandler(key):
    global control
    name = key.char
    
    if(name == 'w'):
        control.Move(100)
        
    if(name == 's'):
        control.Move(-100)
        
    if(name == 'a'):
        control.TurnLeft(100)
       
    if(name == 'd'):
        control.TurnRight(100)      

    if(name == 'e'):
        control.TurnRightOnHimself(100)

    if(name == 'r'):
        control.TurnLeftOnHimself(100)
    
    if (name == 'c'):
        control.Speak("hello")
    
    if (name == 'b'):
        control.Sound("Dog bark 1")

    if (name == 'q'):
        control.stop(control.ALL_MOTORS)
        raise Exception("stop that shit")
        
#Get called when a key is release
def keyReleaseHandler(key):
    global control
    name = key.char
    print(name)
    
    if (name == 'w' or name == 'd' or name == 's' or name == 'a' or name == 'e' or name =='r'):
        print('Arret')
        control.stop(control.ALL_MOTORS)

with keyboard.Listener(
        on_press=keyPressHandler,
        on_release=keyReleaseHandler) as listener:
    listener.join()