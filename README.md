# 🤖 Python LINE Bot 專案 (FastAPI + LINE Bot SDK v3)

這是一個基於 **Python 3.12**、**FastAPI** 與官方最新版 **`line-bot-sdk` (v3)** 所建置的現代化 LINE Bot 專案。具備非同步高效能、完整 HMAC-SHA256 安全簽章防護、結構化事件處理模組，並預設支援 Flex Message 視覺選單卡片與 Quick Reply 快捷按鈕。

---

## 📁 專案目錄結構

```text
c:\User\Documents\1005\
├── .env                  # 實際運行的環境變數（包含 LINE 憑證）
├── .env.example          # 環境變數範本
├── .gitignore            # Git 忽略設定
├── config.py             # 設定檔讀取與狀態檢測模組
├── main.py               # FastAPI 主程式與 Webhook (/callback) 路由
├── requirements.txt      # Python 相依套件清單
├── run.bat               # Windows 一鍵啟動批次檔
├── handlers/             # 事件監聽與業務邏輯
│   ├── message_handler.py # 文字、圖片、貼圖等訊息處理器
│   └── event_handler.py   # 加入好友 (Follow)、退群、按鈕互動 (Postback) 處理器
├── services/             # 外部服務整合
│   └── line_service.py    # LINE Messaging API 發送與 Flex 卡片模板
└── tests/                # 自動化測試
    └── test_webhook.py   # Webhook 與簽章安全性單元測試
```

---

## 🛠️ 第一步：申請與設定 LINE Developers Console

如果您尚未申請 LINE Bot，請按照以下步驟取得金鑰：

1. 前往 [LINE Developers Console](https://developers.line.biz/console/) 並使用您的 LINE 帳號登入。
2. 點擊 **Create a new provider**（建立提供者），輸入名稱（例如：`MyBotProvider`）。
3. 在 Provider 頁面內點選 **Create a Messaging API channel**：
   - 填寫 **Channel name**（機器人名稱）。
   - 填寫 **Channel description**（機器人描述）。
   - 選擇 **Category** 與 **Subcategory**（類別）。
   - 勾選同意條款後點擊 **Create**。
4. **取得金鑰資訊**：
   - 在 **Basic settings** 分頁最下方，複製 **Channel secret**。
   - 切換到 **Messaging API** 分頁最下方，在 **Channel access token (long-lived)** 處點擊 **Issue**（發行）並複製整段 Token。
5. **關閉官方預設自動回覆（非常重要）**：
   - 在 **Messaging API** 分頁中，找到 **Auto-reply messages**，點擊 **Edit** 進入 LINE Official Account Manager。
   - 在「回應設定」中：
     - **回應模式**：選擇「聊天機器人 (Bot)」。
     - **自動回應訊息**：設定為「停用」（避免官方自動回覆與程式衝突）。
     - **Webhook**：設定為「啟用」。

---

## ⚙️ 第二步：設定專案環境變數

開啟專案根目錄下的 `.env` 檔案，填入剛剛取得的金鑰：

```env
LINE_CHANNEL_SECRET=貼上您的Channel_Secret
LINE_CHANNEL_ACCESS_TOKEN=貼上您的Channel_Access_Token
PORT=8000
```

---

## 🚀 第三步：啟動本機伺服器

### 方式一：直接雙擊執行
雙擊專案目錄下的 `run.bat`。

### 方式二：使用終端機指令
```powershell
.\venv\Scripts\Activate.ps1
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

啟動後，瀏覽器開啟 `http://localhost:8000` 會顯示：
```json
{
  "status": "online",
  "message": "LINE Bot Webhook 伺服器運作正常",
  "line_configured": true,
  "webhook_endpoint": "/callback"
}
```

---

## 🌐 第四步：本地穿透與設定 Webhook URL

由於 LINE 伺服器需要透過合法的 HTTPS 公開網址將訊息推送到您的電腦，我們可以使用 **Cloudflare Tunnel**（免費、免註冊、無連線時間限制）或 **ngrok**。

### 推薦：使用 Cloudflare Tunnel (`cloudflared`)
1. 下載 `cloudflared.exe`，或在終端機執行：
   ```powershell
   winget install Cloudflare.cloudflared
   ```
2. 執行穿透指令：
   ```powershell
   cloudflared tunnel --url http://localhost:8000
   ```
3. 終端機會顯示類似網址：
   `https://xxxx-xxxx-xxxx.trycloudflare.com`
4. 將該網址加上 `/callback` 填入 LINE Developers：
   - 進入 LINE Developers Console -> 您的 Channel -> **Messaging API** 分頁。
   - 在 **Webhook settings** 的 **Webhook URL** 填入：
     `https://xxxx-xxxx-xxxx.trycloudflare.com/callback`
   - 開啟 **Use webhook** 開關。
   - 點擊 **Verify**（驗證），若顯示 **Success** 即表示連線成功！

---

## 📱 第五步：掃描 QR Code 實測對話

在 **Messaging API** 分頁最上方有機器人的專屬 **QR Code**，使用手機 LINE 掃描加入好友後即可開始測試！

### 預設支援指令：
- **加入好友**：自動發送繁體中文歡迎訊息與推薦按鈕。
- `ping`：回傳 `Pong!` 伺服器健康狀態與快捷按鈕。
- `說明` 或 `help`：展示原生 **Flex Message** 視覺卡片選單。
- `關於`：顯示當前運行環境與架構說明。
- **發送圖片 / 貼圖**：觸發多媒體訊息專屬回覆。
- **其他任意文字**：自動回音並附帶功能捷徑按鈕。

---

## 🧪 執行自動化測試

本專案附帶完整的單元測試與安全簽章驗證：
```powershell
.\venv\Scripts\pytest tests/ -v
```
