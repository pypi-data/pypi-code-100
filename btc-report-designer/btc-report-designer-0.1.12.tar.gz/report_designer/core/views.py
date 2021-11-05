from copy import deepcopy

from django.contrib import messages
from django.contrib.messages import constants
from django.db import transaction
from django.db.models import F
from django.http import JsonResponse, HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.functional import cached_property
from django.utils.safestring import mark_safe
from django.views.generic import ListView, CreateView, UpdateView
from django.views.generic.list import BaseListView
from django.views.generic.detail import BaseDetailView
from django_filters.views import FilterView

from report_designer.core.actions import FormActionGroup
from report_designer.core.breadcrumbs import BreadcrumbsMixin, Breadcrumb


class TitleMixin:
    """
    Миксин заголовка страницы
    """

    title = None

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        context_data.update({'title': self.get_title()})
        return context_data

    def get_title(self):
        """
        Заголовок страницы
        """
        return self.title


class BackUrlMixin:
    """
    Миксин получение url-адреса для возврата
    """

    back_url = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                'back_url': self.get_back_url(),
            }
        )
        return context

    def get_back_url(self):
        """
        Получение url-адреса возврата
        """
        return self.back_url


class AjaxViewMixin:
    """
    Миксин запросов Ajax
    """

    # HTTP response class
    ajax_response_class = JsonResponse
    is_only_ajax = False

    def dispatch(self, request, *args, **kwargs):
        if self.is_only_ajax and not self.is_ajax:
            raise Http404('Only allow authorized AJAX requests')
        return super().dispatch(request, *args, **kwargs)

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.is_ajax = request.is_ajax()


class AjaxDependentObjectMixin:
    """
    Миксин зависимого объекта
    (По собираемому ключу производятся действия на фронтенде)
    """

    # Зависимый объект, с которым необходимо произвести
    # действие после получения успешного ответа в js
    # Пример объекта: (key, value)
    dependents = ()

    def additional_ajax_response_kwargs(self, context=None, **kwargs):
        ajax_response_kwargs = super().additional_ajax_response_kwargs(context, **kwargs)
        if kwargs.get('success', False):
            if self.dependents:
                dependents = (
                    {
                        'dependent_key': key,
                        'dependent_name': name,
                    }
                    for key, name in self.dependents
                )
                ajax_response_kwargs.update({'dependents': list(dependents)})
        return ajax_response_kwargs


