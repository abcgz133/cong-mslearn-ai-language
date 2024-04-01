from dotenv import load_dotenv
from datetime import datetime
import os

# Import namespaces
# Import namespaces
  import azure.cognitiveservices.speech as speech_sdk

def main():
    try:
        global speech_config

        # Get Configuration Settings
        load_dotenv()
        ai_key = os.getenv('SPEECH_KEY')
        ai_region = os.getenv('SPEECH_REGION')

        # Configure speech service
		speech_config = speech_sdk.SpeechConfig(ai_key, ai_region)
		print('Ready to use speech service in:', speech_config.region)
		
        # Get spoken input
        command = TranscribeCommand()
		# cong: if the input from the audio is "what time is it", then system will continue the next procedure,  
		# to tell the time, to produce the speech , the voice of the exact tiem
		# if the input from the audio is others, then the system will just print the transcribed text. 
        if command.lower() == 'what time is it?':
            TellTime()

    except Exception as ex:
        print(ex)

def TranscribeCommand():
    command = ''

    # Configure speech recognition
	audio_config = speech_sdk.AudioConfig(use_default_microphone=True)
	speech_recognizer = speech_sdk.SpeechRecognizer(speech_config, audio_config)
	print('Speak now...')

	# Process speech input
	speech = speech_recognizer.recognize_once_async().get()
	if speech.reason == speech_sdk.ResultReason.RecognizedSpeech:
		# cong, the variable of "command" is the text of the transcribed voice. 
		command = speech.text
		print(command)
	else:
		print(speech.reason)
    if speech.reason == speech_sdk.ResultReason.Canceled:
        cancellation = speech.cancellation_details
        print(cancellation.reason)
        print(cancellation.error_details)

    # Return the command
    return command


def TellTime():
    now = datetime.now()
    response_text = 'The time is {}:{:02d}'.format(now.hour,now.minute)


    # Configure speech synthesis
	# cong here is the configuration of the category of the language, such as English, and the voice such as male /female
	speech_config.speech_synthesis_voice_name = 'en-GB-LibbyNeural' # change this
	speech_synthesizer = speech_sdk.SpeechSynthesizer(speech_config)
    
	# Synthesize spoken output cong： here is the output of the audio voice.
	speak = speech_synthesizer.speak_text_async(response_text).get()
	if speak.reason != speech_sdk.ResultReason.SynthesizingAudioCompleted:
		print(speak.reason)


    # Print the response
    print(response_text)


if __name__ == "__main__":
    main()