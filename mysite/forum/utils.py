menu = [{'title': 'About', 'url_name': 'about'},
        {'title': 'Social media', 'url_name': 'contact'},
       ]

class DataMixin:
    title_page = None
    cat_selected = None
    paginate_by = 5
    extra_context = {}

    def __init__(self):
        if self.title_page:
            self.extra_context['title'] = self.title_page

        if 'cat_selected' is not None:
            self.extra_context['cat_selected'] = self.cat_selected

    def get_mixin_context(self, context, **kwargs):
        context['cat_selected'] = None
        context.update(kwargs)
        return context