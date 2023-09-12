from django.core.paginator import Paginator

from config.settings import PAGINATOR


class CustomPaginator(Paginator):

    def __init__(self, request, object_list, per_page=None, orphans=0, allow_empty_first_page=True):
        self.request = request
        per_page = request.GET.get(PAGINATOR.get('page_size'), 10)
        super().__init__(object_list, per_page, orphans, allow_empty_first_page)

    def get_page(self, **kwargs):
        page_index = self.request.GET.get(PAGINATOR.get('page_index'), 1)
        if self.per_page > PAGINATOR.get('max_page_size'):
            self.per_page = PAGINATOR.get('max_page_size')
        return super().get_page(number=page_index)
