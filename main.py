# main.py - Personal Expense Tracker for Replit
from flask import Flask, request, render_template_string, jsonify
import json
from datetime import datetime

app = Flask(__name__)

# Default expense categories
DEFAULT_CATEGORIES = [
    "Food & Dining", "Transportation", "Shopping", "Entertainment",
    "Bills & Utilities", "Healthcare", "Education", "Other"
]

# Payment methods
DEFAULT_PAYMENT_METHODS = ["Cash", "Digital (Esewa/Net Banking)", "Card (Credit/Debit)", "Other"]


@app.route('/')
def index():
    """Main page - serves the app interface. Data handled by JavaScript."""
    current_date = datetime.now().strftime('%Y-%m-%d')
    return render_template_string(HTML_TEMPLATE, 
                                default_categories=DEFAULT_CATEGORIES,
                                default_payment_methods=DEFAULT_PAYMENT_METHODS,
                                current_date=current_date)


@app.route('/api/load-demo', methods=['GET'])
def load_demo_data():
    """API endpoint to load demo data for first-time users."""
    demo_expenses = [
        {"id": 1, "item": "Coffee", "amount": 120.00, "category": "Food & Dining", 
         "date": datetime.now().strftime('%Y-%m-%d'), "payment_method": "Cash", "notes": "Morning coffee"},
        {"id": 2, "item": "Bus Fare", "amount": 50.00, "category": "Transportation", 
         "date": datetime.now().strftime('%Y-%m-%d'), "payment_method": "Card", "notes": "Commute to work"},
        {"id": 3, "item": "Netflix", "amount": 649.00, "category": "Entertainment", 
         "date": datetime.now().strftime('%Y-%m-%d'), "payment_method": "UPI", "notes": "Monthly subscription"}
    ]
    return jsonify(demo_expenses)

