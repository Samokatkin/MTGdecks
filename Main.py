from flask import Flask, render_template, redirect, abort
from data.users import User
from data.decks import Decks
from data import db_session
from flask_login import LoginManager, login_required, login_user, logout_user, current_user
from data.forms import DecksForm, RegisterForm, LoginForm
import request
from mtgsdk import Card
app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
db_session.global_init("db/mtg.sqlite")
session = db_session.create_session()
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    session = db_session.create_session()
    return session.query(User).get(user_id)


def get_image(decklist):
    list = []
    for line in decklist.split('\r\n'):
        list.append(line.split()[0])
        name = ' '.join(line.split()[1:])
        car = Card.where(name=name).array()
        for c in car:
            if 'imageUrl' in c:
                card = c['imageUrl']
        list.append(name)
        list.append(card)
    return list


@app.route('/')
@app.route('/index')
def index():
    session = db_session.create_session()
    if current_user.is_authenticated:
        decks = session.query(Decks).filter(
            (Decks.user == current_user) | (Decks.is_private != True))
    else:
        decks = session.query(Decks).filter(Decks.is_private != True)
    return render_template("index.html", decks=decks)


@app.route('/decks/<int:id>')
def deck(id):
    session = db_session.create_session()
    decks = session.query(Decks)
    for i in decks:
        if i.id == id:
            deckl = get_image(i.content)
            lengh = len(deckl) - 1
            return render_template("deck.html", item=i, decklist=deckl, len=lengh)


@app.route('/mydecks')
def mydecks():
    session = db_session.create_session()
    decks = session.query(Decks).filter(
        (Decks.user == current_user) | (Decks.is_private != True))
    return render_template("mydecks.html", decks=decks)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        session = db_session.create_session()
        if session.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
            about=form.about.data
        )
        user.set_password(form.password.data)
        session.add(user)
        session.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        user = session.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/decks',  methods=['GET', 'POST'])
@login_required
def add_decks():
    form = DecksForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        decks = Decks()
        decks.title = form.title.data
        decks.content = form.content.data
        decks.commander1 = form.commander1.data
        decks.commander2 = form.commander2.data
        decks.is_private = form.is_private.data
        current_user.decks.append(decks)
        session.merge(current_user)
        session.commit()
        return redirect('/')
    return render_template('Decks.html', title='Добавление колоды',
                           form=form)


@app.route('/decks/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_decks(id):
    form = DecksForm()
    if request == "GET":
        session = db_session.create_session()
        decks = session.query(Decks).filter(Decks.id == id,
                                          Decks.user == current_user).first()
        if decks:
            form.title.data = decks.title
            form.content.data = form.content.data
            decks.commander1 = form.commander1.data
            decks.commander2 = form.commander2.data
            form.is_private.data = decks.is_private
        else:
            abort(404)
    if form.validate_on_submit():
        session = db_session.create_session()
        decks = session.query(Decks).filter(Decks.id == id,
                                          Decks.user == current_user).first()
        if decks:
            decks.title = form.title.data
            decks.content = form.content.data
            decks.commander1 = form.commander1.data
            decks.commander2 = form.commander2.data
            decks.is_private = form.is_private.data
            session.commit()
            return redirect('/')
        else:
            abort(404)
    return render_template('decks.html', title='Редактирование новости', form=form)


@app.route('/decks_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def decks_delete(id):
    session = db_session.create_session()
    decks = session.query(Decks).filter(Decks.id == id,
                                      Decks.user == current_user).first()
    if decks:
        session.delete(decks)
        session.commit()
    else:
        abort(404)
    return redirect('/')


def main():
    session.commit()
    app.run()


if __name__ == '__main__':
    main()