class ParentMixin:
    """
    Миксин родителя
    """

    parent_model = None
    parent_queryset = None
    kwargs_parent_fk = 'pk'
    parent_field = None
    parent_context_name = 'parent'

    def get_parent_model(self):
        """
        Получение родительской модели
        """
        return self.parent_model

    def get_queryset(self):
        """
        Фильтрация queryset по родителю
        :return:
        """
        queryset = super().get_queryset()
        if self.parent_field:
            queryset = queryset.filter(**{self.parent_field: self.parent})
        return queryset

    def get_parent_queryset(self):
        """
        Получение кверисета родительского объекта
        """
        parent_model = self.get_parent_model()
        assert self.parent_queryset is not None or parent_model is not None, (
            "'%s' должен включать либо атрибут `parent_queryset`, либо атрибут `parent_model`, "
            "или необходимо переопределить метод `get_parent()`." % self.__class__.__name__
        )
        return parent_model.objects.all() if parent_model else self.parent_queryset

    def get_parent_fk(self) -> int:
        """
        Получение pk родителя
        """
        return self.kwargs.get(self.kwargs_parent_fk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({self.parent_context_name: self.parent})
        return context

    def get_serializer_context(self):
        serializer_context = super().get_serializer_context()
        serializer_context.update({self.parent_context_name: self.parent})
        return serializer_context

    @cached_property
    def parent(self):
        """
        Получение родительского объекта
        """
        return get_object_or_404(self.get_parent_queryset(), pk=self.get_parent_fk())


class BreadcrumbsListMixin(BreadcrumbsMixin):
    """
    Миксин со стандратными методами для представлений шиблонов
    """

    title_breadcrumb = None

    def get_breadcrumbs(self, **kwargs):
        breadcrumbs = super().get_breadcrumbs(**kwargs)
        breadcrumbs.add_breadcrumbs(
            Breadcrumb(title=self.title_breadcrumb, url=reverse_lazy(f'{self.request.resolver_match.namespace}:list'))
        )
        return breadcrumbs


class BreadcrumbsDetailMixin:
    """
    Миксин со стандратными методами для представлений шиблонов
    """

    def get_breadcrumbs(self, **kwargs):
        breadcrumbs = super().get_breadcrumbs(**kwargs)
        breadcrumbs.add_breadcrumbs(Breadcrumb(title=self.get_title()))
        return breadcrumbs


class BackUrlDetailMixin(BackUrlMixin):
    """
    Ссылка на список для просмотров
    """

    def get_back_url(self):
        return reverse_lazy(f'{self.request.resolver_match.namespace}:list')


class AjaxResponseMixin(AjaxViewMixin):
    """
    Миксин: Ajax-ответ
    """

    def render_to_response(self, context, **response_kwargs):
        """
        Подготовка ответа
        """
        if self.is_ajax:
            return self.render_to_ajax_response(context, **response_kwargs)
        return super().render_to_response(context, **response_kwargs)

    def render_to_ajax_response(self, context=None, render_template=True, **response_kwargs):
        """
        Подготовка Ajax ответа
        """
        response_kwargs.update(
            {
                **(render_template and {'html': self.render_template(context)} or {}),
                **self.additional_ajax_response_kwargs(context, **response_kwargs),
            }
        )
        return self.ajax_response_class(response_kwargs)

    def render_template(self, context, template_names=None):
        """
        Рендеринг шаблона в Ajax-ответ
        """
        if not template_names:
            template_names = hasattr(self, 'get_template_names') and self.get_template_names()
        return render_to_string(template_name=template_names, context=context, request=self.request)

    def additional_ajax_response_kwargs(self, context=None, **kwargs):
        """
        Дополнительные данные для Ajax-ответа
        """
        return {}


class AjaxFormResponseMixin(AjaxDependentObjectMixin, AjaxResponseMixin):
    """
    Миксин: Ajax-ответ для форм
    """

    success_message = 'Данные успешно сохранены'
    error_message = 'При сохранении данных произошла ошибка'

    def _base_response(self, success, render_template, response_kwargs: dict = None, **context_kwargs):
        """
        Базовый ответ
        """
        context_data = self.get_context_data(**context_kwargs)
        message = success and self.get_success_message(context_data) or self.get_error_message(context_data)
        response = self.render_to_response(
            context_data,
            render_template=render_template,
            success=success,
            message=message,
        )
        if not self.is_ajax:
            messages.add_message(self.request, success and constants.SUCCESS or constants.ERROR, message)
        return response

    def success_response(self):
        """
        Ответ при успешном действии
        """
        if self.is_ajax:
            return self._base_response(success=True, render_template=False)
        return HttpResponseRedirect(self.get_success_url())

    def error_response(self, form=None, render_template=True):
        """
        Ответ при успешном действии
        """
        return self._base_response(success=False, render_template=render_template, form=form)

    def get_success_message(self, context_data):
        """
        Сообщение об успешном действии
        """
        return self.success_message

    def get_error_message(self, context_data):
        """
        Сообщение об успешном действии
        """
        return self.error_message

    def additional_ajax_response_kwargs(self, context=None, **kwargs):
        response_kwargs = super().additional_ajax_response_kwargs(context, **kwargs)
        if kwargs.get('success', False):
            redirect_url = self.get_success_redirect_url()
            if redirect_url:
                response_kwargs.update(redirect_url=redirect_url)
        return response_kwargs

    def get_success_redirect_url(self):
        """
        URL перенаправления после успешного действия
        """
        return None


class ActionGroupMixin:
    """
    Пример:

    В шаблоне:
    {{ action_group }} - action_group_class.name
    """

    action_group_classes = []

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        obj = self.get_object_for_action_groups()
        if self.can_view_action_groups(obj):
            context.update(self.get_action_groups(obj, **kwargs))
        return context

    def get_object_for_action_groups(self):
        """
        Получение объекта для групп действий
        """
        try:
            return self.get_object()
        except AttributeError:
            return None

    def can_view_action_groups(self, obj) -> bool:
        """
        Проверка, можно ли отобразить группы действий
        """
        return True

    def get_action_groups(self, obj, **kwargs) -> dict:
        """
        Получение групп действий
        """
        action_groups = dict()
        for action_group_class in self.get_action_group_classes():
            group_kwargs = self.get_action_group_kwargs(**kwargs)
            kwargs_by_name = group_kwargs.get(f'kwargs_{action_group_class.name}', dict())
            action_class = action_group_class(self.request.user, obj, **kwargs_by_name)
            action_groups.update(
                {
                    action_class.name: action_class,
                }
            )
        return action_groups

    def get_action_group_classes(self):
        """
        Получение классов групп действий
        """
        return deepcopy(self.action_group_classes)

    def get_action_group_kwargs(self, **kwargs):
        """
        Дополнительные параметры для групп действий
        """
        return {}


class DynamicContentMixin(AjaxResponseMixin):
    """
    Представление: Динамическая загрузка контента
    """

    template_name = None
    template_name_content = None

    # URL kwargs типов
    base_type = 'base'
    content_type = 'content'

    ajax_content_name = None

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        # Тип запроса из URL
        self.type = kwargs.get('type')

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        context_data.update({'content_url': self.get_content_url(), 'ajax_content_name': self.ajax_content_name})
        return context_data

    @property
    def is_content_type(self):
        """
        Тип контента
        """
        return self.type == self.content_type

    @property
    def is_base_type(self):
        """
        Базовый тип
        """
        return self.type == self.base_type

    def get_template_names(self):
        """
        Получение шаблона в зависимости от типа запроса
        """
        if self.is_content_type:
            return [self.template_name_content]
        return super().get_template_names()

    def get_content_url(self):
        """
        Получение URL для контента
        """
        return reverse_lazy(self.request.resolver_match.view_name, kwargs=self.get_content_url_kwargs())

    def get_content_url_kwargs(self):
        """
        Параметры URL для контента
        """
        return {'type': self.content_type}


class FormsetManagerMixin:
    """
    Миксин создания/редактирования формсетов
    """

    formset_managers = ()

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data.update(**self.get_formsets(self.request.POST or None, **kwargs))
        return context_data

    def get_formsets(self, data=None, **kwargs):
        """
        Получение формсетов
        """
        formsets = {}
        for manager in self._init_formset_managers(**kwargs):
            manager.init_formset(data=data, **kwargs)
            formsets.update(
                {
                    manager.name: manager.formset,
                }
            )
        return formsets

    def _init_formset_managers(self, **kwargs):
        """
        Инициализация менеджеров формсетов
        """
        managers = []
        for formset_manager in self.get_formset_managers():
            kwargs = self.get_formset_managers_kwargs(**kwargs)
            kwargs_by_manager_name = kwargs.get(f'kwargs_{formset_manager.name}', dict())
            managers.append(formset_manager(parent=self.get_formset_manager_parent(), **kwargs_by_manager_name))
        return managers

    def save_formsets(self, is_valid: bool, **kwargs):
        """
        Сохранение формсетов
        """
        formsets = {}
        for manager in self._init_formset_managers(**kwargs):
            manager.init_formset(data=self.request.POST or None, **kwargs)
            is_valid &= manager.save_formset(is_valid)
            formsets.update(
                {
                    manager.name: manager.formset,
                }
            )
        return is_valid, formsets

    def get_formset_managers(self):
        """
        Получение списка менеджеров
        """
        return self.formset_managers

    def get_formset_managers_kwargs(self, **kwargs):
        """
        Получение kwargs для менеджеров формсетов
        для формсета {'kwargs_manager_name': {'name': value}}
        """
        return kwargs

    def get_formset_manager_parent(self):
        """
        Получение родителя для менеджеров формсетов
        :default: self.object
        """
        return self.object


class CreateUpdateMixin(FormsetManagerMixin, ActionGroupMixin, TitleMixin, AjaxFormResponseMixin):
    """
    Миксин создания / редактирования
    """

    create_mode = False
    edit_mode = False
    action_group_classes = (FormActionGroup,)

    def post(self, request, *args, **kwargs):
        sid = transaction.savepoint()
        form = self.get_form()
        is_valid = self.form_is_valid(form)
        if is_valid:
            self.before_save()
            self.form_save(form)

        # Дополнительное сохранение
        is_valid_additional, data = self.additional_save(is_valid)
        if is_valid and is_valid_additional:
            self.after_save(form=form)
            transaction.savepoint_commit(sid)
            return self.success_response()
        else:
            transaction.savepoint_rollback(sid)
            return self.error_response(form)

    def additional_save(self, is_valid, **kwargs):
        """
        Сохранение дочерних объектов
        """
        return self.save_formsets(is_valid, **kwargs)

    def before_save(self):
        """
        Действие до сохранения формы
        """
        pass

    def after_save(self, **kwargs):
        """
        Действие после сохранения формы
        """
        pass

    def form_is_valid(self, form):
        """
        Валидация формы
        """
        return form.is_valid()

    def form_save(self, form):
        """
        Валидация формы
        """
        self.object = form.save(False)
        self.set_object_additional_values(self.object)
        self.object.save()
        form.save_m2m()

    def form_valid(self, form):
        """
        Действия при валидности формы
        """
        self.before_save()
        self.form_save(form)
        self.after_save(form=form)

    def set_object_additional_values(self, obj):
        """
        Дополнительные данные при сохранении объекта
        """
        pass

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data.update(
            {
                'create_mode': self.create_mode,
                'edit_mode': self.edit_mode,
            }
        )
        return context_data


class CustomCreateView(CreateUpdateMixin, CreateView):
    """
    Представления создания объекта
    """

    create_mode = True

    def get(self, request, *args, **kwargs):
        self.object = None
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = None
        return super().post(request, *args, **kwargs)


class CustomUpdateView(CreateUpdateMixin, UpdateView):
    """
    Представления создания объекта
    """

    update_mode = True

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)


