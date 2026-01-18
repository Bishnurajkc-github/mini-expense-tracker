'''
# mini_expense_tracker.py
expenses = []

while True:
    print("\n📊 MINI EXPENSE TRACKER")
    print("1. Add Expense")
    print("2. View All")
    print("3. Total")
    print("4. Exit")

    choice = input("Choose (1-4): ")

    if choice == "1":
        item = input("Item: ")
        amount = float(input("Amount: "))
        expenses.append({"item": item, "amount": amount})
        print(f"✅ Added: {item} - ₹{amount}")

    elif choice == "2":
        if not expenses:
            print("No expenses yet")
        else:
            print("\n📝 ALL EXPENSES:")
            for i, exp in enumerate(expenses, 1):
                print(f"{i}. {exp['item']}: ₹{exp['amount']}")

    elif choice == "3":
        total = sum(exp["amount"] for exp in expenses)
        print(f"💰 TOTAL: ₹{total}")

    elif choice == "4":
        print("👋 Goodbye!")
        break

    else:
        print("❌ Invalid choice")  '''

# Flask version Python code starts from below:

# flask_expense_tracker.py
from flask import Flask, request, render_template_string

app = Flask(__name__)
expenses = []

html = '''
<!DOCTYPE html>
<html>
<body style="font-family: Arial; padding: 20px;">
    <h2>💰 Expense Tracker</h2>
    <form method="POST">
        <input name="item" placeholder="Item" required>
        <input name="amount" type="number" step="0.01" placeholder="Amount" required>
        <button>Add</button>
    </form>
    <hr>
    <h3>📝 Expenses:</h3>
    {% for e in expenses %}
    <p>{{ e.item }}: ₹{{ e.amount }}</p>
    {% endfor %}
    {% if expenses %}
    <h3>💰 Total: ₹{{ total }}</h3>
    {% endif %}
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def tracker():
    if request.method == 'POST':
        item = request.form.get('item')
        amount = float(request.form.get('amount', 0))
        expenses.append({'item': item, 'amount': amount})

    total = sum(e['amount'] for e in expenses)
    return render_template_string(html, expenses=expenses, total=total)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)