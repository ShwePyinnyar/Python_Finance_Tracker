import pandas as pd
import csv
from datetime import datetime 
from data_entry import *
import seaborn as sns
import matplotlib.pyplot as plt

class CSV:
    csv_file = 'finance_data.csv'
    columns = ['date','amount','category','description']

    @classmethod
    def init_csv(cls):
        try:
            pd.read_csv(cls.csv_file)
        except FileNotFoundError:
            df = pd.DataFrame(columns=cls.columns)
            df.to_csv(cls.csv_file,index=False)

    @classmethod
    def add_entry(cls,date,amount,category,description):
        new_entry = {
            'date':date,
            'amount':amount,
            'category':category,
            'description':description
        }
        with open(CSV.csv_file,'a',newline='') as csvfile:
            writer = csv.DictWriter(csvfile,fieldnames=cls.columns)
            writer.writerow(new_entry)
        print('Entry entered successfully!')

    @classmethod
    def get_transaction(cls,start_date,end_date):
        start_date_str,end_date_str = start_date,end_date
        df = pd.read_csv(cls.csv_file)
        df['date'] = pd.to_datetime(df['date'],format=date_format)
        start_date = datetime.strptime(start_date,date_format)
        end_date = datetime.strptime(end_date,date_format)

        mask = (df['date']>=start_date) & (df['date']<=end_date)
        filtered_df = df.loc[mask]

        if filtered_df.empty:
            print(f"No transactions between '{start_date_str} to '{end_date_str}'.")
            input ("Press Enter to go back to menu...")
            return filtered_df
        else:
            print(f"Transactions from '{start_date_str}' to '{end_date_str}'")
            print(filtered_df.to_string(index=False,formatters={'date': lambda x: x.strftime(date_format)}))

            total_income = filtered_df[filtered_df['category']=='Income']['amount'].sum()
            total_expense = filtered_df[filtered_df['category']=='Expense']['amount'].sum()

            print('\nSummary\n-------------------')
            print(f"\nTotal Income = $'{total_income:.2f}'")
            print(f"\nTotal Expense = $'{total_expense:.2f}'")
            print(f"\nNet Income  = $'{(total_income-total_expense):.2f}'")
            print('\n-------------------')
        
        return filtered_df

def plot(df):
    df.set_index('date',inplace=True)

    income_df = df[df['category']=='Income'].resample("D").sum().reindex(df.index,fill_value=0)
    expense_df = df[df['category']=='Expense'].resample("D").sum().reindex(df.index,fill_value=0)

    plt.figure(figsize=(10,5))
    plt.plot(income_df.index,income_df['amount'],label = "Income", color ='g')
    plt.plot(expense_df.index,expense_df['amount'],label = "Expense", color ='r')
    plt.xlabel("Date")
    plt.ylabel('Amount')
    plt.title("Income and Expense over Time")
    plt.legend()
    plt.grid(True)
    plt.show()


def add():
    CSV.init_csv()
    date = get_date()
    amount = get_amount()
    category = get_category()
    description = get_description()
    CSV.add_entry(date,amount,category,description)

def main():
    while True:
        print("\n1. Add a new entry")
        print("\n2. View the data")
        print("\n3. Exit")
        choice = input("Enter (1-3): ")

        if choice == "1":
            add()
        elif choice =="2":
            start_date = input("Start date : ")
            end_date = input("End Date : ")
            df = CSV.get_transaction(start_date,end_date)
            if df.empty:
                continue

            yn = input("Do you want to see this in plot? ([y]/n): ").lower().strip()
            if yn == "" or yn == "y":
                plot(df)

        elif choice == "3":
            print("Exiting ...")
            break
        else:
            print("Enter the valid choice. (1-3)")

if __name__ == "__main__":
    main()





















