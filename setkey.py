import json
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = "7239898777:AAGZAb1Eo169hhOVSgCsIVR4WQLVLdCSI68"
KEY_FILE = "keys.json"

# Tạo file keys.json nếu chưa tồn tại
if not os.path.exists(KEY_FILE):
    with open(KEY_FILE, "w") as f:
        json.dump({"keys": []}, f)

def load_keys():
    with open(KEY_FILE, "r") as f:
        return json.load(f)["keys"]

def save_keys(keys):
    with open(KEY_FILE, "w") as f:
        json.dump({"keys": keys}, f, indent=2)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Xin chào! Dùng /addkey, /delkey, /listkey để quản lý key.")

async def add_key(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("❌ Hãy nhập key để thêm. Ví dụ: /addkey abc123")
        return
    key = context.args[0]
    keys = load_keys()
    if key in keys:
        await update.message.reply_text("⚠️ Key đã tồn tại.")
    else:
        keys.append(key)
        save_keys(keys)
        await update.message.reply_text(f"✅ Đã thêm key: {key}")

async def del_key(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("❌ Hãy nhập key để xóa. Ví dụ: /delkey abc123")
        return
    key = context.args[0]
    keys = load_keys()
    if key in keys:
        keys.remove(key)
        save_keys(keys)
        await update.message.reply_text(f"🗑️ Đã xóa key: {key}")
    else:
        await update.message.reply_text("❌ Không tìm thấy key.")

async def list_keys(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keys = load_keys()
    if keys:
        await update.message.reply_text("📋 Danh sách key:\n" + "\n".join(keys))
    else:
        await update.message.reply_text("📭 Hiện chưa có key nào.")

# Khởi động bot
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("addkey", add_key))
app.add_handler(CommandHandler("delkey", del_key))
app.add_handler(CommandHandler("listkey", list_keys))
print("🤖 Bot 1 đang chạy...")
app.run_polling()