# CSS Styles
CSS_STYLES = '''
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
            border: none;
            cursor: pointer;
            font-size: 0.95rem;
            display: flex;
            align-items: center;
            gap: 8px;
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

        .copyright {
            text-align: center;
            margin-top: 30px;
            padding: 20px;
            color: white;
            font-size: 0.9rem;
            opacity: 0.8;
        }

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
    </style>
'''

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>💰 Personal Expense Tracker</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    ''' + CSS_STYLES + '''
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>💰 Personal Expense Tracker</h1>
            <p>Your data is stored privately in <strong>your own browser</strong>.</p>
            <div class="nav-links">
                <button onclick="window.location.reload()" class="nav-btn">
                    <span>🔄</span> Refresh
                </button>
                <button onclick="exportToCSV()" class="nav-btn secondary">
                    <span>📥</span> Export CSV
                </button>
                <button onclick="loadDemoData()" class="nav-btn" style="background: #ed8936;">
                    <span>🦄</span> Load Demo
                </button>
                <button onclick="clearAllData()" class="nav-btn" style="background: #f56565;">
                    <span>🗑️</span> Clear Data
                </button>
            </div>
        </div>

        <!-- Stats Dashboard -->
        <div class="stats-grid" id="statsDashboard">
            <!-- Filled by JavaScript -->
        </div>

        <!-- Add Expense Form -->
        <div class="form-container">
            <h2><span>➕</span> Add New Expense</h2>
            <form onsubmit="return addExpense(event)">
                <div class="form-grid">
                    <div class="form-group">
                        <input type="text" id="itemInput" placeholder="Item name" required>
                    </div>
                    <div class="form-group">
                        <input type="number" step="0.01" id="amountInput" placeholder="Amount (Rs.)" required>
                    </div>
                    <div class="form-group">
                        <select id="categoryInput">
                            <option value="">Select Category</option>
                            ''' + ''.join([f'<option value="{cat}">{cat}</option>' for cat in DEFAULT_CATEGORIES]) + '''
                        </select>
                    </div>
                    <div class="form-group">
                        <input type="date" id="dateInput" value="''' + datetime.now().strftime('%Y-%m-%d') + '''">
                    </div>
                    <div class="form-group">
                        <select id="paymentInput">
                            <option value="">Select Payment Method</option>
                            ''' + ''.join([f'<option value="{method}">{method}</option>' for method in DEFAULT_PAYMENT_METHODS]) + '''
                        </select>
                    </div>
                </div>
                <div class="form-group">
                    <textarea id="notesInput" placeholder="Notes (optional)" rows="2"></textarea>
                </div>
                <button type="submit" class="btn-primary">Add Expense</button>
            </form>
        </div>

        <!-- Filters & Expenses Table -->
        <div class="filters">
            <label for="categoryFilter">Filter by Category:</label>
            <select id="categoryFilter" onchange="filterExpenses()">
                <option value="">All Categories</option>
                <!-- Categories filled by JavaScript -->
            </select>
            <button onclick="clearFilter()" style="color: #f56565; background: none; border: none; cursor: pointer; margin-left: auto;">
                ✕ Clear Filter
            </button>
        </div>

        <div class="expenses-container">
            <h2><span>📝</span> Your Expenses</h2>
            <div id="expensesTable">
                <!-- Filled by JavaScript -->
            </div>
        </div>

        <!-- Copyright -->
        <div class="copyright">
            <p>© 2026 Bishnu Raj KC. All rights reserved. | Data stored locally in your browser.</p>
        </div>
    </div>

    <script>
        // ============================================
        // CORE DATA MANAGEMENT (LocalStorage)
        // ============================================
        const STORAGE_KEY = 'personal_expense_tracker_data';

        function getExpenses() {
            const data = localStorage.getItem(STORAGE_KEY);
            try {
                return data ? JSON.parse(data) : [];
            } catch (e) {
                console.error("Error parsing expenses:", e);
                return [];
            }
        }

        function saveExpenses(expenses) {
            localStorage.setItem(STORAGE_KEY, JSON.stringify(expenses));
            renderAll();
        }

        // ============================================
        // CORE APP FUNCTIONS
        // ============================================
        function addExpense(event) {
            event.preventDefault();

            // Get form values
            const item = document.getElementById('itemInput').value.trim();
            const amountInput = document.getElementById('amountInput').value;
            const category = document.getElementById('categoryInput').value || 'Other';
            const date = document.getElementById('dateInput').value;
            const paymentSelect = document.getElementById('paymentInput');
            const paymentMethod = paymentSelect.value ? paymentSelect.value : 'Cash';
            const notes = document.getElementById('notesInput').value.trim();

            // Validate inputs
            if (!item) {
                alert("Please enter an item name");
                return false;
            }

            const amount = parseFloat(amountInput);
            if (isNaN(amount) || amount <= 0) {
                alert("Please enter a valid amount greater than 0");
                return false;
            }

            if (!date) {
                alert("Please select a date");
                return false;
            }

            // Get current expenses and generate new ID
            const expenses = getExpenses();
            const newId = expenses.length > 0 ? Math.max(...expenses.map(e => e.id)) + 1 : 1;

            // Create new expense object
            const newExpense = {
                id: newId,
                item: item,
                amount: amount,
                category: category,
                date: date,
                payment_method: paymentMethod,
                notes: notes,
                created_at: new Date().toISOString()
            };

            // Add to expenses and save
            expenses.push(newExpense);
            saveExpenses(expenses);

            // Reset form (keep date as today)
            event.target.reset();
            document.getElementById('dateInput').value = "''' + datetime.now().strftime('%Y-%m-%d') + '''";

            // Focus back to first input
            document.getElementById('itemInput').focus();

            return false;
        }

        function editExpense(id) {
            const expenses = getExpenses();
            const expenseIndex = expenses.findIndex(e => e.id === id);

            if (expenseIndex === -1) return;

            const expense = expenses[expenseIndex];

            const newItem = prompt('Edit item name:', expense.item);
            if (newItem === null) return;

            const newAmount = prompt('Edit amount (Rs.):', expense.amount);
            if (newAmount === null) return;

            const amountValue = parseFloat(newAmount);
            if (isNaN(amountValue) || amountValue <= 0) {
                alert("Please enter a valid amount");
                return;
            }

            expense.item = newItem.trim();
            expense.amount = amountValue;

            saveExpenses(expenses);
        }

        function deleteExpense(id) {
            if (!confirm('Are you sure you want to delete this expense?')) return;

            const expenses = getExpenses();
            const filteredExpenses = expenses.filter(e => e.id !== id);

            saveExpenses(filteredExpenses);
        }

        function filterExpenses() {
            renderAll();
        }

        function clearFilter() {
            document.getElementById('categoryFilter').value = '';
            renderAll();
        }

        // ============================================
        // UI RENDERING FUNCTIONS
        // ============================================
        function renderStats() {
            const expenses = getExpenses();
            const filteredExpenses = getFilteredExpenses();
            const totalFiltered = filteredExpenses.reduce((sum, e) => sum + e.amount, 0);
            const totalAll = expenses.reduce((sum, e) => sum + e.amount, 0);
            const avg = expenses.length > 0 ? totalAll / expenses.length : 0;

            const statsHTML = `
                <div class="stat-card">
                    <h3>Filtered Total</h3>
                    <div class="value">Rs. ${totalFiltered.toFixed(2)}</div>
                    <div class="label">${filteredExpenses.length} expense(s)</div>
                </div>
                <div class="stat-card">
                    <h3>All-Time Total</h3>
                    <div class="value">Rs. ${totalAll.toFixed(2)}</div>
                    <div class="label">${expenses.length} total expenses</div>
                </div>
                <div class="stat-card">
                    <h3>Average</h3>
                    <div class="value">Rs. ${avg.toFixed(2)}</div>
                    <div class="label">Per expense average</div>
                </div>
            `;

            document.getElementById('statsDashboard').innerHTML = statsHTML;
        }

        function renderExpensesTable() {
            const expenses = getFilteredExpenses();
            const container = document.getElementById('expensesTable');

            if (expenses.length === 0) {
                container.innerHTML = `
                    <div class="no-expenses">
                        <div>📊</div>
                        <h3>No expenses recorded yet</h3>
                        <p>Add your first expense using the form above!</p>
                    </div>
                `;
                return;
            }

            let tableHTML = `
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
            `;

            expenses.forEach(exp => {
                tableHTML += `
                    <tr>
                        <td>${exp.date}</td>
                        <td><strong>${exp.item}</strong></td>
                        <td><span class="category-badge">${exp.category}</span></td>
                        <td class="amount">Rs. ${exp.amount.toFixed(2)}</td>
                        <td>${exp.payment_method}</td>
                        <td>${exp.notes ? (exp.notes.length > 30 ? exp.notes.substring(0, 30) + '...' : exp.notes) : ''}</td>
                        <td class="actions">
                            <button onclick="editExpense(${exp.id})" class="btn-edit">Edit</button>
                            <button onclick="deleteExpense(${exp.id})" class="btn-delete">Delete</button>
                        </td>
                    </tr>
                `;
            });

            tableHTML += '</tbody></table>';
            container.innerHTML = tableHTML;
        }

        function renderCategoryFilter() {
            const expenses = getExpenses();
            const categories = [...new Set(expenses.map(e => e.category))].sort();
            const select = document.getElementById('categoryFilter');

            const currentValue = select.value;
            select.innerHTML = '<option value="">All Categories</option>';

            categories.forEach(cat => {
                const option = document.createElement('option');
                option.value = cat;
                option.textContent = cat;
                option.selected = (cat === currentValue);
                select.appendChild(option);
            });
        }

        function getFilteredExpenses() {
            const expenses = getExpenses();
            const filterValue = document.getElementById('categoryFilter').value;
            if (!filterValue) return expenses;
            return expenses.filter(e => e.category === filterValue);
        }

        function renderAll() {
            renderStats();
            renderExpensesTable();
            renderCategoryFilter();
        }

        // ============================================
        // UTILITY FUNCTIONS
        // ============================================
        async function loadDemoData() {
            if (!confirm('Load demo expenses? This will add sample data to your current list.')) return;

            try {
                console.log("Fetching demo data...");
                const response = await fetch('/api/load-demo');

                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }

                const demoExpenses = await response.json();
                console.log("Demo data received:", demoExpenses);

                const currentExpenses = getExpenses();
                console.log("Current expenses:", currentExpenses);

                // Calculate next available ID
                const maxId = currentExpenses.length > 0 
                    ? Math.max(...currentExpenses.map(e => e.id)) 
                    : 0;

                console.log("Max ID:", maxId);

                // Update IDs for demo expenses
                demoExpenses.forEach((exp, index) => {
                    exp.id = maxId + index + 1;
                });

                console.log("Updated demo expenses:", demoExpenses);

                // Combine and save
                const allExpenses = [...currentExpenses, ...demoExpenses];
                saveExpenses(allExpenses);

                alert(`Demo data loaded successfully! Added ${demoExpenses.length} items.`);

            } catch (error) {
                console.error("Error loading demo data:", error);

                // Fallback data
                const currentExpenses = getExpenses();
                const nextId = currentExpenses.length > 0 
                    ? Math.max(...currentExpenses.map(e => e.id)) + 1 
                    : 1;

                const fallbackDemo = [
                    {
                        id: nextId, 
                        item: "Coffee", 
                        amount: 120.00, 
                        category: "Food & Dining", 
                        date: new Date().toISOString().split('T')[0], 
                        payment_method: "Cash", 
                        notes: "Morning coffee"
                    },
                    {
                        id: nextId + 1, 
                        item: "Bus Fare", 
                        amount: 50.00, 
                        category: "Transportation", 
                        date: new Date().toISOString().split('T')[0], 
                        payment_method: "Card", 
                        notes: "Commute"
                    },
                    {
                        id: nextId + 2, 
                        item: "Netflix", 
                        amount: 649.00, 
                        category: "Entertainment", 
                        date: new Date().toISOString().split('T')[0], 
                        payment_method: "UPI", 
                        notes: "Monthly subscription"
                    }
                ];

                const allExpenses = [...currentExpenses, ...fallbackDemo];
                saveExpenses(allExpenses);

                alert('Demo data loaded (using fallback)!');
            }
        }

        function exportToCSV() {
            const expenses = getExpenses();
            if (expenses.length === 0) {
                alert('No expenses to export!');
                return;
            }

            let csv = 'ID,Item,Amount,Category,Date,Payment Method,Notes\\n';
            expenses.forEach(exp => {
                const escapedNotes = exp.notes ? exp.notes.replace(/"/g, '""') : '';
                csv += `${exp.id},${exp.item},${exp.amount},${exp.category},${exp.date},${exp.payment_method},"${escapedNotes}"\\n`;
            });

            const blob = new Blob([csv], { type: 'text/csv' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `my-expenses-${new Date().toISOString().slice(0,10)}.csv`;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            URL.revokeObjectURL(url);
        }

        function clearAllData() {
            if (confirm('⚠️ WARNING: This will permanently delete ALL your expense data. Continue?')) {
                localStorage.removeItem(STORAGE_KEY);
                alert('All data cleared!');
                renderAll();
            }
        }

        // ============================================
        // INITIALIZE APP ON PAGE LOAD
        // ============================================
        document.addEventListener('DOMContentLoaded', () => {
            console.log("App initialized");

            // Check if first time user
            const expenses = getExpenses();
            console.log("Initial expenses:", expenses);

            if (expenses.length === 0) {
                setTimeout(() => {
                    if (confirm('👋 Welcome! Would you like to load some demo expenses to see how the app works?')) {
                        loadDemoData();
                    }
                }, 500);
            }

            // Initial render
            renderAll();

            // Set today's date if not set
            if (!document.getElementById('dateInput').value) {
                document.getElementById('dateInput').value = new Date().toISOString().split('T')[0];
            }

            // Focus on item input
            document.getElementById('itemInput').focus();
        });
    </script>
</body>
</html>
'''

if __name__ == '__main__':
    print('=' * 60)
    print('💰 PERSONAL EXPENSE TRACKER (Browser-Based)')
    print('=' * 60)
    print('🌐 Each user gets their own private data in their browser.')
    print('💾 No data is stored on the server.')
    print('📱 Fully mobile-compatible design.')
    print('🚀 Open the webview to start using the app!')
    print('© 2026 Bishnu Raj KC. All rights reserved.')
    print('=' * 60)
    app.run(host='0.0.0.0', port=5000, debug=True)