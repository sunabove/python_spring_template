from datetime import datetime, timedelta

def get_yesterday_date():
    today = datetime.today()
    yesterday = today - timedelta(days=1)
    return yesterday.strftime('%y%m%d')

# 실행
print(get_yesterday_date())
