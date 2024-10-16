// Обновленный JavaScript код для работы с модальным окном регистрации
document.getElementById('logo').addEventListener('click', () => {
  location.reload();
});

const profileBtn = document.querySelector('.profile-btn');
const modal = document.getElementById('modal');
const closeBtn = document.querySelector('.close-btn');

// Открытие модального окна при нажатии на кнопку "Profile"
profileBtn.addEventListener('click', () => {
  modal.style.display = 'block';
});

// Закрытие модального окна при нажатии на крестик
closeBtn.addEventListener('click', () => {
  modal.style.display = 'none';
});

// Закрытие модального окна при нажатии вне области окна
window.addEventListener('click', (event) => {
  if (event.target === modal) {
    modal.style.display = 'none';
  }
});
