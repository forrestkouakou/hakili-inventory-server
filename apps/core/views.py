from datetime import datetime, timezone

from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['GET'])
def is_alive(request, version="v1|v2"):
    alive_date = datetime.now(tz=timezone.utc)
    return Response({'is_alive': 'yes', 'date': alive_date})
