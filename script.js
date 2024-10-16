// Обновленный JavaScript код для работы с модальным окном регистрации
document.getElementById('logo').addEventListener('click', () => {
  location.reload();
});

const profileBtn = document.querySelector('.profile-btn');

// Открытие страницы changes.html при нажатии на кнопку "Profile"
profileBtn.addEventListener('click', () => {
  window.location.href = 'changes.html';
});

// Вставка проигрывателя на страницу динамически
document.addEventListener('DOMContentLoaded', () => {
  const playerHTML = `
    <div id="music-player" class="music-player">
      <div class="player-info">
        <img src="https://via.placeholder.com/50" alt="Album Cover" class="album-cover">
        <div class="track-details">
          <p class="track-name">Track Name</p>
          <p class="artist-name">Artist Name</p>
        </div>
      </div>
      <div class="player-controls">
        <button class="control-btn">
          <img src="prev.png" alt="Previous" class="control-icon">
        </button>
        <button id="play-pause-btn" class="control-btn">
          <img src="play.png" alt="Play" class="control-icon">
        </button>
        <button class="control-btn">
          <img src="https://i.ibb.co.com/dBnXfpQ/prev.png" alt="Next" class="control-icon">
        </button>
      </div>
    </div>
  `;

  document.body.insertAdjacentHTML('beforeend', playerHTML); // Добавляем в конец body

  // Логика для переключения кнопки Play/Pause
  const playPauseBtn = document.getElementById('play-pause-btn');
  const playPauseIcon = playPauseBtn.querySelector('img');

  let isPlaying = false; // Следим за состоянием воспроизведения

  playPauseBtn.addEventListener('click', () => {
    if (isPlaying) {
      playPauseIcon.src = 'play.png'; // Меняем изображение на "Play"
      playPauseIcon.alt = 'Play';
    } else {
      playPauseIcon.src = 'https://i.ibb.co.com/cTWPDz1/pause.png'; // Меняем изображение на "Pause"
      playPauseIcon.alt = 'Pause';
    }
    isPlaying = !isPlaying; // Переключаем состояние
  });
});
