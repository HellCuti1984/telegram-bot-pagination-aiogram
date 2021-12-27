from .pagination_handler import register_pagination_handler


def register_handlers(dp):
    register_pagination_handler(dp)
