from telegram import Update, Message
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# مجموعة لتخزين ID كل المواضيع المفلترة
filter_topics = set()

# تفعيل الفلترة على موضوع معين
def messagesfilter_(update: Update, context: CallbackContext):
    global filter_topics
    if update.message.is_topic_message:
        filter_topics.add(update.message.message_thread_id)
        update.message.reply_text("🛑 تم تفعيل فلترة الرسائل على هذا الموضوع. الصور والفيديوهات والملفات فقط مسموح بها.")
    else:
        update.message.reply_text("❌ من فضلك ابعت الأمر داخل الموضوع اللي عايز تفعل فيه الفلترة.")

# إيقاف الفلترة على موضوع معين
def stopmessagesfilter_(update: Update, context: CallbackContext):
    global filter_topics
    if update.message.is_topic_message:
        filter_topics.discard(update.message.message_thread_id)
        update.message.reply_text("✅ تم إيقاف فلترة الرسائل في الموضوع ده.")
    else:
        update.message.reply_text("❌ من فضلك ابعت الأمر داخل الموضوع اللي عايز توقف فيه الفلترة.")

# التعامل مع الرسائل أثناء تفعيل الفلتر
def message_handler(update: Update, context: CallbackContext):
    global filter_topics
    msg: Message = update.message
    if msg and msg.is_topic_message and msg.message_thread_id in filter_topics:
        # لو الرسالة مش صورة أو فيديو أو ملف → تتشال
        if not (msg.photo or msg.video or msg.document):
            try:
                msg.delete()
            except Exception as e:
                print(f"خطأ أثناء حذف الرسالة: {e}")

def main():
    updater = Updater("8498501346:AAH7ms_OYrYaBWnc4aXtCtAxP9Kjj3Dj2DQ", use_context=True)  # ← هنا تحط التوكن بتاعك بين علامات التنصيص
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("messagesfilter", messagesfilter_))
    dp.add_handler(CommandHandler("stopmessagesfilter", stopmessagesfilter_))
    dp.add_handler(MessageHandler(Filters.all & ~Filters.command, message_handler))

    updater.start_polling()
    print("✅ البوت اشتغل بنجاح!")
    updater.idle()

if __name__ == '__main__':
    main()
