document.getElementById('settingsForm').addEventListener('submit', function(event) {
    event.preventDefault(); // Останавливаем стандартное поведение формы (перезагрузку страницы)

    // Получаем значения полей
    const username = document.getElementById('username').value;
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    // Сохраняем данные в локальное хранилище
    localStorage.setItem('username', username);
    localStorage.setItem('email', email);
    localStorage.setItem('password', password);

    // Переход на другую страницу
    window.location.href = 'probnik.html'; // Переход на следующее окно
});
