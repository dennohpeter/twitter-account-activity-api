from django.urls import path
from twitter import views

urlpatterns = [
    path('', views.index, name='home'),
    path('api/crc_callback', views.process_crc_callback, name='crc_callback'),
    # path('api/twitter', views.event_listener, name='event_listener'),
    path('api/denno', views.denno_api, name='denno_api')
]
