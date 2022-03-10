from apps.core.models import WebActionHistory


def web_action_logger(**kwargs):
    if len(kwargs) > 0:
        web_logger = WebActionHistory()
        # web_logger.user = kwargs.get("user", None)
        web_logger.entity = kwargs.get("table_name", None)
        web_logger.item = kwargs.get("item", None)
        web_logger.request_id = kwargs.get("request_id", None)
        web_logger.action_name = kwargs.get("action_name", None)
        web_logger.out_state = kwargs.get("out_state", None)
        web_logger.out_msg = kwargs.get("out_msg", None)
        # web_logger.datetime = datetime.now(tz=timezone.utc)
        web_logger.save()
