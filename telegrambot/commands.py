import os
import sys
import json
import asyncio
from ping import Host
from store import Store
from utils import notify
from telegram import Update, Bot
from telegram.ext import ContextTypes


# start command function
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Command for user if they want to start the bot

    Parameters
    ----------
    update : Update
        Update object from Telegram API
    context : ContextTypes.DEFAULT_TYPE
        Context object from Telegram API
    """
    await update.message.reply_text(
        """
    Secret start command :)
    \nPlease use /help to know more about me.
    \nInshallah, I will be able to help you.    
    """
    )


# help command function
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Command for user if they want to know more about the bot

    Parameters
    ----------
    update : Update
        Update object from Telegram API
    context : ContextTypes.DEFAULT_TYPE
        Context object from Telegram API
    """
    await update.message.reply_text(
        """
    Hi! I am the Pachamama Network Status bot. I can help you check the status of the Pachamama Network.
    \nPlease refer to the below commands to use the bot:
    \n🔥 Popular Commands:
    /cctv - Shows all Online CCTV Members
    /subscribe - Subscribe to the Pachamama Network Status Bot to receive notifications
    /unsubscribe - Unsubscribe from the Pachamama Network Status Bot
    /broadcast <message> - Broadcast a message to all users
    \n🛠️ Debugging Commands:
    /ping <host> - Check the Ping to a Host
    /pinginfo <host> <count> - Check the Ping to a Host with more information
    /showhosts - Show all Hosts
    /addhost <host> <ip> - Add a Host
    /delhost <host> - Delete a Host
    /chatid - Get the Chat ID
    /help - Help
    
    """
    )


async def broadcast_command(
    store, TOKEN, update: Update, context: ContextTypes.DEFAULT_TYPE
):
    """
    Command for user if they want to broadcast a message

    Parameters
    ----------
    store : Store
        Store object from Store class
    TOKEN : str
        Telegram Bot Token
    update : Update
        Update object from Telegram API
    context : ContextTypes.DEFAULT_TYPE
        Context object from Telegram API
    """
    broadcast_chatids = [
        key
        for key, value in store.subscribers.items()
        if "broadcast" in value and value["broadcast"]
    ]

    if str(update.message.chat_id) in broadcast_chatids:
        msg = " ".join(context.args)

        await notify(msg, broadcast_chatids, TOKEN)
    else:
        await update.message.reply_text(
            f"❌ You are not subscribed to the Pachamama Network Status Bot to send a broadcast message."
        )


# error handling function
async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Command for user if they use a command incorrectly

    Parameters
    ----------
    update : Update
        Update object from Telegram API
    context : ContextTypes.DEFAULT_TYPE
        Context object from Telegram API
    """
    print(f"Update {update} caused error {context.error}")
    await update.message.reply_text(
        f"""❌ Command used incorrectly!
        \nPlease try again or use /help."""
    )


# ping command function
async def ping_command(store, update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Command for user if they want to ping a host

    Parameters
    ----------
    store : Store
        Store object from Store class
    update : Update
        Update object from Telegram API
    context : ContextTypes.DEFAULT_TYPE
        Context object from Telegram API
    """
    host = store.hostobj[context.args[0].lower().capitalize()]
    host.ping(1)
    ping = host.pinginfo["average_ping"]
    await update.message.reply_text(f"Ping to {host.host_name}: 🏓\n{ping} ms")


