"""# 1.Data Discovery

## Bagian 1 - Import Library"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.model_selection import cross_val_score

"""## Bagian 2 - Load Dataset

### Load users.csv"""

user = pd.read_csv('users.csv')
user.head()

"""### Load assets.csv"""

asset = pd.read_csv('assets.csv')
asset.head()

"""### Load sample_stream_events.csv"""

stream_event = pd.read_csv('sample_stream_events.csv')
stream_event.head()

"""## Bagian 3 - Data Discovery"""

"""### 1. Cek Struktur Data (Schema dan Jumlah Baris)"""
print(user.info())
print(asset.info())
print(stream_event.info())

"""### 2. Cek Missing Value"""

print(user.isnull().sum())
print(asset.isnull().sum())
print(stream_event.isnull().sum())

"""### 3. Cek Data Duplikat event_id"""

duplicate_count = stream_event['event_id'].duplicated().sum()
print("Jumlah duplicate event_id:", duplicate_count)

"""### 4. Statistik Deskriptif"""

print(stream_event.describe())

"""### 5. Distribusi Action"""

stream_event['action'].value_counts().plot(kind='bar')
plt.title('Distribusi Action')
plt.show()

"""### 6. Distribusi Status"""

stream_event['status'].value_counts().plot(kind='bar')
plt.title('Distribusi Status')
plt.show()

"""### 7. Distribusi Classification"""

stream_event['data_classification'].value_counts().plot(kind='bar')
plt.title('Distribusi Klasifikasi')
plt.show()

"""### 8. Top User"""

stream_event['user_id'].value_counts().head(5).plot(kind='bar')
plt.title('Top User')
plt.show()

"""### 9. Top Used Assets"""

stream_event['asset_id'].value_counts().head(5).plot(kind='bar')
plt.title('Top used Assets')
plt.show()

"""## Bagian 4 - Data Dictionary

| No. | Nama Kolom | Tipe Data | Deskripsi |
|:--- | :--- | :---: | :--- |
|1. | event_id | string | identitas unik yang dimiliki oleh event |
|2. | event_time | datetime | waktu terjadinya event untuk analisis kronologi aktivitas |
|3. | user_id | string | identitas unik yang dimiliki oleh setiap pengguna yang melakukan aktivitas |
|4. | dept | string | departemen tempat kerja pengguna |
|5. | role | string | jabatan pengguna yang menentukan hak akses dalam sistem |
|6. | device_type | string | jenis perangkat yang digunakan untuk mengakses sistem |
|7. | source_ip | string | alamat ip pengguna saat mengakses sistem |
|8. | asset_id | string | identitas jenis aset yang diakses pengguna |
|9. | asset_type | string | jenis aset yang diakses |
|10. | event_id | string | identitas unik yang dimiliki oleh event |
|11. | data_classification | string | tingkat klasfikasi data yang diakses |
|12. | action | string | jenis aktivitas yang dilakukan pengguna |
|13. | status | string | status hasil dari aktivitas |
|14. | bytes_out | integer | jumlah data yang ditransfer keluar dari sistem |
|15. | records_accessed | integer | jumlah data yang diakses dalam 1 aktivitas |
|16. | latency_ms | float | waktu sistem merespon terhadap aktivitas pengguna |
|17. | risk_score | float | skor risiko yang menunjukkan seberapa tinggi ancaman tindakan terhadap sistem |
|18. | label | string | kategori akhir suatu aktivitas |
"""

user.columns

asset.columns

stream_event.columns

"""# 2. Data Science

## Bagian 1 - Merge Dataset
Gabungkan stream_event dengan user
"""

merged = stream_event.merge(
    user,
    on = 'user_id',
    how = 'left'
)
merged.head()

"""## Bagian 2 - Membuat fitur analitik"""

event_per_user = merged.groupby('user_id').size().reset_index(name='event_count')
event_per_user.head()

failed_login_rate = merged[merged['status_x'] == 'failed'].groupby('user_id').size().reset_index(name='failed_login_count')
failed_login_rate.head()

total_bytes_out = merged.groupby('user_id')['bytes_out'].sum().reset_index(name='total_bytes_out')
total_bytes_out.head()

access_to_restricted_ratio = merged[merged['data_classification'] == 'restricted'].groupby('user_id').size().reset_index(name='access_to_restricted_count')
access_to_restricted_ratio.head()

avg_latency = merged.groupby('user_id')['latency_ms'].mean().reset_index(name='avg_latency_ms')
avg_latency.head()

merged = stream_event.merge(
    user,
    on = 'user_id',
    how = 'left'
)

features = (
    event_per_user
    .merge(failed_login_rate, on='user_id', how='left')
    .merge(total_bytes_out, on='user_id', how='left')
    .merge(access_to_restricted_ratio, on='user_id', how='left')
    .merge(avg_latency, on='user_id', how='left')
)

features = features.fillna(0)

merged = merged.merge(
    features,
    on='user_id',
    how='left'
)
merged.head()

"""## Bagian 3 - EDA dengan Visualisasi

### 1. Distribusi Label Event
"""

