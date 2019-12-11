import numpy as np
from flask import Flask, render_template, redirect, url_for, request, jsonify, flash
from app.module.login_database import login_db, get_info_db, register_db
from app.module.Info import Info
from app.module.web_lab import web_lab_get, web_lab_insert, web_lab_delete, web_lab_revise
from app.module.trade import get_trades, get_sell_trades, get_trade, register_trade, get_buy_trades, delete_trades, purchase_trade
from app.module.wishlist import get_wish_list, insert_wish_list
from app.module.user_database import get_user_info, delete_user_info
from app.module.database import Database


database = Database()
info_user = Info()
app = Flask(__name__)

@app.route('/main', methods=['GET'])
def main():
    try:
        index = int(request.args.get('index'))
    except:
        index = 1
    id = info_user.id
    id, name, money = get_info_db(database, id)
    trades = get_trades(database)
    start = np.amax([1, index - 5])
    end = np.amin([(((len(trades) - 1) // 10) + 2), start + 10])
    length = list(np.arange(start, end))
    trades = trades[(index - 1) * 10 + 1: index * 10 + 1]
    user = [{'id': id, 'name': name, 'money': money}]
    if database.valid:
        return render_template('/main.html', user=user, trades=trades, length=length, mode=info_user.mode)
    else:
        return redirect(url_for('bad_access'))

@app.route('/bad_access')
def bad_access():
    database.valid = True
    return render_template('/bad_access.html')

@app.route('/mypage')
def mypage():
    if info_user.mode == 'seller':
        return redirect(url_for('mypage_seller'))
    elif info_user.mode == 'buyer':
        return redirect(url_for('mypage_buyer'))
    else:
        return redirect(url_for('bad_access'))

@app.route('/mypage_seller')
def mypage_seller():
    id = info_user.id
    trades = get_sell_trades(database, id)
    if database.valid:
        return render_template('/mypage_seller.html', trades=trades)
    else:
        return redirect(url_for('bad_access'))


@app.route('/trade_delete', methods=['POST'])
def trade_delete():
    tid_list = request.form.getlist('delete')
    delete_trades(database, tid_list)
    return redirect(url_for('mypage_seller'))

@app.route('/mypage_buyer')
def mypage_buyer():
    id = info_user.id
    trades = get_buy_trades(database, id)
    wishlists = get_wish_list(database, id)
    if database.valid:
        return render_template('/mypage_buyer.html', trades=trades, wishlists=wishlists)
    else:
        return redirect(url_for('bad_access'))

@app.route('/purchase', methods=['POST'])
def purchase():
    id = info_user.id
    trades = get_wish_list(database, id)
    t_ids = []
    amounts = []
    for trade in trades:
        amounts.append(int(request.form.get('{}'.format(trade['t_id']))))
        t_ids.append(trade['t_id'])
    purchase_trade(database, t_ids, amounts, info_user.id)
    return redirect(url_for('mypage_buyer'))

@app.route('/product', methods=['GET'])
def product():
    tid = request.args.get('tid')
    trade = get_trade(database, tid)
    return render_template('/product.html', trade=trade)

@app.route('/register_wishlist', methods=['GET'])
def register_wishlist():
    tid = request.args.get('tid')
    insert_wish_list(database, info_user.id, tid)
    trade = get_trade(database, tid)
    if database.valid:
        return render_template('/product.html', trade=trade)
    else:
        database.valid = True
        return render_template('/product.html', trade=trade)

@app.route('/trade_register')
def trade_register():
    return render_template('/trade_register.html')

@app.route('/trade_register_check', methods=['POST'])
def trade_register_check():
    title = request.form['title']
    item_name = request.form['item_name']
    price = request.form['price']
    des = request.form['description']
    item_num = request.form['item_num']
    if register_trade(database, title, des, item_name, item_num, price, info_user.id):
        return redirect(url_for('main'))
    else:
        return redirect(url_for('trade_register'))

'''
admin page implementation
'''
@app.route('/admin_main')
def admin_main():
    if info_user.id != 'admin':
        return redirect(url_for('bad_access'))
    return render_template('admin_main.html')

@app.route('/admin_user_info')
def admin_user_info():
    if info_user.id != 'admin':
        return redirect(url_for('bad_access'))
    users = get_user_info(database)
    return render_template('admin_user_info.html', users=users)

@app.route('/admin_user_delete', methods=['POST'])
def admin_user_delete():
    if info_user.id != 'admin':
        return redirect(url_for('bad_access'))
    id_list = request.form.getlist('delete')
    delete_user_info(database, id_list)
    return redirect(url_for('admin_user_info'))

@app.route('/admin_trade_info')
def admin_trade_info():
    if info_user.id != 'admin':
        return redirect(url_for('bad_access'))
    trades = get_trades(database)
    return render_template('admin_trade_info.html', trades=trades)

'''
register page implementation
'''

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/register_check', methods=['POST'])
def register_check():
    id = request.form['id']
    password = request.form['password']
    name = request.form['name']
    if register_db(database, id, password, name):
        return redirect(url_for('login'))
    else:
        return redirect(url_for('register'))

'''
login page implementation
'''

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/login_check', methods=['POST'])
def login_check():
    id = request.form['id']
    password = request.form['password']
    try:
        info_user.get_mode(request.form['buyer-seller'])
    except:
        return redirect(url_for('login'))
    if login_db(database, id, password):
        info_user.update(True, id)
        if id == 'admin':
            return redirect(url_for('admin_main'))
        return redirect(url_for('main'))
    else:
        return redirect(url_for('login'))