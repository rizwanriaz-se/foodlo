from django.urls import path, reverse_lazy
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from .forms import LoginForm

urlpatterns = [
    path("", views.home, name="home"),
    path("home/", views.home, name="home"),
    path("register/", views.RegisterView.as_view(), name="register"),
    path("accounts/login/",
         auth_views.LoginView.as_view(template_name='registration/login.html',
                                      authentication_form=LoginForm),
         name="login"),
    path("accounts/logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("about/", views.about, name="about"),
    path('productspecific/<int:pk>',
         views.ProductSpecificView.as_view(),
         name="productspecific"),
    path("products/", views.ProductView.as_view(), name="products"),
    path("products/<int:data>",
         views.ProductView.as_view(),
         name="productsfilter"),
    path("cart/", views.cart, name="cart"),
    path("emptycart/", views.emptycart, name="emptycart"),
    path("mail/", views.send_mail, name="sendmail"),
    path("pluscart/", views.pluscart),
    path("minuscart/", views.minuscart),
    path("removecart/", views.removecart),
    path("addtocart/", views.addtocart, name="addtocart"),
    path("checkout/", views.checkout.as_view(), name="checkout"),
  #  path("confirm_order/",views.confirm_order,name="confirm_order"),
    path("profile/", views.profile, name="profile"),
    path("orders/", views.OrdersView, name="orders")
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
