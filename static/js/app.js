const API = '/api';

// Загружаем категории в зависимости от выбранного типа
async function loadCategories() {
  const type = document.querySelector('input[name="type"]:checked').value;
  const res = await fetch(`${API}/categories/?type=${type}`);
  const categories = await res.json();
  const select = document.getElementById('category');
  select.innerHTML = categories.map(c => `<option value="${c.id}">${c.name}</option>`).join('');
}

// Обновляем баланс и список транзакций
async function refreshDashboard() {
  // Баланс
  const balResp = await fetch(`${API}/balance/`);
  const balData = await balResp.json();
  document.getElementById('balance').textContent = balData.balance.toFixed(2);

  // Транзакции
  const txResp = await fetch(`${API}/transactions/`);
  const transactions = await txResp.json();
  const list = document.getElementById('transactions-list');
  if (transactions.length === 0) {
    list.innerHTML = '<p>Нет операций</p>';
    return;
  }
  list.innerHTML = transactions.map(tx => `
    <div class="transaction-item">
      <div>
        <span class="${tx.type} amount">${tx.type === 'income' ? '+' : '-'}${tx.amount.toFixed(2)} ₽</span>
        <small>${tx.note ? tx.note : ''}</small>
      </div>
      <div>${new Date(tx.date).toLocaleDateString()}</div>
    </div>
  `).join('');
}

// Добавление новой транзакции
async function addTransaction() {
  const type = document.querySelector('input[name="type"]:checked').value;
  const amount = parseFloat(document.getElementById('amount').value);
  const category_id = parseInt(document.getElementById('category').value);
  const note = document.getElementById('note').value;

  if (!amount || !category_id) {
    alert('Заполните сумму и категорию');
    return;
  }

  await fetch(`${API}/transactions/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ type, amount, category_id, note })
  });

  // Очистка и обновление
  document.getElementById('amount').value = '';
  document.getElementById('note').value = '';
  refreshDashboard();
}

// Инициализация
document.addEventListener('DOMContentLoaded', () => {
  // Подгружаем категории при смене типа
  document.querySelectorAll('input[name="type"]').forEach(radio => {
    radio.addEventListener('change', loadCategories);
  });
  document.getElementById('submit-btn').addEventListener('click', addTransaction);

  loadCategories();
  refreshDashboard();
});

document.getElementById('resetBtn').addEventListener('click', () => {
    if (confirm('Вы уверены? Все транзакции будут удалены безвозвратно. Баланс станет 0.')) {
        resetData();
    }
});

async function resetData() {
    try {
        const response = await fetch('/api/reset', { method: 'POST' });
        const result = await response.json();
        if (response.ok) {
            alert(result.message);
            // Обновляем баланс и список транзакций на экране
            document.getElementById('balance').textContent = '0';
            document.getElementById('transactions').innerHTML = '';
        } else {
            alert('Ошибка сброса: ' + result.detail);
        }
    } catch (error) {
        console.error('Ошибка сети:', error);
        alert('Не удалось выполнить сброс. Проверьте соединение.');
    }
}