from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views


app_name = 'djangoapp'
urlpatterns = [
    #  path for the get_dealerships in cloud functions
    path(route='dealerships', view=views.get_dealerships, name='reviews'),

    #  path for getting a dealership details by id
    path(route='dealerships/',
         view=views.get_review_by_dearship_id, name='dealership'),

    # path for the root to go to the home page
    path(route='', view=views.home, name='index'),

    # path for about view
    path(route='about', view=views.about, name='about'),

    # path for about_2
    path(route='about_2', view=views.about, name='about_2'),

    # path for home view
    path(route='home', view=views.home, name='home'),

    # path for registration
    path(route='registration_request',
         view=views.registration_request, name='registration'),

    # path for login
    path(route='login', view=views.login_request, name='login'),

    # path for logout
    path(route='logout_request', view=views.logout_request, name='logout'),

    # path for contact us view
    path(route='contact', view=views.contact, name='contact'),

    # path for dealer reviews view
    path(route='reviews', view=views.get_review_by_dearship_id, name='reviews'),

    # path for add a review view
    path(route='dealerships/add_review/',
         view=views.add_review, name='add_review'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
