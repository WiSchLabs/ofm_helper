from django.conf.urls import url

from core.views.checklist_views import CreateChecklistItemView, DeleteChecklistItemView, \
                                       GetChecklistItemsForTodayView, GetChecklistItemsView, \
                                       UpdateChecklistItemView, UpdateChecklistPriorityView

app_name = 'checklist'
urlpatterns = [
    url(r'^get_checklist_items/?$', GetChecklistItemsView.as_view(),
        name='get_checklist_items'),
    url(r'^get_checklist_items_for_today/?$', GetChecklistItemsForTodayView.as_view(),
        name='get_checklist_items_for_today'),
    url(r'^add_checklist_item/?$', CreateChecklistItemView.as_view(),
        name='add_checklist_item'),
    url(r'^update_checklist_item/?$', UpdateChecklistItemView.as_view(),
        name='update_checklist_item'),
    url(r'^delete_checklist_item/?$', DeleteChecklistItemView.as_view(),
        name='delete_checklist_item'),
    url(r'^update_checklist_priority/?$', UpdateChecklistPriorityView.as_view(),
        name='update_checklist_priority'),
]
