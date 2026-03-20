import json
import os
from datetime import datetime, date
from slack_sdk import WebClient

# 設定
base_path = os.path.dirname(__file__)
PLANTS_FILE = os.path.join(base_path, "plants.json")
client = WebClient(token=os.environ["SLACK_BOT_TOKEN"])
today = date.today()

with open(PLANTS_FILE, "r", encoding="utf-8") as f:
    plants = json.load(f)

updated = False
messages = []

for plant in plants:
    last_date = datetime.strptime(plant["last_watered"], "%Y-%m-%d").date()
    days_passed = (today - last_date).days
    
    if days_passed >= plant["interval"]:
        messages.append(f"🌿 **{plant['name']}** に水をあげる時間です！ (前回から{days_passed}日経過)")
        plant["last_watered"] = str(today)
        updated = True

# 更新があれば保存

if messages:
    full_message = "\n".join(messages)
    client.chat_postMessage(channel="kusa", text=full_message)
    print("水やりの通知を送信しました。")
else:
    print("今日は水やりの対象となる植物はありませんでした。")

if updated:
    with open(PLANTS_FILE, "w", encoding="utf-8") as f:
        json.dump(plants, f, ensure_ascii=False, indent=2)
    print("植物の水やり情報を更新しました。")