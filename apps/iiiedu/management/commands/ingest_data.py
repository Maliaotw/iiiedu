import os
import pandas as pd
from django.core.management.base import BaseCommand
from django.conf import settings
from iiiedu.models import Branch, Tag, Cate, Course

class Command(BaseCommand):
    help = '同步導入資料庫課程數據 (不覆寫圖表 JSON)'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('--- 開始執行數據庫同步 Pipeline ---'))
        
        # 1. 讀取數據 (Extract)
        file_path = os.path.join(settings.BASE_DIR, 'data', 'raw', 'iiiedu.xlsx')
        if not os.path.exists(file_path):
            self.stdout.write(self.style.ERROR(f'找不到原始數據: {file_path}'))
            return

        df = pd.read_excel(file_path)
        self.stdout.write(f'成功讀取 {len(df)} 筆原始數據。')

        # 2. 數據清洗
        df['Training_StartDate'] = pd.to_datetime(df['Training_StartDate'], errors='coerce')
        df = df.dropna(subset=['Class_Name', 'Training_StartDate'])

        # 3. 導入資料庫 (Load to DB)
        self.stdout.write('正在同步 PostgreSQL 資料庫...')
        import_count = 0
        for _, row in df.iterrows():
            branch, _ = Branch.objects.get_or_create(
                md5_address=str(row.get('md5_address', 'default')),
                defaults={
                    'city': str(row.get('city', '未知')),
                    'unit': str(row.get('unit', '資策會')),
                    'addr': str(row.get('address', '未知地址'))
                }
            )

            cate, _ = Cate.objects.get_or_create(name=str(row.get('cate', '一般')))
            tag, _ = Tag.objects.get_or_create(name=str(row.get('tag', '其他')), cate=cate)

            _, created = Course.objects.update_or_create(
                class_id=str(row.get('Class_ID')),
                defaults={
                    'name': str(row.get('Class_Name')),
                    'branch': branch,
                    'Tag': tag,
                    'mongo_id': str(row.get('Unnamed: 0', '0')),
                    'summary': str(row.get('Course_content', '無')),
                    'Price_Ownpay': int(row.get('Price_Ownpay', 0)),
                    'Training_Hours': int(row.get('Training_Hours', 0)),
                    'Training_StartDate': row['Training_StartDate'],
                    'Training_EndDate': pd.to_datetime(row.get('Training_EndDate'), errors='coerce') or row['Training_StartDate'],
                    'link': str(row.get('link', ''))
                }
            )
            if created:
                import_count += 1

        self.stdout.write(self.style.SUCCESS(f'資料庫同步完成，新增 {import_count} 筆課程。'))
        self.stdout.write(self.style.WARNING('注意：圖表數據以 static/data/iiiedu/chart_data.json 為主，本指令未進行覆寫。'))
