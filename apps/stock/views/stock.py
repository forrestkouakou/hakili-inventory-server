from rest_framework import viewsets, permissions, status
from rest_framework.response import Response

from apps.core import apps_config
from apps.core import apps_config as core
from apps.stock.serializers import *
from apps.stock.transactions import TransactionProcess as Tnx
from lib.config import django_logger

tnx = Tnx()


class BrandViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows product brand to be viewed or edited.
    """
    serializer_class = BrandSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Brand.objects.filter(company=self.kwargs['company_pk'])


class CategoryViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows product category to be viewed or edited.
    """
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Category.objects.filter(company=self.kwargs['company_pk'])


class ProductViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows product to be viewed or edited.
    """
    serializer_class = ProductReadSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Product.objects.filter(company=self.kwargs['company_pk'])

    def get_serializer_class(self):
        serializer_class = self.serializer_class

        if self.request.method in apps_config.WRITE_METHODS:
            serializer_class = ProductWriteSerializer

        return serializer_class


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
        product = Product.objects.filter(pk=product_id).first()

        if product.company_id == company_pk and all([company_pk, product.company_id]) is True:
            transaction = data.get('transaction')
            order = data.get('order')
            quantity = order.get('quantity')
            try:
                quantity = abs(int(quantity))
                if quantity <= 0:
                    raise ValueError
            except (ValueError, TypeError) as e:
                django_logger.error('{}'.format(e))
                context = "NULL_OR_MISSING_QUANTITY"
                return Response({'status': False, 'context': context}, status=status.HTTP_400_BAD_REQUEST)

            # Check if the transaction type is specified in the transaction
            if transaction.get('type') in TNX_TYPE:
                tnx_type = transaction.get('type')

                # Initiate Product and Order/OrderItem values to false
                product_processed_message = ''
                product_updated = False
                order_processed = False

                if product_updated:
                    # TODO: find a better place to put successful messages
                    django_logger.info(product_processed_message)

                    order_processed = tnx.order_create_process(
                        tnx_type=tnx_type,
                        quantity=quantity,
                        order=data.get('order'),
                        product=product
                    )

                if order_processed:
                    # TODO rollback product update if order is not processed
                    django_logger.info("order_create_process SUCCESSFUL")

                    transaction_processed = tnx.order_tnx_operation(
                        tnx_type=tnx_type,
                        transaction=transaction,
                        order=order,
                        order_item=order_processed
                    )

                    if transaction_processed:
                        django_logger.info("order_tnx_operation SUCCESSFUL")

                context = "SUCCESSFUL_ORDER_CREATE"

                # product_serializer = ProductReadSerializer(product_updated).data
                # print("product_serializer ==> {}".format(product_serializer))
                # order_serializer = OrderSerializer(order_processed.order).data
                # print("order_serializer ==> {}".format(order_serializer))
                # order_item_serializer = OrderItemSerializer(order_processed).data
                # print("order_item_serializer ==> {}".format(order_item_serializer))
                #
                # product_serializer.pop('company', '')
                # product_serializer.pop('brand', '')
                # product_serializer.pop('category', '')
                # product_serializer.pop('metadata', '')
                #
                #
                # serializer_data = {
                #     'product': dict(product_serializer),
                #     'order': dict(order_serializer)
                # }

                return Response(
                    {
                        'status': True,
                        'context': context,
                        # 'data': serializer_data # TODO: return the product and the order details
                    },
                    status=status.HTTP_201_CREATED)
            else:
                context = "NULL_OR_MISSING_TNX_TYPE"
                return Response({'status': False, 'context': context}, status=status.HTTP_400_BAD_REQUEST)

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
            return Response({'status': False, 'context': 'UNSUCCESSFUL_ORDER_UPDATE'}, status=status.HTTP_400_BAD_REQUEST)


class OrderItemViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows order item to be viewed or edited.
    """
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    # permission_classes = [permissions.IsAuthenticated]
