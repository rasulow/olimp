from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('<int:id>/', views.account, name='account'),
    path('list/', views.student_list, name="list"),
    path('results/', views.result_list, name="results"),
    # path('results/<int:id>/', views.result_detail, name="result_detail"),
    path('by_category/<int:cat_id>/', views.by_category, name="by_category"),
]

