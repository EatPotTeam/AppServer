from flask import g, jsonify
from . import api
from .. import db
from ..models import Coupon


@api.route('/coupons', methods=['GET'])
def get_all_coupons():
    user = g.current_user
    coupons = user.coupons
    coupons_list = []
    for coupon in coupons:
        if not coupon.order_id:
            coupons_list.append({
                'coupon_id': coupon.id,
                'discount_price': coupon.discount_price
            })
    return jsonify({
        'result': coupons_list
    })


@api.route('/coupons/<int:type>', methods=['GET'])
def get_new_coupon(type):
    user = g.current_user
    coupon = Coupon(discount_price=type)
    user.coupons.append(coupon)
    db.session.add(coupon)
    db.session.add(user)
    db.session.commit()
    return jsonify({
        'result': 'success'
    })