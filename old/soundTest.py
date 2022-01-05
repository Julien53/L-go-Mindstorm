import ev3_dc as ev3

MAC = "00:16:53:48:91:73"

with ev3.Voice(protocol=ev3.BLUETOOTH, host=MAC, lang='it') as voice:
    (
        voice.speak(
            '''
            Bona sera, cara Francesca! Come stai?
            Non vedo l'ora di venire in Italia.
            Stasera è una bella serata.
            '''
        ) + voice.speak(
            '''
            Hello Brian,
            this is your LEGO EV3 device.
            I speak english and hope, you can understand me.
            If not so, select another language please.
            ''',
            lang='en'
        ) + voice.speak(
            '''
            Guten Abend, lieber Kurt! Wie geht es Dir?
            Hier regnet es viel, wie schon den ganzen März und April.
            ''',
            lang='de'
        )
        
    ).start(thread=False)