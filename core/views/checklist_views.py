from braces.views import JSONResponseMixin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View

from core.models import ChecklistItem, Matchday, Match, Checklist


@method_decorator(login_required, name='dispatch')
class GetChecklistItemsView(JSONResponseMixin, View):
    def get(self, request):
        checklist_items = ChecklistItem.objects.filter(checklist__user=request.user)

        checklist_items_json = [_get_checklist_item_in_json(item) for item in checklist_items]

        return self.render_json_response(checklist_items_json)


@method_decorator(login_required, name='dispatch')
class GetChecklistItemsForTodayView(JSONResponseMixin, View):
    def get(self, request):
        current_matchday = Matchday.get_current()
        home_match_tomorrow = Match.objects.filter(
            user=request.user,
            matchday__season__number=current_matchday.season.number,
            matchday__number=current_matchday.number + 1,
            is_home_match=True
        )
        checklist_items = ChecklistItem.objects.filter(checklist__user=request.user)
        checklist_items_everyday = checklist_items.filter(
            to_be_checked_on_matchdays=None,
            to_be_checked_on_matchday_pattern=None,
            to_be_checked_if_home_match_tomorrow=False
        )
        filtered_checklist_items = []
        filtered_checklist_items.extend(checklist_items_everyday)
        checklist_items_this_matchday = checklist_items.filter(
            to_be_checked_on_matchdays__isnull=False,
            to_be_checked_on_matchday_pattern=None,
            to_be_checked_if_home_match_tomorrow=False
        )
        filtered_checklist_items.extend([c for c in checklist_items_this_matchday if
                                         current_matchday.number in [int(x) for x in
                                                                     c.to_be_checked_on_matchdays.split(',')]])
        if home_match_tomorrow:
            checklist_items_home_match = checklist_items.filter(
                to_be_checked_on_matchdays=None,
                to_be_checked_on_matchday_pattern=None,
                to_be_checked_if_home_match_tomorrow=True
            )
            filtered_checklist_items.extend(checklist_items_home_match)
        if current_matchday.number > 0:
            checklist_items_matchday_pattern_pre = checklist_items.filter(
                to_be_checked_on_matchdays=None,
                to_be_checked_on_matchday_pattern__isnull=False,
                to_be_checked_if_home_match_tomorrow=False
            )
            checklist_items_matchday_pattern = [c for c
                                                in checklist_items_matchday_pattern_pre
                                                if current_matchday.number % c.to_be_checked_on_matchday_pattern == 0]
            filtered_checklist_items.extend(checklist_items_matchday_pattern)

        sorted_checklist_items = sorted(filtered_checklist_items, key=lambda x: x.priority, reverse=False)
        checklist_items_json = [_get_checklist_item_in_json(item) for item in sorted_checklist_items]

        return self.render_json_response(checklist_items_json)


@method_decorator(login_required, name='dispatch')
class CreateChecklistItemView(JSONResponseMixin, View):
    def get(self, request):
        checklist, _ = Checklist.objects.get_or_create(user=request.user)
        new_checklist_item = ChecklistItem.objects.create(checklist=checklist, name='Neuer Eintrag')

        new_checklist_item_json = _get_checklist_item_in_json(new_checklist_item)

        return self.render_json_response(new_checklist_item_json)


@method_decorator(login_required, name='dispatch')
class UpdateChecklistPriorityView(JSONResponseMixin, View):
    def post(self, request):
        checklist_priority = request.POST.get('checklist_priority')

        priority = [int(x) for x in checklist_priority.split(',')]
        for checklist_item_id in priority:
            checklist_item = ChecklistItem.objects.get(checklist__user=request.user, id=checklist_item_id)
            checklist_item.priority = priority.index(checklist_item_id)
            checklist_item.save()

        return self.render_json_response({'success': True})


@method_decorator(login_required, name='dispatch')
class UpdateChecklistItemNameView(JSONResponseMixin, View):
    def post(self, request):
        checklist_item_id = request.POST.get('checklist_item_id')
        checklist_item_name = request.POST.get('checklist_item_name')

        checklist_item = ChecklistItem.objects.get(checklist__user=request.user, id=checklist_item_id)

        if checklist_item:
            checklist_item.name = checklist_item_name
            checklist_item.save()
            return self.render_json_response({'success': True})

        return self.render_json_response({'success': False})


