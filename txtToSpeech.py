import pyttsx

engine = pyttsx.init()

voices = engine.getProperty( 'voices' )
for voice in voices:
    if voice.id == "english":
        engine.setProperty( 'voice', voice.id )
        engine.say( 'Turn right to merge onto A3 toward Koln' )

engine.runAndWait()
