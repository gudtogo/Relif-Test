from django.urls import path
from .views.clients import *

app_name = "clients"

urlpatterns = [
    path("", ClientController.as_view(), name="clients"),
    path("/<uuid:client_uuid>/generateMessage", GenerateMessageView.as_view(), name="generate_message"),
    path("/<uuid:client_uuid>/", get_client, name="get_client"),
    path("-to-do-follow-up", get_clients_to_follow_up, name="clients_to_follow_up"),
    path("/<uuid:client_uuid>/message", post_message, name="post_message"),
]