stream_event['label'].value_counts().plot(
    kind='pie',
    autopct='%1.1f%%'
)
plt.ylabel('')
plt.title('Distribusi Label')
plt.show()

"""### 2. Distribusi Risk Score"""

plt.hist(stream_event['risk_score'], bins=20)
plt.title('Distribusi Risk Score')
plt.xlabel('Risk Score')
plt.ylabel('Frekuensi')
plt.show()

"""### 3. Boxplot Risk Score berdasarkan Label"""

sns.boxplot(
    data=stream_event,
    x='label',
    y='risk_score'
)
plt.xticks(rotation=90)
plt.title('Risk Score berdasarkan Label')
plt.show()

"""### 4. Persebaran Risk Score berdasarkan Bytes Out"""

plt.scatter(
    stream_event['bytes_out'],
    stream_event['risk_score']
)

plt.xlabel('Bytes Out')
plt.ylabel('Risk Score')
plt.title('Bytes Out vs Risk Score')
plt.show()

"""## Bagian 4 - Model Deteksi Anomali / Klasifikasi"""

X = merged[
[
'event_count',
'failed_login_count',
'total_bytes_out',
'access_to_restricted_count',
'avg_latency_ms'
]
]

y = merged['label']

X_train,X_test,y_train,y_test = train_test_split(
    X,y,
    test_size=0.2,
    random_state=42
)

rf = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

rf.fit(X_train,y_train)

y_pred = rf.predict(X_test)

"""## Bagian 5 - Evaluasi"""

from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
import matplotlib.pyplot as plt

# Prediksi data test
y_pred = rf.predict(X_test)

# Confusion Matrix
cm = confusion_matrix(y_test, y_pred)

# Visualisasi
disp = ConfusionMatrixDisplay(
    confusion_matrix=cm,
    display_labels=rf.classes_
)

disp.plot(cmap='Blues')
plt.title('Confusion Matrix - Random Forest')
plt.xticks(rotation=90)
plt.show()

print(classification_report(y_test,y_pred))

scores = cross_val_score(
    rf,
    X,
    y,
    cv=5,
    scoring='f1_macro'
)

print(scores)
print("Mean F1 Macro:", scores.mean())

"""# 3. Data Security

## Bagian 1 - Menemukan pola risiko

### 1. Akses dari Terminated User (Inactive User)
"""

risk1 = merged[merged['status_y'] != 'active']

"""### 2. Download Besar dari Data Confidental / Restricted"""

risk2 = merged[
    (merged['data_classification'].isin(['confidential','restricted'])) &
    (merged['bytes_out'] > merged['bytes_out'].quantile(0.95))
]

"""### 3. Permision change dari IP eksternal"""

risk3 = merged[
    (merged['action'] == 'permission_change')
]

"""## Bagian 2 - Membuat Security_Alert"""

def security_alert(event):

  #CRITICAL
  if (event['label'] in ['exfiltration_suspected', 'privilege_abuse']
      or event['risk_score'] >= 90
  ):
      return 'CRITICAL'

  #HIGH
  elif (event['data_classification'] in ['confidential', 'restricted']
        and event['bytes_out'] > 100000
  ):
      return 'HIGH'

  #MEDIUM
  elif (event['failed_login_count'] >= 3
        or event['risk_score'] >= 60
  ):
      return 'MEDIUM'

  #LOW
  else:
    return 'LOW'

"""## Bagian 3 - Memuat stream_generator.py"""

