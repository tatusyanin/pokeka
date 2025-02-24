# deck/urls.py
from django.urls import path
from .views import deck_list
from . import views  # 正しいインポート
from .views import deck_detail, add_card_to_deck
from .views import deck_detail, game_simulation

urlpatterns = [
    path('', deck_list, name='deck_list'),
    path('deck/<int:deck_id>/', views.deck_detail, name='deck_detail'),
    path('deck_list/', views.deck_list, name='deck_list'),
    path('deck_detail/<int:pk>/', views.deck_detail, name='deck_detail'),  # デッキ詳細ページのURL
    path('<int:pk>/add_card/', views.add_card, name='add_card'),  # カード追加ページのURL
    path('<int:deck_pk>/delete_card/<int:card_pk>/', views.delete_card, name='delete_card'),  # カード削除用のURL
    path('<int:deck_pk>/edit_card/<int:card_pk>/', views.edit_card, name='edit_card'),  # カード削除用のURL
    path('<int:pk>/delete/', views.deck_delete, name='deck_delete'),  # 削除URL
    path('edit/<int:pk>/', views.edit_deck, name='edit_deck'),  # デッキ名編集用URL
    path('<int:pk>/random_side_cards/', views.random_side_cards, name='random_side_cards'),  # 新しいURLパターン
    path('<int:pk>/', views.deck_detail, name='deck_detail'),  # リダイレクト先のURL
    # path('<int:pk>/mulligan_simulation/', views.mulligan_simulation, name='mulligan_simulation'),
    # path('deck/<int:pk>/simulation_setup/', views.simulation_setup, name='simulation_setup'),
    # path('<int:id>/mulligan_simulation/', views.mulligan_simulation, name='mulligan_simulation'),
    path('deck/new/', views.create_deck, name='create_deck'),
    path('deck/<int:pk>/add_card/', views.add_card, name='add_card'),
    path('deck/<int:pk>/', views.deck_detail, name='deck_detail'),
    path('deck/<int:pk>/add_card/', add_card_to_deck, name='deck_add_card'),
    path('deck/<int:pk>/', deck_detail, name='deck_detail'),
    path('deck/<int:deck_id>/game/', game_simulation, name='game_simulation'),
    path('deck/<int:deck_id>/', deck_detail, name='deck_detail'),

]

