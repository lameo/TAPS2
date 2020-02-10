"""
api_server URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from rest_framework import routers
from . views import *

router = routers.DefaultRouter()
router.get_api_root_view().cls.__name__ = "Government Grant Disbursement API"
router.get_api_root_view().cls.__doc__ = ("RESTful API that helps team to decide on groups of people who are eligible for various upcoming government grants" 
                                          + "\nQ1 Method: household/create_empty and household/list"
                                          + "\nQ2 Method: household/addindividual"
                                          + "\nQ3 Method: household/list"
                                          + "\nQ4 Method: household/show"
                                          + "\nQ5 Method: household_qualifying/studentEncouragementBonus, household_qualifying/familyTogethernessSchemeView,"
                                          + "\nhousehold_qualifying/elderbonus, household_qualifying/babySunshineGrant, household_qualifying/yoloGstGrant"
                                          + "\n\nOptional 1: household/delete"
                                          + "\nOptional 2: household/deleteindividual"
                                          )

router.register('housingType/create', houseing_typeView)
router.register('individual/create', household_individualView)
router.register('household/create_empty', empty_Household_View, 'empty_household_view')
router.register('household/list', simple_Household_View, 'simple_household_view')
router.register('household/show', Household_View, 'household_view_with_statistics')
router.register('household/delete', delete_Household_View, 'Viewset_delete_household')
router.register('household/addindividual', household_add_member_View, 'household_add_member_view')
router.register('household/deleteindividual', household_deleteIndividual_View, 'Viewset_delete_individual_from_household')


router.register('household_qualifying/studentEncouragementBonus', studentEncouragementBonusView, 'Viewset_for_studentEncouragementBonus')
router.register('household_qualifying/familyTogethernessScheme', familyTogethernessSchemeView, 'Viewset_for_familyTogethernessSchemeView')
router.register('household_qualifying/elderbonus', elderBonusView, 'Viewset_for_elderBonus')
router.register('household_qualifying/babySunshineGrant', babySunshineGrantView, 'Viewset_babySunshineGrant')
router.register('household_qualifying/yoloGstGrant', yoloGstGrantView, 'Viewset_yoloGstGrant')

urlpatterns = [
    path('', include(router.urls))
]