async def ping_info_command(store, update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Command for user if they want to ping a host with more information

    Parameters
    ----------
    store : Store
        Store object from Store class
    update : Update
        Update object from Telegram API
    context : ContextTypes.DEFAULT_TYPE
        Context object from Telegram API
    """
    host = store.hostobj[context.args[0].lower().capitalize()]
    count = int(context.args[1])
    host.ping(count)
    ping_times = ""
    for ping in host.pinginfo["ping_times"]:
        ping_times += f"\n    {ping} ms"
    await update.message.reply_text(
        f"""
    Ping to {host.host_name}: 🏓🏓
    Average Ping: {host.pinginfo['average_ping']} ms
    Ping Count: {host.pinginfo['ping_count']}
    Success Rate: {host.pinginfo['success_rate']}
    
Ping Times: {ping_times}
    """
    )


# add host command function
async def add_host_command(store, update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Command for user if they want to add a host

    Parameters
    ----------
    store : Store
        Store object from Store class
    update : Update
        Update object from Telegram API
    context : ContextTypes.DEFAULT_TYPE
        Context object from Telegram API
    """
    host = (f"{context.args[0]}".lower()).capitalize()
    ip = f"{context.args[1]}"

    if host not in store.hostobj.keys():
        store.add_host(host, ip)
        await update.message.reply_text(f"✅ Host - IP\n{host} - {ip}\nAdded")
    else:
        await update.message.reply_text(f"❌ Host already exists!")


async def remove_host_command(
    store, update: Update, context: ContextTypes.DEFAULT_TYPE
):
    """
    Command for user if they want to remove a host

    Parameters
    ----------
    store : Store
        Store object from Store class
    update : Update
        Update object from Telegram API
    context : ContextTypes.DEFAULT_TYPE
        Context object from Telegram API
    """
    host = (f"{context.args[0]}".lower()).capitalize()
    if host in store.hostobj.keys():
        store.remove_host(host)
        await update.message.reply_text(f"✅ Host\n{host}\nRemoved")
    else:
        await update.message.reply_text(f"❌ Host doesn't exist!")


# show hosts command function
async def show_hosts_command(store, update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Command for user if they want to see all hosts

    Parameters
    ----------
    store : Store
        Store object from Store class
    update : Update
        Update object from Telegram API
    context : ContextTypes.DEFAULT_TYPE
        Context object from Telegram API
    """
    hosts_string = "Host - IP\n"
    for name, host in store.hostobj.items():
        hosts_string += f"{(host.host_name).capitalize()} - {host.ip}\n"
    await update.message.reply_text(hosts_string)


# chatid command function
async def chatid_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Command for user if they want to see their chat ID

    Parameters
    ----------
    update : Update
        Update object from Telegram API
    context : ContextTypes.DEFAULT_TYPE
        Context object from Telegram API
    """
    await update.message.reply_text(update.message.chat_id)


# subscribe command function
async def subscribe_command(store, update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Command for user if they want to subscribe to the bot

    Parameters
    ----------
    store : Store
        Store object from Store class
    update : Update
        Update object from Telegram API
    context : ContextTypes.DEFAULT_TYPE
        Context object from Telegram API
    """
    chatid = str(update.message.chat_id)
    print(chatid)
    arguments = context.args
    if arguments == []:
        await update.message.reply_text(
            f"""❗️ To subscribe to the Pachamama Network Status Bot, please type the names of the notifications you want to receive:
            \n📹 cctv: CCTV login and logout notifications
            \n🚨 down: Restaurant network down notifications
            \n🟢 status: Restaurant internet speed notifications
            \n🔉 broadcast: Broadcast messages from the Pachamama Network Status Bot
            \n\nFor example, type:'/subscribe cctv broadcast down'"""
        )

    else:
        if chatid not in store.subscribers:
            store.add_subscriber(chatid)
        store.update_subscriptions(True, chatid, arguments)
        listofsubs = f"\n"
        for key, value in store.subscribers[chatid].items():
            if value == True:
                listofsubs += f"✅{key}\n"
            else:
                listofsubs += f"❌{key}\n"
        await update.message.reply_text(
            f"""🔊 You are subscribed to the Pachamama Network Status Bot
            \n You will now receive these notifications from the bot:
            \n{listofsubs}
            \nTo unsubscribe from the Pachamama Network Status Bot, please type '/unsubscribe'
            """
        )


# unsubscribe command function
async def unsubscribe_command(
    store, update: Update, context: ContextTypes.DEFAULT_TYPE
):
    """
    Command for user if they want to unsubscribe from the bot

    Parameters
    ----------
    store : Store
        Store object from Store class
    update : Update
        Update object from Telegram API
    context : ContextTypes.DEFAULT_TYPE
        Context object from Telegram API
    """
    chatid = str(update.message.chat_id)

    arguments = context.args
    if chatid not in store.subscribers:
        await update.message.reply_text(
            f"❌ You are not already subscribed to the Pachamama Network Status Bot"
        )
    elif arguments == []:
        await update.message.reply_text(
            f"""❗️ To unsubscribe to the Pachamama Network Status Bot, please type the names of the notifications you want to unsubscribe from:
            \n📹 cctv: CCTV login and logout notifications
            \n🚨 down: Restaurant network down notifications
            \n🟢 status: Restaurant internet speed notifications
            \n🔉 broadcast: Broadcast messages from the Pachamama Network Status Bot
            \n👍 all: All notifications
            \n\nFor example, to unsub to some notifications, type:'/unsubscribe cctv status'
            \nTo unsub to all notifications, type:'/unsubscribe all'"""
        )

    elif "all" in arguments:
        store.remove_subscriber(chatid)
        await update.message.reply_text(
            f"🔇 You have been unsubscribed from the Pachamama Network Status Bot completely"
        )
    else:
        store.update_subscriptions(False, chatid, arguments)
        listofsubs = f"\n"
        for key, value in store.subscribers[chatid].items():
            if value == True:
                listofsubs += f"✅{key}\n"
            else:
                listofsubs += f"❌{key}\n"

        await update.message.reply_text(
            f"""🔈 You are now only subscribed to these notifications:
            \n{listofsubs}"""
        )


async def subscribers_command(
    store, update: Update, context: ContextTypes.DEFAULT_TYPE
):
    """
    Command for user if they want to see all subscribers

    Parameters
    ----------
    store : Store
        Store object from Store class
    update : Update
        Update object from Telegram API
    context : ContextTypes.DEFAULT_TYPE
        Context object from Telegram API
    """
    all_subscribers = f"🔊 Subscribers:\n"
    for key in store.subscribers:
        all_subscribers += f"{key}\n"
    print(all_subscribers)
    await update.message.reply_text(all_subscribers)


async def cctv_online(cctv, update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Command for user if they want to see all online CCTV users

    Parameters
    ----------
    cctv : dict
        Dictionary of CCTV objects
    update : Update
        Update object from Telegram API
    context : ContextTypes.DEFAULT_TYPE
        Context object from Telegram API
    """
    all_online = f"📹 Online CCTV Users:\n"
    for key, value in cctv.members.items():
        if value.logged_in == True:
            all_online += f"{value.name.capitalize()} - {value.logged_in_time}\n"
    print(all_online)
    await update.message.reply_text(all_online)


async def ping_all(store, TOKEN):
    """
    Function to ping all hosts and send notifications to subscribers

    Parameters
    ----------
    store : Store
        Store object from Store class
    subscribers : dict
        Dictionary of subscribers
    TOKEN : str
        Telegram bot token
    """
    error_codes = {0: "\U0001F7E2", 1: "\U0001F7E1", 2: "\U0001F534", 3: "\u2620"}
    while True:
        print("pinging")
        for key, single_hostobj in store.hostobj.items():
            single_hostobj.ping(4)
            status = single_hostobj.pinginfo["status"]
            average_ping = single_hostobj.pinginfo["average_ping"]
            if status == False:
                print(
                    f"{single_hostobj.host_name}: network down"
                    and single_hostobj.down_notify_flag == False
                )
                error_code = single_hostobj.down()
            elif status == True and (120 < average_ping < 200):
                error_code = single_hostobj.amber()
            elif status == True and (average_ping >= 200):
                error_code = single_hostobj.red()
            elif status == True and (average_ping <= 120):
                error_code = single_hostobj.green()
            else:
                pass
            down_chatids = [
                key
                for key, value in store.subscribers.items()
                if "down_sub" in value and value["down_sub"]
            ]
            status_chatids = [
                key
                for key, value in store.subscribers.items()
                if "status_sub" in value and value["status_sub"]
            ]
            if error_code == 3:
                msg = f"""🚨 {single_hostobj.host_name} is down!
                        \nContact Benji to fix the network asap!
                        \n(https://t.me/owen97779)"""
                await notify(msg, down_chatids, TOKEN)
            if error_code != -1 and error_code != 3:
                msg = f"""⚠️ {single_hostobj.host_name}:
                Online: {status}
                Internet Speed: {error_codes[error_code]}
                Average ping: {str(round(average_ping, 2)) + "ms"}"""
                await notify(msg, status_chatids, TOKEN)
        await asyncio.sleep(10)
