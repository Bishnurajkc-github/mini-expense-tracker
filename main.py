# main.py - Advanced Expense Tracker for Replit
from flask import Flask, request, render_template_string, redirect, url_for
import json
import os
from datetime import datetime
from collections import defaultdict

app = Flask(__name__)

# File to store expenses
DATA_FILE = "expenses.json"

# Default expense categories
DEFAULT_CATEGORIES = [
    "Food & Dining", "Transportation", "Shopping", "Entertainment",
    "Bills & Utilities", "Healthcare", "Education", "Other"
]

def load_expenses():
    """Load expenses from JSON file"""
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r') as f:
                return json.load(f)
        except:
            return []
    return []

def save_expenses(expenses):
    """Save expenses to JSON file"""
    try:
        with open(DATA_FILE, 'w') as f:
            json.dump(expenses, f, indent=2)
        return True
    except:
        return False

def get_stats(expenses):
    """Calculate statistics"""
    if not expenses:
        return {'total': 0, 'count': 0, 'average': 0}

    total = sum(e['amount'] for e in expenses)
    count = len(expenses)
    average = total / count if count > 0 else 0

    return {
        'total': total,
        'count': count,
        'average': average
    }

@app.route('/', methods=['GET', 'POST'])
def index():
    """Main page - shows all expenses and add form"""
    expenses = load_expenses()
    stats = get_stats(expenses)

    # Get filter parameters from URL
    category_filter = request.args.get('category', '')

    # Apply filters if provided
    filtered_expenses = expenses.copy()
    if category_filter:
        filtered_expenses = [e for e in filtered_expenses if e.get('category', '') == category_filter]

    # Get unique categories for filter dropdown
    categories = sorted(set(e.get('category', 'Other') for e in expenses))

    # Handle POST request for adding expenses
    if request.method == 'POST':
        # Generate ID
        new_id = max([e.get('id', 0) for e in expenses], default=0) + 1

        # Get form data
        item = request.form.get('item', '').strip()
        try:
            amount = float(request.form.get('amount', 0))
        except:
            amount = 0
        category = request.form.get('category', 'Other').strip()
        date = request.form.get('date', datetime.now().strftime('%Y-%m-%d'))
        payment_method = request.form.get('payment_method', 'Cash').strip()
        notes = request.form.get('notes', '').strip()

        # Create expense dictionary
        expense = {
            'id': new_id,
            'item': item,
            'amount': amount,
            'category': category,
            'date': date,
            'payment_method': payment_method,
            'notes': notes,
            'created_at': datetime.now().isoformat()
        }

        expenses.append(expense)
        save_expenses(expenses)
        return redirect('/')

    return render_template_string(HTML_TEMPLATE, 
                                expenses=filtered_expenses,
                                stats=stats,
                                categories=categories,
                                default_categories=DEFAULT_CATEGORIES,
                                category_filter=category_filter,
                                now=datetime.now())

@app.route('/edit/<int:expense_id>', methods=['GET', 'POST'])
def edit_expense(expense_id):
    """Edit an existing expense"""
    expenses = load_expenses()

    # Find the expense to edit
    expense_to_edit = None
    for expense in expenses:
        if expense.get('id') == expense_id:
            expense_to_edit = expense
            break

    if not expense_to_edit:
        return redirect('/')

    if request.method == 'POST':
        # Update expense data
        expense_to_edit['item'] = request.form.get('item', expense_to_edit['item'])
        try:
            expense_to_edit['amount'] = float(request.form.get('amount', expense_to_edit['amount']))
        except:
            pass
        expense_to_edit['category'] = request.form.get('category', expense_to_edit.get('category', 'Other'))
        expense_to_edit['date'] = request.form.get('date', expense_to_edit['date'])
        expense_to_edit['payment_method'] = request.form.get('payment_method', expense_to_edit.get('payment_method', 'Cash'))
        expense_to_edit['notes'] = request.form.get('notes', expense_to_edit.get('notes', ''))

        save_expenses(expenses)
        return redirect('/')

    # For GET request, show edit form
    return render_template_string(EDIT_TEMPLATE, 
                                expense=expense_to_edit,
                                default_categories=DEFAULT_CATEGORIES)

