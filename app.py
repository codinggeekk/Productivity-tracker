"""
Employee Productivity Analysis System - Backend
Flask API with Pandas data processing
"""
import flask
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import io
import json
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
import random

app = Flask(__name__)
CORS(app)

# Constants
FULLTIME_STANDARD_HOURS = 200
PARTTIME_STANDARD_HOURS = 100
HOURS_PER_LEAVE_DAY = 8
PRODUCTIVITY_THRESHOLD = 90

def generate_sample_data(num_employees=100):
    """Generate sample employee data for testing"""
    departments = ['Engineering', 'Sales', 'Marketing', 'HR', 'Finance', 'Operations', 'IT', 'Customer Service']
    employment_types = ['Full-Time', 'Part-Time']
    
    data = []
    for i in range(1, num_employees + 1):
        emp_type = random.choice(employment_types)
        standard_hours = FULLTIME_STANDARD_HOURS if emp_type == 'Full-Time' else PARTTIME_STANDARD_HOURS
        
        # Generate realistic data
        leave_days = random.randint(0, 5)
        # Vary actual hours to create different productivity levels
        if random.random() < 0.7:  # 70% productive employees
            actual_hours = random.randint(int(standard_hours * 0.90), int(standard_hours * 1.05))
        else:  # 30% less productive
            actual_hours = random.randint(int(standard_hours * 0.60), int(standard_hours * 0.89))
        
        data.append({
            'Employee_ID': f'EMP{i:04d}',
            'Name': f'Employee {i}',
            'Department': random.choice(departments),
            'Employment_Type': emp_type,
            'Actual_Hours': actual_hours - (leave_days * HOURS_PER_LEAVE_DAY * random.uniform(0.8, 1.0)),
            'Leave_Days': leave_days
        })
    
    return pd.DataFrame(data)

def calculate_productivity(df):
    """Calculate productivity metrics for employees"""
    df = df.copy()
    
    # Determine standard hours based on employment type
    df['Standard_Hours'] = df['Employment_Type'].apply(
        lambda x: FULLTIME_STANDARD_HOURS if x == 'Full-Time' else PARTTIME_STANDARD_HOURS
    )
    
    # Calculate expected hours after deducting leaves
    df['Leave_Hours_Deduction'] = df['Leave_Days'] * HOURS_PER_LEAVE_DAY
    df['Expected_Hours'] = df['Standard_Hours'] - df['Leave_Hours_Deduction']
    
    # Ensure expected hours don't go negative
    df['Expected_Hours'] = df['Expected_Hours'].clip(lower=1)
    
    # Calculate productivity percentage
    df['Productivity_Percentage'] = (df['Actual_Hours'] / df['Expected_Hours'] * 100).round(2)
    
    # Classify productivity
    df['Productivity_Status'] = df['Productivity_Percentage'].apply(
        lambda x: 'Productive' if x >= PRODUCTIVITY_THRESHOLD else 'Not Productive'
    )
    
    # Round numeric columns
    df['Actual_Hours'] = df['Actual_Hours'].round(2)
    
    return df

def generate_summary_stats(df):
    """Generate summary statistics"""
    summary = {
        'total_employees': len(df),
        'productive_count': len(df[df['Productivity_Status'] == 'Productive']),
        'not_productive_count': len(df[df['Productivity_Status'] == 'Not Productive']),
        'average_productivity': df['Productivity_Percentage'].mean().round(2),
        'fulltime_stats': {},
        'parttime_stats': {}
    }
    
    # Full-time statistics
    ft_df = df[df['Employment_Type'] == 'Full-Time']
    if len(ft_df) > 0:
        summary['fulltime_stats'] = {
            'count': len(ft_df),
            'productive': len(ft_df[ft_df['Productivity_Status'] == 'Productive']),
            'not_productive': len(ft_df[ft_df['Productivity_Status'] == 'Not Productive']),
            'average_productivity': ft_df['Productivity_Percentage'].mean().round(2),
            'average_hours': ft_df['Actual_Hours'].mean().round(2)
        }
    
    # Part-time statistics
    pt_df = df[df['Employment_Type'] == 'Part-Time']
    if len(pt_df) > 0:
        summary['parttime_stats'] = {
            'count': len(pt_df),
            'productive': len(pt_df[pt_df['Productivity_Status'] == 'Productive']),
            'not_productive': len(pt_df[pt_df['Productivity_Status'] == 'Not Productive']),
            'average_productivity': pt_df['Productivity_Percentage'].mean().round(2),
            'average_hours': pt_df['Actual_Hours'].mean().round(2)
        }
    
    # Department statistics
    dept_stats = df.groupby('Department').agg({
        'Productivity_Percentage': 'mean',
        'Employee_ID': 'count'
    }).round(2).to_dict('index')
    summary['department_stats'] = dept_stats
    
    return summary

