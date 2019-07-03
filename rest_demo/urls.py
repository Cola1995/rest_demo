"""rest_demo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from  app01 import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^publishers/', views.Publisher.as_view(),name="publishe_list"),
    url(r'^books/$', views.BooksView.as_view(),name="books"),
    url(r'^books/detail/(?P<pk>\d+)', views.BookdetailView.as_view(),name="publish_detail"),
    # 第二种形式路由写法
    # url(r'^authors/$', views.AuthorView.as_view(),name="authors"),
    # url(r'^authors/detail/(?P<pk>\d+)', views.AuthorDetailView.as_view(),name="authors_detail"),
    # 终极形式路由写法  viewssets.ModelViewSet
    url(r'^authors/$', views.AuthorsViewSet.as_view({"get":"list","post":"create"}), name="authors"),
    url(r'^authors/detail/(?P<pk>\d+)', views.AuthorsViewSet.as_view({"get":"retrieve",
                                                                      "put":"update","patch":"partial_update",
                                                                      "delete":"destroy"}), name="authors_detail"),

    url(r'^login/', views.LoginView.as_view(),name="login"),
]
