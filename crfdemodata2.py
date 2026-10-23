import calendar
from datetime import datetime
import os
import time
import pandas as pd
DEMO_FILE = "/storage/emulated/0/Download/demographics_inventory.csv"
DEMO_COLUMNS = ["PROTOCOL NUMBER","SITE NUMBER","INVESTIGATOR","DATE OF INVESTIGATION","SUBJECT ID","SCREENING NUMBER","ENROLLMENT DATE","NAME OF CANDIDATE","DOB","AGE","GENDER","CONTACT NUMBER","DIABETES","ALLERGY","CARDIAC DISEASE","SMOKING","ALCOHOL","OTHERS ADDICTIONS"]
def clear_screen( ):
    os.system("clear")
def calculate_exact_age(dob_str, inv_date_str):
    try:
        dob = datetime.strptime(dob_str.strip(), "%d/%m/%Y").date()
        inv_date = datetime.strptime(inv_date_str.strip(), "%d/%m/%Y").date()
        if inv_date < dob:
            return "Invalid Date (DOB > Inv Date)"
        years = inv_date.year - dob.year
        months = inv_date.month - dob.month
        days = inv_date.day - dob.day
        if days < 0:
            months -= 1
            prev_month = inv_date.month - 1 if inv_date.month > 1 else 12
            prev_year = inv_date.year if inv_date.month > 1 else inv_date.year - 1
            _, days_in_prev_month = calendar.monthrange(prev_year, prev_month)
            days += days_in_prev_month
        if months < 0:
            years -= 1
            months += 12
        return f"{years}Y {months}M {days}D"
    except Exception:
        return "N/A"
def load_demo_db():
    if os.path.exists(DEMO_FILE):
        try:
            return pd.read_csv(DEMO_FILE, dtype=str)
        except Exception:
            return pd.DataFrame(columns=DEMO_COLUMNS, dtype=str)
    return pd.DataFrame(columns=DEMO_COLUMNS, dtype=str)
def collect_demographics():
    demo_df = load_demo_db()
    print("=" * 60)
    print(" 1. DEMOGRAPHIC DATA COLLECTION ")
    print("=" * 60)
    protocol_number = input("Enter Protocol Number :- ").strip()
    site_number = input("Enter Site Number :- ").strip()
    investigator = input("Enter Investigator Name :- ").strip()
    inv_date = input(
        "Enter Date of Investigation (DD/MM/YYYY) :- "
    ).strip()
    subject_id = input("Enter Subject ID :- ").strip()
    screening_number = input("Enter Screening Number :- ").strip()
    enrollment_date = input("Enter Enrollment Date (DD/MM/YYYY) :- ").strip()
    candidate_name = input("Enter Name of Candidate :- ").strip()
    dob = input("Enter Date of Birth (DD/MM/YYYY) :- ").strip()
    age = calculate_exact_age(dob, inv_date)
    print(f"Auto-Calculated Age :- {age}")
    gender = input("Enter Gender [MALE/FEMALE/OTHER] :- ").strip()
    contact_number = input("Enter Contact Number :- ").strip()
    print("=" *60)
    print("2.CLINICAL & STATISTICAL DATA COLLECTION ")
    diabetes = input("Enter details of Diabetes:- ").strip()
    allergy = input("Enter allergy details:- ").strip()
    cardiac = input("Enter CARDIAC DISEASE details:- ").strip()
    print("3.Enter social details")
    smoking = input("Enter Smoking details:- ").strip()
    alcohol = input("Enter Alcohol Consumption details:- ").strip()
    addictions = input("Enter Others Addictions details:- ").strip()
    demo_df = demo_df.astype(str)
    # Check for existing record to update or append
    if (
        not demo_df.empty
        and protocol_number.lower()
        in demo_df["PROTOCOL NUMBER"].str.lower().values
    ):
        idx = demo_df[
            demo_df["PROTOCOL NUMBER"].str.lower() == protocol_number.lower()
        ].index[0]
        demo_df.at[idx, "SITE NUMBER"] = site_number
        demo_df.at[idx, "INVESTIGATOR"] = investigator
        demo_df.at[idx, "DATE OF INVESTIGATION"] = inv_date
        demo_df.at[idx, "SUBJECT ID"] = subject_id
        demo_df.at[idx, "SCREENING NUMBER"] = screening_number
        demo_df.at[idx, "ENROLLMENT DATE"] = enrollment_date
        demo_df.at[idx, "NAME OF CANDIDATE"] = candidate_name
        demo_df.at[idx, "DOB"] = dob
        demo_df.at[idx, "AGE"] = age
        demo_df.at[idx, "GENDER"] = gender
        demo_df.at[idx, "CONTACT NUMBER"] = contact_number
        demo_df.at[idx, "DIABETES"]=diabetes
        demo_df.at[idx, "ALLERGY"]=allergy
        demo_df.at[idx, "CARDIAC DISEASE"]=cardiac
        demo_df.at[idx, "SMOKING"]=smoking
        demo_df.at[idx, "ALCOHOL"]=alcohol
        demo_df.at[idx, "OTHERS ADDICTION"]=addictions
    else:
        new_row = pd.DataFrame(
            [
                {
                    "PROTOCOL NUMBER": protocol_number,
                    "SITE NUMBER": site_number,
                    "INVESTIGATOR": investigator,
                    "DATE OF INVESTIGATION": inv_date,
                    "SUBJECT ID": subject_id,
                    "SCREENING NUMBER": screening_number,
                    "ENROLLMENT DATE": enrollment_date,
                    "NAME OF CANDIDATE": candidate_name,
                    "DOB": dob,
                    "AGE": age,
                    "GENDER": gender,
                    "CONTACT NUMBER": contact_number,
                    "DIABETES": diabetes,
                    "ALLERGY": allergy,
                    "CARDIAC DISEASE": cardiac,
                    "SMOKING": smoking,
                    "ALCOHOL": alcohol,
                    "OTHERS ADDICTIONS": addictions,
                }
            ],
            dtype=str,
        )
        demo_df = pd.concat([demo_df, new_row], ignore_index=True)
    demo_df.to_csv(DEMO_FILE, index=False)
    # Return key fields to pass automatically into Module 2
    return protocol_number, age, gender
    time.sleep(2)
    clear_screen( )
    