import os
import time
import pandas as pd
def clear_screen( ):
    os.system("clear")
CLINICAL_FILE = "/storage/emulated/0/Download/clinical_inventory.csv"
CLINICAL_COLUMNS = ["PROTOCOL NUMBER","VISIT_STATUS","VISIT_NUMBER","DATE","BLOOD PRESSURE","PULSE","TEMPERATURE","REMARKS",]
def load_clinical_db():
    if os.path.exists(CLINICAL_FILE):
        try:
            return pd.read_csv(CLINICAL_FILE, dtype=str)
        except Exception:
            return pd.DataFrame(columns=CLINICAL_COLUMNS, dtype=str)
    return pd.DataFrame(columns=CLINICAL_COLUMNS, dtype=str)
def collect_clinical(protocol_number, age=None, gender=None):
    clinical_df = load_clinical_db()
    print( "=" * 60)
    print(" 2. CLINICAL VISITS LOG ")
    print("=" * 60)
    print(f"1. Protocol Number:- {protocol_number}")
    # Remove any existing records for this protocol number to allow fresh updates
    if not clinical_df.empty and "PROTOCOL NUMBER" in clinical_df.columns:
        clinical_df = clinical_df[
            clinical_df["PROTOCOL NUMBER"].astype(str).str.strip().str.lower()
            != str(protocol_number).strip().lower()
        ]
    has_visit = (
        input("\nIs any clinical visit come? [Yes/No] :- ").strip().lower()
    )
    new_rows = []
    if has_visit in ["yes", "y"]:
        visit_counter = 1
        while True:
            print(f"\n--- Data at Visit #{visit_counter} ---")
            visit_date = input("1. Date (DD/MM/YYYY) :- ").strip()
            bp = input("2. Blood Pressure:- ").strip()
            pulse = input("3. Pulse :- ").strip()
            temp = input("4. Temperature  :- ").strip()
            remarks = input("5. Remarks :- ").strip()
            new_rows.append({"PROTOCOL NUMBER": protocol_number,"VISIT_STATUS": "YES","VISIT_NUMBER": f"Visit {visit_counter}","DATE": visit_date,"BLOOD PRESSURE": bp,"PULSE": pulse,"TEMPERATURE": temp,"REMARKS": remarks,})
            visit_counter += 1
            cont = (input("Press Enter to add another visit, or type 'done' to finish :- ").strip().lower())
            if cont == "done":
                break
    else:
        # Logging "NO VISIT" row
        new_rows.append({"PROTOCOL NUMBER": protocol_number,"VISIT_STATUS": "NO","VISIT_NUMBER": "N/A","DATE": "N/A","BLOOD PRESSURE": "N/A","PULSE": "N/A","TEMPERATURE": "N/A","REMARKS": "NO VISIT",})
        print("\nLogged 'NO VISIT' for this protocol.")
    # Save to CSV inventory
    updated_df = pd.concat(
        [clinical_df, pd.DataFrame(new_rows, dtype=str)], ignore_index=True
    )
    updated_df.to_csv(CLINICAL_FILE, index=False)
    time.sleep(2)
    clear_screen( )
