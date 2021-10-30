from tornadmin.decorators import action


@action(
    label='Delete selected',
    require_confirmation=True,
    modal_title='Delete selected?',
    modal_body='Are you sure you want to permanently delete selected items? This action can\'t be undone.',
    modal_button_label='Delete',
    modal_button_class='outline-danger'
)
async def delete_selected(admin, handler, queryset):
    await queryset.delete()
