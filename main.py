# main.py - Personal Expense Tracker for Replit
from flask import Flask, request, render_template_string, jsonify
import json
from datetime import datetime
from collections import defaultdict

app = Flask(__name__)

# We no longer need a global DATA_FILE. Each user's data stays in their browser.

# Default expense categories remain the same
DEFAULT_CATEGORIES = [
    "Food & Dining", "Transportation", "Shopping", "Entertainment",
    "Bills & Utilities", "Healthcare", "Education", "Other"
]

@app.route('/')
def index():
    """Main page - serves the app interface. Data handled by JavaScript."""
    return render_template_string(HTML_TEMPLATE, default_categories=DEFAULT_CATEGORIES)

# ============================================
# NEW: Optional API Endpoints for Advanced Use
# ============================================
# These are NOT required for basic Option B but show how a hybrid approach works.
@app.route('/api/load-demo', methods=['GET'])
def load_demo_data():
    """(Optional) API endpoint to load demo data for first-time users."""
    demo_expenses = [
        {"id": 1, "item": "Coffee", "amount": 120.00, "category": "Food & Dining", "date": datetime.now().strftime('%Y-%m-%d'), "payment_method": "Cash", "notes": "Morning coffee"},
        {"id": 2, "item": "Bus Fare", "amount": 50.00, "category": "Transportation", "date": datetime.now().strftime('%Y-%m-%d'), "payment_method": "Card", "notes": "Commute to work"},
        {"id": 3, "item": "Netflix", "amount": 649.00, "category": "Entertainment", "date": datetime.now().strftime('%Y-%m-%d'), "payment_method": "UPI", "notes": "Monthly subscription"}
    ]
    return jsonify(demo_expenses)

# ============================================
# MAIN HTML TEMPLATE WITH JAVASCRIPT
# ============================================
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>💰 Personal Expense Tracker</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        /* [Keep ALL your CSS styles from the previous version exactly as they were] */
        /* This ensures mobile compatibility and beautiful design remains. */
    </style>
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
            <form onsubmit="addExpense(event)">
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
                            {% for cat in default_categories %}
                            <option value="{{ cat }}">{{ cat }}</option>
                            {% endfor %}
                        </select>
                    </div>
                    <div class="form-group">
                        <input type="date" id="dateInput" value="''' + datetime.now().strftime('%Y-%m-%d') + '''">
                    </div>
                    <div class="form-group">
                        <input type="text" id="paymentInput" placeholder="Payment Method">
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
            return data ? JSON.parse(data) : [];
        }

        function saveExpenses(expenses) {
            localStorage.setItem(STORAGE_KEY, JSON.stringify(expenses));
            renderAll(); // Update UI after save
        }

        // ============================================
        // CORE APP FUNCTIONS
        // ============================================
        function addExpense(event) {
            event.preventDefault();
            const expenses = getExpenses();
            const newId = expenses.length > 0 ? Math.max(...expenses.map(e => e.id)) + 1 : 1;

            const newExpense = {
                id: newId,
                item: document.getElementById('itemInput').value,
                amount: parseFloat(document.getElementById('amountInput').value),
                category: document.getElementById('categoryInput').value || 'Other',
                date: document.getElementById('dateInput').value,
                payment_method: document.getElementById('paymentInput').value || 'Cash',
                notes: document.getElementById('notesInput').value,
                created_at: new Date().toISOString()
            };

            expenses.push(newExpense);
            saveExpenses(expenses);

            // Reset form
            event.target.reset();
            document.getElementById('dateInput').value = '''' + datetime.now().strftime('%Y-%m-%d') + '''';
        }

        function editExpense(id) {
            const expenses = getExpenses();
            const expense = expenses.find(e => e.id === id);
            if (!expense) return;

            // Simple inline edit - for a better UX, consider a modal
            const newItem = prompt('Edit item name:', expense.item);
            if (newItem !== null) expense.item = newItem;
            const newAmount = prompt('Edit amount (Rs.):', expense.amount);
            if (newAmount !== null) expense.amount = parseFloat(newAmount);

            saveExpenses(expenses);
        }

        function deleteExpense(id) {
            if (!confirm('Are you sure you want to delete this expense?')) return;
            const expenses = getExpenses().filter(e => e.id !== id);
            saveExpenses(expenses);
        }

        function filterExpenses() {
            renderAll(); // Re-render with filter applied
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
            const total = filteredExpenses.reduce((sum, e) => sum + e.amount, 0);
            const avg = expenses.length > 0 ? expenses.reduce((sum, e) => sum + e.amount, 0) / expenses.length : 0;

            document.getElementById('statsDashboard').innerHTML = `
                <div class="stat-card">
                    <h3>Filtered Total</h3>
                    <div class="value">Rs. ${total.toFixed(2)}</div>
                    <div class="label">${filteredExpenses.length} expense(s)</div>
                </div>
                <div class="stat-card">
                    <h3>All-Time Total</h3>
                    <div class="value">Rs. ${expenses.reduce((sum, e) => sum + e.amount, 0).toFixed(2)}</div>
                    <div class="label">${expenses.length} total expenses</div>
                </div>
                <div class="stat-card">
                    <h3>Average</h3>
                    <div class="value">Rs. ${avg.toFixed(2)}</div>
                    <div class="label">Per expense average</div>
                </div>
            `;
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

            tableHTML += `</tbody></table>`;
            container.innerHTML = tableHTML;
        }

        function renderCategoryFilter() {
            const expenses = getExpenses();
            const categories = [...new Set(expenses.map(e => e.category))].sort();
            const select = document.getElementById('categoryFilter');

            // Keep current selection
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
                const response = await fetch('/api/load-demo');
                const demoExpenses = await response.json();
                const currentExpenses = getExpenses();

                // Adjust IDs to avoid conflicts
                const maxId = currentExpenses.length > 0 ? Math.max(...currentExpenses.map(e => e.id)) : 0;
                demoExpenses.forEach((exp, index) => {
                    exp.id = maxId + index + 1;
                });

                saveExpenses([...currentExpenses, ...demoExpenses]);
                alert('Demo data loaded!');
            } catch (error) {
                // Fallback if API fails
                const fallbackDemo = [
                    {id: getExpenses().length + 1, item: "Coffee", amount: 120.00, category: "Food & Dining", date: "''' + datetime.now().strftime('%Y-%m-%d') + '''", payment_method: "Cash", notes: "Morning coffee"},
                    {id: getExpenses().length + 2, item: "Bus Fare", amount: 50.00, category: "Transportation", date: "''' + datetime.now().strftime('%Y-%m-%d') + '''", payment_method: "Card", notes: "Commute"},
                    {id: getExpenses().length + 3, item: "Netflix", amount: 649.00, category: "Entertainment", date: "''' + datetime.now().strftime('%Y-%m-%d') + '''", payment_method: "UPI", notes: "Monthly subscription"}
                ];
                saveExpenses([...getExpenses(), ...fallbackDemo]);
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
                csv += `${exp.id},${exp.item},${exp.amount},${exp.category},${exp.date},${exp.payment_method},"${exp.notes}"\\n`;
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
            // Check if first time user
            if (getExpenses().length === 0) {
                if (confirm('👋 Welcome! Would you like to load some demo expenses to see how the app works?')) {
                    loadDemoData();
                }
            }
            renderAll();
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
    print('© 2026 Bishnu Raj KC. All rights reserved.')
    print('=' * 60)
    app.run(host='0.0.0.0', port=5000, debug=True)