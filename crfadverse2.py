import os
import pandas as pd
import time
def clear_screen( ):
    os.system("clear")
AE_FILE = "/storage/emulated/0/Download/adverse_events_inventory.csv"
AE_COLUMNS = ["PROTOCOL NUMBER","AE_STATUS","DESCRIPTION OF ADVERSE EFFECT","DATE OF ONSET","SEVERITY","ACTION TAKEN","OUTCOME","MEDICINE GIVEN","MEDICINE START DATE","MEDICINE END DATE","FREQUENCY",]
def load_ae_db():
    if os.path.exists(AE_FILE):
        try:
            return pd.read_csv(AE_FILE, dtype=str)
        except Exception:
            return pd.DataFrame(columns=AE_COLUMNS, dtype=str)
    return pd.DataFrame(columns=AE_COLUMNS, dtype=str)
def collect_adverse_events(protocol_number):
    ae_df = load_ae_db()
    print("=" * 60)
    print(" 4. ADVERSE EFFECTS & MEDICATIONS LOG ")
    print("=" * 60)
    print(f"Protocol Number :- {protocol_number}")
    # Remove any existing records for this protocol number to allow fresh updates
    if not ae_df.empty:
        ae_df = ae_df[
            ae_df["PROTOCOL NUMBER"].astype(str).str.strip().str.lower()
            != str(protocol_number).strip().lower()
        ]
    has_ae = (input("Is any adverse effect happened? [Yes/No] :- ").strip().lower())
    new_rows = []
    if has_ae in ["yes", "y"]:
        ae_counter = 1
        while True:
            print(f"\n--- Adverse Effect Entry #{ae_counter} ---")
            ae_desc = input("1. Description of Adverse Effect :- ").strip()
            date_onset = input("2. Date of Onset (DD/MM/YYYY) :- ").strip()
            severity = input("3. Severity [Mild/Moderate/Severe] :- ").strip()
            action_taken = input("4. Action Taken :- ").strip()
            outcome = input("5. Outcome [Resolved/Ongoing/Recovered with sequelae] :- ").strip()
            med_given = input("6. Medicine Given :- ").strip()
            med_start = input("7. Medicine Start Date (DD/MM/YYYY) :- ").strip()
            med_end = input("8. Medicine End Date (DD/MM/YYYY) :- ").strip()
            frequency = input("9. Frequency [e.g., OD, BD, TDS, QID] :- ").strip()
            new_rows.append({"PROTOCOL NUMBER": protocol_number,"AE_STATUS": "YES","DESCRIPTION OF ADVERSE EFFECT": ae_desc,"DATE OF ONSET": date_onset,"SEVERITY": severity,"ACTION TAKEN": action_taken,"OUTCOME": outcome,"MEDICINE GIVEN": med_given,"MEDICINE START DATE": med_start,"MEDICINE END DATE": med_end,"FREQUENCY": frequency,})
            ae_counter += 1
            cont = (input("\nPress Enter to add another adverse effect, or type 'end' to finish :- ").strip().lower())
            if cont == "end":
                break
    else:
        # Logging "No adverse effect" row
        new_rows.append({"PROTOCOL NUMBER": protocol_number,"AE_STATUS": "NO","DESCRIPTION OF ADVERSE EFFECT": "No adverse effect","DATE OF ONSET": "N/A","SEVERITY": "N/A","ACTION TAKEN": "N/A","OUTCOME": "N/A","MEDICINE GIVEN": "N/A","MEDICINE START DATE": "N/A","MEDICINE END DATE": "N/A","FREQUENCY": "N/A",})
        print(" Logged 'No adverse effect' for this protocol.")
    # Append new records to DataFrame and save to CSV
    updated_df = pd.concat(
        [ae_df, pd.DataFrame(new_rows, dtype=str)], ignore_index=True
    )
    updated_df.to_csv(AE_FILE, index=False)
    time.sleep(2)
    clear_screen( )
    