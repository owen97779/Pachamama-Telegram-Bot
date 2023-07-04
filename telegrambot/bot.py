import os
import asyncio
from functools import partial
from cctv import CCTV
from ping import Host
from store import Store
from typing import Final
from container import start_webhook_server
from telegram.ext import Application, CommandHandler
from commands import (
    start_command,
    help_command,
    broadcast_command,
    chatid_command,
    ping_command,
    ping_info_command,
    add_host_command,
    remove_host_command,
    show_hosts_command,
    subscribe_command,
    unsubscribe_command,
    subscribers_command,
    cctv_online,
    error,
    ping_all,
)


def main():
    # with open("TOKEN.env", "r") as file:
    #     TOKEN = file.read().replace("\n", "")
    # with open("CCTV_SERVER_HOST.env", "r") as file:
    #     CCTV_SERVER_HOST = file.read().replace("\n", "")
    # with open("CCTV_MQTT_TOPIC.env", "r") as file:
    #     CCTV_MQTT_TOPIC = file.read().replace("\n", "")

    TOKEN = os.getenv("TOKEN")
    CCTV_SERVER_HOST = os.getenv("CCTV_SERVER_HOST")
    CCTV_MQTT_TOPIC = os.getenv("CCTV_MQTT_TOPIC")

    cctv = CCTV(CCTV_SERVER_HOST, CCTV_MQTT_TOPIC)
    store = Store("hosts.json", "subscribers.json")
    store.load()
    # print("Store loaded")
    # for store in store.allsubscribers:
    #     print(f"{store}: {store.allsubscribers[store]}")
    app = Application.builder().token(TOKEN).build()
    print("Bot started")

    # add command handlers

    app.add_handler(CommandHandler("start", start_command))  # start command
    app.add_handler(CommandHandler("help", help_command))  # help command

    broadcast_command_partial = partial(
        broadcast_command, store, TOKEN
    )  # broadcast command with subscribers argument
    app.add_handler(
        CommandHandler("broadcast", broadcast_command_partial)
    )  # broadcast command

    app.add_handler(CommandHandler("chatid", chatid_command))  # ping command

    ping_command_partial = partial(
        ping_command, store
    )  # ping command with hostobj argument
    app.add_handler(CommandHandler("ping", ping_command_partial))  # ping command

    ping_info_command_partial = partial(
        ping_info_command, store
    )  # ping info command with hostobj argument
    app.add_handler(
        CommandHandler("pinginfo", ping_info_command_partial)
    )  # ping info command

    add_host_command_partial = partial(
        add_host_command, store
    )  # add host command with hostobj argument
    app.add_handler(
        CommandHandler("addhost", add_host_command_partial)
    )  # add host command

    remove_host_command_partial = partial(
        remove_host_command, store
    )  # remove host command
    app.add_handler(
        CommandHandler("delhost", remove_host_command_partial)
    )  # remove host command

    show_hosts_command_partial = partial(
        show_hosts_command, store
    )  # show hosts command with hostobj argument
    app.add_handler(
        CommandHandler("showhosts", show_hosts_command_partial)
    )  # show hosts command

    subscribe_command_partial = partial(subscribe_command, store)  # add subscriber
    app.add_handler(
        CommandHandler("subscribe", subscribe_command_partial)
    )  # add subscriber

    subscribers_command_partial = partial(
        subscribers_command, store
    )  # show subscribers
    app.add_handler(
        CommandHandler("subscribers", subscribers_command_partial)
    )  # show subscribers

    unsubscribe_command_partial = partial(
        unsubscribe_command, store
    )  # remove subscriber
    app.add_handler(
        CommandHandler("unsubscribe", unsubscribe_command_partial)
    )  # remove subscriber

    cctv_online_partial = partial(
        cctv_online, cctv
    )  # cctv online command with cctv argument
    app.add_handler(CommandHandler("cctv", cctv_online_partial))  # cctv online command

    # add error handling
    app.add_error_handler(error)

    loop = asyncio.get_event_loop()
    loop.create_task(ping_all(store, TOKEN))
    loop.create_task(cctv.connect(store, TOKEN))
    loop.create_task(start_webhook_server(store, TOKEN))

    # message checking for every n number of seconds
    print("Polling started")
    app.run_polling(poll_interval=3)


if __name__ == "__main__":
    main()
