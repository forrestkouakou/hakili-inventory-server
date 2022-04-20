from decimal import Decimal, DecimalException

from django.db.models import F

from apps.core import apps_config as core
from apps.stock.models import Order, OrderItem, Transaction
from lib.config import django_logger


class TransactionProcess:

    @staticmethod
    def product_add_process(quantity, product):
        # Initialize the logger
        django_logger.info("product_add_process INITIALIZE")
        # TODO: Verify if not max_alert_threshold when adding products
        #   available_qty = product.quantity
        #   available_qty + quantity should is > max_alert_threshold

        # Add the given quantity to what we have in stock
        product.quantity = F('quantity') + quantity
        # Verify if the product is not marked as non-available and make it available by adding some products
        if not product.is_available:
            product.is_available = True
        # Save the product
        core.save_handler(product)
        return product

    @staticmethod
    def product_remove_process(quantity, product):
        # Initialize the logger
        django_logger.info("product_remove_process INITIALIZE")
        # TODO: Verify if not min_alert_threshold when removing products
        #   available_qty = product.quantity
        #   available_qty - quantity should is < min_alert_threshold

        # Subtract the given quantity of what we have in stock
        product.quantity = F('quantity') - quantity
        # Save the product
        core.save_handler(product)

        # Verify if the quantity left for the product is null and mark it as available if yes
        # Find another place for this block :(
        if product.quantity == 0:
            product.is_available = False
            core.save_handler(product)  # Save the product
        return product

    @staticmethod
    def order_create_process(tnx_type, quantity, order, product):
        # TODO: Verify that the price is a Decimal value

        # Initialize the logger
        django_logger.info("order_create_process INITIALIZE")

        # Let's check if the price is set
        price = order.get('price')
        try:
            price = Decimal(price)
            print("price ==> {}".format(price))
            # Check if the price is specified in the order or not and compute the sub_total with it
            if price is Decimal(0):
                if tnx_type == 'credit':
                    price = product.purchase_price
                    print('credit initiated')
                    django_logger.info('credit initiated')
                if tnx_type == 'debit':
                    price = product.selling_price
                    print('debit initiated')
                    django_logger.info('debit initiated')

            sub_total = quantity * price

            grand_total = total_amount = sub_total  # Tax, Shipping and Discount are not set for the moment

            order_data = {
                "company": product.company,
                "sub_total": sub_total,
                "total_amount": total_amount,
                "grand_total": grand_total,
                "payment_type": order.get('payment_type', ''),
                "order_status": order.get('order_status', '')
            }

            order_processing = Order(**order_data)
            order_processed = core.save_handler(order_processing)
            if order_processed:
                django_logger.info("order_create_process SUCCESSFUL")
                return TransactionProcess.order_item_create_process(
                    order=order_processed,
                    product=product,
                    price=price,
                    discount=order.get('discount', 0),
                    quantity=quantity,
                    summary=order.get('summary', '')
                )
        except (DecimalException, ValueError, TypeError) as e:
            django_logger.error("{}".format(e))
            return False

    @staticmethod
    def order_item_create_process(**kwargs):
        django_logger.info("order_item_create_process INITIALIZE")
        order_item = OrderItem()
        order_item.order = kwargs.get('order')
        order_item.product = kwargs.get('product')
        order_item.price = kwargs.get('price')
        order_item.discount = kwargs.get('discount')
        order_item.quantity = kwargs.get('quantity')
        order_item.summary = kwargs.get('summary')

        return core.save_handler(order_item)

    @staticmethod
    def order_tnx_operation(tnx_type, transaction, order, order_item):
        django_logger.info("order_tnx_operation INITIALIZE")
        transaction_processing = Transaction()
        transaction_processing.order = order_item.order
        transaction_processing.code = order.get('payment_code', '')
        transaction_processing.type = tnx_type
        transaction_processing.mode = transaction.get('mode', '')
        transaction_processing.status = transaction.get('status', '')
        transaction_processing.summary = transaction.get('summary', '')

        return core.save_handler(transaction_processing)
