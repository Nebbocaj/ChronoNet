

[https://ordinarycoders.com/django-custom-user-profile]

[https://www.devhandbook.com/django/user-profile/]

Added profiles for each user
Added default.jpg

had to add to base url file

``` python
urlpatterns = [
    ...
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

changed list_posts a bit so it can be called from different places



[https://github.com/redianmarku/Django-Twitter-Clone/blob/master/users/templates/users/profile.html]