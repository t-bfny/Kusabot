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
due_messages = []
status_lines = []

for plant in plants:
    last_date = datetime.strptime(plant["last_watered"], "%Y-%m-%d").date()
    days_passed = (today - last_date).days

    if days_passed >= plant["interval"]:
        due_messages.append(f"🌿 *{plant['name']}* に水をあげる時間です！ (前回から{days_passed}日経過)")
        plant["last_watered"] = str(today)
        updated = True
        days_passed = 0

    status_lines.append(f"• {plant['name']}: {days_passed}日経過 / {plant['interval']}日間隔")

sections = []
if due_messages:
    sections.append("\n".join(due_messages))
else:
    sections.append("💧 本日水やりが必要な植物はありません。")
sections.append("*🌱 全植物の状況*\n" + "\n".join(status_lines))

full_message = "\n\n".join(sections)
client.chat_postMessage(channel="kusa", text=full_message)
print("通知を送信しました。")

if updated:
    with open(PLANTS_FILE, "w", encoding="utf-8") as f:
        json.dump(plants, f, ensure_ascii=False, indent=2)
    print("植物の水やり情報を更新しました。")