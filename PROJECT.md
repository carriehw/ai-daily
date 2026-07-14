# AI・日報 — 專案說明文件

每日自動生成嘅 AI 新聞快訊網站，涵蓋國際／香港／中國／台灣四大市場，重點追蹤 Claude / ChatGPT / Gemini 動態。每條新聞附「點解重要」，用香港 AI 用家兼投資者視角解讀。

---

## 1. 成品

| 項目 | 內容 |
|---|---|
| 公開網站 | **https://carriehw.github.io/ai-daily/** （任何人唔使帳號都睇到、share 得） |
| GitHub Repo | https://github.com/carriehw/ai-daily （public） |
| 更新頻率 | 每朝約 8:00（香港時間）自動更新 |
| 部署方式 | GitHub Pages（GitHub Actions，`build_type=workflow`） |

---

## 2. 架構同資料流

```
  ┌─ smol.ai RSS ────────┐
  ├─ 國際媒體 (agent) ────┤ →  合併去重  →  data.json  ─┐
  └─ 大中華媒體 (agent) ──┘   （每條含 why）             │
                                                        ▼
                                   build.py  (PYTHONIOENCODING=utf-8)
                                                        │
                                                        ▼
                                   index.html  （單檔、內聯、無外部資源）
                                                        │
                                   git push → GitHub Actions → GitHub Pages
                                                        │
                                                        ▼
                                   https://carriehw.github.io/ai-daily/
```

### 檔案清單
| 檔案 | 用途 |
|---|---|
| `data.json` | 新聞數據源（唯一要改嘅內容檔） |
| `build.py` | 讀 `data.json` 生成 `index.html`；跑之前必須 `PYTHONIOENCODING=utf-8` |
| `index.html` | 產出嘅單頁網站（自動生成，唔好手改） |
| `.github/workflows/deploy.yml` | GitHub Actions 部署 workflow |
| `.nojekyll` | 叫 Pages 唔好用 Jekyll 處理（避免 build 失敗） |
| `CLAUDE.md` | 俾 AI 睇嘅專案守則（開發用） |
| `PROJECT.md` | 本文件（人睇嘅說明） |

---

## 3. `data.json` 結構

```jsonc
{
  "date": "2026-07-14",                       // ISO 日期（做 <title>）
  "date_display": "2026年7月14日 · 星期二",    // Hero 顯示嘅人話日期
  "sources_note": "OpenAI · Anthropic · …",   // 文末數據源列表
  "sections": [                                // 五個固定版塊（次序固定）
    "模型發布/更新", "產品發布/更新", "行業動態", "論文研究", "技巧與觀點"
  ],
  "items": [
    {
      "title":   "標題（保留產品英文名）",
      "summary": "≤60 中文字摘要（跟編輯守則）",
      "source":  "來源媒體名",
      "url":     "原文連結",
      "time":    "7月9日",                     // 人話時間，唔用 ISO
      "section": "模型發布/更新",              // 必屬上面五個之一
      "market":  "國際",                       // 國際 / 香港 / 中國 / 台灣
      "why":     "≤35 字『點解重要』（跟編輯守則）"
    }
  ]
}
```

---

## 4. 每日更新流程（自動）

Scheduled task `ai-daily-update` 每朝約 8 點跑：

1. **抓料**（三路並行）：`ai-daily-news` skill 抓 smol.ai + 兩個 agent 分頭掃國際／大中華媒體
2. **整理**：合併去重、精選 30–40 條、每條補 `why`、跟足《粵語編輯守則》
3. **重建**：`PYTHONIOENCODING=utf-8 python build.py`
4. **發布**（自我修復流程）：
   ```bash
   git add -A
   git diff --cached --quiet || git commit -m "Daily update YYYY-MM-DD"
   git pull --rebase --autostash origin main
   git push origin main
   ```
5. GitHub Actions 自動部署，1–2 分鐘後網站更新

> ⚠️ App 冇開時排程唔會跑，會等下次開 App 補跑。

---

## 5. 手動更新（如要即刻改）

```bash
cd ~/Desktop/Claude/ai-daily
# 改 data.json
PYTHONIOENCODING=utf-8 python build.py
git add -A && git commit -m "manual update" && git push
```

---

## 6. 陷阱 / 維護筆記

- **部署一定要用 GitHub Actions**（`build_type=workflow`）。唔好轉返 legacy Jekyll，會 `Page build failed`。
- **Windows 編碼**：跑 `build.py` / `fetch_news.py` 前一定要 `PYTHONIOENCODING=utf-8`，否則 cp1252 crash。
- **認證**：`git push` 靠 Windows Credential Manager 存嘅 credential。若 token 過期令自動 push 失敗，喺 terminal 重新 `gh auth login`。
- **gh CLI 路徑**：`C:\Program Files\GitHub CLI\gh.exe`。
- **artifact path `.`**：整個 repo 都會 publish 上 Pages（`build.py`、`data.json` 都睇得到）。目前無敏感資料，安全。將來若加 secret，記得改 workflow 只 publish 產出檔。

---

## 7. 編輯守則

見同目錄 skill 版本嘅 `references/editorial-style-guide.md`，或 scheduled task prompt 內嵌版本。核心：口語書面化廣東話、禁「但/但係/不過」、術語即場拆解、`why` 要貼身唔離地。
