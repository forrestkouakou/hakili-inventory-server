from rest_framework import viewsets, permissions, status
from rest_framework.response import Response

from apps.core import apps_config as core
from apps.core.utils import http_return
from apps.product.models import Product
from apps.stock.models import (
    Order,
    OrderItem,
)
from apps.stock.serializers import (
    OrderSerializer,
    OrderItemSerializer,
)
from apps.stock.transactions import TransactionProcess as Tnx
from lib.config import django_logger
from lib.enums import TNX_TYPE

tnx = Tnx()


class OrderViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows order to be viewed or edited.
    """
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(company=self.kwargs['company_pk'])

    def create(self, request, *args, **kwargs):
        """
        Create method override to save Order and OrderItem and Transaction
        We should make sure that every order takes into account the other classes
        """
        data = request.data
        company_pk = int(kwargs.get('company_pk', None))
        product_id = data.get('product')

        # TODO: Add a try/except block here
        # Get the product information
        product = Product.objects.filter(pk=product_id).first()

        # Make sure the company_id received matches the company the product belongs to
        if product.company_id == company_pk and all([company_pk, product.company_id]) is True:
            transaction = data.get('transaction')
            order = data.get('order')
            quantity = order.get('quantity')
            # Try to convert the quantity received to a non-nullable and positive integer
            #   throw an error if the cast is not possible
            try:
                quantity = abs(int(quantity))
                if quantity <= 0:
                    raise ValueError
            except (ValueError, TypeError) as e:
                django_logger.error('{}'.format(e))
                return http_return(False, 'NULL_OR_MISSING_QUANTITY', status.HTTP_400_BAD_REQUEST)

            # Check if the transaction type is specified in the transaction
            if transaction.get('type') in TNX_TYPE:
                tnx_type = transaction.get('type')

                # Initiate processes to false
                product_processed_message = ''
                product_updated = False
                order_processed = False

    def update(self, request, *args, **kwargs):
        data = request.data
        order_pk = int(kwargs.get('pk', None))
        order_data = data.get('order')

        # TODO: take transaction state into account in order to create a line of transaction
        #   example bellow
        """
        transaction_data = data.get('transaction')
        "transaction": {
            "status": "success",
            "summary": "TNX summary"
        }
        """
        order = Order.objects.filter(pk=order_pk).first()
        if order:
            if 'payment_type' in order_data:
                order.payment_type = order_data['payment_type']
            if 'order_status' in order_data:
                order.order_status = order_data['order_status']
            order_updated = core.save_handler(order)
            if order_updated:
                return Response({'status': True, 'context': 'SUCCESSFUL_ORDER_UPDATE'}, status=status.HTTP_200_OK)
            return Response({'status': False, 'context': 'UNSUCCESSFUL_ORDER_UPDATE'},
                            status=status.HTTP_400_BAD_REQUEST)


class OrderItemViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows order item to be viewed or edited.
    """
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    # permission_classes = [permissions.IsAuthenticated]
