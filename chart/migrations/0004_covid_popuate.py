
"""
DB 현행화 작업이 실행될 때, csv 파일 자료를 DB에 자동적으로 적재한다.
"""
import csv
import os
from django.db import migrations
from django.conf import settings


Date = 0
Country = 1
Confirmed = 2
Recovered = 3
Deaths = 4


def add_Covid(apps, schema_editor):
    Covid = apps.get_model('chart', 'Covid')  # (app_label, model_name)
    csv_file = os.path.join(settings.BASE_DIR, 'covid.csv')
    with open(csv_file) as dataset:                   # 파일 객체 dataset
        reader = csv.reader(dataset)                    # 파일 객체 dataset에 대한 판독기 획득
        next(reader)  # ignore first row (headers)      # __next__() 호출 때마다 한 라인 판독
        for entry in reader:                            # 판독기에 대하여 반복 처리
            Covid.objects.create(   # DB 행 생성
                Date=entry[Date],
                Country=entry[Country],
                Confirmed=entry[Confirmed],
                Recovered=entry[Recovered],        # int()로 변환하고, 다시 bool()로 변환
                Deaths=entry[Deaths]
            )

class Migration(migrations.Migration):
    dependencies = [                            # 선행 관계
        ('chart', '0003_covid'),         # app_label, preceding migration file
    ]
    operations = [                              # 작업
        migrations.RunPython(add_Covid),   # add_passengers 함수를 호출
    ]