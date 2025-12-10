# Employee Productivity Analysis System

A comprehensive full-stack application for analyzing employee productivity based on working hours, leave days, and employment type (full-time vs part-time).

## 📋 Features

### Backend (Python + Flask + Pandas)
- ✅ CSV and Excel file upload processing
- ✅ Automatic productivity calculation based on:
  - Standard hours (200 for full-time, 100 for part-time)
  - Leave day deductions (8 hours per leave)
  - Actual hours worked
- ✅ Productivity classification (≥90% = Productive)
- ✅ Separate analysis for full-time and part-time employees
- ✅ Department-wise statistics
- ✅ Export to Excel (multiple sheets)
- ✅ Export to PDF reports
- ✅ Generate sample employee data for testing

### Frontend (HTML + CSS + JavaScript)
- ✅ Modern, responsive dashboard interface
- ✅ File upload with drag-and-drop support
- ✅ Real-time data visualization with Chart.js:
  - Productivity distribution (doughnut chart)
  - Full-time vs Part-time comparison (bar chart)
  - Department performance (bar chart)
  - Hours analysis (grouped bar chart)
- ✅ Advanced filtering:
  - Search by name or employee ID
  - Filter by department
  - Filter by employment type
  - Filter by productivity status
- ✅ Tabbed interface for different employee categories
- ✅ Summary cards with key metrics
- ✅ Export functionality (Excel & PDF)
- ✅ Clean, professional UI with gradient designs

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)
- Modern web browser (Chrome, Firefox, Safari, Edge)

### Step 1: Install Python Dependencies

Create a virtual environment (recommended):
```bash
python -m venv venv

# On Windows:
venv\Scripts\activate

# On Mac/Linux:
source venv/bin/activate
```

Install required packages:
```bash
pip install flask flask-cors pandas openpyxl reportlab numpy
```

### Step 2: Backend Setup

1. Save the backend code as `app.py`
2. Make sure all dependencies are installed
3. Run the Flask server:
```bash
python app.py
```

The server will start on `http://localhost:5000`

### Step 3: Frontend Setup

1. Save the frontend HTML code as `index.html`
2. Open `index.html` in your web browser, OR
3. Serve it using Python's built-in server:
```bash
# In a new terminal, navigate to the folder with index.html
python -m http.server 8000
```
Then open `http://localhost:8000` in your browser

## 📊 Data Format

### Required CSV/Excel Columns

Your employee data file must contain these columns:

| Column Name | Description | Example |
|------------|-------------|---------|
| Employee_ID | Unique employee identifier | EMP0001 |
| Name | Employee full name | John Doe |
| Department | Department name | Engineering |
| Employment_Type | Full-Time or Part-Time | Full-Time |
| Actual_Hours | Hours worked in the month | 185.5 |
| Leave_Days | Number of leave days taken | 2 |

### Sample Data Structure

```csv
Employee_ID,Name,Department,Employment_Type,Actual_Hours,Leave_Days
EMP0001,John Doe,Engineering,Full-Time,185.5,2
EMP0002,Jane Smith,Sales,Part-Time,92.0,1
EMP0003,Bob Johnson,Marketing,Full-Time,195.0,0
```

## 🎯 How to Use

### 1. Generate Sample Data (Testing)
- Click the **"Generate Sample Data"** button
- A file with 100 sample employees will be downloaded
- Use this file to test the system

### 2. Upload Your Data
- Click **"Choose File"** button
- Select your CSV or Excel file
- The filename will appear next to the button

### 3. Analyze Data
- Click the **"Analyze Data"** button
- Wait for processing (usually a few seconds)
- Results will appear below

### 4. View Results
- **Summary Cards**: See total employees, productive count, and averages
- **Charts**: Visual representation of productivity metrics
- **Tables**: Detailed employee data in tabbed format
  - All Employees
  - Full-Time Only
  - Part-Time Only

### 5. Apply Filters
- **Search**: Type employee name or ID
- **Department**: Select specific department
- **Employment Type**: Filter by Full-Time or Part-Time
- **Status**: Filter by Productive or Not Productive

### 6. Export Reports
- Click **"Export to Excel"** for detailed spreadsheet with multiple sheets
- Click **"Export to PDF"** for formatted PDF report

## 🔢 Productivity Calculation Logic

```
1. Determine Standard Hours:
   - Full-Time = 200 hours/month
   - Part-Time = 100 hours/month

2. Calculate Leave Deduction:
   - Leave Hours = Leave Days × 8 hours

3. Calculate Expected Hours:
   - Expected Hours = Standard Hours - Leave Hours

4. Calculate Productivity:
   - Productivity % = (Actual Hours ÷ Expected Hours) × 100

5. Classify:
   - Productive: ≥ 90%
   - Not Productive: < 90%
```

