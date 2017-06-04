import requests
from flask import g, jsonify, request, url_for
# from celery import current_app as current_celery
from . import api
from .. import db
from ..models import Order, OrderItem, ORDER_STATUS, Coupon
# from ..utils import wait_payment


@api.route('/orders', methods=['GET'])
def get_all_orders():
    user = g.current_user
    orders = user.orders
    order_list = []
    for order in orders:
        # add order_items
        order_items = order.order_items
        orderItem_list = []
        for order_item in order_items:
            orderItem_list.append({
                'row': order_item.row,
                'col': order_item.col
            })
        # add coupons
        coupon_list = []
        coupons = order.coupons_used
        for coupon in coupons:
            coupon_list.append({
                'discount_price': coupon.discount_price
            })
        # add order
        order_list.append({
            'order_id': order.id,
            'cinema_name': order.cinema_name,
            'movie_name': order.movie_name,
            'time': order.time,
            'total_price': order.total_price,
            'status': order.status,
            'redeem_code': order.redeem_code,
            'order_items': orderItem_list,
            'coupons': coupon_list
        })
    return jsonify({
        'result': order_list
    })


@api.route('/orders/<int:id>', methods=['GET'])
def get_order(id):
    user = g.current_user
    order = Order.query.get_or_404(id)
    if order.user_id != user.id:
        return jsonify({
            'error': 'forbidden'
        })
    # add order_items
    order_items = order.order_items
    orderItem_list = []
    for order_item in order_items:
        orderItem_list.append({
            'row': order_item.row,
            'col': order_item.col
        })
    # add coupons
    coupons = order.coupons_used
    coupon_list = []
    for coupon in coupons:
        coupon_list.append({
            'discount_price': coupon.discount_price
        })
    # add order
    order_info = {
        'order_id': order.id,
        'cinema_name': order.cinema_name,
        'movie_name': order.movie_name,
        'time': order.time,
        'total_price': order.total_price,
        'status': order.status,
        'redeem_code': order.redeem_code,
        'order_items': orderItem_list,
        'coupons': coupon_list
    }
    return jsonify({
        'result': order_info
    })


@api.route('/orders', methods=['POST'])
def new_order():
    data = request.json
    user = g.current_user
    # new order
    order = Order(cinema_name=data['cinema_name'],
                  movie_name=data['movie_name'],
                  time=data['time'],
                  total_price=data['total_price'])
    url = 'http://localhost:5000/api/broadcast/' + str(data['broadcast_id'])
    # new order item
    orderItem_list = data['order_items']
    if orderItem_list:
        for orderItem in orderItem_list:
            res = requests.post(url=url, json=orderItem)
            res_json = res.json()
            if res_json['result'] == 'seat has been lock':
                # cancel all previous booking
                for prev in orderItem_list:
                    if prev['row'] == orderItem['row'] and prev['col'] == orderItem['col']:
                        break
                    else:
                        requests.delete(url=url, json=prev)
                # cancel the session record
                db.session.rollback()
                return jsonify({
                    'error': 'seat has been lock'
                })
            order_item = OrderItem(row=orderItem['row'],
                                  col=orderItem['col'])
            order.order_items.append(order_item)
            db.session.add(order_item)
    # coupon used
    coupons_list = data['coupons']
    if coupons_list:
        for coupon_item in coupons_list:
            coupon = Coupon.query.get_or_404(int(coupon_item['coupon_id']))
            order.coupons_used.append(coupon)
            db.session.add(coupon)
    user.orders.append(order)
    db.session.add(order)
    db.session.add(user)
    db.session.commit()
    # task = wait_payment.delay(order_id=order.id)
    return jsonify({
        'result': 'success'
        # 'location': url_for('api.task_status', task_id=task.id)
    })


@api.route('/orders/<int:id>', methods=['DELETE'])
def delete_order(id):
    order = Order.query.get_or_404(id)
    # cancel order lock seat
    order_items = order.order_items
    url = 'http://localhost:5000/api/broadcast/' + str(order.broadcast_id)
    for order_item in order_items:
        requests.delete(url=url,
                        json={'row': order_item.row, 'col': order_item.col})
        db.session.delete(order_item)
    # cancel coupons
    coupons = order.coupons_used
    for coupon in coupons:
        coupon.order_id = None
        db.session.add(coupon)
    # cancel order
    db.session.delete(order)
    db.session.commit()
    return jsonify({
        'result': 'success'
    })


@api.route('/orders/<int:id>/paid', methods=['POST'])
def order_paid(id):
    order = Order.query.get_or_404(id)
    data = request.json
    order.status = ORDER_STATUS['PAID']
    code = Order.generate_redeem_code()
    while Order.query.filter_by(redeem_code=code).first():
        code = Order.generate_redeem_code()
    order.redeem_code = code
    db.session.add(order)
    db.session.commit()
    return jsonify({
        'result': 'success'
    })


# @api.route('/status/<task_id>')
# def task_status(task_id):
#     task = wait_payment.AsyncResult(task_id)
#     if task.state == 'PENDING':
#         # job did not start yet
#         response = {
#             'state': task.state,
#             'status': 'Pending...'
#         }
#     elif task.state != 'FAILURE':
#         response = {
#             'state': task.state,
#             'current': task.info.get('current', 0),
#             'total': task.info.get('total', 1),
#             'status': task.info.get('status', '')
#         }
#         if 'result' in task.info:
#             response['result'] = task.info['result']
#     else:
#         # something went wrong in the background job
#         response = {
#             'state': task.state,
#             'status': str(task.info),  # this is the exception raised
#         }
#     return jsonify(response)