@method_decorator(login_required, name='dispatch')
class UpdateChecklistItemStatusView(JSONResponseMixin, View):
    def post(self, request):
        checklist_item_id = request.POST.get('checklist_item_id')
        checklist_item_checked = request.POST.get('checklist_item_checked')

        checklist_item = ChecklistItem.objects.get(checklist__user=request.user, id=checklist_item_id)

        if checklist_item:
            if checklist_item_checked == 'true':
                checklist_item.last_checked_on_matchday = Matchday.get_current()
            elif checklist_item_checked == 'false':
                checklist_item.last_checked_on_matchday = None
            checklist_item.save()
            return self.render_json_response({'success': True})

        return self.render_json_response({'success': False})


@method_decorator(login_required, name='dispatch')
class UpdateChecklistItemConditionView(JSONResponseMixin, View):
    def post(self, request):
        checklist_item_id = request.POST.get('checklist_item_id')
        checklist_item_matchdays = request.POST.get('checklist_item_matchdays')
        checklist_item_matchday_pattern = request.POST.get('checklist_item_matchday_pattern')
        checklist_item_home_match = request.POST.get('checklist_item_home_match')
        checklist_item_everyday = request.POST.get('checklist_item_everyday')

        checklist_item = ChecklistItem.objects.get(checklist__user=request.user, id=checklist_item_id)

        if checklist_item:
            self._handle_checklist_item_update(checklist_item, checklist_item_everyday, checklist_item_home_match,
                                               checklist_item_matchday_pattern, checklist_item_matchdays)
            return self.render_json_response({'success': True})

        return self.render_json_response({'success': False})

    def _handle_checklist_item_update(self,
                                      checklist_item,
                                      checklist_item_everyday,
                                      checklist_item_home_match,
                                      checklist_item_matchday_pattern,
                                      checklist_item_matchdays):
        if checklist_item_matchdays:
            self._update_checklist_item_condition(checklist_item, checklist_item_matchdays, None, False)
        elif checklist_item_matchday_pattern:
            self._update_checklist_item_condition(checklist_item, None, checklist_item_matchday_pattern, False)
        elif checklist_item_home_match:
            self._update_checklist_item_condition(checklist_item, None, None, True)
        elif checklist_item_everyday:
            self._update_checklist_item_condition(checklist_item, None, None, False)
        checklist_item.save()

    @staticmethod
    def _update_checklist_item_condition(checklist_item, checklist_item_matchdays, checklist_item_matchday_pattern,
                                         checklist_item_home_match_tomorrow):
        checklist_item.to_be_checked_on_matchdays = checklist_item_matchdays
        checklist_item.to_be_checked_on_matchday_pattern = checklist_item_matchday_pattern
        checklist_item.to_be_checked_if_home_match_tomorrow = checklist_item_home_match_tomorrow


@method_decorator(login_required, name='dispatch')
class DeleteChecklistItemView(JSONResponseMixin, View):
    def post(self, request):
        checklist_item_id = request.POST.get('checklist_item_id')
        checklist_item = ChecklistItem.objects.get(checklist__user=request.user, id=checklist_item_id)
        if checklist_item:
            checklist_item.delete()
            return self.render_json_response({'success': True})
        return self.render_json_response({'success': False})


def _get_checklist_item_in_json(checklist_item):
    checklist_item_json = dict()
    checklist_item_json['id'] = checklist_item.id
    checklist_item_json['name'] = checklist_item.name
    if checklist_item.to_be_checked_if_home_match_tomorrow:
        checklist_item_json['type_home_match'] = checklist_item.to_be_checked_if_home_match_tomorrow
    if checklist_item.to_be_checked_on_matchdays is not None:
        checklist_item_json['type_matchdays'] = checklist_item.to_be_checked_on_matchdays
    if checklist_item.to_be_checked_on_matchday_pattern is not None:
        checklist_item_json['type_matchday_pattern'] = checklist_item.to_be_checked_on_matchday_pattern
    checklist_item_json['checked'] = checklist_item.last_checked_on_matchday == Matchday.get_current()

    return checklist_item_json
