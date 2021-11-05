from report_designer.core.utils import RenderMixin, prepare_attrs


class BoundAction(RenderMixin):
    """
    Дейсвие:

    - обычное:ссылка (<a href=""></a>)
    - обычное:кнопка (<a class="btn" href=""></a>)
    - утверждение:кнопка (<button type="button"></button>)
    - дропдаун:кнопка
    """

    title = 'Действие'
    template_name = 'report_designer/core/actions/action.html'

    # html параменты
    tag_name = 'a'  # a, button
    common_css_classes = ''

    def __init__(self, user, obj=None, **kwargs) -> None:
        self.user = user
        self.obj = obj
        self.kwargs = kwargs
        self.title = kwargs.pop('title', None)
        self.url = kwargs.pop('url', None) or self.get_url()
        self.css_classes = kwargs.pop('css_classes', '') or ''

    def get_title(self) -> str:
        """
        Заголовок кнопки
        """
        return self.title

    def get_context_data(self):
        context_data = super().get_context_data()
        context_data.update(
            {
                'title': self.get_title(),
                'url': self.url,
                'tag_name': self.tag_name,
                'data_attrs': prepare_attrs(self.get_data_attrs(), prefix='data'),
                'attrs': prepare_attrs(self.get_attrs()),
                'css_classes': self.get_css_classes(),
                **self.kwargs
            }
        )
        return context_data

    def get_url(self) -> str:
        """
        Получение url-дейсвия
        """
        return '#'

    def get_attrs(self) -> dict:
        """
        Получение атрибутов
        """
        return {}

    def get_data_attrs(self) -> dict:
        """
        Получение дата-атрибутов
        """
        return {}

    def get_css_classes(self) -> str:
        """
        Получение css-классов
        """
        return ' '.join([self.common_css_classes, self.css_classes])


class BaseBoundAction(BoundAction):
    """
    Базовое действие
    """

    def get_attrs(self) -> dict:
        attrs = super().get_attrs()
        attrs.update({
            'href': self.url,
        })
        return attrs


class DropdownBoundAction(BaseBoundAction):
    """
    Действие в выпадающем списке
    """

    template_name = 'report_designer/core/actions/dropdown_action.html'


class SimpleBoundAction(BaseBoundAction):
    """
    Простое действие (ссылка в виде кнопки)
    """

    common_css_classes = 'btn btn-primary pull-right'


class SimpleModalBoundAction(SimpleBoundAction):
    """
    Простое действие c модалкой
    """

    common_css_classes = SimpleBoundAction.common_css_classes + ' js-rd-ajax-load-modal-btn'

    def get_data_attrs(self) -> dict:
        data_attrs = super().get_data_attrs()
        data_attrs.update({'modal-lg': self.kwargs.pop('is_large', False)})
        return data_attrs


class UpdateDropdownModalBoundAction(DropdownBoundAction):
    """
    Действие редактирования через модалку
    """

    common_css_classes = 'js-rd-ajax-load-modal-btn'

    def get_url(self) -> str:
        if self.obj and hasattr(self.obj, 'get_edit_url'):
            return self.obj.get_edit_url()
        return super().get_url()


class BaseFormSaveBoundAction(SimpleBoundAction):
    """
    Действие отправки формы
    """

    tag_name = 'button'
    common_css_classes = SimpleBoundAction.common_css_classes + ' js-rd-form-submit-btn'

    def get_attrs(self) -> dict:
        attrs = super().get_attrs()
        attrs.update({
            'type': 'submit',
        })
        return attrs


class Action:
    """
    Действие
    """

    title = 'Действие'
    bound_action = BoundAction

    def __init__(self, title=None, url=None, **kwargs):
        super().__init__()
        if title:
            self.title = title
        self.url = url
        self.css_classes = kwargs.get('css_classes')
        self.kwargs = kwargs

    def get_bound_action(self, user, obj=None):
        return self.bound_action(user, obj, **self.get_bound_action_kwargs())

    def get_bound_action_kwargs(self) -> dict:
        return {
            'title': self.title,
            'url': self.url,
            'css_classes': self.css_classes,
            **self.kwargs,
        }


class SimpleAction(Action):
    """
    Простое действие кнопкой
    """

    bound_action = SimpleBoundAction


class SimpleModalAction(Action):
    """
    Простое действие c модалкой
    """

    bound_action = SimpleModalBoundAction


class FormSaveSubmitAction(Action):
    """
    Действие отправки формы (Сохранение)
    """

    title = 'Сохранить'
    bound_action = BaseFormSaveBoundAction


class UpdateDropdownModalAction(Action):
    """
    Действие редактирования объекта в модальной форме
    """

    title = 'Редактировать'
    bound_action = UpdateDropdownModalBoundAction


class ActionGroup(RenderMixin):
    """
    Группа действий
    """

    name = 'action_group'
    template_name = 'report_designer/core/actions/action_group.html'
    actions = dict()
    bound_actions = dict()
    css_classes = 'pull-right'

    def __init__(self, user, obj=None, **kwargs):
        self.user = user
        self.obj = obj
        self.kwargs = kwargs
        self.actions = self.get_actions()

    def __iter__(self):
        for key, action in self.get_bound_actions().items():
            yield action

    def get_template_name(self) -> str:
        return self.template_name

    def get_context_data(self):
        context_data = super().get_context_data()
        context_data.update(
            {
                'action_group': self, **self.get_css_classes(),
                **self.kwargs
            }
        )
        return context_data

    def get_actions(self) -> dict:
        """
        Получение действий
        """
        actions = dict()
        for base in self.__class__.__bases__:
            actions.update(self._get_actions(base.__dict__))
        actions.update(self._get_actions(self.__class__.__dict__))
        return actions

    def _get_actions(self, class_dict):
        actions = dict()
        for name, action in class_dict.items():
            if isinstance(action, Action):
                actions.update({name: action})
        return actions

    def get_bound_actions(self):
        if not self.bound_actions:
            bound_actions = dict()
            for name, action in self.actions.items():
                bound_action = action.get_bound_action(self.user, self.obj)
                bound_actions.update({name: bound_action})
            self.bound_actions = bound_actions
        return self.bound_actions

    def get_css_classes(self):
        return dict(css_classes=self.css_classes)


class FormActionGroup(ActionGroup):
    """
    Группа действий в форме
    """

    submit = FormSaveSubmitAction()


class DropdownActionGroup(ActionGroup):
    """
    Группа действий (Выпадающий список)
    """

    name = 'dropdown_action_group'
    template_name = 'report_designer/core/actions/dropdown_action_group.html'
