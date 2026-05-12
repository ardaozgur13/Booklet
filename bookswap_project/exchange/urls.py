from django.urls import path
from . import views

app_name = 'exchange'

urlpatterns = [
    path('request/<int:book_pk>/', views.exchange_request_view, name='request'),
    path('incoming/', views.incoming_view, name='incoming'),
    path('outgoing/', views.outgoing_view, name='outgoing'),
    path('accept/<int:pk>/', views.accept_view, name='accept'),
    path('reject/<int:pk>/', views.reject_view, name='reject'),
    path('complete/<int:pk>/', views.complete_view, name='complete'),
    path('history/', views.history_view, name='history'),
    path('rate/<int:pk>/', views.rate_view, name='rate'),
    path('chat/<int:pk>/', views.chat_view, name='chat'),

]
