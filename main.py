import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from fastai.vision.all import load_learner

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

def start(update, context):
    update.message.reply_text(
        "I am a Telegram Bot (powered by Deep learning) and Developed by Sai Tej \n\n "
        "EN : Send Me Your Room Photo I will tell you is it Clean or Messy 😏 \n"
        "TE : మీ గది ఫోటోను నాకు పంపండి అది శుభ్రంగా లేదా దారుణంగా ఉందని నేను మీకు చెప్తాను😏 \n"
        "HI : अपना कमरा फोटो भेजें मैं आपको बताऊंगा कि यह साफ है या गन्दा है😏 \n"
        "TM : உங்கள் அறை புகைப்படத்தை அனுப்புங்கள் இது சுத்தமானதா அல்லது குழப்பமானதா என்பதை நான் உங்களுக்குச் சொல்வேன்😏 "

    )

def help_command(update, context):
    update.message.reply_text('My only purpose is to tell you if you are your room is Clean or Messy. Send Me a photo')

def load_model():
    global model
    model = load_learner('CleanMessyModel.pkl')
    print('Model loaded')

def detect_room(update, context):
    user = update.message.from_user
    photo_file = update.message.photo[-1].get_file()
    photo_file.download('user_photo.jpg')
    logger.info("Photo of %s: %s", user.first_name, 'user_photo.jpg')

    label = model.predict('user_photo.jpg')[0]
    if label == "Clean":
        update.message.reply_text(
            "EN : Looks like you Room is Clean. I hope you keep it clean daily!😉 \n\n"
            "TE : మీ గది శుభ్రంగా ఉన్నట్లు కనిపిస్తోంది. మీరు దీన్ని ప్రతిరోజూ శుభ్రంగా ఉంచుతారని నేను ఆశిస్తున్నాను! 😉\n"
            "HI : लगता है कि आप कक्ष स्वच्छ हैं। मुझे आशा है कि आप इसे दैनिक साफ रखेंगे! 😉\n"
            "TM : நீங்கள் அறை சுத்தமாக இருப்பது போல் தெரிகிறது. தினமும் அதை சுத்தமாக வைத்திருப்பீர்கள் என்று நம்புகிறேன்! 😉"         
        )
    else:
        update.message.reply_text(
            "EN: Looks like you Room is not Clean. Clean it Now ! 😠\n\n"
            "TE: మీ గది శుభ్రంగా లేదనిపిస్తోంది. ఇప్పుడు శుభ్రం చేయండి ! 😠\n"
            "HI: लगता है कि आप कक्ष साफ नहीं है। इसे अभी साफ करें ! 😠\n"
            "TM: நீங்கள் அறை சுத்தமாக இல்லை என்று தெரிகிறது. இப்போது சுத்தம் செய்யுங்கள் ! 😠\n"
            
        )

def main():
    load_model()
    updater = Updater(token="1298160601:AAG-_q_rZTNP2y4XkA58u1hHpwY8SggCo2s", use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help_command))

    dp.add_handler(MessageHandler(Filters.photo, detect_room))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()