@app.route('/delete/<int:expense_id>')
def delete_expense(expense_id):
    """Delete an expense"""
    expenses = load_expenses()

    # Remove expense with matching ID
    expenses = [e for e in expenses if e.get('id') != expense_id]

    # Reassign IDs
    for i, expense in enumerate(expenses, 1):
        expense['id'] = i

    save_expenses(expenses)
    return redirect('/')

@app.route('/export')
def export_csv():
    """Export expenses to CSV"""
    expenses = load_expenses()

    if not expenses:
        return "No expenses to export", 404

    # Convert to CSV format
    csv_data = "ID,Item,Amount,Category,Date,Payment Method,Notes\n"
    for exp in expenses:
        csv_data += f"{exp.get('id', '')},{exp.get('item', '')},{exp.get('amount', '')},"
        csv_data += f"{exp.get('category', '')},{exp.get('date', '')},"
        csv_data += f"{exp.get('payment_method', '')},\"{exp.get('notes', '')}\"\n"

    # Return CSV as downloadable file
    from flask import make_response
    response = make_response(csv_data)
    response.headers["Content-Disposition"] = "attachment; filename=expenses.csv"
    response.headers["Content-Type"] = "text/csv"

    return response

@app.route('/summary')
def summary():
    """Show detailed summary"""
    expenses = load_expenses()

    if not expenses:
        return render_template_string(SUMMARY_TEMPLATE, 
                                    category_totals={}, 
                                    monthly_totals={},
                                    total=0,
                                    expense_count=0)

    # Calculate category totals
    category_totals = defaultdict(float)
    for exp in expenses:
        category = exp.get('category', 'Other')
        category_totals[category] += exp.get('amount', 0)

    # Calculate monthly totals
    monthly_totals = defaultdict(float)
    for exp in expenses:
        month = exp.get('date', '')[:7]  # Get YYYY-MM
        if month:
            monthly_totals[month] += exp.get('amount', 0)

    total = sum(exp.get('amount', 0) for exp in expenses)

    return render_template_string(SUMMARY_TEMPLATE,
                                category_totals=dict(category_totals),
                                monthly_totals=dict(monthly_totals),
                                total=total,
                                expense_count=len(expenses))

