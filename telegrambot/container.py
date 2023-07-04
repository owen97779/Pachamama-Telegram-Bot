import asyncio
from utils import notify
from aiohttp import web
from functools import partial


async def webhook_handler(store, TOKEN, request):
    """
    webhook_handler function to handle webhook requests from GitHub.

    Parameters
    ----------
    store: Store
        The store object.
    TOKEN: Final
        The bot token.
    request: Request
        The request object.

    """
    data = await request.post()
    event_type = request.headers.get("X-GitHub-Event")
    broadcast_chatids = [
        key
        for key, value in store.subscribers.items()
        if "broadcast_sub" in value and value["broadcast_sub"]
    ]
    if event_type == "push":
        pass
        
    #     # Process the push event payload
    #     branch = data.get('ref')
    #     commits = data.get('commits')
    #     print(f"Push event received for branch {branch}")
    #     print("Commits:")
    #     for commit in commits:
    #         print(commit.get('message'))

    #     # Add your webhook handling logic here

    # elif event_type == 'pull_request':
    #     # Process the pull request event payload
    #     action = data.get('action')
    #     pr_number = data.get('number')
    #     print(f"Pull request event received - action: {action}, PR number: {pr_number}")

    #     # Add your webhook handling logic here

    else:
        print("Unsupported event type")
    
    msg = f"""❕ The bot has received a new update, it will now restart!\n
        Please resubscribe to receive new notifications.
        Contact Benji if you require any assistance.
        (https://t.me/owen97779)"""
    print("RESTART MESSAGE SENT")
    await notify(msg, broadcast_chatids, TOKEN)

    return web.Response(text="Webhook processed successfully")


async def start_webhook_server(store, TOKEN):
    """
    start_webhook_server function to start the webhook server.

    Parameters
    ----------
    store: Store
        The store object.
    TOKEN: Final
        The bot token.
    """
    app = web.Application()
    webhook_handler_partial = partial(webhook_handler, store, TOKEN)
    app.router.add_post("/webhook", webhook_handler_partial)

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", 8989)
    await site.start()
    print("Webhook server started on http://localhost:8989")
