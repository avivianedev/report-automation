from datetime import date, timedelta


def generate_formated_date(date, format):
    return date.strftime(format)


def generate_date_range():
    today = date.today()
    
    yesterday = today - timedelta(days=1)
    
    inicial_date = yesterday.replace(day=1)
    end_date = yesterday
    
    return inicial_date, end_date





