
---

## How to Run

```bash
# Clone the repo
git clone https://github.com/Dinesh-012/Demand-Product-Finder.git
cd Demand-Product-Finder

# Create and activate virtual environment
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # Mac/Linux

# Install dependencies
pip install -r requirements.txt
playwright install chromium

# Run the dashboard
streamlit run web/app.py