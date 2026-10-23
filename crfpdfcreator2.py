import os
from fpdf import FPDF
import pandas as pd
# Inventory File Paths
DEMO_FILE = "/storage/emulated/0/Download/demographics_inventory.csv"
CLINICAL_FILE = "/storage/emulated/0/Download/clinical_inventory.csv"
LAB_TEST_FILE = "/storage/emulated/0/Download/lab_test_inventory.csv"
AE_FILE = "/storage/emulated/0/Download/adverse_events_inventory.csv"
def generate_pdf_report(target_protocol=None):
    if not target_protocol:
        target_protocol = (
            input("\nEnter Protocol Number to generate PDF :- ").strip()
        )
    target_clean = str(target_protocol).strip().lower()
    # 1. Load DataFrames
    demo_df = (pd.read_csv(DEMO_FILE, dtype=str) if os.path.exists(DEMO_FILE) else pd.DataFrame())
    clinical_df = (pd.read_csv(CLINICAL_FILE, dtype=str) if os.path.exists(CLINICAL_FILE) else pd.DataFrame())
    lab_df = (pd.read_csv(LAB_TEST_FILE, dtype=str) if os.path.exists(LAB_TEST_FILE) else pd.DataFrame())
    ae_df = (pd.read_csv(AE_FILE, dtype=str) if os.path.exists(AE_FILE) else pd.DataFrame()
    )
    # 2. Clean Header Whitespace
    for df in [demo_df, clinical_df, lab_df, ae_df]:
        if not df.empty:
            df.columns = df.columns.str.strip()
    # 3. Filter Records for Target Protocol Number
    demo_match = (demo_df[demo_df["PROTOCOL NUMBER"].astype(str).str.strip().str.lower()== target_clean] if not demo_df.empty else pd.DataFrame())
    clinical_match = (clinical_df[clinical_df["PROTOCOL NUMBER"].astype(str).str.strip().str.lower()== target_clean] if not clinical_df.empty else pd.DataFrame())
    lab_match = (lab_df[lab_df["PROTOCOL NUMBER"].astype(str).str.strip().str.lower()== target_clean] if not lab_df.empty else pd.DataFrame())
    ae_match = (ae_df[ae_df["PROTOCOL NUMBER"].astype(str).str.strip().str.lower()== target_clean] if not ae_df.empty else pd.DataFrame())
    if (demo_match.empty and clinical_match.empty and lab_match.empty and ae_match.empty):
        print(f"\n No matching records found for Protocol '{target_protocol}'.")
        return
    d_row = demo_match.iloc[0] if not demo_match.empty else {}
    c_row = clinical_match.iloc[0] if not clinical_match.empty else {}
    l_row = lab_match.iloc[0] if not lab_match.empty else {}
    pdf = FPDF(orientation="P", unit="mm", format="A4")
    pdf.add_page()
    # Title Banner
    pdf.set_font("Helvetica", style="B", size=14)
    pdf.cell(0, 8, "CASE REPORT FORM(CRF)",new_x="LMARGIN", new_y="NEXT", align="C",)
    pdf.set_font("Helvetica", style="I", size=9)
    pdf.cell(0,5,"A STUDY TO EVALUATE THE SAFETY AND EFFICANCY OF A DRUG ON A PATIENT",new_x="LMARGIN",new_y="NEXT",align="C",)
    pdf.ln(4)
    def section_header(title):
        pdf.set_font("Helvetica", style="B", size=10)
        pdf.cell(0, 6, title, new_x="LMARGIN", new_y="NEXT", align="L")
        pdf.ln(1)
    # TABLE 1: Site Info
    section_header("SECTION 1: STUDY & SITE INFORMATION")
    t1_data = [
        ["PROTOCOL NUMBER","SITE NUMBER","INVESTIGATOR","DATE OF INVESTIGATION",],[
            str(d_row.get("PROTOCOL NUMBER", target_protocol)),
            str(d_row.get("SITE NUMBER", "N/A")),
            str(d_row.get("INVESTIGATOR", "N/A")),
            str(d_row.get("DATE OF INVESTIGATION", "N/A")),
        ],]
    pdf.set_font("Helvetica", size=8)
    with pdf.table() as table:
        for row in t1_data:
            r = table.row()
            for cell_val in row:
                r.cell(cell_val)
    pdf.ln(4)
    # TABLE 2: Enrollment Identifiers
    section_header("SECTION 2: SUBJECT ENROLLMENT IDENTIFIERS")
    t2_data = [
        ["SUBJECT ID", "SCREENING NUMBER", "ENROLLMENT DATE"],
        [
            str(d_row.get("SUBJECT ID", "N/A")),
            str(d_row.get("SCREENING NUMBER", "N/A")),
            str(d_row.get("ENROLLMENT DATE", "N/A")),
        ],
    ]
    pdf.set_font("Helvetica", size=8)
    with pdf.table() as table:
        for row in t2_data:
            r = table.row()
            for cell_val in row:
                r.cell(cell_val)
    pdf.ln(4)
    # TABLE 3: Demographic & Contact
    section_header("SECTION 3: DEMOGRAPHIC & CONTACT DETAILS")
    t3_data = [
        ["PARAMETER / FIELD", "RECORDED DETAILS"],
        ["NAME OF CANDIDATE", str(d_row.get("NAME OF CANDIDATE", "N/A"))],
        ["DATE OF BIRTH", str(d_row.get("DOB", "N/A"))],
        ["CALCULATED AGE", str(d_row.get("AGE", "N/A"))],
        ["GENDER", str(d_row.get("GENDER", "N/A"))],
        ["CONTACT NUMBER", str(d_row.get("CONTACT NUMBER", "N/A"))],
    ]
    pdf.set_font("Helvetica", size=8)
    with pdf.table(col_widths=(60, 120)) as table:
        for row in t3_data:
            r = table.row()
            r.cell(row[0])
            r.cell(row[1])
    pdf.ln(4)
        # TABLE 5: Lifestyle Parameters
    section_header("SECTION 5: LIFESTYLE & ADDICTION PARAMETERS")
    t4_data = [
        ["SMOKING", "ALCOHOL", "OTHERS ADDICTIONS"],
        [
            str(d_row.get("SMOKING", "N/A")),
            str(d_row.get("ALCOHOL", "N/A")),
            str(d_row.get("OTHERS ADDICTIONS", "N/A")),
        ],
    ]
    pdf.set_font("Helvetica", size=8)
    with pdf.table() as table:
        for row in t4_data:
            r = table.row()
            for cell_val in row:
                r.cell(cell_val)
    pdf.ln(4)
    #Table5:Clinical data
    section_header("SECTION 6: PERMANENT DISEASE DETAILS ")
    t5_data=[
        ["DIABETES","ALLERGY","CARDIAC DISEASE"],
        [
            str(d_row.get("DIABETES", "N/A")),
            str(d_row.get("ALLERGY", "N/A")),
            str(d_row.get("OTHERS ADDICTIONS", "N/A")),
        ],
    ]
    pdf.set_font("Helvetica", size=8)
    with pdf.table()as table:
        for row in t5_data:
            r = table.row()
            for cell_val in row:
                r.cell(cell_val)
    pdf.ln(4)
