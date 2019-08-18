from datetime import date, timedelta
import pandas as pd
from typing import Tuple, Optional


def get_patient(file: str) -> None:

    """A function that returns the name and information of any patient who is
    due for a follow up survey – the info is represented below
    (name, mrn, email, phone number, which survey they are due for) – in case of
    missing information, the entry will appear as 'nan'.
    """
    patient_list = []
    df = pd.read_csv(file)
    for i in range(len(df)):
        survey = get_survey(file, i)
        if survey is not None:
            new_t = df['patient_name'][i], df['mrn'][i], df['email'][i],\
                df['phone_number'][i], survey
            patient_list.append(new_t)

    for patient in patient_list:
        print('{} is {} – mrn: {}, email: {}, phone: {}'.format(
            patient[0], patient[4], patient[1], patient[2], patient[3]))


def get_survey(file: str, row: int) -> Optional[str]:
    """A function that determines if a patient is due for a follow up email."""

    df = pd.read_csv(file)
    due_dates = get_due_dates(file, row)

    if due_dates is None:
        return None
    x = date.today()

    # quarter survey
    diff_25 = due_dates[0] - x
    if diff_25.days <= 0 and abs(diff_25.days) <= 30:
        if isinstance(df['qualtrics_yr025_timestamp'][row], float):
            return 'Due for 3-month survey'
    elif diff_25.days > 0 and diff_25.days <= 15:
        if isinstance(df['qualtrics_yr025_timestamp'][row], float):
            return 'Due for 3-month survey'
    # half year survey
    diff_50 = due_dates[1] - x
    if diff_50.days <= 0 and abs(diff_50.days) <= 30:
        if isinstance(df['qualtrics_yr05_timestamp'][row], float):
            return 'Due for a 6-month survey'

    elif diff_50.days > 0 and diff_50.days <= 15:
        if isinstance(df['qualtrics_yr05_timestamp'][row], float):
            return 'Due for a 6-month survey'

    # three quarter year survey
    diff_75 = due_dates[2] - x
    if diff_75.days <= 0 and abs(diff_75.days) <= 30:
        if isinstance(df['qualtrics_yr075_timestamp'][row], float):
            return 'Due for a 9-month survey'

    elif diff_75.days > 0 and diff_75.days <= 15:
        if isinstance(df['qualtrics_yr075_timestamp'][row], float):
            return 'Due for a 9-month survey'

    # year survey
    diff_1 = due_dates[3] - x
    if diff_1.days <= 0 and abs(diff_1.days) <= 60:
        if isinstance(df['qualtrics_yr1_timestamp'][row], float):
            return 'Due for a 1-year survey'

    elif diff_1.days > 0 and diff_1.days <= 15:
        if isinstance(df['qualtrics_yr1_timestamp'][row], float):
            return 'Due for a 1-year survey'

    # year and half survey
    diff_15 = due_dates[4] - x
    if diff_15.days <= 0 and abs(diff_15.days) <= 60:
        if isinstance(df['qualtrics_yr15_timestamp'][row], float):
            return 'Due for a 1.5-year survey'

    elif diff_15.days > 0 and diff_15.days <= 30:
        if isinstance(df['qualtrics_yr15_timestamp'][row], float):
            return 'Due for a 1.5-year survey'

    # 2 year survey
    diff_2 = due_dates[5] - x
    if diff_2.days <= 0 and abs(diff_2.days) <= 180:
        if isinstance(df['qualtrics_yr2_timestamp'][row], float):
            return 'Due for a 2-year survey'

    elif diff_2.days > 0 and abs(diff_2.days) <= 30:
        if isinstance(df['qualtrics_yr2_timestamp'][row], float):
            return 'Due for a 2-year survey'

    # 5 year survey
    diff_5 = due_dates[6] - x
    if diff_5.days <= 0 and abs(diff_5.days) <= 180:
        if isinstance(df['qualtrics_yr5_timestamp'][row], float):
            return 'Due for a 5-year survey'

    elif diff_5.days > 0 and diff_5.days <= 60:
        if isinstance(df['qualtrics_yr5_timestamp'][row], float):
            return 'Due for a 5-year survey'

    # 10 year survey
    diff_10 = due_dates[7] - x
    if diff_10.days <= 0 and abs(diff_10.days) <= 180:
        if isinstance(df['qualtrics_yr10_timestamp'][row], float):
            return 'Due for a 10-year survey'

    elif diff_10.days > 0 and diff_10.days <= 60:
        if isinstance(df['qualtrics_yr10_timestamp'][row], float):
            return 'Due for a 10-year survey'

    return None


def get_due_dates(file: str, row: int) -> Optional[Tuple]:
    """A function that returns the due dates for each survey for a respective
    patient. None is returned if patient has no initial survey data"""

    df = pd.read_csv(file)
    s_d = df['initial_sur_complete_date'][row]
    if not isinstance(s_d, float):
        t_d = s_d.split('/')
        initial_date = date(int('20' + t_d[2]), int(t_d[0]), int(t_d[1]))
        q_25 = initial_date + timedelta(days=90) # ask khalid if this is fine
        q_50 = initial_date + timedelta(days=180)
        q_75 = initial_date + timedelta(days=270)
        q_1 = initial_date + timedelta(days=360)
        q_15 = initial_date + timedelta(days=540)
        q_2 = initial_date + timedelta(days=720)
        q_5 = initial_date + timedelta(days=1800)
        q_10 = initial_date + timedelta(days=3600)

        return q_25, q_50, q_75, q_1, q_15, q_2, q_5, q_10

    return None


if __name__ == '__main__':
    FILE_NAME = ''
    get_patient(FILE_NAME)

