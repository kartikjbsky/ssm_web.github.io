from flask import Flask, render_template, request, send_from_directory
import os
import re
from datetime import datetime

app = Flask(__name__)

# Plot directories
LC_DIR = 'static/light_curves'
FOV_DIR = 'static/sources_fov'
IC_DIR = 'static/integrated_counts'

# Excel configuration
app.config['EXCEL_FILE'] = 'sharp_peaks.csv'  # Ensure this file exists in /static/
app.config['STATIC_FOLDER'] = 'static'

@app.route('/', methods=['GET', 'POST'])
def index():
    matched_plots = []
    integrated_counts = []

    if request.method == 'POST':
        start_date = request.form['start_date']
        end_date = request.form['end_date']

        # Convert user input to datetime
        try:
            start_dt = datetime.strptime(start_date, '%Y-%m-%d')
            end_dt = datetime.strptime(end_date, '%Y-%m-%d')
        except ValueError:
            return "Invalid date format. Please use YYYY-MM-DD."

        # Load Integrated Counts (max 3)
        for fname in sorted(os.listdir(IC_DIR)):
            if fname.endswith('.png'):
                integrated_counts.append(os.path.join(IC_DIR, fname))
                if len(integrated_counts) >= 3:
                    break

        # Get Light Curve and FOV plots, match by dwell number
        lc_files = [f for f in os.listdir(LC_DIR) if f.endswith('.png')]
        fov_files = [f for f in os.listdir(FOV_DIR) if f.endswith('.png')]

        lc_dict = {}
        for fname in lc_files:
            match = re.match(r'(\d{4}-\d{2}-\d{2})_to_(\d{4}-\d{2}-\d{2})_LC_dwell_(\d+)\.png', fname)
            if match:
                file_start = datetime.strptime(match.group(1), '%Y-%m-%d')
                file_end = datetime.strptime(match.group(2), '%Y-%m-%d')
                dwell = match.group(3)

                if file_end >= start_dt and file_start <= end_dt:
                    lc_dict[dwell] = os.path.join(LC_DIR, fname)

        for fname in fov_files:
            match = re.match(r'(\d{4}-\d{2}-\d{2})_to_(\d{4}-\d{2}-\d{2})_FOV_dwell_(\d+)\.png', fname)
            if match:
                file_start = datetime.strptime(match.group(1), '%Y-%m-%d')
                file_end = datetime.strptime(match.group(2), '%Y-%m-%d')
                dwell = match.group(3)

                if file_end >= start_dt and file_start <= end_dt and dwell in lc_dict:
                    matched_plots.append({
                        'dwell': dwell,
                        'lc_path': lc_dict[dwell],
                        'fov_path': os.path.join(FOV_DIR, fname)
                    })

    return render_template('index.html', matched_plots=matched_plots, integrated_counts=integrated_counts)

@app.route('/get_excel')
def get_excel():
    """Serves the Excel file for the Excel viewer."""
    return send_from_directory(app.config['STATIC_FOLDER'], app.config['EXCEL_FILE'])

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/design')
def design():
    return render_template('design.html')

@app.route('/documents')
def documents():
    return render_template('documents.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')


if __name__ == '__main__':
    app.run(debug=True)
