from dotenv import load_dotenv
from datetime import datetime
import os

# Import namespaces
import azure.cognitiveservices.speech as speech_sdk
from playsound import playsound


def main():
    try:
        global speech_config
        global translation_config

        # 1.Get Configuration Settings
        load_dotenv()
        ai_key = os.getenv('SPEECH_KEY')
        ai_region = os.getenv('SPEECH_REGION')

		# 2.1 Configure translation
		# cong: this "SpeechTranslationConfig" is the configuration which used to translate spoken input into text
		translation_config = speech_sdk.translation.SpeechTranslationConfig(ai_key, ai_region)
		translation_config.speech_recognition_language = 'en-US'
		translation_config.add_target_language('fr')
		translation_config.add_target_language('es')
		# cong: hi = Hindi
		translation_config.add_target_language('hi')
		print('Ready to translate from',translation_config.speech_recognition_language)

	    # 2.2 Configure speech
		# cong: this "speech_config" is the configuration which is used to synthesize translations into speech as we know that "speech" is used here but not included "translation"
		speech_config = speech_sdk.SpeechConfig(ai_key, ai_region)


        # 3. Get user input the type of target language
        targetLanguage = ''
        while targetLanguage != 'quit':
            targetLanguage = input('\nEnter a target language\n fr = French\n es = Spanish\n hi = Hindi\n Enter anything else to stop\n').lower()
            if targetLanguage in translation_config.target_languages:
			# 4. translate and synthesize
                Translate(targetLanguage)
            else:
                targetLanguage = 'quit'
                

    except Exception as ex:
        print(ex)

def Translate(targetLanguage):
    translation = ''

    # 1. Translate speech
    # cong: "TranslationRecognizer" can be used to recognize and translate speech using the default system microphone for input.
	audio_config = speech_sdk.AudioConfig(use_default_microphone=True)
	# cong: parameter of "translation_config" is used to set the configuration of key and location, etc. 
	translator = speech_sdk.translation.TranslationRecognizer(translation_config, audio_config = audio_config)
	print("Speak now...")
	# cong, the result is the SpeechRecognitionResult which inclueds: Duration,OffsetInTicks,Properties,Reason,ResultId,Text,Translations
	result = translator.recognize_once_async().get()
	print('Translating "{}"'.format(result.text))
	# cong, the truly important is this result.translations. it can recognize the speech and translate it into , such as, French
	translation = result.translations[targetLanguage]
	print(translation)


	# 2. Synthesize translation
	voices = {
			 "fr": "fr-FR-HenriNeural",
			 "es": "es-ES-ElviraNeural",
			 "hi": "hi-IN-MadhurNeural"
	}
	speech_config.speech_synthesis_voice_name = voices.get(targetLanguage)
	# cong: the truly important is below objects which can synthesize the translated text.
	speech_synthesizer = speech_sdk.SpeechSynthesizer(speech_config)
	speak = speech_synthesizer.speak_text_async(translation).get()
	if speak.reason != speech_sdk.ResultReason.SynthesizingAudioCompleted:
		print(speak.reason)



if __name__ == "__main__":
    main()