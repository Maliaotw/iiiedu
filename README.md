# IIIEDU - 數據分析與課程管理平台

本專案是一個基於 Django 的教育數據分析與課程管理平台，旨在自動化處理課程數據（如資策會課程），並透過 Highcharts 提供直觀的視覺化分析圖表。

## 🚀 核心功能

*   **數據自動化導入**：支援從 Excel (`.xlsx`) 檔案自動導入課程資料至 PostgreSQL 資料庫。
*   **數據分析與快取**：透過 `ingest_data` 指令進行數據清洗、分析，並生成 `chart_data.json` 供前端圖表即時調用。
*   **視覺化圖表**：整合 Highcharts，展示熱門課程、月份分佈、認證統計等趨勢圖。
*   **課程管理系統**：
    *   課程搜尋與分頁。
    *   標籤化分類（認證、專業課程、養成班）。
    *   校區與領域 (Series) 關聯查詢。
*   **容器化部署**：完整的 Dockerfile 與 Docker-compose 配置，支援 NAS 與伺服器快速部署。

## 🛠️ 技術棧

*   **Backend**: Python 3.12, Django, Pandas, Django REST Framework.
*   **Package Manager**: `uv` (Astral).
*   **Frontend**: Semantic UI, Highcharts, jQuery.
*   **Database**: PostgreSQL.
*   **Server**: uWSGI (整合靜態檔案管理).

## 📂 專案結構

```text
├── apps/iiiedu/          # Django App (核心業務邏輯)
│   ├── management/      # 自定義指令 (數據導入與分析)
│   ├── models.py        # 課程、標籤、校區等資料模型
│   └── views.py         # 圖表與課程展示視圖
├── config/              # Django 專案全域配置
├── data/
│   ├── raw/             # 原始 Excel 數據存放處 (已 GitIgnore)
│   └── static/          # 生產環境靜態檔案
├── static/              # 前端資源 (JS, CSS, Themes, Chart JSON)
└── templates/           # HTML 模板
```

## ⚙️ 本地開發環境設定

### 1. 安裝 `uv` 與依賴

本專案建議使用 `uv` 進行快速開發：

```bash
# 安裝依賴並建立虛擬環境
uv sync
```

### 2. 環境變數配置

請參考 `.env.example` 建立自己的 `.env` 檔案：

```bash
cp .env.example .env
# 請編輯 .env 填入正確的 DJANGO_SECRET_KEY 與 DATABASE_URL
```

### 3. 數據導入與分析

將您的數據放入 `data/raw/iiiedu.xlsx`，然後執行：

```bash
# 執行遷移
uv run manage.py migrate

# 導入數據並更新圖表分析結果
uv run manage.py ingest_data
```

### 4. 啟動伺服器

```bash
uv run manage.py runserver
```

## 🐳 Docker / NAS 部署

我們提供了專為 NAS (或伺服器) 優化的配置：

```bash
# 使用生產環境配置啟動
docker-compose -f docker-compose-nas.yml up -d
```

啟動後，服務會自動：
1. 執行 `collectstatic` 收集靜態檔案。
2. 透過 `uWSGI` 的 `static-map` 整合靜態資源與 Django 服務於 `8001` 埠啟動。

## 🔒 安全性說明

*   `.env` 包含敏感金鑰與資料庫密碼，已排除於 Git 追蹤之外。
*   Django Admin 介面已停用以簡化系統。
*   建議在生產環境中關閉 `DEBUG=False` 並設置正確的 `ALLOWED_HOSTS`。
