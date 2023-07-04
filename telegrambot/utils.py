from telegram import Bot

async def notify(msg: str, chatids, TOKEN):
    """
    Notify function to send a message to all subscribers for the bot.
    Parameters
    ----------
    msg: str
        The specified message to be broadcasted to all subscribers.
    subscribers: list
        List of subscribers.
    TOKEN: Final
        The bot token.
    """
    bot = Bot(token=TOKEN)
    for chatid in chatids:
        await bot.send_message(int(chatid), text=msg)