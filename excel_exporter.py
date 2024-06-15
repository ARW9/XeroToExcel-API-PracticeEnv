# excel_exporter.py
import pandas as pd

def export_to_excel(balance_sheet_data, profit_loss_data, filename='XeroReports.xlsx'):
    # Convert data to DataFrames
    balance_sheet_df = pd.DataFrame(balance_sheet_data)
    profit_loss_df = pd.DataFrame(profit_loss_data)

    # Write DataFrames to an Excel file
    with pd.ExcelWriter(filename, engine='openpyxl') as writer:
        balance_sheet_df.to_excel(writer, sheet_name='Balance Sheet', index=False)
        profit_loss_df.to_excel(writer, sheet_name='Profit & Loss', index=False)
    print(f"Reports exported successfully to {filename}")
