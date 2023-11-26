from dotenv import load_dotenv
import os 
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler,MessageHandler,filters
from elevenlabs import generate,save
import openai
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage,SystemMessage
from langchain.chains import ConversationChain


#Commands 
#/start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    to_send = f'Hello {update.message.from_user.full_name} \n I a am Chat Bot, Made by Tufail \n\n To see the *Help* menue use /help command. '
    await context.bot.send_message(chat_id=update.effective_chat.id, text= to_send,parse_mode='Markdown')

#/text_to_speech 
async def text_to_speech(update:Update,context:ContextTypes.DEFAULT_TYPE) :
    chatid = update.message.chat_id
    text = update.message.text
    text = text.replace('/texttospeech','')

    aud = generate(
        text=text,
        voice='RDL23HMearCQQZp3GIHa'
    )

    filename = f'{chatid}.wav'

    with open(filename,'wb') as fb:
        fb.write(aud)

    await context.bot.send_audio(update.message.chat_id,audio=filename,read_timeout=30,write_timeout=30)

#/help 
async def help(update:Update,context:ContextTypes.DEFAULT_TYPE):
    to_send = '''
/start : Start the message 
/texttospeech : Convert Text to Speech 
/help : View the Help Menue 
/madara : Convert Text to Madara VOICE (Coming soon) '''
    await context.bot.send_message(update.message.chat_id,text=to_send)

#Handel Message 
async def handel_message(update:Update,context:ContextTypes.DEFAULT_TYPE):
    from_user = update.message.text
    if from_user.lower() in ('hello', 'hi','hey'):
        await context.bot.send_message(update.message.chat_id,text=f'Hello {update.message.from_user.first_name} ')
    else:
        message_for_ai = [ 
        SystemMessage(content= 'You are a General purpose Chat bot'),
        HumanMessage(content= from_user)]

        conversation = ConversationChain(llm=chat)

        to_send = conversation.run(message_for_ai)
        print(f'From User : {from_user}')
        await context.bot.send_message(update.message.chat_id,text= to_send )
        


        

if __name__ == '__main__':
    load_dotenv()
    token = os.getenv('TOKEN')
    openai_api_key = os.getenv('OPENAI_AP_KEY')
    chat = ChatOpenAI(api_key=openai_api_key, max_tokens=520,temperature=0.2)

    application = ApplicationBuilder().token(token).build()
    
    #Commands 
    start_handler = CommandHandler('start', start)
    speech_handler = CommandHandler('texttospeech',text_to_speech)
    help_handler = CommandHandler('help',help)
    #Message
    message_handler = MessageHandler(filters.TEXT,handel_message)

    application.add_handler(start_handler)
    application.add_handler(speech_handler)
    application.add_handler(help_handler)
    application.add_handler(message_handler)
    


    application.run_polling()