### Example Calculation

**Full-Time Employee:**
- Standard: 200 hours
- Leave: 2 days = 16 hours
- Expected: 200 - 16 = 184 hours
- Actual: 185.5 hours
- Productivity: (185.5 ÷ 184) × 100 = 100.82% ✅ **Productive**

**Part-Time Employee:**
- Standard: 100 hours
- Leave: 1 day = 8 hours
- Expected: 100 - 8 = 92 hours
- Actual: 85 hours
- Productivity: (85 ÷ 92) × 100 = 92.39% ✅ **Productive**

## 🛠️ API Endpoints

### 1. Generate Sample Data
```
GET /api/generate-sample?count=100
Response: Excel file download
```

### 2. Analyze Productivity
```
POST /api/analyze
Content-Type: multipart/form-data
Body: file (CSV or Excel)
Response: JSON with analysis results
```

### 3. Export to Excel
```
POST /api/export-excel
Content-Type: application/json
Body: Analysis data
Response: Excel file download
```

### 4. Export to PDF
```
POST /api/export-pdf
Content-Type: application/json
Body: Analysis data
Response: PDF file download
```

### 5. Health Check
```
GET /health
Response: {"status": "healthy", "timestamp": "..."}
```

## 📱 Browser Compatibility

- ✅ Chrome (recommended)
- ✅ Firefox
- ✅ Safari
- ✅ Edge
- ✅ Mobile browsers (responsive design)

## 🎨 Customization

### Modify Productivity Thresholds
In `app.py`, change:
```python
PRODUCTIVITY_THRESHOLD = 90  # Change to your desired percentage
```

### Modify Standard Hours
In `app.py`, change:
```python
FULLTIME_STANDARD_HOURS = 200  # Adjust as needed
PARTTIME_STANDARD_HOURS = 100  # Adjust as needed
HOURS_PER_LEAVE_DAY = 8       # Adjust as needed
```

### Customize UI Colors
In `index.html`, modify the CSS gradient colors:
```css
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
```

## 🐛 Troubleshooting

### "Connection refused" error
- Make sure the Flask backend is running on port 5000
- Check if the API_URL in index.html matches your backend URL

### File upload fails
- Verify file format (CSV or Excel only)
- Check if all required columns are present
- Ensure column names match exactly (case-sensitive)

### Charts not displaying
- Ensure Chart.js CDN is accessible
- Check browser console for JavaScript errors
- Try refreshing the page

### Export buttons not working
- Verify backend is running
- Check browser console for CORS errors
- Ensure you've analyzed data first

## 📦 Project Structure

```
productivity-system/
├── app.py                 # Backend Flask application
├── index.html            # Frontend dashboard
├── requirements.txt      # Python dependencies
└── README.md            # This file
```

## 📄 requirements.txt

Create this file with:
```
flask==3.0.0
flask-cors==4.0.0
pandas==2.1.4
openpyxl==3.1.2
reportlab==4.0.7
numpy==1.26.2
```

## 🔐 Security Notes

⚠️ **Important for Production:**
- This is a development setup
- For production, add authentication
- Implement file upload validation
- Add rate limiting
- Use HTTPS
- Sanitize user inputs
- Implement proper error logging

## 📞 Support

For issues or questions:
1. Check the troubleshooting section
2. Review the API endpoints documentation
3. Verify your data format matches requirements
4. Check browser console for errors

## 🎓 Educational Purpose

This system demonstrates:
- Full-stack web development
- RESTful API design
- Data processing with Pandas
- Interactive data visualization
- File upload/download handling
- Responsive web design
- Chart.js integration
- Flask backend development

## 📈 Future Enhancements

Potential additions:
- [ ] User authentication and authorization
- [ ] Database integration (PostgreSQL/MySQL)
- [ ] Real-time data updates
- [ ] Email report delivery
- [ ] Historical trend analysis
- [ ] Employee performance predictions
- [ ] Multi-month comparison
- [ ] Custom report templates
- [ ] Mobile app version
- [ ] API rate limiting

## ✨ Credits

Built with:
- Flask (Backend framework)
- Pandas (Data processing)
- Chart.js (Data visualization)
- ReportLab (PDF generation)
- OpenPyXL (Excel processing)

---

**Version:** 1.0.0  
**Last Updated:** December 2024  
**License:** MIT (modify as needed)