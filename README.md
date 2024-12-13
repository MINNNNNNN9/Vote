# 問卷調查系統

這是一個基於 Django 開發的問卷調查系統，支持單選題和多選題，並提供結果統計功能。

## 功能特點

- 支持單選題和多選題
- 問卷結果即時統計
- 分頁顯示問卷列表
- 完整的數據驗證
- 響應式界面設計

## 技術棧

- Python 3.8+
- Django 3.2+
- SQLite3 數據庫
- Bootstrap 5 前端框架

## 安裝說明

1. 克隆項目：
```bash
git clone git@github.com:MINNNNNNN9/Vote.git
cd Questionnaire
```

2. 創建並激活虛擬環境：
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
.\venv\Scripts\activate  # Windows
```

3. 安裝依賴：
```bash
pip install -r requirements.txt
```

4. 執行數據庫遷移：
```bash
python manage.py migrate
```

5. 創建超級用戶：
```bash
python manage.py createsuperuser
```

6. 運行開發服務器：
```bash
python manage.py runserver
```

## 使用說明

1. 訪問管理後台 (http://localhost:8000/admin) 創建問卷
2. 在首頁查看所有問卷列表
3. 點擊問卷進行投票
4. 查看投票結果和統計信息

## 開發計劃

- [ ] 添加用戶認證功能
- [ ] 實現問卷導出功能
- [ ] 添加更多的單元測試
- [ ] 優化前端界面
- [ ] 添加問卷模板功能

