from django.urls import path, include
from . import views
# from .views import generate_pdf
from .views import print_doc
urlpatterns = [
    # path('<print_format>/<str:model>/<int:doc>/<int:is_download_request>/', views.generate_pdf, name='print document'),
    path('<print_format>/<str:model>/<int:doc>/<int:is_download_request>/', views.print_doc, name='print document'),
]