import logging
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from flask import request, flash
import os
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
app = Flask(__name__)

# Настройка логирования
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Конфигурация для работы с SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'  # Для работы с сессиями и flash-сообщениями
db = SQLAlchemy(app)

# Модель для таблицы Registered
class Registered(db.Model):
    __tablename__ = 'registered'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    photo = db.Column(db.String(200))  # Новый столбец для фото


# Модель для таблицы Contact
class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    message = db.Column(db.Text, nullable=False)

# Модель для таблицы отзывов
class Com(db.Model):
    __tablename__ = 'coms'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    comment = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Comment {self.id} by {self.username}>'

# Главная страница с отзывами
@app.route('/')
def home():
    # Перенаправляем на регистрацию, если пользователь не авторизован
    return redirect(url_for('register'))

# Регистрация пользователя
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        photo = request.files.get('photo')  # Получаем фото из формы

        # Проверка на уникальность email и имени пользователя
        if Registered.query.filter_by(email=email).first() or Registered.query.filter_by(username=username).first():
            flash('Пользователь с таким именем или email уже существует', 'error')
            return redirect(url_for('register'))

        # Хэшируем пароль
        hashed_password = generate_password_hash(password, method="pbkdf2:sha256")

        # Сохраняем фото, если оно есть
        photo_filename = None
        if photo and allowed_file(photo.filename):
            filename = secure_filename(photo.filename)
            photo_filename = os.path.join('static/uploads', filename)
            photo.save(photo_filename)

        # Создаем нового пользователя
        new_user = Registered(username=username, email=email, password=hashed_password, photo=photo_filename)
        db.session.add(new_user)
        db.session.commit()

        flash('Регистрация прошла успешно. Теперь вы можете войти.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')


# Вход пользователя
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = Registered.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['username'] = user.username
            flash('Вы успешно вошли в систему.', 'success')
            return redirect(url_for('index'))
        else:
            flash('Неправильный email или пароль.', 'error')

    return render_template('login.html')

# Выход пользователя
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    flash('Вы вышли из системы.', 'info')
    return redirect(url_for('index'))

# Главная страница с отзывами
@app.route('/index')
def index():
    #ф Проверяем, есть ли пользователь в сессии
    if 'user_id' not in session:
        flash('Пожалуйста, войдите в систему.', 'warning')
        return redirect(url_for('login'))  # Если не залогинен, перенаправляем на страницу входа

    reviews = Com.query.all()  # Получаем все отзывы из базы данных
    return render_template('index.html', reviews=reviews)

@app.route('/add_review', methods=['POST'])
def add_review():
    if 'user_id' not in session:
        flash('Пожалуйста, войдите в систему.', 'warning')
        return redirect(url_for('login'))

    comment = request.form['comment']
    username = session.get('username', 'Guest')  # Получаем имя пользователя или используем "Guest"
    new_review = Com(username=username, email=session.get('username', ''), comment=comment)
    db.session.add(new_review)
    db.session.commit()
    flash('Ваш отзыв успешно добавлен!', 'success')
    return redirect(url_for('index'))

@app.route('/newsite.html', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        try:
            # Получаем данные из формы
            name = request.form['name']
            email = request.form['email']
            message = request.form['message']

            logger.debug(f"Полученные данные: Имя={name}, Email={email}, Сообщение={message}")

            # Сохраняем данные в базе
            new_contact = Contact(name=name, email=email, message=message)
            db.session.add(new_contact)

            # Логируем перед коммитом
            logger.debug("Коммитим в базу данных")
            db.session.commit()  # Коммитим транзакцию для сохранения изменений
            logger.info(f"Контакт сохранен: {name}, {email}")

            return redirect(url_for('thank_you'))

        except Exception as e:
            # Логируем ошибку
            db.session.rollback()  # Откатываем изменения в случае ошибки
            logger.error(f"Ошибка при сохранении контакта: {e}")  # Логирование ошибки
            return "Произошла ошибка при сохранении данных. Пожалуйста, попробуйте еще раз."

    return render_template('newsite.html')

@app.route('/pista.html')
def pista():
    return render_template("pista.html")

@app.route('/wagon.html')
def wagon():
    return render_template("wagon.html")

@app.route('/camaro.html')
def camaro():
    return render_template("camaro.html")

@app.route('/gran.html')
def gran():
    return render_template("gran.html")

@app.route('/wmv20.html')
def wmv20():
    return render_template("wmv20.html")

@app.route('/lamba.html')
def lamba():
    return render_template("lamba.html")

@app.route('/sedan.html')
def sedan():
    return render_template("sedan.html")

@app.route('/infiniti.html')
def infiniti():
    return render_template("infiniti.html")

@app.route('/porsche.html')
def porsche():
    return render_template("porsche.html")

@app.route('/8series.html')
def series8():
    return render_template("8series.html")

@app.route('/xseries.html')
def seriesx():
    return render_template("xseries.html")

@app.route('/account', methods=['GET'])
def account():
    if 'user_id' not in session:
        flash('Пожалуйста, войдите в систему.', 'warning')
        return redirect(url_for('login'))

    user = Registered.query.get(session['user_id'])
    reviews = Com.query.filter_by(username=user.username).all()
    return render_template("account.html", user=user, reviews=reviews)

@app.route('/update_password', methods=['POST'])
def update_password():
    if 'user_id' not in session:
        flash('Пожалуйста, войдите в систему.', 'warning')
        return redirect(url_for('login'))

    new_password = request.form['new_password']
    hashed_password = generate_password_hash(new_password, method="pbkdf2:sha256")

    user = Registered.query.get(session['user_id'])
    user.password = hashed_password
    db.session.commit()
    flash('Пароль успешно обновлен.', 'success')
    return redirect(url_for('account'))


if __name__ == '__main__':
    # Обернем вызов создания таблиц в контекст приложения
    with app.app_context():
        db.create_all()  # Создаёт таблицы при первом запуске
    app.run(debug=True)
