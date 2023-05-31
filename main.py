from flask import Flask,render_template,request,session,make_response,abort
from flask_mail import Mail,Message
from flask_sqlalchemy import SQLAlchemy
import os
from werkzeug.utils import secure_filename
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///crab-base.db'
db = SQLAlchemy(app)
app.config['UPLOAD_FOLDER'] = 'media' 

app.config['MAIL_SERVER'] = 'smtp.gmail.com' 
app.config['MAIL_PORT'] = 465 
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USERNAME'] = ''
app.config['MAIL_PASSWORD'] = ''  

mail = Mail(app)


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    photo = db.Column(db.LargeBinary, nullable=False)  # Используем BLOB для хранения фотографий
    quantity = db.Column(db.Integer, nullable=False)
    is_active = db.Column(db.Boolean, default=True)

class City(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    coordinates = db.Column(db.String(50), nullable=False)
    is_active = db.Column(db.Boolean, default=True)

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author_name = db.Column(db.String(100), nullable=False)
    text = db.Column(db.Text, nullable=False)
    photo = db.Column(db.LargeBinary, nullable=False)  # Используем BLOB для хранения фотографий
    is_active = db.Column(db.Boolean, default=True)


@app.route('/get_photo/<int:review_id>')
def get_photo(review_id):
    review = Review.query.get(review_id)
    if review is None or review.photo is None:
        abort(404)  # Если отзыв или изображение не найдены, возвращаем ошибку 404
    response = make_response(review.photo)
    response.headers.set('Content-Type', 'image/jpeg')  # Установка типа контента в соответствии с форматом изображения
    return response

@app.route('/get_photo_product/<int:product_id>')
def get_photo_product(product_id):
    product = Product.query.get(product_id)
    if product is None or product.photo is None:
        abort(404)  # Если отзыв или изображение не найдены, возвращаем ошибку 404
    response = make_response(product.photo)
    response.headers.set('Content-Type', 'image/jpeg')  # Установка типа контента в соответствии с форматом изображения
    return response



@app.route('/admin',methods = ['POST','GET'])
def admiin():
   if request.method =='POST':
        login = request.form['login']
        password = request.form['password']
        print(login,password)
        if login == 'admin' and password == 'root':
  
            return render_template('add_product.html')
   else:
       
    return render_template('admin.html')

@app.route('/product',methods = ['GET','POST'])
def product():
    if request.method == 'POST':
        name = request.form.get('review-name')
        price = float(request.form.get('review-price'))
        photo = request.files['review-photo']
        quantity = int(request.form.get('review-quantity'))
        is_active = bool(request.form.get('review-active'))

        # Сохранение фотографии на диск
        filename = secure_filename(photo.filename)
        photo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        # Читаем байтовые данные фотографии
        with open(os.path.join(app.config['UPLOAD_FOLDER'], filename), 'rb') as f:
            photo_data = f.read()

        # Создание объекта Product и сохранение данных в базу данных
        product = Product(name=name, price=price, photo=photo_data, quantity=quantity, is_active=is_active)
        db.session.add(product)
        db.session.commit()

        return 'Товар успешно добавлен'
    
    return render_template('add_product.html')
    

@app.route('/city',methods = ['GET','POST'])
def city():
    if request.method == 'POST':
        name = request.form['city-name']
        phone = request.form['city-phone']
        coordinates = request.form['city-coordinates']
        is_active = 'city-active' in request.form

        city = City(name=name, phone=phone, coordinates=coordinates, is_active=is_active)
        db.session.add(city)
        db.session.commit()

        return 'City added successfully!'
    
    
    return render_template('add_city.html')

@app.route('/review', methods=['GET', 'POST'])
def review():
    if request.method == 'POST':
        author_name = request.form.get('review-author')
        text = request.form.get('review-text')
        photo = request.files['review-photo']  # Получаем объект FileStorage

        # Сохраняем фотографию на диск
        filename = secure_filename(photo.filename)
        photo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        is_active = bool(request.form.get('review-active'))

        # Читаем байтовые данные фотографии
        with open(os.path.join(app.config['UPLOAD_FOLDER'], filename), 'rb') as f:
            photo_data = f.read()

        # Сохраняем данные в модель Review
        review = Review(author_name=author_name, text=text, photo=photo_data, is_active=is_active)
        db.session.add(review)
        db.session.commit()

        return 'Отзыв успешно сохранен'
    return render_template('add_review.html')

@app.route('/',methods = ['GET','POST'])
def index():
    cities = City.query.all()
    reviews = Review.query.all()
    products = Product.query.all()
    email = 'anonim@bk.ru'
    if request.method == 'POST':
        name = request.form['name_un']
        phone = request.form['phone_un']

        msg = Message(f'Новое сообщение от {name}',sender=email,recipients=['developer2023@bk.ru'])
        msg.body = f'Просьба перезвонить на номер {phone}'
        mail.send(msg)

        return 'Письмо успешно отправлено'

    return render_template('index.html',cities=cities,reviews=reviews,products=products)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True,host = "0.0.0.0")
    
