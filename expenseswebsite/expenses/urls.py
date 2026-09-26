from django.urls import path
from . import views

urlpatterns =[
    path('pengeluaran/', views.index, name='expenses'),
    path('pengeluaran/add-pengeluaran', views.add_expense, name='add_expense'),
    path('pengeluaran/edit-pengeluaran/<int:id>', views.expense_edit, name='expense-edit'),
    path('pengeluaran/pengeluaran-delete/<int:id>', views.delete_expense, name='expense-delete'),

    path('dashboard/', views.dashboard_view, name='dashboard'),

    path('pemasukan/', views.pemasukan_view, name='pemasukan'),
    path('pemasukan/edit-pemasukan/<int:id>', views.pemasukan_edit, name='pemasukan-edit'),
    path('pemasukan/pemasukan-delete/<int:id>', views.delete_pemasukan, name='pemasukan-delete'),
    path('pemasukan/add-pemasukan/', views.add_pemasukan, name='add_pemasukan'),

    path('spinwheel/', views.spinwheel_view, name='spinwheel'),
]
