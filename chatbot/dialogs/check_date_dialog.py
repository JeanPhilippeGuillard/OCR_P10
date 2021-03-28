import datetime as dt

def check_date_is_past(date_str):
    """
    Check that the date provided by user is not in the past
    """
    try :
        date = dt.datetime.strptime(date_str, "%Y-%m-%d")
        return date < (dt.datetime.today() - dt.timedelta(days=1))
    except Exception as error:
        print("Exception")
        return False

def check_dpt_before_rtn_date(dpt_date_str, rtn_date_str):
    try:
        dpt_date = dt.datetime.strptime(dpt_date_str, "%Y-%m-%d")
        rtn_date = dt.datetime.strptime(rtn_date_str, "%Y-%m-%d")
        return rtn_date < dpt_date
    except Exception as error:
        return False

"""dep_date = "2021-03-27"
rtn_date = "2021-03-26"
print(check_date_past(dep_date))
print(check_dpt_rtn_date(dep_date, rtn_date))"""