# HTML Templates
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>💰 Advanced Expense Tracker</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
            line-height: 1.6;
            color: #333;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
        }

        .header {
            background: rgba(255, 255, 255, 0.95);
            border-radius: 20px;
            padding: 30px;
            margin-bottom: 25px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.1);
            text-align: center;
        }

        .header h1 {
            color: #2d3748;
            font-size: 2.8rem;
            margin-bottom: 10px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .header p {
            color: #718096;
            font-size: 1.1rem;
        }

        .nav-links {
            display: flex;
            justify-content: center;
            gap: 15px;
            margin-top: 25px;
            flex-wrap: wrap;
        }

        .nav-btn {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 12px 25px;
            border-radius: 50px;
            text-decoration: none;
            font-weight: 600;
            transition: all 0.3s ease;
            display: flex;
            align-items: center;
            gap: 8px;
            border: none;
            cursor: pointer;
            font-size: 0.95rem;
        }

        .nav-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 20px rgba(102, 126, 234, 0.3);
        }

        .nav-btn.secondary {
            background: #48bb78;
        }

        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 25px;
        }

        .stat-card {
            background: rgba(255, 255, 255, 0.95);
            border-radius: 20px;
            padding: 25px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.08);
            transition: all 0.3s ease;
            text-align: center;
        }

        .stat-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 15px 40px rgba(0,0,0,0.12);
        }

        .stat-card h3 {
            color: #4a5568;
            font-size: 1rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 10px;
        }

        .stat-card .value {
            font-size: 2.5rem;
            font-weight: 700;
            color: #2d3748;
            margin: 10px 0;
        }

        .stat-card .label {
            color: #718096;
            font-size: 0.9rem;
        }

        .form-container {
            background: rgba(255, 255, 255, 0.95);
            border-radius: 20px;
            padding: 30px;
            margin-bottom: 25px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.1);
        }

        .form-container h2 {
            color: #2d3748;
            margin-bottom: 25px;
            font-size: 1.5rem;
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .form-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 20px;
        }

        .form-group {
            margin-bottom: 15px;
        }

        input, select, textarea {
            width: 100%;
            padding: 15px;
            border: 2px solid #e2e8f0;
            border-radius: 12px;
            font-size: 1rem;
            transition: all 0.3s ease;
            background: white;
        }

        input:focus, select:focus, textarea:focus {
            outline: none;
            border-color: #667eea;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        }

        .btn-primary {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 16px 40px;
            border: none;
            border-radius: 12px;
            font-size: 1.1rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            width: 100%;
            margin-top: 10px;
        }

        .btn-primary:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 25px rgba(102, 126, 234, 0.3);
        }

        .filters {
            background: rgba(255, 255, 255, 0.95);
            border-radius: 20px;
            padding: 20px;
            margin-bottom: 25px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.08);
            display: flex;
            align-items: center;
            gap: 15px;
            flex-wrap: wrap;
        }

        .filters label {
            font-weight: 600;
            color: #4a5568;
        }

        .expenses-container {
            background: rgba(255, 255, 255, 0.95);
            border-radius: 20px;
            padding: 30px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.1);
            margin-bottom: 30px;
        }

        .expenses-container h2 {
            color: #2d3748;
            margin-bottom: 25px;
            font-size: 1.5rem;
            display: flex;
            align-items: center;
            gap: 10px;
        }

        table {
            width: 100%;
            border-collapse: separate;
            border-spacing: 0;
        }

        thead {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        }

        th {
            padding: 20px;
            text-align: left;
            color: white;
            font-weight: 600;
            font-size: 0.9rem;
            text-transform: uppercase;
            letter-spacing: 1px;
        }

        th:first-child {
            border-top-left-radius: 12px;
        }

        th:last-child {
            border-top-right-radius: 12px;
        }

        td {
            padding: 20px;
            border-bottom: 1px solid #e2e8f0;
        }

        tr:hover td {
            background: #f7fafc;
        }

        .category-badge {
            display: inline-block;
            padding: 8px 16px;
            border-radius: 50px;
            font-size: 0.85rem;
            font-weight: 600;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }

        .amount {
            font-weight: 700;
            color: #e53e3e;
            font-size: 1.1rem;
        }

        .actions {
            display: flex;
            gap: 10px;
        }

        .btn-edit, .btn-delete {
            padding: 8px 16px;
            border-radius: 8px;
            text-decoration: none;
            font-weight: 600;
            font-size: 0.85rem;
            transition: all 0.3s ease;
            border: none;
            cursor: pointer;
        }

        .btn-edit {
            background: #48bb78;
            color: white;
        }

        .btn-delete {
            background: #f56565;
            color: white;
        }

        .btn-edit:hover, .btn-delete:hover {
            transform: translateY(-2px);
        }

        .no-expenses {
            text-align: center;
            padding: 60px 20px;
            color: #718096;
        }

        .no-expenses i {
            font-size: 4rem;
            margin-bottom: 20px;
            opacity: 0.5;
        }

        /* Copyright Section */
        .copyright {
            text-align: center;
            margin-top: 30px;
            padding: 20px;
            color: white;
            font-size: 0.9rem;
            opacity: 0.8;
        }

        /* Responsive design */
        @media (max-width: 768px) {
            .header h1 {
                font-size: 2rem;
            }

            .stats-grid {
                grid-template-columns: 1fr;
            }

            .form-grid {
                grid-template-columns: 1fr;
            }

            table {
                display: block;
                overflow-x: auto;
            }

            .nav-links {
                flex-direction: column;
                align-items: center;
            }

            .nav-btn {
                width: 100%;
                justify-content: center;
            }
        }

        .flash-message {
            background: #48bb78;
            color: white;
            padding: 15px;
            border-radius: 12px;
            margin-bottom: 20px;
            text-align: center;
            animation: slideIn 0.3s ease;
        }

        @keyframes slideIn {
            from {
                opacity: 0;
                transform: translateY(-20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>💰 Advanced Expense Tracker</h1>
            <p>Track your expenses easily and efficiently</p>

            <div class="nav-links">
                <a href="/" class="nav-btn">
                    <span>🏠</span> Dashboard
                </a>
                <a href="/summary" class="nav-btn secondary">
                    <span>📊</span> Summary
                </a>
                <a href="/export" class="nav-btn" style="background: #ed8936;">
                    <span>📥</span> Export CSV
                </a>
            </div>
        </div>

        <div class="stats-grid">
            <div class="stat-card">
                <h3>Total Expenses</h3>
                <div class="value">Rs. {{ "%.2f"|format(stats.total) }}</div>
                <div class="label">Overall spending</div>
            </div>

            <div class="stat-card">
                <h3>Number of Expenses</h3>
                <div class="value">{{ stats.count }}</div>
                <div class="label">Total transactions</div>
            </div>

            <div class="stat-card">
                <h3>Average per Expense</h3>
                <div class="value">Rs. {{ "%.2f"|format(stats.average) }}</div>
                <div class="label">Per transaction average</div>
            </div>
        </div>

        <div class="form-container">
            <h2><span>➕</span> Add New Expense</h2>
            <form method="POST">
                <div class="form-grid">
                    <div class="form-group">
                        <input type="text" name="item" placeholder="Item name" required>
                    </div>

                    <div class="form-group">
                        <input type="number" step="0.01" name="amount" placeholder="Amount (Rs.)" required>
                    </div>

                    <div class="form-group">
                        <select name="category">
                            <option value="">Select Category</option>
                            {% for cat in default_categories %}
                            <option value="{{ cat }}">{{ cat }}</option>
                            {% endfor %}
                        </select>
                    </div>

                    <div class="form-group">
                        <input type="date" name="date" value="{{ now.strftime('%Y-%m-%d') }}">
                    </div>

                    <div class="form-group">
                        <input type="text" name="payment_method" placeholder="Payment Method">
                    </div>
                </div>

                <div class="form-group">
                    <textarea name="notes" placeholder="Notes (optional)" rows="2"></textarea>
                </div>

                <button type="submit" class="btn-primary">
                    Add Expense
                </button>
            </form>
        </div>

        <div class="filters">
            <label for="category-filter">Filter by Category:</label>
            <select id="category-filter" onchange="window.location.href=this.value ? '/?category=' + this.value : '/'">
                <option value="">All Categories</option>
                {% for cat in categories %}
                <option value="{{ cat }}" {% if cat == category_filter %}selected{% endif %}>{{ cat }}</option>
                {% endfor %}
            </select>

            {% if category_filter %}
            <a href="/" style="color: #f56565; text-decoration: none; margin-left: auto;">
                ✕ Clear Filter
            </a>
            {% endif %}
        </div>

        <div class="expenses-container">
            <h2><span>📝</span> All Expenses</h2>

            {% if expenses %}
            <table>
                <thead>
                    <tr>
                        <th>Date</th>
                        <th>Item</th>
                        <th>Category</th>
                        <th>Amount</th>
                        <th>Payment</th>
                        <th>Notes</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
                    {% for expense in expenses %}
                    <tr>
                        <td>{{ expense.date }}</td>
                        <td><strong>{{ expense.item }}</strong></td>
                        <td><span class="category-badge">{{ expense.category }}</span></td>
                        <td class="amount">Rs. {{ "%.2f"|format(expense.amount) }}</td>
                        <td>{{ expense.payment_method }}</td>
                        <td>{{ expense.notes[:30] }}{% if expense.notes|length > 30 %}...{% endif %}</td>
                        <td class="actions">
                            <a href="/edit/{{ expense.id }}" class="btn-edit">Edit</a>
                            <a href="/delete/{{ expense.id }}" class="btn-delete" 
                               onclick="return confirm('Are you sure you want to delete this expense?')">
                                Delete
                            </a>
                        </td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
            {% else %}
            <div class="no-expenses">
                <div>📊</div>
                <h3>No expenses recorded yet</h3>
                <p>Add your first expense using the form above!</p>
            </div>
            {% endif %}
        </div>

        <!-- Copyright Section -->
        <div class="copyright">
            <p>© 2026 Bishnu Raj KC. All rights reserved.</p>
        </div>
    </div>
</body>
</html>
'''

EDIT_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Edit Expense</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
            line-height: 1.6;
            color: #333;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
            display: flex;
            align-items: center;
            justify-content: center;
        }

        .edit-container {
            background: white;
            border-radius: 20px;
            padding: 40px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.2);
            max-width: 600px;
            width: 100%;
        }

        .edit-header {
            text-align: center;
            margin-bottom: 30px;
        }

        .edit-header h2 {
            color: #2d3748;
            font-size: 2rem;
            margin-bottom: 10px;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 10px;
        }

        .edit-header p {
            color: #718096;
        }

        .form-group {
            margin-bottom: 20px;
        }

        label {
            display: block;
            margin-bottom: 8px;
            font-weight: 600;
            color: #4a5568;
        }

        input, select, textarea {
            width: 100%;
            padding: 15px;
            border: 2px solid #e2e8f0;
            border-radius: 12px;
            font-size: 1rem;
            transition: all 0.3s ease;
        }

        input:focus, select:focus, textarea:focus {
            outline: none;
            border-color: #667eea;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        }

        .button-group {
            display: flex;
            gap: 15px;
            margin-top: 30px;
        }

        .btn-save, .btn-cancel {
            flex: 1;
            padding: 16px;
            border: none;
            border-radius: 12px;
            font-size: 1rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            text-align: center;
            text-decoration: none;
        }

        .btn-save {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }

        .btn-cancel {
            background: #e2e8f0;
            color: #4a5568;
        }

        .btn-save:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 25px rgba(102, 126, 234, 0.3);
        }

        .btn-cancel:hover {
            background: #cbd5e0;
        }

        /* Copyright Section */
        .copyright {
            text-align: center;
            margin-top: 30px;
            padding: 20px;
            color: white;
            font-size: 0.9rem;
            opacity: 0.8;
        }
    </style>
</head>
<body>
    <div class="edit-container">
        <div class="edit-header">
            <h2><span>✏️</span> Edit Expense</h2>
            <p>Update your expense details</p>
        </div>

        <form method="POST">
            <div class="form-group">
                <label>Item Name</label>
                <input type="text" name="item" value="{{ expense.item }}" required>
            </div>

            <div class="form-group">
                <label>Amount (Rs.)</label>
                <input type="number" step="0.01" name="amount" value="{{ expense.amount }}" required>
            </div>

            <div class="form-group">
                <label>Category</label>
                <select name="category">
                    {% for cat in default_categories %}
                    <option value="{{ cat }}" {% if cat == expense.category %}selected{% endif %}>{{ cat }}</option>
                    {% endfor %}
                    {% if expense.category not in default_categories %}
                    <option value="{{ expense.category }}" selected>{{ expense.category }} (Custom)</option>
                    {% endif %}
                </select>
            </div>

            <div class="form-group">
                <label>Date</label>
                <input type="date" name="date" value="{{ expense.date }}">
            </div>

            <div class="form-group">
                <label>Payment Method</label>
                <input type="text" name="payment_method" value="{{ expense.payment_method }}">
            </div>

            <div class="form-group">
                <label>Notes</label>
                <textarea name="notes" rows="3">{{ expense.notes }}</textarea>
            </div>

            <div class="button-group">
                <a href="/" class="btn-cancel">Cancel</a>
                <button type="submit" class="btn-save">Save Changes</button>
            </div>
        </form>

        <!-- Copyright Section -->
        <div class="copyright">
            <p>© 2026 Bishnu Raj KC. All rights reserved.</p>
        </div>
    </div>
</body>
</html>
'''

SUMMARY_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Expense Summary</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
            line-height: 1.6;
            color: #333;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
        }

        .header {
            background: rgba(255, 255, 255, 0.95);
            border-radius: 20px;
            padding: 30px;
            margin-bottom: 25px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.1);
            text-align: center;
        }

        .header h1 {
            color: #2d3748;
            font-size: 2.5rem;
            margin-bottom: 10px;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 15px;
        }

        .back-btn {
            display: inline-block;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 12px 25px;
            border-radius: 50px;
            text-decoration: none;
            font-weight: 600;
            margin-top: 20px;
            transition: all 0.3s ease;
        }

        .back-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 25px rgba(102, 126, 234, 0.3);
        }

        .summary-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 25px;
            margin-bottom: 25px;
        }

        .summary-card {
            background: rgba(255, 255, 255, 0.95);
            border-radius: 20px;
            padding: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.08);
        }

        .summary-card h2 {
            color: #2d3748;
            margin-bottom: 25px;
            font-size: 1.3rem;
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .category-item, .monthly-item {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 15px 0;
            border-bottom: 1px solid #e2e8f0;
        }

        .category-item:last-child, .monthly-item:last-child {
            border-bottom: none;
        }

        .category-name {
            font-weight: 600;
            color: #4a5568;
        }

        .amount {
            font-weight: 700;
            color: #e53e3e;
        }

        .percentage {
            color: #718096;
            font-size: 0.9rem;
        }

        .progress-bar {
            flex-grow: 1;
            height: 8px;
            background: #e2e8f0;
            border-radius: 4px;
            margin: 0 15px;
            overflow: hidden;
        }

        .progress {
            height: 100%;
            background: linear-gradient(90deg, #667eea, #764ba2);
            border-radius: 4px;
        }

        .overall-stats {
            background: rgba(255, 255, 255, 0.95);
            border-radius: 20px;
            padding: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.08);
            margin-bottom: 30px;
        }

        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            padding: 20px 0;
        }

        .stat-item {
            text-align: center;
        }

        .stat-label {
            font-size: 0.9rem;
            color: #718096;
            margin-bottom: 5px;
        }

        .stat-value {
            font-size: 2rem;
            font-weight: 700;
            color: #2d3748;
        }

        /* Copyright Section */
        .copyright {
            text-align: center;
            margin-top: 30px;
            padding: 20px;
            color: white;
            font-size: 0.9rem;
            opacity: 0.8;
        }

        @media (max-width: 768px) {
            .summary-grid {
                grid-template-columns: 1fr;
            }

            .stats-grid {
                grid-template-columns: 1fr;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1><span>📊</span> Expense Summary</h1>
            <a href="/" class="back-btn">
                ← Back to Dashboard
            </a>
        </div>

        <div class="summary-grid">
            <div class="summary-card">
                <h2><span>📂</span> Expenses by Category</h2>
                {% if category_totals %}
                    {% for category, amount in category_totals.items()|sort(attribute='1', reverse=True) %}
                    <div class="category-item">
                        <span class="category-name">{{ category }}</span>
                        <div class="progress-bar">
                            <div class="progress" style="width: {{ (amount/total*100 if total > 0 else 0)|round }}%"></div>
                        </div>
                        <div style="text-align: right;">
                            <div class="amount">Rs. {{ "%.2f"|format(amount) }}</div>
                            <div class="percentage">
                                {{ "%.1f"|format(amount/total*100 if total > 0 else 0) }}%
                            </div>
                        </div>
                    </div>
                    {% endfor %}
                {% else %}
                    <p style="text-align: center; color: #718096; padding: 20px;">
                        No category data available
                    </p>
                {% endif %}
            </div>

            <div class="summary-card">
                <h2><span>📅</span> Monthly Breakdown</h2>
                {% if monthly_totals %}
                    {% for month, amount in monthly_totals.items()|sort(reverse=True) %}
                    <div class="monthly-item">
                        <span class="category-name">{{ month }}</span>
                        <div class="progress-bar">
                            <div class="progress" style="width: {{ (amount/total*100 if total > 0 else 0)|round }}%"></div>
                        </div>
                        <div class="amount">Rs. {{ "%.2f"|format(amount) }}</div>
                    </div>
                    {% endfor %}
                {% else %}
                    <p style="text-align: center; color: #718096; padding: 20px;">
                        No monthly data available
                    </p>
                {% endif %}
            </div>
        </div>

        <div class="overall-stats">
            <h2><span>💰</span> Overall Statistics</h2>
            <div class="stats-grid">
                <div class="stat-item">
                    <div class="stat-label">Total Expenses</div>
                    <div class="stat-value">Rs. {{ "%.2f"|format(total) }}</div>
                </div>
                <div class="stat-item">
                    <div class="stat-label">Number of Expenses</div>
                    <div class="stat-value">{{ expense_count }}</div>
                </div>
                <div class="stat-item">
                    <div class="stat-label">Average per Expense</div>
                    <div class="stat-value">
                        Rs. {{ "%.2f"|format(total/expense_count if expense_count > 0 else 0) }}
                    </div>
                </div>
            </div>
        </div>

        <!-- Copyright Section -->
        <div class="copyright">
            <p>© 2026 Bishnu Raj KC. All rights reserved.</p>
        </div>
    </div>
</body>
</html>
'''

# Run the app
if __name__ == '__main__':
    print("=" * 60)
    print("💰 ADVANCED EXPENSE TRACKER")
    print("=" * 60)
    print("🚀 Starting server...")
    print("🌐 Open the webview or click the URL that appears above")
    print("💾 Data is automatically saved to 'expenses.json'")
    print("© 2026 Bishnu Raj KC. All rights reserved.")
    print("=" * 60)
    app.run(host='0.0.0.0', port=5000, debug=True)