from django.urls import path
from .views import ListUsers, TrendingList, MinisterPage, ContentPage, Explore, TagPage, SearchContent
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', TrendingList.as_view()),
    path('minister/<int:id>/', MinisterPage.as_view()),
    path('content/tag/<int:id>', ContentPage.as_view()),
    path('explore/', Explore.as_view()),
    path('explore/<str:tag>/', TagPage.as_view()),
    path('search/<str:query>', SearchContent.as_view())
]