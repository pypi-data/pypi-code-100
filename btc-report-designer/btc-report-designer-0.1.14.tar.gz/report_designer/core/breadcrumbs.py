from report_designer.core.utils import RenderMixin


class Breadcrumb(RenderMixin):
    """
    Хлебная крошка
    """

    template_name = 'report_designer/core/breadcrumbs/breadcrumb.html'

    def __init__(self, title, url=None, **kwargs) -> None:
        super().__init__()
        self.title = title
        self.url = url
        self.kwargs = kwargs

    def get_context_data(self):
        context = dict(title=self.title, url=self.url)
        context.update(**self.kwargs)
        return context


class Breadcrumbs(RenderMixin):
    """
    Хлебные крошки
    """

    template_name = 'report_designer/core/breadcrumbs/breadcrumbs.html'
    breadcrumbs = tuple()

    def __init__(self, *breadcrumb: Breadcrumb, **kwargs) -> None:
        super().__init__()
        self.breadcrumbs = breadcrumb
        self.kwargs = kwargs

    def get_context_data(self):
        context = dict(breadcrumbs=self.breadcrumbs)
        context.update(**self.kwargs)
        return context

    def add_breadcrumbs(self, *breadcrumb: Breadcrumb) -> None:
        """
        Добавление хлебных крошек
        """
        self.breadcrumbs += breadcrumb


class BreadcrumbsMixin:
    """
    Миксин хлебных крошек
    Пример:

    В шаблоне:
    {{ breadcrumbs }} - breadcrumbs_context_name

    Добавление:
    def get_breadcrumbs(self, **kwargs) -> Breadcrumbs:
        breadcrumbs = super().get_breadcrumbs(**kwargs)
        breadcrumbs.add_breadcrumbs(Breadcrumb(title='Реестр', url=reverse_lazy('obj:list')),
                                    Breadcrumb(title=self.parent, url=self.parent.get_detail_url()),
                                    Breadcrumb(title=self.title))
        return breadcrumbs
    """

    breadcrumbs_context_name = 'breadcrumbs'
    breadcrumbs_css_classes = 'breadcrumbs_white'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            self.breadcrumbs_context_name: self.get_breadcrumbs(**kwargs),
        })
        return context

    def get_breadcrumbs_kwargs(self, **kwargs):
        kwargs.update(dict(breadcrumbs_css_classes=self.breadcrumbs_css_classes))
        return kwargs

    def get_breadcrumbs(self, **kwargs) -> Breadcrumbs:
        """
        Получение хлебных крошек
        """
        kwargs = self.get_breadcrumbs_kwargs(**kwargs)
        return Breadcrumbs(**kwargs)
