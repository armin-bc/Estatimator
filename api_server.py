from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import subprocess
import json
import os
import sys
from pathlib import Path

# Add project root to path to ensure imports work correctly
sys.path.append(str(Path(__file__).resolve().parent))

# Import from your existing backend
from scripts.generate_insights import PromptRenderer
from scripts.api_calls import generate_response
import scripts.constants as const
from scripts.utils import load_ifo_data, extract_metrics_from_excel, read_text_file

app = Flask(__name__, static_folder="public")
CORS(app)  # Enable CORS for all routes


# Serve static files from your frontend
@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve(path):
    if path != "" and os.path.exists(app.static_folder + "/" + path):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, "index.html")


@app.route("/api/analyze", methods=["POST"])
def analyze():
    """Main endpoint to process data from the frontend tool and return analysis"""
    try:
        data = request.json
        segment = data.get("segment", "FinSum")  # Default to FinSum if not provided

        # Map frontend segment names to backend segment codes
        segment_mapping = {
            "Retail": "PB",  # Assuming Retail maps to Private Bank
            "Corporate": "CB",
            "Investment": "IB",
            "Total": "FinSum",
        }

        # Convert frontend segment name to backend segment code
        segment_code = segment_mapping.get(segment, "FinSum")

        # Get selected KPIs and convert to macro_kpis format
        selected_kpis = data.get("kpis", [])
        macro_kpis = []
        if "Ifo" in selected_kpis:
            macro_kpis.append("ifo")
        if "PMI" in selected_kpis:
            macro_kpis.append("pmi")

        # Get user comments
        user_comments = data.get("comments", "")

        # Process uploaded files
        main_documents = data.get("mainDocuments", [])
        additional_documents = data.get("additionalDocuments", [])

        # Load data based on selection
        segment_name = const.SEGMENTS[segment_code]
        df_ifo = (
            load_ifo_data(
                os.path.join(const.PROJECT_ROOT, "data", "202504_ifo_gsk_prepared.csv")
            )
            if "ifo" in macro_kpis
            else None
        )
        pmi_pdf_path = (
            os.path.join(const.PROJECT_ROOT, "data", "202502_pmi.pdf")
            if "pmi" in macro_kpis
            else None
        )
        bank_data_all_dict = extract_metrics_from_excel(
            os.path.join(const.PROJECT_ROOT, "data", "FDS-Q4-2024-13032025.xlsb")
        )
        bank_data_dict = bank_data_all_dict.get(segment_name, {})
        example = read_text_file(
            os.path.join(const.PROJECT_ROOT, "data", "examples.txt")
        )

        # Prepare context
        context = {
            "segment": segment_name,
            "domain": "Banking",
            "product_type": "Loans",
            "bank_data": bank_data_dict,
            "ifo_data": df_ifo.to_string(index=True) if df_ifo is not None else None,
            "pmi_data": (
                "Please find the PMI data in the PDF report."
                if pmi_pdf_path is not None
                else None
            ),
            "user_comments": user_comments,
            "example": example,
        }

        # Generate response
        renderer = PromptRenderer(template_dir=Path("prompts"))
        prompt = renderer.render_instruction_prompt(context)

        # Call Gemini API
        ai_response = generate_response(prompt, pmi_pdf_path)

        # Process the response into an easy-to-use format for the frontend
        analysis_result = {
            "variance_analysis": {"title": "Variance Analysis", "content": ai_response},
            "trend_analysis": {
                "title": "Trend Analysis",
                "summary": "The AI has analyzed trends based on the provided data and macro indicators.",
            },
        }

        return jsonify(
            {
                "success": True,
                "message": "Analysis completed successfully",
                "result": analysis_result,
            }
        )

    except Exception as e:
        print(f"Error: {str(e)}")
        return (
            jsonify(
                {"success": False, "message": f"Error processing request: {str(e)}"}
            ),
            500,
        )


@app.route("/api/upload", methods=["POST"])
def upload_file():
    """Endpoint to handle file uploads"""
    try:
        if "file" not in request.files:
            return jsonify({"success": False, "message": "No file part"}), 400

        file = request.files["file"]
        if file.filename == "":
            return jsonify({"success": False, "message": "No selected file"}), 400

        # Create upload directory if it doesn't exist
        upload_dir = os.path.join(const.PROJECT_ROOT, "uploads")
        os.makedirs(upload_dir, exist_ok=True)

        # Save the file
        file_path = os.path.join(upload_dir, file.filename)
        file.save(file_path)

        return jsonify(
            {
                "success": True,
                "message": "File uploaded successfully",
                "filename": file.filename,
                "path": file_path,
            }
        )

    except Exception as e:
        return (
            jsonify({"success": False, "message": f"Error uploading file: {str(e)}"}),
            500,
        )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
