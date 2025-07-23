import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

st.set_page_config(page_title="Expense Tracker", layout="centered")
st.title("💰 Expense Tracker with Budget")

# Files
EXPENSE_FILE = "expenses.csv"
BUDGET_FILE = "budget.txt"

# --- Load Budget ---
def load_budget():
    if os.path.exists(BUDGET_FILE):
        with open(BUDGET_FILE, "r") as f:
            return float(f.read())
    return 0.0

# --- Save Budget ---
def save_budget(budget):
    with open(BUDGET_FILE, "w") as f:
        f.write(str(budget))

# --- Budget Section ---
st.header("📌 Set Monthly Budget")
current_budget = load_budget()
new_budget = st.number_input("Enter your monthly budget (RM)", value=current_budget, min_value=0.0, format="%.2f")

if st.button("Save Budget"):
    save_budget(new_budget)
    st.success(f"✅ Budget saved: RM{new_budget:.2f}")

# --- Add New Expense ---
st.header("📝 Add New Expense")
date = st.date_input("Date")
category = st.selectbox("Category", ["Food", "Transport", "Entertainment", "Bills", "Other"])
amount = st.number_input("Amount", min_value=0.0, format="%.2f")
note = st.text_input("Note (optional)")

if st.button("Add Expense"):
    new_expense = pd.DataFrame([[date, category, amount, note]], columns=["Date", "Category", "Amount", "Note"])
    
    if os.path.exists(EXPENSE_FILE):
        df = pd.read_csv(EXPENSE_FILE)
        df = pd.concat([df, new_expense], ignore_index=True)
    else:
        df = new_expense

    df.to_csv(EXPENSE_FILE, index=False)
    st.success(f"✅ Expense added: RM{amount:.2f} for {category}")

# --- Show Expenses and Budget Summary ---
st.header("📋 All Expenses")

if os.path.exists(EXPENSE_FILE):
    df = pd.read_csv(EXPENSE_FILE)
    st.dataframe(df)

    total_spent = df["Amount"].sum()
    remaining_budget = new_budget - total_spent

    st.subheader("📊 Budget Summary")
    st.metric("Total Spent", f"RM{total_spent:.2f}")
    st.metric("Remaining Budget", f"RM{remaining_budget:.2f}")

    # --- Pie Chart ---
    st.header("📈 Spending Distribution (Pie Chart)")

    category_totals = df.groupby("Category")["Amount"].sum()

    if not category_totals.empty:
        fig, ax = plt.subplots()
        ax.pie(category_totals, labels=category_totals.index, autopct="%1.1f%%", startangle=90)
        ax.axis("equal")
        st.pyplot(fig)
    else:
        st.info("Not enough data for pie chart.")
else:
    st.info("No expenses recorded yet.")

