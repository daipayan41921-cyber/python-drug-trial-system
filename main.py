from crfdemodata2 import collect_demographics
from crflabdata2 import collect_clinical
from crftest2 import collect_lab_tests
from crfadverse2 import collect_adverse_events
from crfpdfcreator2 import generate_pdf_report
def main():
    while True:
        print("\n" + "=" * 60)
        print(" CASE REPORT FORM(CRF) ")
        print("=" * 60)
        print("Type 1 for data entry on server)")
        print("Type 2 to Generate PDF Report from existing database")
        print("Type 3 for Exit")
        print("=" * 60)
        choice = input("Enter choice (1-3) :- ").strip()
        if choice == "1":
            # Step 1: Demographics
            protocol_num, age, gender = collect_demographics()

            # Step 2: Clinical
            collect_clinical(protocol_num, age, gender)

            # Step 3: Lab Tests
            collect_lab_tests(protocol_num)

            # Step 4: Adverse Events & Medications
            collect_adverse_events(protocol_num)

            # Step 5: PDF Report
            gen = input("Generate PDF report now? [Y/N] :- ").strip().lower()
            if gen == "y":
                generate_pdf_report(protocol_num)
        elif choice == "2":
            generate_pdf_report()
        elif choice == "3":
            print("\nExiting program...")
            
if __name__ == "__main__":
    main()
    