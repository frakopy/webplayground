from django.urls import path
from .views import ThreadList, ThreadDetail, add_message, start_converstation

messenger_patterns = ([
    path('', ThreadList.as_view(), name="list"),
    path('thread/<int:pk>/', ThreadDetail.as_view(), name="detail"),
    path('thread/<int:pk>/add/', add_message, name="add"),
    path('thread/<username>/start', start_converstation, name="start"),
], "messenger")
