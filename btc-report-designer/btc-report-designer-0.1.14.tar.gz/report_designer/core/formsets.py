from django.forms import BaseInlineFormSet, inlineformset_factory
from django.utils.functional import cached_property

from report_designer.core.utils import RenderMixin


class CustomBaseInlineFormSet(RenderMixin, BaseInlineFormSet):
    """
    Кастомный BaseInlineFormSet
    """

    template_name = 'report_designer/core/forms/formset.html'
    context_object_name = 'formset'
    _can_add_item = True

    # Дополнительные классы
    css_formset_container = None
    css_forms_container = None

    def can_add_item(self):
        """
        Можно ли добавлять
        """
        return self._can_add_item

    @cached_property
    def is_empty(self):
        """
        Пустой формсет
        """
        total_forms_count = self.total_form_count()
        empty_forms_count = sum(
            not self.forms[i].has_changed()
            for i in range(self.initial_form_count(), total_forms_count)
        )
        return not bool(total_forms_count - len(self.deleted_forms) - empty_forms_count)

    def get_context_data(self):
        context_data = super().get_context_data()
        context_data.update({
            'css_formset_container': self.css_formset_container,
            'css_forms_container': self.css_forms_container,
            'css_header': self.css_header,
        })
        return context_data


class FormsetManager:
    """
    Менеджер формсета
    """

    parent_model = None
    model = None
    custom_form = None
    custom_formset = BaseInlineFormSet
    extra = 0
    min_num = 0
    validate_min = False
    initial = None
    fk_name = None

    name = None
    prefix = None
    formset_class = None
    _formset = None

    title = None  # Заголовок формсета
    btn_add_title = 'Добавить'

    _is_post = False

    def __init__(self, parent=None, **kwargs):
        self.parent = parent
        if self.name is None:
            raise AttributeError('Не указан name')
        self.manager_kwargs = kwargs

    @property
    def formset(self):
        return self._formset

    def get_initial(self, **kwargs):
        """
        Начальные данные
        """
        return self.initial

    def get_prefix(self) -> str:
        """
        Префикс формсета
        """
        prefix = f'{self.prefix}_{self.name}' if self.prefix else ''
        if self.parent and prefix:
            prefix += f'-{self.parent.pk}'
        return prefix

    def get_formset_class(self, **kwargs):
        if self.formset_class:
            return self.formset_class
        return inlineformset_factory(
            self.parent_model,
            self.model,
            extra=self.extra,
            min_num=self.min_num,
            validate_min=self.validate_min,
            form=self.custom_form,
            fk_name=self.fk_name,
            formset=self.custom_formset,
        )

    def _init_formset(self, data, instance, prefix, **kwargs):
        """
        Получение формсета
        """
        initial = self.get_initial(**kwargs)
        self.update_extra(initial)
        formset_class = self.get_formset_class(**kwargs)
        return formset_class(
            data,
            instance=instance,
            prefix=prefix,
            initial=initial,
            queryset=self.get_queryset(),
            form_kwargs=self.get_manager_kwargs(),
        )

    def get_manager_kwargs(self):
        """
        Дополнительные параметры формсета
        """
        return self.manager_kwargs

    def update_extra(self, initial):
        """
        Обновление extra форм
        """
        if initial:
            self.extra += len(initial)

    def init_formset(self, data, **kwargs):
        """
        Инициализация формсета
        """
        self._is_post = bool(data)
        self._formset = kwargs.get(self.name)
        if not self._formset:
            self._formset = self._init_formset(data, self.parent, self.get_prefix(), **kwargs)
            setattr(self._formset, 'parent', self.parent)
            setattr(self._formset, 'title', self.title)
            setattr(self._formset, 'name', f'js-rd-{self.name}')
            setattr(self._formset, 'btn_add_title', self.btn_add_title)

    def save_formset(self, is_valid: bool):
        """
        Сохранение формсета
        """
        is_valid &= self._formset.is_valid()
        if is_valid:
            self._formset.save()
            self.after_save()
        return is_valid

    def get_queryset(self):
        """
        Получение кверисет
        """
        return None

    def after_save(self) -> None:
        """
        Действия после успешного сохранения формсета
        """
        pass
