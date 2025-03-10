import os
import json
from dotenv import load_dotenv


DATA_FILE = "data.json"

def load_data(filepath):
    if os.path.exists(filepath):
        with open(filepath, "r") as file:
            try:
                data = json.load(file)
                
            except json.JSONDecodeError:
                print(f"Warning: {filepath} was empty.")
                save_data(filepath, {})
                return {}
    return {}

def save_data(filepath, data):
    with open(filepath, "w") as file:
        return json.dump(data, file, indent=4)

# Classes
class BudgetingSplit():
    def __init__(self, savings, needs, wants):
        self.savings = savings
        self.needs = needs
        self.wants = wants

    def __str__(self):
        return f"({int(self.savings * 100)}/{int(self.needs * 100)}/{int(self.wants * 100)})"
    
    # Investments, holidays, etc.
    def calculateSavings(self, salary):
        return salary * self.savings
    
    # Food, petrol and others, including haircut.
    def calculateNeeds(self, salary):
        return salary * self.needs
    
    # Wants, leisure, clothes, tech, etc.
    def calculateWants(self, salary):
        return salary * self.wants

class Wallet():
    def __init__(self, id, balance):
        self.id = id
        self.balance = balance
        self.income = {}
        self.expenses = {}

    def addExpense(self, description, value):
        self.balance -= value
        if description in self.expenses:
            self.expenses[description] += value
        else:
            self.expenses = {description: value}
            
        return self.expenses
    
    def addIncome(self, value):
        self.balance += value
        return self.balance
    
    def __str__(self):
        return f"{self.balance:.2f}"

def submitSalary(budgeting_split: BudgetingSplit, salary, savings_wallet: Wallet, needs_wallet: Wallet, wants_wallet: Wallet):
    savingsBreakdown = round(budgeting_split.calculateSavings(salary), 2)
    needsBreakdown = round(budgeting_split.calculateNeeds(salary), 2)
    wantsBreakdown = round(budgeting_split.calculateWants(salary), 2)

    savings_wallet.addIncome(savingsBreakdown)
    needs_wallet.addIncome(needsBreakdown)
    wants_wallet.addIncome(wantsBreakdown)

    updated_dictionary = {
        "savings": savings_wallet.balance,
        "needs": needs_wallet.balance,
        "wants": wants_wallet.balance,
    }
    save_data(DATA_FILE, updated_dictionary)

    message = f"""
\nHere is this week's salary distribution:\n 
\tSavings = +${savingsBreakdown:.2f}
\tNeeds = +${needsBreakdown:.2f}
\tWants = +${wantsBreakdown:.2f}\n

Updating the relevant wallets...
    """

    return print(message)

balances = load_data(DATA_FILE)
def main():
    global balances
    budgeting_split = BudgetingSplit(savings=0.5, needs=0.4, wants=0.1)
    savings_wallet = Wallet(id="Savings", balance=balances.get("savings", 0))
    needs_wallet = Wallet(id="Needs", balance=balances.get("needs", 0))
    wants_wallet = Wallet(id="Wants", balance=balances.get("wants", 0))
    wallets = [savings_wallet, needs_wallet, wants_wallet]
    
    while True:
        os.system('clear' if os.name == 'posix' else 'cls')
        print(f"\n/////////////////////////////////////////////////\n//")
        print(f"// ----- Dylan's Budgeting Plan {budgeting_split} -----")
        print(f"// 1. Submit salary for this week")
        print(f"// 2. Add expenses")
        print(f"// 3. View balances")
        print(f"// 4. Exit")
        print(f"//\n///////////////////////////////////////////////\n")
        try:
            userInput = int(input((">> ")))
            if userInput == 1: 
                while True:
                    try:
                        salary = float(input(f"How much did you earn this week? "))
                        submitSalary(budgeting_split, salary, savings_wallet, needs_wallet, wants_wallet)
                        input("Press Enter to return to the menu...")
                        break
                    except:
                        print("Please enter an amount.")

            elif userInput == 2:
                print("\nWhere would you like the expense to occur?\n")
                for id, wallet in enumerate(wallets):
                    print(str(id+1) + ".", wallet.id + ":", "$" + str(wallet))
                
                backIndex = len(wallets) + 1

                print(f"{backIndex}. Go back")
                
                while True:
                    try:
                        targetIndex = int(input(f"\nSelect wallet: "))
                        if targetIndex == backIndex:
                            break
                        else:
                            targetWallet = wallets[targetIndex - 1]
                            expenseDescription = str(input("What did you spend on? "))
                            expenseValue = float(input("How much was it? "))
                            targetWallet.addExpense(expenseDescription, expenseValue)
                            print(targetWallet.expenses)
                            input("\nPress Enter to return to the menu...")
                            break

                    except:
                        print("Wallet choice invalid.")

            elif userInput == 3:
                print(f"""
Current balances:\n
\tSavings Account = ${savings_wallet}
\tNeeds Account = ${needs_wallet}
\tWants Account = ${wants_wallet}
                      """)
                input("Press Enter to return to the menu...")
            
            elif userInput == 4:
                print("Exiting...\n")
                break

            else:
                print("Error: Invalid selection")
        except ValueError: 
            print("Choose a valid option.") 
        
if __name__ == "__main__":
    main()

