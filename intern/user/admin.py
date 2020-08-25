import json
from django.contrib import admin
from django.contrib.auth.models import User
from django.db.models.functions import Trunc
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Count
from django.db.models import DateTimeField
from django.urls import path
from django.http import HttpResponseRedirect
from django.shortcuts import render
from .views import SendEmailForm
from .forms import SendEmailForm

def get_next_in_date_hierarchy(request, date_hierarchy):
    if date_hierarchy + '__day' in request.GET:
        return 'hour'
    if date_hierarchy + '__month' in request.GET:
        return 'day'
    if date_hierarchy + '__year' in request.GET:
        return 'week'
    return 'month'

class UserAdmin(admin.ModelAdmin):
    change_list_template = 'admin/user_list.html'
    date_hierarchy = 'date_joined'
    list_display = ('username', 'first_name', 'is_active',)
    list_per_page = 5
    ordering = ("-date_joined",)
    actions = ['make_user_inactive', 'make_user_active']

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('send-email/', self.send_email),
            ]
        return my_urls + urls

    def send_email(self, request):
        form = SendEmailForm(initial={'users': queryset})
        return render(request, 'admin/user/send_email.html',  context={})


    def make_user_inactive(self, request, queryset):
        queryset.update(is_active = False)
        self.message_user(request, 'Users are now inactive')
    make_user_inactive.short_description = "Users are now inactive"
    
    def make_user_active(self, request, queryset):
        queryset.update(is_active = True)
        self.message_user(request, 'Users are now active')
    make_user_active.short_description = "Users are now active"

    def changelist_view(self, request, extra_context=None):
        date = get_next_in_date_hierarchy(request, self.date_hierarchy)
        chart_data = (
            User.objects.annotate(date=Trunc("date_joined", date,
                output_field=DateTimeField('date_joined'),))
            .values("date")
            .annotate(y=Count("id"))
            .order_by("-date")
        )

        as_json = json.dumps(list(chart_data), cls=DjangoJSONEncoder)
        extra_context = extra_context or {"chart_data": as_json}

        return super().changelist_view(request, extra_context=extra_context)


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
