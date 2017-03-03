from django.conf.urls import url

from core.views.checklist_views import CreateChecklistItemView, DeleteChecklistItemView, \
                                       GetChecklistItemsForTodayView, GetChecklistItemsView, \
                                       UpdateChecklistItemNameView, UpdateChecklistPriorityView, \
                                       UpdateChecklistItemStatusView, UpdateChecklistItemConditionView, \
                                       UpdateChecklistItemConditionInversionView

app_name = 'checklist'

urlpatterns = [
    url(r'^get_checklist_items/?$', GetChecklistItemsView.as_view(),
        name='get_checklist_items'),
    url(r'^get_checklist_items_for_today/?$', GetChecklistItemsForTodayView.as_view(),
        name='get_checklist_items_for_today'),
    url(r'^add_checklist_item/?$', CreateChecklistItemView.as_view(),
        name='add_checklist_item'),
    url(r'^delete_checklist_item/?$', DeleteChecklistItemView.as_view(),
        name='delete_checklist_item'),

    url(r'^update_checklist_item_name/?$', UpdateChecklistItemNameView.as_view(),
        name='update_checklist_item_name'),
    url(r'^update_checklist_item_condition/?$', UpdateChecklistItemConditionView.as_view(),
        name='update_checklist_item_condition'),
    url(r'^update_checklist_item_condition_inversion/?$', UpdateChecklistItemConditionInversionView.as_view(),
        name='update_checklist_item_condition_inversion'),
    url(r'^update_checklist_item_status/?$', UpdateChecklistItemStatusView.as_view(),
        name='update_checklist_item_status'),
    url(r'^update_checklist_priority/?$', UpdateChecklistPriorityView.as_view(),
        name='update_checklist_priority'),
]
