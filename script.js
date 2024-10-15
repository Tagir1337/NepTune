document.getElementById('contact-form').addEventListener('submit', function(e) {
    e.preventDefault();

    const name = document.getElementById('name').value;
    const email = document.getElementById('email').value;
    const message = document.getElementById('message').value;

    alert(`Спасибо, ${name}! Ваше сообщение отправлено.`);

    // Здесь можно добавить логику для отправки данных на сервер
    this.reset(); // Сбросить форму после отправки
});
