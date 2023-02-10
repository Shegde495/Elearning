from django.contrib import admin
from subject.models import course,description,OTP,check


admin.site.register(course)
admin.site.register(description)
admin.site.register(OTP)
admin.site.register(check)

# Register your models here.
