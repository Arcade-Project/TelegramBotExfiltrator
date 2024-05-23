import requests
import time

def get_bot_info(api_key):
    url = f"https://api.telegram.org/bot{api_key}/getMe"
    response = requests.get(url)
    if response.status_code == 200:
        bot_info = response.json()
        if bot_info['ok']:
            return bot_info['result']
        else:
            return {"error": "Invalid API key or bot not found"}
    else:
        return {"error": f"HTTP error {response.status_code}"}

def get_updates(api_key, offset=None):
    url = f"https://api.telegram.org/bot{api_key}/getUpdates"
    if offset:
        url += f"?offset={offset}"
    response = requests.get(url)
    if response.status_code == 200:
        updates = response.json()
        if updates['ok']:
            return updates['result']
        else:
            return {"error": "Failed to get updates"}
    else:
        return {"error": f"HTTP error {response.status_code}"}

def get_chat_info(api_key, chat_id):
    url = f"https://api.telegram.org/bot{api_key}/getChat?chat_id={chat_id}"
    response = requests.get(url)
    if response.status_code == 200:
        chat_info = response.json()
        if chat_info['ok']:
            return chat_info['result']
        else:
            return {"error": "Failed to get chat info"}
    else:
        return {"error": f"HTTP error {response.status_code}"}

def main():
    api_key = input("Enter the Telegram bot API key: ")
    bot_info = get_bot_info(api_key)
    if "error" in bot_info:
        print(bot_info["error"])
        return

    print(f"Bot ID: {bot_info['id']}")
    print(f"Bot Username: {bot_info['username']}")
    print(f"Bot First Name: {bot_info['first_name']}")
    print(f"Is Bot: {bot_info['is_bot']}")

    offset = None
    seen_chats = set()

    while True:
        updates = get_updates(api_key, offset)
        if "error" in updates:
            print(updates["error"])
            break
        else:
            if updates:
                last_update_id = updates[-1]['update_id']
                for update in updates:
                    if 'message' in update:
                        chat_id = update['message']['chat']['id']
                        if chat_id not in seen_chats:
                            seen_chats.add(chat_id)
                            chat_info = get_chat_info(api_key, chat_id)
                            if "error" in chat_info:
                                print(chat_info["error"])
                            else:
                                chat_title = chat_info.get('title', 'Private Chat')
                                if chat_info['type'] in ['group', 'supergroup']:
                                    print(f"\nGroup ID: {chat_id}")
                                    print(f"Group Title: {chat_title}")
                offset = last_update_id + 1
            else:
                print("No new updates found.")
                break
        time.sleep(1)  # Pause to prevent rapid consecutive requests

if __name__ == "__main__":
    main()
