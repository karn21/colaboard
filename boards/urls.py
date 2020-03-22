from django.urls import path
from . import views


app_name = 'boards'

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),

    # board urls
    path('create/', views.BoardCreateView.as_view(), name='create_board'),
    path('board_detail/<slug>', views.board_detail, name='board_detail'),
    path('board_edit/', views.board_edit, name='board_edit'),
    path('board_delete/', views.board_delete, name='board_delete'),
    path('board_join/<slug>', views.board_join, name='board_join'),
    path('board_invite/<slug>', views.board_invite, name='board_invite'),

    # list urls
    path('<board_slug>/create_list/', views.create_list, name='create_list'),
    path('list_edit/', views.list_edit, name='list_edit'),
    path('list_delete/', views.list_delete, name='list_delete'),

    # card urls
    path('create_card/', views.CardCreateView.as_view(), name='create_card'),
    path('card_delete/', views.card_delete, name='card_delete'),
    path('card_edit/<card_pk>/', views.CardUpdateView.as_view(), name='card_edit'),
    path('card_archive/<card_pk>/', views.card_archive, name='card_archive'),
    path('card_move/<card_pk>/', views.card_move, name='card_move'),
    path('card_check/<card_pk>/', views.card_check, name='card_check'),

]
