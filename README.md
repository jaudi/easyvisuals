# EasyVisuals

Visual analytics for companies — priced per **solution**, not per user.

## The Problem

Power BI charges per user. A team of 50 people viewing one dashboard pays 50 licences.
EasyVisuals flips the model: you pay once for the solution, your whole company uses it.

---

## Our Products

### 1. 🐳 Custom Streamlit Dashboard — Docker Delivery
We build a tailored Streamlit dashboard for your data.
You tell us your columns, KPIs, and chart types.
We deliver a **Docker container** you run inside your own environment.

- ✅ Runs entirely inside your company (data never leaves)
- ✅ Unlimited internal users — no per-seat cost
- ✅ No dependency on external cloud services
- ✅ One-time delivery, low friction for your IT team

**Best for:** Companies with internal infrastructure who want full control.

---

### 2. 🔗 Custom Streamlit Dashboard — Hosted Link
Same custom dashboard, but we host it for you.
You get a **professional URL** to share with your team or clients — no setup required on your side.

- ✅ Ready to use immediately
- ✅ Hosted on professional infrastructure (not Streamlit Cloud)
- ✅ We manage updates and uptime
- ✅ Shareable with unlimited viewers

**Best for:** Companies that want zero IT involvement and a fast go-live.

---

### 3. 📊 Power BI Consultancy — Finance
Expert consultancy for finance teams already using Power BI.
We help you get more value from your existing investment: reports, data models, DAX, governance.

- ✅ Finance-specific expertise (P&L, cash flow, budgeting, forecasting)
- ✅ Report design and optimisation
- ✅ Data model architecture
- ✅ Training for your finance team

**Best for:** Finance departments that need Power BI expertise without hiring full-time.

---

## The Demo Tool

The Streamlit app in this repository is our **marketing demo**.
It lets prospects define columns, upload data, build charts, and export a PDF —
so they can see what we deliver before they commit.

```bash
# Run the demo locally
pip install -r requirements.txt
streamlit run easyvisuals.py
```

---

## Tech Stack

- **Dashboards:** Python · Streamlit · Plotly · Pandas
- **PDF Export:** ReportLab
- **Delivery:** Docker
- **Hosting (Product 2):** DigitalOcean / Railway / Azure Container Apps

## Contact

Interested in a dashboard for your company? Open an issue or reach out via GitHub.

## License

MIT License
