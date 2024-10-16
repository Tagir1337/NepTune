-- Создание таблицы пользователей (User)
CREATE TABLE "User" (
    username_id SERIAL PRIMARY KEY,  -- Уникальный идентификатор пользователя
    username VARCHAR(50) NOT NULL,   -- Имя пользователя
    password VARCHAR(50) NOT NULL,   -- Пароль
    email VARCHAR(100) NOT NULL,     -- Электронная почта
    phone_number VARCHAR(20)         -- Номер телефона
);

-- Создание таблицы артистов (Artist)
CREATE TABLE "Artist" (
    artist_id SERIAL PRIMARY KEY,    -- Уникальный идентификатор артиста
    name VARCHAR(100) NOT NULL,      -- Имя артиста
    genre VARCHAR(50),               -- Жанр музыки
    views INT DEFAULT 0              -- Количество просмотров
);

-- Создание таблицы музыки (Music)
CREATE TABLE "Music" (
    music_id SERIAL PRIMARY KEY,     -- Уникальный идентификатор трека
    title VARCHAR(100) NOT NULL,     -- Название трека
    artist_id INT NOT NULL,          -- Ссылка на таблицу артистов
    duration INT,                    -- Продолжительность трека (в секундах)
    release_date DATE,               -- Дата выхода трека
    FOREIGN KEY (artist_id) REFERENCES "Artist" (artist_id) ON DELETE CASCADE -- Связь с таблицей артистов
);

-- Создание таблицы плейлистов (Playlist)
CREATE TABLE "Playlist" (
    playlist_id SERIAL PRIMARY KEY,  -- Уникальный идентификатор плейлиста
    user_id INT NOT NULL,            -- Ссылка на таблицу пользователей
    name VARCHAR(100) NOT NULL,      -- Название плейлиста
    FOREIGN KEY (user_id) REFERENCES "User" (username_id) ON DELETE CASCADE  -- Связь с таблицей пользователей
);

-- Создание таблицы связи между плейлистами и музыкой (PlaylistMusic)
CREATE TABLE "PlaylistMusic" (
    playlist_music_id SERIAL PRIMARY KEY,   -- Уникальный идентификатор записи
    playlist_id INT NOT NULL,               -- Ссылка на таблицу плейлистов
    music_id INT NOT NULL,                  -- Ссылка на таблицу музыки
    FOREIGN KEY (playlist_id) REFERENCES "Playlist" (playlist_id) ON DELETE CASCADE,  -- Связь с таблицей плейлистов
    FOREIGN KEY (music_id) REFERENCES "Music" (music_id) ON DELETE CASCADE           -- Связь с таблицей музыки
);
