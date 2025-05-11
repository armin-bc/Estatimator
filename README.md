# FinAI – AI-Powered Commentary on Bank KPIs

FinAI is an analysis tool that uses generative AI (Google Gemini 2.5 Pro) to generate professional financial commentary based on structured bank data and macroeconomic indicators. It is especially designed to interpret and explain developments in credit loss provisions in the context of internal performance and external economic signals.

This tool is built for banking professionals, risk analysts, and reporting teams who want to combine quantitative inputs with qualitative insights – whether for internal reporting, risk assessments, or regulatory summaries.

## Features

- Segment-specific analysis: Corporate Bank, Private Bank, Investment Bank, or Total Bank
- Integration of macroeconomic indicators: IFO Business Climate Index and PMI Composite Index
- Structured Excel data support (e.g., .xlsb financial data supplement)
- PDF support (e.g., PMI reports via File API or Vertex AI)
- Optional user comments to influence or contextualize analysis
- Flexible prompt templating with Jinja2
- Gemini 2.5 Pro integration via Vertex AI or Google Generative AI SDK
- CLI interface with configurable flags

## Installation

1. Clone the repository:

git clone https://github.com/engelkai/FinAI.git

cd FinAI


2. (Recommended) Create a virtual environment:

python -m venv .venv

source .venv/bin/activate 
On Windows: .venv\Scripts\activate


3. Install dependencies:

pip install -r requirements.txt


4. Set up your `.env` file:

GOOGLE_API_KEY=your_api_key_here

> You need a valid Gemini API key to run the application.

## Usage

You can run the application via command line:

python main.py --segment CB --macro_kpis ifo pmi --user_comments "Please account for temporary provisioning effects in Q3 2023."


### CLI Arguments

| Argument          | Description                                                       |
|-------------------|-------------------------------------------------------------------|
| `--segment`       | The bank segment to analyze (`CB`, `PB`, `IB`, `FinSum`)          |
| `--macro_kpis`    | One or more macro indicators to include (`ifo`, `pmi`)            |
| `--user_comments` | Optional free-form notes or comments for the AI to consider       |

## Project Structure

.
├── main.py # Entry point
├── prompts/
│ └── instruction.jinja2 # Main Jinja2 prompt template
├── scripts/
│ ├── api_calls.py # Handles Gemini API calls and retries
│ ├── generate_insights.py # Prompt rendering logic
│ ├── utils.py # Data loading and preprocessing (Excel, PDF, text)
│ └── constants.py # Model config and label mappings
├── data/
│ ├── FDS-Q4-2024-13032025.xlsb # Example financial data supplement
│ ├── 202504_ifo.csv # Example IFO data
│ ├── 202502_pmi.pdf # Example PMI PDF
│ └── examples.txt # Reference text examples
├── requirements.txt
└── .env


## Requirements

- Python 3.9 or higher
- Valid Gemini API key (Google Generative AI or Vertex AI)
- Internet access to use the API

## Notes

- When PMI is selected, the corresponding PDF will be passed directly to Gemini (either via Vertex AI `Part.from_file` or Gemini File API upload).
- The prompt includes detailed role instructions and analytic expectations.
- Jinja2 is used for dynamic, data-driven prompt construction.

## License

This project is private and not licensed for public use. Internal use only.

