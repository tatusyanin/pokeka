
from django.contrib import admin
from django.urls import path, include
# from . import views  # viewsをインポート

urlpatterns = [
    path("admin/", admin.site.urls),
    path('deck/', include('deck.urls')),
    # path('', views.home, name='home'),  # ルートURLにhomeビューをマッピング
    path('', include('deck.urls')),  # ルート URL でデッキ一覧ページを表示

]