# TABLE 6: Clinical Visits
    section_header("SECTION 6: CLINICAL VISITS RECORD")

    is_no_visit = clinical_match.empty or (
        len(clinical_match) == 1
        and (
            str(clinical_match.iloc[0].get("VISIT_STATUS", "")).strip().upper() == "NO"
            or str(clinical_match.iloc[0].get("REMARKS", "")).strip().upper() == "NO VISIT"
        )
    )

    if is_no_visit:
        t6_data = [
            ["STATUS", "REMARKS"],
            ["NO VISIT", "No clinical visit recorded for this protocol"],
        ]
        pdf.set_font("Helvetica", size=8)
        with pdf.table(col_widths=(60, 120)) as table:
            for row in t6_data:
                r = table.row()
                r.cell(row[0])
                r.cell(row[1])
        pdf.ln(4)
    else:
        t6_headers = [
            "VISIT #",
            "DATE",
            "BLOOD PRESSURE",
            "PULSE",
            "TEMPERATURE",
            "REMARKS",
        ]
        t6_rows = [t6_headers]

        for _, row in clinical_match.iterrows():
            t6_rows.append(
                [
                    str(row.get("VISIT_NUMBER", "N/A")),
                    str(row.get("DATE", "N/A")),
                    str(row.get("BLOOD PRESSURE", "N/A")),
                    str(row.get("PULSE", "N/A")),
                    str(row.get("TEMPERATURE", "N/A")),
                    str(row.get("REMARKS", "N/A")),
                ]
            )

        pdf.set_font("Helvetica", size=8)
        with pdf.table(col_widths=(25, 25, 35, 25, 25, 45)) as table:
            for row in t6_rows:
                r = table.row()
                for cell_val in row:
                    r.cell(cell_val)
        pdf.ln(4)
    # TABLE 7: Lab Reports
    section_header("SECTION 7: LABORATORY INVESTIGATION REPORTS")

    def get_val(row, key1, key2):
        val = row.get(key1, row.get(key2, None))
        return str(val) if val is not None and pd.notna(val) else "N/A"
    t7_data = [
        [
            "TEST PARAMETER",
            "NORMAL RANGE",
            "OBSERVED VALUE",
            "REMARKS / STATUS",
        ],
        [
            "HAEMOGLOBIN",
            get_val(l_row, "HAEMOGLOBIN_RANGE", "HAEMOGLOBIN RANGE"),
            get_val(l_row, "HAEMOGLOBIN_VALUE", "HAEMOGLOBIN VALUE"),
            get_val(l_row, "HAEMOGLOBIN_STATUS", "HAEMOGLOBIN STATUS"),
        ],
        [
            "WBC COUNT",
            get_val(l_row, "WBC_RANGE", "WBC RANGE"),
            get_val(l_row, "WBC_VALUE", "WBC VALUE"),
            get_val(l_row, "WBC_STATUS", "WBC STATUS"),
        ],
        [
            "PLATELET COUNT",
            get_val(l_row, "PLATELET_RANGE", "PLATELET RANGE"),
            get_val(l_row, "PLATELET_VALUE", "PLATELET VALUE"),
            get_val(l_row, "PLATELET_STATUS", "PLATELET STATUS"),
        ],
        [
            "RBC COUNT",
            get_val(l_row, "RBC_RANGE", "RBC RANGE"),
            get_val(l_row, "RBC_VALUE", "RBC VALUE"),
            get_val(l_row, "RBC_STATUS", "RBC STATUS"),
        ],
        [
            "GLUCOSE LEVEL",
            get_val(l_row, "GLUCOSE_RANGE", "GLUCOSE RANGE"),
            get_val(l_row, "GLUCOSE_VALUE", "GLUCOSE VALUE"),
            get_val(l_row, "GLUCOSE_STATUS", "GLUCOSE STATUS"),
        ],
        [
            "BILIRUBIN LEVEL",
            get_val(l_row, "BILIRUBIN_RANGE", "BILIRUBIN RANGE"),
            get_val(l_row, "BILIRUBIN_VALUE", "BILIRUBIN VALUE"),
            get_val(l_row, "BILIRUBIN_STATUS", "BILIRUBIN STATUS"),
        ],
    ]
    pdf.set_font("Helvetica", size=8)
    with pdf.table(col_widths=(50, 45, 45, 40)) as table:
        for row in t7_data:
            r = table.row()
            for cell_val in row:
                r.cell(cell_val)
    pdf.ln(4)
    # TABLE 8: Adverse Events
    section_header("SECTION 8: ADVERSE EVENTS REPORTED")

    is_no_ae = ae_match.empty or (
        len(ae_match) == 1
        and str(ae_match.iloc[0].get("AE_STATUS", "")).strip().upper() == "NO"
    )

    if is_no_ae:
        t8_data = [
            ["STATUS", "DESCRIPTION OF ADVERSE EFFECT"],
            ["NO ADVERSE EFFECT REPORTED", "No adverse effect occurred during trial"],
        ]
        pdf.set_font("Helvetica", size=8)
        with pdf.table(col_widths=(60, 120)) as table:
            for row in t8_data:
                r = table.row()
                r.cell(row[0])
                r.cell(row[1])
        pdf.ln(4)
    else:
        t8_headers = [
            "DESCRIPTION OF ADVERSE EFFECT",
            "DATE OF ONSET",
            "SEVERITY",
            "ACTION TAKEN",
            "OUTCOME",
        ]
        t8_rows = [t8_headers]

        for _, row in ae_match.iterrows():
            t8_rows.append(
                [
                    str(row.get("DESCRIPTION OF ADVERSE EFFECT", "N/A")),
                    str(row.get("DATE OF ONSET", "N/A")),
                    str(row.get("SEVERITY", "N/A")),
                    str(row.get("ACTION TAKEN", "N/A")),
                    str(row.get("OUTCOME", "N/A")),
                ]
            )

        pdf.set_font("Helvetica", size=8)
        with pdf.table(col_widths=(45, 30, 30, 40, 35)) as table:
            for row in t8_rows:
                r = table.row()
                for cell_val in row:
                    r.cell(cell_val)
        pdf.ln(4)

    # TABLE 9: Concomitant Medications
    section_header("SECTION 9: CONCOMITANT MEDICATIONS & CAUSE")

    if is_no_ae:
        t9_data = [
            ["STATUS", "DETAILS"],
            ["NO CONCOMITANT MEDICATIONS", "No medication prescribed for adverse events"],
        ]
        pdf.set_font("Helvetica", size=8)
        with pdf.table(col_widths=(60, 120)) as table:
            for row in t9_data:
                r = table.row()
                r.cell(row[0])
                r.cell(row[1])
    else:
        t9_headers = [
            "ASSOCIATED ADVERSE EFFECT (CAUSE)",
            "MEDICINE GIVEN",
            "START DATE",
            "END DATE",
            "FREQUENCY",
        ]
        t9_rows = [t9_headers]

        for _, row in ae_match.iterrows():
            t9_rows.append(
                [
                    str(row.get("DESCRIPTION OF ADVERSE EFFECT", "N/A")),
                    str(row.get("MEDICINE GIVEN", "N/A")),
                    str(row.get("MEDICINE START DATE", "N/A")),
                    str(row.get("MEDICINE END DATE", "N/A")),
                    str(row.get("FREQUENCY", "N/A")),
                ]
            )

        pdf.set_font("Helvetica", size=8)
        with pdf.table(col_widths=(45, 40, 30, 30, 35)) as table:
            for row in t9_rows:
                r = table.row()
                for cell_val in row:
                    r.cell(cell_val)
    pdf.ln(4)
 # ----------------------------------------------------
    # SECTION 9: INVESTIGATOR DECLARATION & SIGNATURE
    # ----------------------------------------------------
    section_header("SECTION 9: INVESTIGATOR DECLARATION & SIGNATURE")

    pdf.set_font("Helvetica", size=8)
    declaration_statements = (
        "1. I hereby declare that all clinical observations, laboratory reports, and trial data recorded in "
        "this Case Report Form (CRF) are accurate, complete, and verified.\n"
        "2. The trial was conducted in accordance with the study protocol, Good Clinical Practice (GCP) guidelines, "
        "and applicable regulatory standards.\n"
        "3. All adverse events and concomitant medications administered during the trial have been thoroughly documented and evaluated.\n"
        "4. I confirm that subject confidentiality and informed consent procedures were strictly maintained throughout the study duration."
    )
    pdf.multi_cell(0, 4.5, declaration_statements)
    pdf.ln(6)

    # Fetch Investigator Name dynamically from Section 1/Demographic data
    investigator_name = str(d_row.get("INVESTIGATOR", "N/A"))
    site_number = str(d_row.get("SITE NUMBER", "N/A"))

    pdf.set_font("Helvetica", style="B", size=8)
    
    # Signature Layout Table
    sig_table_data = [
        [f"INVESTIGATOR NAME: {investigator_name}", "SIGNATURE: ___________________________"],
        [f"SITE NUMBER: {site_number}", "DATE OF SIGNATURE: ____________________"]
    ]

    with pdf.table(col_widths=(100, 80), borders_layout="NONE", line_height=6) as table:
        for row in sig_table_data:
            r = table.row()
            r.cell(row[0])
            r.cell(row[1])
            

    # Save Output
    out_pdf = f"/storage/emulated/0/Download/crf_{target_protocol}.pdf"
    pdf.output(out_pdf)
    print(f"\n[+] Unified PDF generated successfully: {out_pdf}")
