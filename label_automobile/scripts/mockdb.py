from label_automobile.models.product import Product
from label_automobile.models import shopping_cart
import os
import sys
import transaction as ts

from pyramid.paster import (
    get_appsettings,
    setup_logging,
)
from datetime import datetime
from pyramid.scripts.common import parse_vars

from ..models.meta import Base
from ..models import (
    get_engine,
    get_tm_session,
    get_session_factory,
    User,
    Product,
    ShoppingCart,
    Order,
    )


def usage(argv):
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri> [var=value]\n'
          '(example: "%s development.ini")' % (cmd, cmd))
    sys.exit(1)


def main(argv=sys.argv):
    if len(argv) < 2:
        usage(argv)
    config_uri = argv[1]
    options = parse_vars(argv[2:])
    setup_logging(config_uri)
    settings = get_appsettings(config_uri, options=options)

    engine = get_engine(settings)
    Base.metadata.create_all(engine)
    session_factory = get_session_factory(engine)

    with ts.manager:
        dbsession = get_tm_session(session_factory, ts.manager)
        user = User()
        user.name = "John"
        user.surname = "Doe"
        user.email = "johndoe@example.com"
        dbsession.add(user)

        product = Product(
            name='Discraft Ultra Star', 
            description= 'Ultimate frisbee disc. 175g', 
            price= 20)
        dbsession.add(product)

        shopping_cart = ShoppingCart(
            user_id = dbsession.query(User).first().id, 
            product = dbsession.query(Product).first().id)
        dbsession.add(shopping_cart)

        order = Order(
            shopping_cart_id= dbsession.query(ShoppingCart).first().id,
            delivery_datetime= datetime.now(),
            address= '221B Baker Street, London, UK',
        )
        dbsession.add(order)
