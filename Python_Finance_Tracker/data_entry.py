from datetime import datetime

date_format = "%d-%m-%Y"
categories = {'I':'Income',
              'E':'Expense'}

def get_date(allow_default=False):
    date_str = input("Enter the date (dd-mm-yyyy): ")
    if allow_default and not date_str:
        return datetime.today().strftime(date_format)
    try:
        valid_date = datetime.strptime(date_str,date_format)
        return valid_date.strftime(date_format)
    except ValueError:
        print(f"Invalid date. The date format must be in '{date_format}'.")
        return get_date(allow_default=False)
    
def get_amount():
    try:
        amount = float(input("Enter the amount: "))
        if amount <=0:
            raise ValueError("The amount must be a positive number.")
        return amount
    except ValueError as e:
        print(e)
        return get_amount()
    
def get_category():
    category = input("Enter either 'I' for 'Income' or 'E' for 'Expense'.").upper()
    if category in categories:
            return categories[category]
    
    print("Invalid category. 'I' for 'Income'. 'E' for 'Expense'.")
    return get_category()
    
def get_description(): 
    return input('Enter description (Optional): ')


    
    












