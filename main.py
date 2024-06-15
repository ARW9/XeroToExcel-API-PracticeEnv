# main.py
from xero_client import authenticate, get_balance_sheet, get_profit_loss
from excel_exporter import export_to_excel

def main():
    # Authenticate with Xero
    authenticate()

    # Replace with your organization ID
    organization_id = 'YOUR_ORGANIZATION_ID'

    # Fetch reports from Xero
    balance_sheet = get_balance_sheet(organization_id)
    profit_loss = get_profit_loss(organization_id)

    # Extract data from the reports (this might need adjustments based on the actual structure of the data)
    balance_sheet_data = balance_sheet['reports'][0]['rows']
    profit_loss_data = profit_loss['reports'][0]['rows']

    # Export data to Excel
    export_to_excel(balance_sheet_data, profit_loss_data)

if __name__ == "__main__":
    main()
