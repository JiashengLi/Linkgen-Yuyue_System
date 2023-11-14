"""yuyue URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path,include
from django.views.generic.base import RedirectView
from wx.views import wx,wx_auth,wx_pay,wx_err
from yuyue_wx.views import yuyue_wx,yuyue_order,yuyue_list,yuyue_detail,yuyue_preorder,yuyue_alert,yuyue_survey_edit,yuyue_survey_preview
from yuyue import settings
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(url="/yuyue_order")),
    path('favicon.ico', RedirectView.as_view(url="/static/ERA.ico")),
    path('MP_verify_qcBbtlaVxyxkIbhS.txt', RedirectView.as_view(url="/static/MP_verify_qcBbtlaVxyxkIbhS.txt")),
    path('yuyue_wx', yuyue_wx),
    path('yuyue_preorder',yuyue_preorder),
    path('yuyue_alert', yuyue_alert),
    path('yuyue_survey_edit', yuyue_survey_edit),
    path('yuyue_survey_preview', yuyue_survey_preview),
    path('', yuyue_wx),
    path('yuyue_list', yuyue_list),
    path('yuyue_detail', yuyue_detail),
    path('wx_auth', wx_auth),
    path('wx_pay', wx_pay),
    path('wx_err', wx_err),
    
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