class ModalInformationMessageMixin:
    """
    Миксин вывода информации в модальном окне
    """

    template_modal_information = 'report_designer/modal_information_body.html'

    def render_modal_information(self, title=None, message=None):
        """
        Рендеринг тела модального окна сообщения
        """
        return render_to_string(self.template_modal_information, {'title': title, 'message': message})


class ObjectActionAjaxView(
    TitleMixin,
    ModalInformationMessageMixin,
    AjaxFormResponseMixin,
    BaseDetailView,
):
    """
    Дейтсвие над объектом
    """

    http_method_names = ('post',)
    join_errors = False

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self._errors = []

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        is_valid = self.valid_action()
        if is_valid:
            self.action()
            return self.success_response()
        else:
            return self.error_response(render_template=False)

    def valid_action(self):
        """
        Можно ли совершить действие
        """
        return True

    def action(self):
        """
        Действие
        """
        pass

    def add_error(self, error):
        """
        Добавление ошибки
        """
        self._errors.append(error)

    def errors(self):
        """
        Список ошибок
        """
        if self.join_errors:
            return mark_safe("\n".join(self._errors))
        return self._errors

    def additional_ajax_response_kwargs(self, context=None, **kwargs):
        response_kwargs = super().additional_ajax_response_kwargs(context, **kwargs)
        if not kwargs.get('success', False):
            response_kwargs.update({'html': self.render_modal_information(self.get_title(), self.errors())})
        return response_kwargs


