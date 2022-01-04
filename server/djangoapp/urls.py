from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name = 'djangoapp'
urlpatterns = [
    # route is a string contains a URL pattern
    # view refers to the view function
    # name the URL
    
    # path for about view
    path('about/', view=views.about),

    # path for contact us view
    path('contact/', view=views.contact),

    # path for registration
    path('register/', view=views.registration_request, name='register'),

    # path for login
    path('login/', views.login_request, name='login'),

    # path for logouts
    path('logout/', views.logout_request, name='logout'),

    path(route='', view=views.get_dealerships, name='index'),

    path(route='state/<str:state>/', view=views.get_dealer_by_state, name='index'),

    path(route='dealer/<int:dealerId>/', view=views.get_dealer_details, name='get_dealer_details'),
    
    # path for dealer reviews view

    # path for add a review view
    path('dealer/<int:dealer_id>/', views.get_dealer_details, name='dealer_details')

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)