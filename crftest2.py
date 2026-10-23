import os
import time
import pandas as pd
def clear_screen( ):
    os.system("clear")
LAB_TEST_FILE = "/storage/emulated/0/Download/lab_test_inventory.csv"
LAB_TEST_COLUMNS = [
    "PROTOCOL NUMBER","HAEMOGLOBIN_RANGE","HAEMOGLOBIN_VALUE","HAEMOGLOBIN_STATUS","WBC_RANGE","WBC_VALUE","WBC_STATUS","PLATELET_RANGE","PLATELET_VALUE","PLATELET_STATUS","RBC_RANGE","RBC_VALUE","RBC_STATUS","GLUCOSE_RANGE","GLUCOSE_VALUE","GLUCOSE_STATUS","BILIRUBIN_RANGE","BILIRUBIN_VALUE","BILIRUBIN_STATUS",]
def load_lab_test_db():
    if os.path.exists(LAB_TEST_FILE):
        try:
            return pd.read_csv(LAB_TEST_FILE, dtype=str)
        except Exception:
            return pd.DataFrame(columns=LAB_TEST_COLUMNS, dtype=str)
    return pd.DataFrame(columns=LAB_TEST_COLUMNS, dtype=str)
def evaluate_parameter(param_name):
    print(f"\n--- {param_name} ---")
    normal_range = input(f"Enter Normal Range for {param_name} :- ").strip()
    obs_value = input(f"Enter Observed Test Value for {param_name} :- ").strip()
    status = "NORMAL"
    try:
        val = float(obs_value)
        if "-" in normal_range:
            parts = normal_range.split("-")
            min_v = float(parts[0].strip())
            max_v = float(parts[1].strip())
            if val < min_v:
                status = "LOW"
            elif val > max_v:
                status = "HIGH"
            else:
                status = "NORMAL"
        elif normal_range.startswith("<"):
            max_v = float(normal_range.replace("<", "").strip())
            status = "HIGH" if val > max_v else "NORMAL"
        elif normal_range.startswith(">"):
            min_v = float(normal_range.replace(">", "").strip())
            status = "LOW" if val < min_v else "NORMAL"
    except ValueError:
        # Fallback manual input if range format is custom text
        status = (input(f"Could not auto-evaluate. Enter Status for {param_name} [HIGH/LOW/NORMAL] :- ").strip().upper())
    print(f"Evaluated Status: {status}")
    return normal_range, obs_value, status
def collect_lab_tests(protocol_number):
    lab_df = load_lab_test_db()
    print("\n" + "=" * 60)
    print(" 3. LABORATORY TEST REPORTS COLLECTION ")
    # Collect 6 parameters with range & auto-status evaluation
    hb_range, hb_val, hb_status = evaluate_parameter("HAEMOGLOBIN")
    wbc_range, wbc_val, wbc_status = evaluate_parameter("WBC COUNT")
    plt_range, plt_val, plt_status = evaluate_parameter("PLATELET COUNT")
    rbc_range, rbc_val, rbc_status = evaluate_parameter("RBC COUNT")
    glu_range, glu_val, glu_status = evaluate_parameter("GLUCOSE LEVEL")
    bil_range, bil_val, bil_status = evaluate_parameter("BILIRUBIN LEVEL")
    row_data = {
        "PROTOCOL NUMBER": protocol_number,
        "HAEMOGLOBIN_RANGE": hb_range,
        "HAEMOGLOBIN_VALUE": hb_val,
        "HAEMOGLOBIN_STATUS": hb_status,
        "WBC_RANGE": wbc_range,
        "WBC_VALUE": wbc_val,
        "WBC_STATUS": wbc_status,
        "PLATELET_RANGE": plt_range,
        "PLATELET_VALUE": plt_val,
        "PLATELET_STATUS": plt_status,
        "RBC_RANGE": rbc_range,
        "RBC_VALUE": rbc_val,
        "RBC_STATUS": rbc_status,
        "GLUCOSE_RANGE": glu_range,
        "GLUCOSE_VALUE": glu_val,
        "GLUCOSE_STATUS": glu_status,
        "BILIRUBIN_RANGE": bil_range,
        "BILIRUBIN_VALUE": bil_val,
        "BILIRUBIN_STATUS": bil_status,
    }
    lab_df = lab_df.astype(str)
    if (
        not lab_df.empty
        and protocol_number.lower()
        in lab_df["PROTOCOL NUMBER"].str.lower().values
    ):
        idx = lab_df[
            lab_df["PROTOCOL NUMBER"].str.lower() == protocol_number.lower()
        ].index[0]
        for col, val in row_data.items():
            lab_df.at[idx, col] = val
    else:
        new_row = pd.DataFrame([row_data], dtype=str)
        lab_df = pd.concat([lab_df, new_row], ignore_index=True)
    lab_df.to_csv(LAB_TEST_FILE, index=False)
    time.sleep(2)
    clear_screen( )