class CreateUpdateAjaxMixin:
    """
    Миксин: Ajax создание / редактирование
    """

    template_name = 'report_designer/modal_form_body.html'
    form_name = 'create'
    is_only_ajax = True

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data.update({'form_name': self.form_name})
        return context_data


class CreateAjaxView(CreateUpdateAjaxMixin, CustomCreateView):
    """
    Представление: Ajax создание объекта
    """

    pass


class UpdateAjaxView(CreateUpdateAjaxMixin, CustomUpdateView):
    """
    Представление: Ajax редактирование объекта
    """

    pass


class CustomBaseListView(ActionGroupMixin, ListView):
    """
    Базовое представление списка объектов
    """

    is_paginate = True
    paginate_choices = (10, 20, 30)
    pagination_count_name = 'pagination_count'

    def get_paginate_by(self, queryset):
        if self.is_paginate:
            paginate_by = (
                self.request.GET.get(self.pagination_count_name)
                or self.request.session.get(self.pagination_count_name)
                or self.paginate_choices[0]
            )
            self.save_paginate_by(paginate_by)
            return paginate_by

    def save_paginate_by(self, paginate_by):
        """
        Сохранение пагинации в сессию
        """
        self.request.session[self.pagination_count_name] = paginate_by

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                'is_paginate': self.is_paginate,
                'paginate_choices': self.paginate_choices,
                'pagination_count_name': self.pagination_count_name,
            }
        )
        return context