# Commented out IPython magic to ensure Python compatibility.
# %%writefile stream_generator.py
# 
# import argparse
# import json
# import random
# import time
# from datetime import datetime, timedelta
# 
# DEPTS = [
#     'Finance', 'HR', 'Engineering', 'Sales',
#     'Legal', 'Data Science', 'Operations'
# ]
# 
# ROLES = [
#     'analyst', 'manager', 'engineer',
#     'director', 'intern', 'admin'
# ]
# 
# DEVICES = [
#     'laptop', 'mobile', 'workstation',
#     'server', 'vpn_gateway'
# ]
# 
# ASSETS = [
#     ('cust_db', 'database', 'restricted'),
#     ('payroll', 'database', 'confidential'),
#     ('crm', 'saas', 'confidential'),
#     ('data_lake', 'storage', 'restricted'),
#     ('git_repo', 'code', 'internal'),
#     ('bi_dashboard', 'dashboard', 'internal'),
#     ('public_web', 'web', 'public'),
#     ('ticketing', 'saas', 'internal')
# ]
# 
# 
# def build_users(n=150, seed=42):
# 
#     random.seed(seed)
# 
#     users = []
# 
#     for i in range(1, n + 1):
# 
#         users.append({
#             'user_id': f'U{i:04d}',
#             'dept': random.choice(DEPTS),
#             'role': random.choice(ROLES),
#             'clearance': random.choice(
#                 ['public', 'internal', 'confidential', 'restricted']
#             ),
#             'status': random.choices(
#                 ['active', 'terminated'],
#                 weights=[95, 5]
#             )[0]
#         })
# 
#     for idx in [6, 22, 79]:
#         if idx < len(users):
#             users[idx]['status'] = 'terminated'
# 
#     return users
# 
# 
# def event_stream(total=1000, seed=42):
# 
#     random.seed(seed)
# 
#     users = build_users(seed=seed)
# 
#     start = datetime.now().replace(microsecond=0)
# 
#     for n in range(1, total + 1):
# 
#         u = random.choice(users)
# 
#         asset = random.choice(ASSETS)
# 
#         action = random.choices(
#             [
#                 'login',
#                 'logout',
#                 'read',
#                 'query',
#                 'download',
#                 'upload',
#                 'delete',
#                 'permission_change',
#                 'schema_discovery'
#             ],
#             weights=[22, 8, 25, 18, 10, 6, 2, 1, 1]
#         )[0]
# 
#         bytes_out = max(
#             0,
#             int(random.gauss(80000, 50000))
#         )
# 
#         src = f"10.10.{random.randint(1,20)}.{random.randint(2,254)}"
# 
#         status = random.choices(
#             ['success', 'failed'],
#             weights=[90, 10]
#         )[0]
# 
#         risk = 0
# 
#         if u['status'] == 'terminated':
#             risk += 45
# 
#         if action in ['delete', 'permission_change']:
#             risk += 25
# 
#         if (
#             asset[2] in ['restricted', 'confidential']
#             and u['clearance'] in ['public', 'internal']
#         ):
#             risk += 25
# 
#         if bytes_out > 200000:
#             risk += 10
# 
#         label = 'normal'
# 
#         # Exfiltration
#         if n in range(
#             int(total * 0.20),
#             int(total * 0.20) + 20
#         ):
# 
#             u = users[22]
# 
#             asset = (
#                 'payroll',
#                 'database',
#                 'confidential'
#             )
# 
#             action = 'download'
# 
#             bytes_out = random.randint(
#                 5_000_000,
#                 10_000_000
#             )
# 
#             src = '185.220.101.2'
# 
#             status = 'success'
# 
#             risk = 95
# 
#             label = 'exfiltration_suspected'
# 
#         # Compromised account
#         elif n in range(
#             int(total * 0.55),
#             int(total * 0.55) + 20
#         ):
# 
#             u = users[22]
# 
#             asset = (
#                 'cust_db',
#                 'database',
#                 'restricted'
#             )
# 
#             action = random.choice([
#                 'login',
#                 'query',
#                 'schema_discovery'
#             ])
# 
#             bytes_out = random.randint(
#                 100_000,
#                 1_000_000
#             )
# 
#             src = '45.77.21.13'
# 
#             status = random.choice([
#                 'failed',
#                 'success'
#             ])
# 
#             risk = 85
# 
#             label = 'compromised_account'
# 
#         # Privilege abuse
#         elif n in range(
#             int(total * 0.80),
#             int(total * 0.80) + 15
#         ):
# 
#             u = users[79]
# 
#             asset = (
#                 'git_repo',
#                 'code',
#                 'internal'
#             )
# 
#             action = 'permission_change'
# 
#             bytes_out = 0
# 
#             src = '103.12.44.9'
# 
#             status = 'success'
# 
#             risk = 90
# 
#             label = 'privilege_abuse'
# 
#         elif risk >= 60:
# 
#             label = 'policy_violation'
# 
#         yield {
# 
#             'event_id': f'EVT{n:07d}',
# 
#             'event_time':
#                 (start + timedelta(seconds=n * 10))
#                 .isoformat(),
# 
#             'user_id': u['user_id'],
# 
#             'dept': u['dept'],
# 
#             'role': u['role'],
# 
#             'device_type': random.choice(
#                 DEVICES
#             ),
# 
#             'source_ip': src,
# 
#             'asset_id': asset[0],
# 
#             'asset_type': asset[1],
# 
#             'data_classification': asset[2],
# 
#             'action': action,
# 
#             'status': status,
# 
#             'bytes_out': bytes_out,
# 
#             'records_accessed':
#                 max(
#                     0,
#                     int(
#                         bytes_out /
#                         random.randint(100, 1000)
#                     )
#                 ),
# 
#             'latency_ms':
#                 max(
#                     1,
#                     int(
#                         random.gauss(120, 20)
#                     )
#                 ),
# 
#             'risk_score':
#                 min(
#                     100,
#                     risk + random.randint(0, 8)
#                 ),
# 
#             'label': label
#         }
# 
# 
# def main():
# 
#     parser = argparse.ArgumentParser()
# 
#     parser.add_argument(
#         '--events',
#         type=int,
#         default=1000
#     )
# 
#     parser.add_argument(
#         '--speed',
#         type=float,
#         default=0.0
#     )
# 
#     parser.add_argument(
#         '--out',
#         default='stream_events.jsonl'
#     )
# 
#     args = parser.parse_args()
# 
#     with open(
#         args.out,
#         'w',
#         encoding='utf8'
#     ) as f:
# 
#         for event in event_stream(args.events):
# 
#             line = json.dumps(
#                 event,
#                 ensure_ascii=False
#             )
# 
#             print(line)
# 
#             f.write(line + '\n')
# 
#             if args.speed > 0:
#                 time.sleep(args.speed)
# 
# 
# if __name__ == '__main__':
#     main()