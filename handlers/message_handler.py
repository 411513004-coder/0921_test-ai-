import logging
from linebot.v3.webhooks import (
    MessageEvent,
    TextMessageContent,
    ImageMessageContent,
    StickerMessageContent
)
from services import line_service
from services import ai_service
import config

logger = logging.getLogger("line_bot")

def register_message_handlers(handler):
    """註冊各類訊息事件處理器"""

    @handler.add(MessageEvent, message=TextMessageContent)
    def handle_text_message(event: MessageEvent):
        user_text = event.message.text.strip()
        reply_token = event.reply_token
        user_id = event.source.user_id if event.source else "default_user"

        logger.info(f"收到來自使用者 {user_id} 的文字訊息: {user_text}")

        # 指令解析
        lower_text = user_text.lower()
        if lower_text == "ping":
            line_service.reply_text(
                reply_token,
                "🏓 Pong! LINE Bot 伺服器連線正常！",
                quick_reply_items=["選單", "自我介紹", "ping"]
            )
        elif lower_text in ["說明", "help", "選單", "menu", "功能"]:
            carousel = line_service.create_interactive_menu_carousel()
            line_service.reply_flex(reply_token, "互動式功能選單", carousel)
        elif lower_text in ["清除記憶", "清除對話", "重設", "reset", "clear"]:
            ai_service.clear_user_history(user_id)
            line_service.reply_text(
                reply_token,
                "🧹 已為您清除對話記憶！接下來我們可以開啟一個全新的話題囉。",
                quick_reply_items=["選單", "請向我自我介紹", "ping"]
            )
        elif lower_text in ["領取key教學", "教學", "key教學", "gemini教學"]:
            guide = ai_service.get_gemini_free_guide()
            line_service.reply_text(
                reply_token,
                guide,
                quick_reply_items=["選單", "ping"]
            )
        elif lower_text in ["關於", "about"]:
            has_gemini = "✅ 已啟用 (Gemini 2.5 Flash)" if config.is_gemini_configured() else "⏳ 尚未設定 (可免費申請)"
            about_msg = (
                "ℹ️ 【系統環境與架構】\n"
                "• 核心技術：Python 3.12 + FastAPI (非同步)\n"
                "• SDK 版本：LINE Bot SDK v3 (官方最新)\n"
                f"• AI 智慧對話：{has_gemini}\n"
                "• 穿透服務：Cloudflare Tunnel\n"
                "• 方案費用：100% 免費無額外開銷"
            )
            line_service.reply_text(
                reply_token,
                about_msg,
                quick_reply_items=["選單", "ping"]
            )
        else:
            # 智能 AI 對話處理
            ai_reply = ai_service.ask_gemini(user_id, user_text)
            line_service.reply_text(
                reply_token,
                ai_reply,
                quick_reply_items=["選單", "清除記憶", "ping"]
            )

    @handler.add(MessageEvent, message=ImageMessageContent)
    def handle_image_message(event: MessageEvent):
        reply_token = event.reply_token
        logger.info("收到圖片訊息")
        line_service.reply_text(
            reply_token,
            "📷 已收到您傳送的圖片！如需進行 AI 圖片辨識，可在 message_handler 中串接視覺模型。",
            quick_reply_items=["說明"]
        )

    @handler.add(MessageEvent, message=StickerMessageContent)
    def handle_sticker_message(event: MessageEvent):
        reply_token = event.reply_token
        logger.info("收到貼圖訊息")
        line_service.reply_text(
            reply_token,
            "✨ 收到您可愛的貼圖囉！",
            quick_reply_items=["說明", "ping"]
        )
