import streamlit as st
import pandas as pd
import google.generativeai as genai
from datetime import datetime

# Set page config
st.set_page_config(
    page_title="Business Budget Planner",
    layout="wide"
)

# Hardcoded Gemini API key
api_key = "AIzaSyDrksJ5fvEXs7ZCKS4qQ4-LFgP8M4MZAE0"

# Configure Gemini API
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-2.0-flash')

# App title and description
st.title("Business Budget Planner")
st.markdown("Create a comprehensive budget plan for your business")

# Sidebar for inputs
with st.sidebar:
    st.header("Business Information")
    business_name = st.text_input("Business Name", "My Business")
    budget_period = st.selectbox("Budget Period", ["Monthly", "Quarterly", "Annual"])
    
    st.header("Revenue")
    estimated_revenue = st.number_input("Estimated Revenue ($)", min_value=0, value=10000)
    
    st.header("Expenses")
    st.subheader("Fixed Expenses")
    rent = st.number_input("Rent/Mortgage ($)", min_value=0, value=2000)
    utilities = st.number_input("Utilities ($)", min_value=0, value=500)
    salaries = st.number_input("Salaries ($)", min_value=0, value=3000)
    insurance = st.number_input("Insurance ($)", min_value=0, value=400)
    
    st.subheader("Variable Expenses")
    marketing = st.number_input("Marketing ($)", min_value=0, value=800)
    supplies = st.number_input("Supplies ($)", min_value=0, value=600)
    travel = st.number_input("Travel ($)", min_value=0, value=300)
    miscellaneous = st.number_input("Miscellaneous ($)", min_value=0, value=200)

# Calculate total expenses and net profit
fixed_expenses = rent + utilities + salaries + insurance
variable_expenses = marketing + supplies + travel + miscellaneous
total_expenses = fixed_expenses + variable_expenses
net_profit = estimated_revenue - total_expenses

# Create budget data
budget_data = {
    "Category": ["Revenue", "Fixed Expenses", "Variable Expenses", "Total Expenses", "Net Profit"],
    "Amount ($)": [estimated_revenue, fixed_expenses, variable_expenses, total_expenses, net_profit]
}

# Create detailed expenses data
expenses_data = {
    "Expense Category": ["Rent/Mortgage", "Utilities", "Salaries", "Insurance", 
                         "Marketing", "Supplies", "Travel", "Miscellaneous"],
    "Type": ["Fixed", "Fixed", "Fixed", "Fixed", 
             "Variable", "Variable", "Variable", "Variable"],
    "Amount ($)": [rent, utilities, salaries, insurance, 
                   marketing, supplies, travel, miscellaneous]
}

# Main content
st.header(f"{business_name} - {budget_period} Budget Plan")

# Display budget summary
st.subheader("Budget Summary")
df_summary = pd.DataFrame(budget_data)
st.dataframe(df_summary)

# Display detailed expenses
st.subheader("Expense Breakdown")
df_expenses = pd.DataFrame(expenses_data)
st.dataframe(df_expenses)

# Pie chart for expenses
st.subheader("Expense Distribution")
expenses_categories = ["Rent/Mortgage", "Utilities", "Salaries", "Insurance", 
                      "Marketing", "Supplies", "Travel", "Miscellaneous"]
expenses_values = [rent, utilities, salaries, insurance, 
                  marketing, supplies, travel, miscellaneous]

# Use Matplotlib for pie chart
import matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(10, 6))
ax.pie(expenses_values, labels=expenses_categories, autopct='%1.1f%%', startangle=90)
ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle
st.pyplot(fig)

# Get budget insights from Gemini
if st.button("Generate Budget Insights"):
    with st.spinner("Generating insights..."):
        prompt = f"""
        Analyze this business budget:
        - Business Name: {business_name}
        - Budget Period: {budget_period}
        - Revenue: ${estimated_revenue}
        - Fixed Expenses: ${fixed_expenses}
        - Variable Expenses: ${variable_expenses}
        - Total Expenses: ${total_expenses}
        - Net Profit: ${net_profit}
        
        Provide 3-4 specific budget recommendations or insights in bullet points.
        Be concise and practical.
        """
        
        try:
            response = model.generate_content(prompt)
            st.subheader("Budget Insights")
            st.markdown(response.text)
        except Exception as e:
            st.error(f"Error generating insights: {str(e)}")

# Save budget as CSV
if st.button("Download Budget"):
    combined_data = pd.concat([
        df_summary, 
        pd.DataFrame({"Category": [""], "Amount ($)": [""]}),
        pd.DataFrame({"Category": ["Expense Details"], "Amount ($)": [""]}),
        df_expenses.rename(columns={"Expense Category": "Category"})
    ])
    
    csv = combined_data.to_csv(index=False)
    date_str = datetime.now().strftime("%Y%m%d")
    st.download_button(
        label="Confirm Download",
        data=csv,
        file_name=f"{business_name}_{budget_period}_Budget_{date_str}.csv",
        mime="text/csv"
    )

# Footer
st.markdown("---")
st.markdown("<div style='text-align: center;'>Made by Aditya Soni</div>", unsafe_allow_html=True)