@app.route('/api/generate-sample', methods=['GET'])
def generate_sample():
    """Generate sample employee data"""
    try:
        num_employees = int(request.args.get('count', 100))
        df = generate_sample_data(num_employees)
        
        # Save to Excel in memory
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Employee Data')
        output.seek(0)
        
        return send_file(
            output,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            as_attachment=True,
            download_name=f'sample_employee_data_{num_employees}.xlsx'
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/analyze', methods=['POST'])
def analyze_productivity():
    """Analyze employee productivity from uploaded file"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'Empty filename'}), 400
        
        # Read file based on extension
        if file.filename.endswith('.csv'):
            df = pd.read_csv(file)
        elif file.filename.endswith(('.xlsx', '.xls')):
            df = pd.read_excel(file)
        else:
            return jsonify({'error': 'Unsupported file format. Use CSV or Excel'}), 400
        
        # Validate required columns
        required_columns = ['Employee_ID', 'Name', 'Department', 'Employment_Type', 'Actual_Hours', 'Leave_Days']
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            return jsonify({'error': f'Missing columns: {", ".join(missing_columns)}'}), 400
        
        # Calculate productivity
        df_processed = calculate_productivity(df)
        
        # Generate summary statistics
        summary = generate_summary_stats(df_processed)
        
        # Prepare response data
        response = {
            'summary': summary,
            'data': df_processed.to_dict('records'),
            'fulltime_data': df_processed[df_processed['Employment_Type'] == 'Full-Time'].to_dict('records'),
            'parttime_data': df_processed[df_processed['Employment_Type'] == 'Part-Time'].to_dict('records')
        }
        
        return jsonify(response)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/export-excel', methods=['POST'])
def export_excel():
    """Export analyzed data to Excel"""
    try:
        data = request.json
        df = pd.DataFrame(data['data'])
        
        # Create Excel file in memory
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            # All employees
            df.to_excel(writer, index=False, sheet_name='All Employees')
            
            # Full-time employees
            ft_df = df[df['Employment_Type'] == 'Full-Time']
            if len(ft_df) > 0:
                ft_df.to_excel(writer, index=False, sheet_name='Full-Time')
            
            # Part-time employees
            pt_df = df[df['Employment_Type'] == 'Part-Time']
            if len(pt_df) > 0:
                pt_df.to_excel(writer, index=False, sheet_name='Part-Time')
            
            # Productive employees
            prod_df = df[df['Productivity_Status'] == 'Productive']
            if len(prod_df) > 0:
                prod_df.to_excel(writer, index=False, sheet_name='Productive')
            
            # Not productive employees
            not_prod_df = df[df['Productivity_Status'] == 'Not Productive']
            if len(not_prod_df) > 0:
                not_prod_df.to_excel(writer, index=False, sheet_name='Not Productive')
        
        output.seek(0)
        
        return send_file(
            output,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            as_attachment=True,
            download_name=f'productivity_report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.xlsx'
        )
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/export-pdf', methods=['POST'])
def export_pdf():
    """Export analyzed data to PDF"""
    try:
        data = request.json
        
        # Create PDF in memory
        output = io.BytesIO()
        doc = SimpleDocTemplate(output, pagesize=A4)
        elements = []
        styles = getSampleStyleSheet()
        
        # Title
        title = Paragraph("Employee Productivity Report", styles['Title'])
        elements.append(title)
        elements.append(Spacer(1, 20))
        
        # Summary
        summary_text = f"""
        <b>Report Generated:</b> {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}<br/>
        <b>Total Employees:</b> {data['summary']['total_employees']}<br/>
        <b>Productive:</b> {data['summary']['productive_count']}<br/>
        <b>Not Productive:</b> {data['summary']['not_productive_count']}<br/>
        <b>Average Productivity:</b> {data['summary']['average_productivity']}%
        """
        summary_para = Paragraph(summary_text, styles['Normal'])
        elements.append(summary_para)
        elements.append(Spacer(1, 20))
        
        # Data table
        df = pd.DataFrame(data['data'])
        table_data = [['ID', 'Name', 'Department', 'Type', 'Hours', 'Productivity %', 'Status']]
        
        for _, row in df.iterrows():
            table_data.append([
                str(row['Employee_ID']),
                str(row['Name'])[:20],
                str(row['Department'])[:15],
                str(row['Employment_Type'])[:10],
                f"{row['Actual_Hours']:.1f}",
                f"{row['Productivity_Percentage']:.1f}%",
                str(row['Productivity_Status'])[:15]
            ])
        
        table = Table(table_data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        elements.append(table)
        
        doc.build(elements)
        output.seek(0)
        
        return send_file(
            output,
            mimetype='application/pdf',
            as_attachment=True,
            download_name=f'productivity_report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.pdf'
        )
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()})

if __name__ == '__main__':
    app.run(debug=True, port=5000)