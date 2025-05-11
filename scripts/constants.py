import os

# Folders
FILE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(FILE_DIR)

# Model
MODEL = "gemini-2.0-flash"
MAX_RETRIES = 5
RETRY_DELAY = 3

# KPI Lables and Segments
KPI_LABELS = {
    "provision_for_credit_losses_bps_avg_loans": [
        "provision for credit losses (bps of average loans)"
    ],
    "allowance_loan_losses": ["allowance for loan losses"],
    "average_loans": ["average loans (gross of allowance for loan losses)"],
    "cost_income_ratio": ["cost/income"],
    "net_interest_income": ["net interest income"],
}

# Sheet names mapped to business segments
SEGMENTS = {
    "FinSum": "total_bank",
    "CB": "corporate_bank",
    "IB": "investment_bank",
    "PB": "private_bank",
}