class AjaxContentListView(AjaxResponseMixin, CustomBaseListView):
    """
    Представление: Ajax-загрузка списка объектов
    """

    pass


class DynamicContentBaseListView(DynamicContentMixin, FilterView, CustomBaseListView):
    """
    Представление: Динамическая загрузка списка объектов
    """

    def get_queryset(self):
        # Если указан filterset и тип запроса == self.base_type,
        # возвращается пустой queryset
        queryset = super().get_queryset()
        if self.is_base_type:
            return queryset.none()
        return queryset


class DynamicContentTableBaseView(TitleMixin, DynamicContentBaseListView):
    """
    Представление: Представление списка объектов в виде таблицы
    """

    template_name = 'report_designer/core/dynamic_tables/base.html'
    ajax_template_name = 'report_designer/core/dynamic_tables/content.html'
    template_name_content = 'report_designer/core/dynamic_tables/table.html'
    table_class = None
    filters_clear = True

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        context_data.update(
            {
                **self.get_table_context_data(context_data),
                'filters_clear': self.filters_clear,
            }
        )
        return context_data

    def get_table_context_data(self, context):
        """
        Таблица в контексте шаблона
        """
        if self.is_content_type:
            return {'table': self.init_table(context.get('object_list'))}
        return {}

    def init_table(self, queryset, **kwargs):
        """
        Инициализация таблицы
        """
        table_class = self.get_table_class()
        if not table_class:
            return
        table = table_class(queryset=queryset, request_get=self.request.GET.copy(), **self.get_table_kwargs())
        table.create_table()
        return table

    def get_table_class(self):
        """
        Класс таблицы
        """
        return self.table_class

    def get_table_kwargs(self):
        """
        Параметры таблицы
        """
        return {}

    def save_paginate_by(self, paginate_by):
        if self.is_content_type:
            super().save_paginate_by(paginate_by)

    def get_template_names(self):
        if self.is_base_type and self.is_ajax:
            return [self.ajax_template_name]
        return super().get_template_names()


class Select2BaseListView(AjaxViewMixin, BaseListView):
    """
    Загрузка полей select2
    """

    fields = ('name', 'id')

    def get(self, request, *args, **kwargs):
        empty_label = self.get_empty_label()
        data = (
            *(empty_label and ({'id': '', 'name': empty_label},) or ()),
            *list(self.get_queryset().values(*self.fields)),
        )
        return self.ajax_response_class(data, safe=False)

    def get_empty_label(self):
        """
        Получение пустого значения
        """
        return self.request.GET.get('empty_label')
