from datetime import date, timedelta


def generate_formated_date(date, format):
    return date.strftime(format)


def generate_date_range():
    today = date.today()
    is_monday = today.weekday() == 0    
    inicial_date = today - timedelta(days= 3) if is_monday else today - timedelta(days= 1)
    end_date = today - timedelta(days= 1)
    return inicial_date, end_date






