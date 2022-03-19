資策會課程分析網頁
===

# 說明

使用scrapy進行爬取清理，最後以highchart圖表呈現在網頁，快速了解熱門課程、認證，程式語言以及主題熱門度等資訊。

# 安裝環境

1. 設置環境變數, 編輯`.example.env`改為`.env`

2. 安裝依賴
    ```
    pip install -r requirements.txt
    ```

# 如何運行

1. 同步數據庫
    
    ```
    python manage.py makemigrations
    python manage.py migrate
    ```
    
    若要操作後台, 可以建立superuser
    ```
    python manage.py createsuperuser --noinput
    ```

2. 運行腳本

    ```
    python manage.py runserver 0.0.0.0:8000
    ```


# Demo演示

https://iiiedu-jrptmn2eua-uc.a.run.app

![](https://i.imgur.com/DTkYgoe.png)

