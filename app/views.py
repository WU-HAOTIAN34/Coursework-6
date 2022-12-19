import copy
from flask import request, flash, render_template, url_for, redirect, session, json, current_app
from app import app, db
import datetime
from .forms import LoginForm, AddItemForm, PurchaseForm, EditItemForm, EditInformationForm, RegisterForm, SearchForm
from .models import User, Item, Order, Cart, Collection
from datetime import datetime
import base64


@app.route('/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    return render_template('login.html', form=form)


@app.route('/admin', methods=['GET', 'POST'])
def admin():
    return render_template('adminIndex.html')


@app.route('/user', methods=['GET', 'POST'])
def user():
    return render_template('userIndex.html')




@app.route('/loginVali', methods=['GET', 'POST'])
def loginVali():
    username = request.form.get('username')
    password = request.form.get('password')
    identity = request.form.get('identity')
    temp = int(identity)
    if temp == 0:
        user = User.query.filter(User.username == username, User.password == password, User.job == 0).first()
    else:
        user = User.query.filter(User.username == username, User.password == password, User.job == 1).first()
    print(user)
    if user:
        session.pop('user')
        session['user'] = [user.username, user.password, user.phone, user.name, user.job, user.id]
        if user.job:
            current_app.logger.info("Admin logged in")
            data = {'word': 2}
            return json.dumps(data)
        else:
            current_app.logger.info("Admin logged in")
            data = {'word': 1}
            return json.dumps(data)
    else:
        current_app.logger.info("Admin logged in")
        data = {'word': 0}
        return json.dumps(data)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    return render_template('register.html', form=form)


@app.route('/registerVali', methods=['GET', 'POST'])
def registerVali():
    username = request.form.get('username')
    password = request.form.get('password')
    name = request.form.get('name')
    phone = request.form.get('phone')
    identity = request.form.get('identity')
    print(identity)
    user = User.query.filter(User.username == username).all()
    if not user:
        temp = int(identity)
        if temp == 0:
            user_ = User(username=username, password=password, job=0, name=name, phone=phone)
        else:
            user_ = User(username=username, password=password, job=1, name=name, phone=phone)
        db.session.add(user_)
        db.session.commit()
        data = {'word': 1}
        return json.dumps(data)
    else:
        data = {'word': 0}
        return json.dumps(data)



@app.route('/add', methods=['GET', 'POST'])
def add():
    form = AddItemForm()
    item = Item.query.all()
    item_list = []
    for i in item:
        temp = base64.b64encode(i.image)
        temp = str(temp)
        byte_str = copy.deepcopy(temp[2:len(temp) - 1])
        item_list.append([i, byte_str])
    if form.validate_on_submit():
        file = request.files['image'].read()
        name = form.item_name.data
        description = form.description.data
        price = form.price.data
        item = Item(item_name=name, description=description, price=price, image=file)
        db.session.add(item)
        db.session.commit()
        flash('ok')
        return redirect(url_for('login'))
    return render_template('home.html', form=form, ds=item_list, base64=base64)


@app.route('/shop', methods=['GET', 'POST'])
def shop():
    form = SearchForm()
    item = Item.query.all()
    user_id = session.get('user')[5]
    item_list = []
    for i in item:
        temp = base64.b64encode(i.image)
        temp = str(temp)
        byte_str = copy.deepcopy(temp[2:len(temp) - 1])
        favor = Collection.query.filter(Collection.item_id == i.id, Collection.user_id == user_id).all()
        a = 1
        if not favor:
            a = 0
        item_list.append([i, byte_str, a])
    if form.validate_on_submit():
        name = form.search.data
        if name == '':
            item = Item.query.all()
        else:
            temp = "%" + name + "%"
            item = Item.query.filter(Item.item_name.like(temp)).all()
        form = SearchForm()
        user_id = session.get('user')[5]
        item_list = []
        for i in item:
            temp = base64.b64encode(i.image)
            temp = str(temp)
            byte_str = copy.deepcopy(temp[2:len(temp) - 1])
            favor = Collection.query.filter(Collection.item_id == i.id, Collection.user_id == user_id).all()
            a = 1
            if not favor:
                a = 0
            item_list.append([i, byte_str, a])
        return render_template('item.html', item=item_list, base64=base64, page=1, form=form)
    return render_template('item.html', item=item_list, base64=base64, page=1, form=form)


@app.route('/information', methods=['GET', 'POST'])
def information():
    user = session.get("user")
    return render_template('userInformation.html', user=user)


@app.route('/getSession', methods=['GET', 'POST'])
def getSession():
    user = session.get('user')
    return user


@app.route('/itemDetail', methods=['GET'])
def itemDetail():
    form = PurchaseForm()
    item_id = request.args.get('id')
    item = Item.query.filter(Item.id == item_id).first()
    temp = base64.b64encode(item.image)
    temp = str(temp)
    byte_str = copy.deepcopy(temp[2:len(temp) - 1])
    return render_template('itemDetail.html', item=[item, byte_str], form=form)


@app.route('/test', methods=['GET', 'POST'])
def test():
    item = request.form.get('item')
    print(item)
    return 1


@app.route('/purchase', methods=['GET', 'POST'])
def purchase():
    user_id = session.get('user')[5]
    curr_time = datetime.now()
    province = request.form.get('province')
    city = request.form.get('city')
    item_id = request.form.get('item_id')
    number = int(request.form.get('number'))
    destination = '' + province + city
    item = Item.query.filter(Item.id == item_id).first()
    price = item.price
    money = float(price) * number
    order = Order(user_id=user_id, item_id=item_id, time=curr_time, number=number, destination=destination, money=money)
    db.session.add(order)
    db.session.commit()
    data = {'word': 1}
    return json.dumps(data)


@app.route('/collect', methods=['GET', 'POST'])
def collect():
    user_id = session.get('user')[5]
    item_id = request.form.get('item_id')
    number = int(request.form.get('number'))
    item = Item.query.filter(Item.id == item_id).first()
    price = item.price
    money = float(price) * number
    province = request.form.get('province')
    city = request.form.get('city')
    destination = '' + province + city
    cart = Cart(user_id=user_id, item_id=item_id, number=number, money=money, destination=destination)
    db.session.add(cart)
    db.session.commit()
    data = {'word': 1}
    return json.dumps(data)


@app.route('/order', methods=['GET', 'POST'])
def order():
    user_id = session.get('user')[5]
    order = db.session.query(Order.id, Order.user_id, Order.item_id, Order.time, Order.money, Order.destination,
                             Order.number, Item.image, Item.price, Item.item_name, Item.description)\
        .join(Item, Order.item_id == Item.id).filter(Order.user_id == user_id).all()
    order_list = []
    for i in order:
        temp = base64.b64encode(i.image)
        temp = str(temp)
        byte_str = copy.deepcopy(temp[2:len(temp) - 1])
        a = i.time
        day = datetime(a.year, a.month, a.day, a.hour, a.minute, int(a.second))
        order_list.append([i, byte_str, i.number * 500, day])
    return render_template('order.html', order=order_list, base64=base64)


@app.route('/collection', methods=['GET', 'POST'])
def collection():
    user_id = session.get('user')[5]
    collection = db.session.query(Collection.id, Collection.user_id, Collection.item_id, Item.image, Item.price,
                                  Item.item_name).join(Item, Collection.item_id == Item.id)\
        .filter(Collection.user_id == user_id).all()
    collection_list = []
    for i in collection:
        temp = base64.b64encode(i.image)
        temp = str(temp)
        byte_str = copy.deepcopy(temp[2:len(temp) - 1])
        collection_list.append([i, byte_str, 1])
    return render_template('item.html', item=collection_list, base64=base64, page=2)


@app.route('/cartItem', methods=['GET', 'POST'])
def cartItem():
    user_id = session.get('user')[5]
    cart = db.session.query(Cart.id, Cart.user_id, Cart.item_id, Cart.money, Cart.destination, Cart.number, Item.image,
                            Item.price, Item.item_name, Item.description).join(Item, Cart.item_id == Item.id)\
        .filter(Cart.user_id == user_id).all()
    cart_list = []
    for i in cart:
        print(i)
        temp = base64.b64encode(i.image)
        temp = str(temp)
        byte_str = copy.deepcopy(temp[2:len(temp) - 1])
        cart_list.append([i, byte_str, i.number * 500])
    return render_template('shoppingCart.html', cart=cart_list, base64=base64)


@app.route('/cancelOrder', methods=['GET', 'POST'])
def cancelOrder():
    order_id = request.args.get('id')
    order = Order.query.filter_by(id=order_id).first()
    db.session.delete(order)
    db.session.commit()
    return redirect('order')


@app.route('/cancelCart', methods=['GET', 'POST'])
def cancelCart():
    cart_id = request.args.get('id')
    cart = Cart.query.filter_by(id=cart_id).first()
    db.session.delete(cart)
    db.session.commit()
    return redirect('cartItem')


@app.route('/purchaseCart', methods=['GET', 'POST'])
def purchaseCart():
    cart_id = request.args.get('id')
    cart = Cart.query.filter_by(id=cart_id).first()
    curr_time = datetime.now()
    order = Order(user_id=cart.user_id, item_id=cart.item_id, time=curr_time, number=cart.number,
                  destination=cart.destination, money=cart.money)
    db.session.delete(cart)
    db.session.commit()
    db.session.add(order)
    db.session.commit()
    return redirect('cartItem')


@app.route('/makeFavor', methods=['GET', 'POST'])
def makeFavor():
    user_id = session.get('user')[5]
    item_id = request.form.get('item_id')
    collection = Collection(user_id=user_id, item_id=item_id)
    db.session.add(collection)
    db.session.commit()
    data = {'word': 1}
    return json.dumps(data)


@app.route('/cancelFavor', methods=['GET', 'POST'])
def cancelFavor():
    user_id = session.get('user')[5]
    item_id = request.form.get('item_id')
    collection = Collection.query.filter(Collection.user_id == user_id, Collection.item_id == item_id).all()
    for i in collection:
        db.session.delete(i)
        db.session.commit()
    data = {'word': 1}
    return json.dumps(data)


@app.route('/deleteFavor', methods=['GET', 'POST'])
def deleteFavor():
    favor_id = request.args.get('id')
    collection = Collection.query.filter(Collection.id == favor_id).first()
    db.session.delete(collection)
    db.session.commit()
    return redirect('collection')


@app.route('/orderAdmin', methods=['GET', 'POST'])
def orderAdmin():
    order = db.session.query(Order.id, Order.user_id, Order.item_id, Order.money, Order.destination, Order.number,
                             Order.time, Item.price, Item.item_name, User.name, User.phone)\
        .join(Item, Order.item_id == Item.id).join(User, Order.user_id == User.id).all()
    order_list = []
    for i in order:
        price = i.number * 500
        a = i.time
        day = datetime(a.year, a.month, a.day, a.hour, a.minute, int(a.second))
        order_list.append([i, price, day])
    return render_template('orderAdmin.html', order=order_list)


@app.route('/itemAdmin', methods=['GET', 'POST'])
def itemAdmin():
    item = Item.query.all()
    user_id = session.get('user')[5]
    item_list = []
    for i in item:
        temp = base64.b64encode(i.image)
        temp = str(temp)
        byte_str = copy.deepcopy(temp[2:len(temp) - 1])
        favor = Collection.query.filter(Collection.item_id == i.id, Collection.user_id == user_id).all()
        a = 1
        if not favor:
            a = 0
        item_list.append([i, byte_str, a])
    return render_template('itemAdmin.html', item=item_list, base64=base64)


@app.route('/userAdmin', methods=['GET', 'POST'])
def userAdmin():
    user_list = User.query.all()
    user = []
    for i in user_list:
        temp = ''
        num = 0
        length = len(i.password)
        for j in i.password:
            if (num >= 0 and num <= 1) or (num >= length - 3 and num <= length - 1):
                temp = temp + j
            else:
                temp = temp + '*'
            num += 1
        user.append([i, temp])
    return render_template('userAdmin.html', user=user)


@app.route('/', methods=['GET', 'POST'])
def logout():
    session.pop('user')
    form = LoginForm
    return render_template('login.html', form=form)


@app.route('/deleteOrder', methods=['GET', 'POST'])
def deleteOrder():
    order_id = request.form.get('id')
    order = Order.query.filter_by(id=order_id).first()
    db.session.delete(order)
    db.session.commit()
    data = {'word': 1}
    return json.dumps(data)


@app.route('/batchDeleteOrder', methods=['GET', 'POST'])
def batchDeleteOrder():
    order_id = request.form.get('id')
    temp = str(order_id)
    temp2 = copy.deepcopy(temp[0:len(temp) - 1])
    a = temp2.split(' ')
    id_list = []
    for i in a:
        id_list.append(int(i))
    for i in id_list:
        order = Order.query.filter_by(id=i).first()
        db.session.delete(order)
        db.session.commit()
    data = {'word': 1}
    return json.dumps(data)


@app.route('/deleteItem', methods=['GET', 'POST'])
def deleteItem():
    item_id = request.form.get('id')
    item = Item.query.filter_by(id=item_id).first()
    favor = Collection.query.filter_by(item_id=item.id).all()
    cart = Cart.query.filter_by(item_id=item.id).all()
    order = Order.query.filter_by(item_id=item.id).all()
    for i in favor:
        db.session.delete(i)
        db.session.commit()
    for i in cart:
        db.session.delete(i)
        db.session.commit()
    for i in order:
        db.session.delete(i)
        db.session.commit()
    db.session.delete(item)
    db.session.commit()
    data = {'word': 1}
    return json.dumps(data)


@app.route('/batchDeleteItem', methods=['GET', 'POST'])
def batchDeleteItem():
    item_id = request.form.get('id')
    temp = str(item_id)
    temp2 = copy.deepcopy(temp[0:len(temp) - 1])
    a = temp2.split(' ')
    id_list = []
    for i in a:
        id_list.append(int(i))
    for i in id_list:
        item = Item.query.filter_by(id=i).first()
        favor = Collection.query.filter_by(item_id=item.id).all()
        cart = Cart.query.filter_by(item_id=item.id).all()
        order = Order.query.filter_by(item_id=item.id).all()
        for j in favor:
            db.session.delete(j)
            db.session.commit()
        for j in cart:
            db.session.delete(j)
            db.session.commit()
        for j in order:
            db.session.delete(j)
            db.session.commit()
        db.session.delete(item)
        db.session.commit()
    data = {'word': 1}
    return json.dumps(data)


@app.route('/addItem', methods=['GET', 'POST'])
def addItem():
    form = AddItemForm()
    if form.validate_on_submit():
        name = form.item_name.data
        price = form.price.data
        description = form.description.data
        image = request.files['image'].read()
        item = Item(item_name=name, description=description, price=price, image=image)
        db.session.add(item)
        db.session.commit()
        return redirect(url_for('itemAdmin'))
    return render_template('edit.html', form=form, base64=base64, ds=1)


@app.route('/editItem', methods=['GET', 'POST'])
def editItem():
    form = EditItemForm()
    item_id = request.args.get('id')
    item = Item.query.filter_by(id=item_id).first()
    temp = base64.b64encode(item.image)
    temp = str(temp)
    byte_str = copy.deepcopy(temp[2:len(temp) - 1])
    if form.validate_on_submit():
        name = form.item_name.data
        price = form.price.data
        description = form.description.data
        image = request.files['image'].read()
        item.item_name = name
        item.description = description
        item.price = price
        temp = str(base64.b64encode(image))
        if temp != "b''":
            item.image = image
        db.session.commit()
        return redirect(url_for('itemAdmin'))
    return render_template('edit.html', form=form, base64=base64, ds=2, item=[item, byte_str])


@app.route('/editInformation', methods=['GET', 'POST'])
def editInformation():
    form = EditInformationForm()
    user_ = session.get('user')
    if form.validate_on_submit():
        user = User.query.filter_by(id=user_[5]).first()
        name = form.name.data
        phone = form.phone.data
        password = form.password.data
        user.password = password
        user.name = name
        user.phone = phone
        db.session.commit()
        user1 = User.query.filter_by(id=user_[5]).first()
        session.pop('user')
        session['user'] = [user1.username, user1.password, user1.phone, user1.name, user1.job, user1.id]
        return redirect(url_for('information'))
    return render_template('editInformation.html', user=user_, form=form)


@app.route('/sale', methods=['GET', 'POST'])
def sale():
    return render_template('chart.html')


@app.route('/getSale', methods=['GET', 'POST'])
def getSale():
    item_list = Item.query.all()
    sale_list = []
    money = []
    for i in item_list:
        num = 0
        order_list = Order.query.filter_by(item_id=i.id).all()
        for j in order_list:
            num += j.money
        sale_list.append(i.item_name)
        money.append(num)
    data = {'name': sale_list, 'money': money}
    return json.dumps(data)
