# AI 日報 webapp

每日 AI 新聞五版塊日報，公開網站，每朝約 8 點自動更新。

## 係咩嚟
- **公開網站（主）**：https://carriehw.github.io/ai-daily/ （GitHub Pages，任何人唔使登入都睇到）
- **Repo**：github.com/carriehw/ai-daily（public）
- 舊 Artifact URL 已棄用，唔再更新

## 檔案 / 資料流
```
data.json（新聞數據，每項要有 why 欄位）
  → build.py（跑之前要 set PYTHONIOENCODING=utf-8）
  → index.html（單檔，內聯無外部資源）
```
- `.github/workflows/deploy.yml` + `.nojekyll`：GitHub Actions 部署

## 每日更新流程
1. 用 `ai-daily-news` skill 抓 smol.ai + 兩個 agent 掃國際 / 大中華媒體
2. 去重寫入 `data.json`（每項要有 why）
3. 跑 `build.py`
4. `git add -A && git commit && git push` → 1-2 分鐘自動 live
- 已有 scheduled task `ai-daily-update`（每朝約 8 點）；App 冇開就等下次開 App 補跑

## 規格（用戶定義，唔准走樣）
- 五個**固定**版塊：模型發布/更新、產品發布/更新、行業動態、論文研究、技巧與觀點
- 全局連續編號（唔喺版塊內重新計）
- 頂部 Hero：日期 + 總條數 + 五版塊統計；中部錨點導航
- 卡片含：序號、標題、來源 chip、≤60 字中文摘要、原文連結（`_blank noopener`）
- 內容範圍：國際 + 香港 + 中國 + 台灣四市場（各有市場 chip 色），重點 Claude/ChatGPT/Gemini
- **來源必須有國際媒體**，唔可以淨係中國媒體
- 時間用人話格式，唔用 ISO

## 陷阱
- ⚠️ 部署一定要用 GitHub Actions（`build_type=workflow`），唔好轉返 legacy Jekyll → 會 "Page build failed"
- gh CLI 喺 `C:\Program Files\GitHub CLI\gh.exe`；git 身份 user.name=carriehw

## 用戶偏好
繁體中文（粵語書面）；先思考再動手、簡潔、精確、目標驅動；綠升紅跌。
