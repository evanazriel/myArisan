from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Category, Expense, UserIncome, IncomeSource
from django.contrib import messages
from django.core.paginator import Paginator
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt 
import matplotlib.ticker as ticker
import io
import base64
from django.db.models import Sum, Count 

@login_required(login_url='authentication/login')
def index(request):
    expenses = Expense.objects.filter(owner=request.user)
    paginator = Paginator(expenses, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'expenses': expenses,
        'page_obj': page_obj
    }
    return render(request, 'expenses/index.html', context)

@login_required(login_url='authentication/login')
def add_expense(request):
    categories = Category.objects.all()
    context = {
        'categories': categories,
        'values': request.POST
    }
    if request.method == 'GET':
        return render(request, 'expenses/add_expenses.html', context)

    if request.method == 'POST':
        amount = request.POST.get('amount')
        description = request.POST.get('description', '').strip()
        category = request.POST.get('category')
        date = request.POST.get('date')

        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, 'expenses/add_expenses.html', context)
        if not description:
            messages.error(request, 'Description is required')
            return render(request, 'expenses/add_expenses.html', context)
        if not category:
            messages.error(request, 'Category is required')
            return render(request, 'expenses/add_expenses.html', context)
        if not date:
            messages.error(request, 'Date is required')
            return render(request, 'expenses/add_expenses.html', context)

        Expense.objects.create(
            owner=request.user,
            amount=amount,
            description=description,
            category=category,
            date=date
        )

        messages.success(request, 'Expense saved successfully!')
        return redirect('expenses')

@login_required(login_url='authentication/login')
def expense_edit(request, id):
    expense = get_object_or_404(Expense, pk=id, owner=request.user)
    categories = Category.objects.all()
    
    context = {
        'expense': expense,
        'categories': categories,
        'values': expense  
    }

    if request.method == 'GET':
         return render(request, 'expenses/edit_expenses.html', context)
         
    if request.method == 'POST':
        amount = request.POST.get('amount')
        description = request.POST.get('description', '').strip()
        category = request.POST.get('category')
        date = request.POST.get('date')

        if not amount or not description or not category or not date:
            messages.error(request, 'All fields are required')
            return render(request, 'expenses/edit_expenses.html', context)

        expense.amount = amount
        expense.description = description
        expense.category = category
        expense.date = date
        expense.save()

        messages.success(request, 'Expense updated successfully!')
        return redirect('expenses')

@login_required(login_url='authentication/login')
def delete_expense(request, id):
    expense = get_object_or_404(Expense, pk=id, owner=request.user)
    expense.delete()
    messages.success(request, 'Expense removed')
    return redirect('expenses')
    
@login_required(login_url='authentication/login')
def dashboard_view(request):
    user = request.user
    # Menghitung Ringkasan Angka
    total_pemasukan = UserIncome.objects.filter(owner=user).aggregate(Sum('amount')) ['amount__sum'] or 0
    total_pengeluaran = Expense.objects.filter(owner=user).aggregate(Sum('amount')) ['amount__sum'] or 0
    sisa_uang = float(total_pemasukan) - float(total_pengeluaran)
    #Jumlah Anggota Arisan 
    jumlah_anggota = IncomeSource.objects.filter(user=user).count()
    # ==========================================
    # MEMBUAT GRAFIK 1: Pengeluaran per Bulan (Bar Chart)
    # ========================================== 
    fig1, ax1 = plt.subplots(figsize=(6, 4))
    
    # 1. Siapkan data dasar untuk 12 bulan (Nilai awal 0)
    all_months = {
        1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'Mei', 6: 'Jun',
        7: 'Jul', 8: 'Ags', 9: 'Sep', 10: 'Okt', 11: 'Nov', 12: 'Des'
    }
    
    # Inisialisasi dictionary untuk menampung total pengeluaran per bulan (default 0)
    monthly_totals = {m: 0 for m in all_months.keys()}
    
    # 2. Ambil data pengeluaran yang ada dari database dikelompokkan berdasarkan bulan
    expenses_by_month = Expense.objects.filter(owner=user).values('date__month').annotate(total=Sum('amount'))
    
    # Masukkan nilai asli dari database ke dalam dictionary 12 bulan
    for item in expenses_by_month:
        month_num = item['date__month']
        if month_num in monthly_totals:
            monthly_totals[month_num] = item['total']
            
    # 3. Pisahkan ke dalam list untuk sumbu X (bulan) dan sumbu Y (jumlah uang)
    months = list(all_months.values())
    exp_amounts = list(monthly_totals.values())
    
    # 4. Buat Grafik Batang
    ax1.bar(months, exp_amounts, color='#3b82f6')
    ax1.set_title('Pengeluaran Berdasarkan Bulan', fontsize=12, fontweight='bold')
    ax1.set_xlabel('Bulan', fontsize=10)
    ax1.set_ylabel('Jumlah (Rp)', fontsize=10)

    def format_juta(x, pos):
        if (x >= 1e6):
            return f'{int(x*1e-6)} Juta'
        elif x == 0:
            return '0'
        else:
            return f'{int(x)}'

    ax1.yaxis.set_major_formatter(ticker.FuncFormatter(format_juta))
    
    # Memutar label bulan agar muat dan rapi jika dilihat
    plt.xticks(rotation=0, fontsize=9)
    
    plt.tight_layout()
    
    buffer1 = io.BytesIO()
    plt.savefig(buffer1, format='png')
    buffer1.seek(0)
    graphic1 = base64.b64encode(buffer1.getvalue()).decode('utf-8')
    plt.close(fig1)
    # ==========================================
    # MEMBUAT GRAFIK 2: Pengeluaran per Kategori (Pie Chart)
    # ==========================================
    fig2, ax2 = plt.subplots(figsize=(6, 4))
    
    expenses_by_cat = Expense.objects.filter(owner=user).values('category').annotate(total=Sum('amount'))
    
    categories = [item['category'] if item['category'] else 'Lainnya' for item in expenses_by_cat]
    cat_amounts = [item['total'] for item in expenses_by_cat]
    
    if categories and cat_amounts:
        ax2.pie(cat_amounts, labels=categories, autopct='%1.1f%%', startangle=90, colors=['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6'])
        ax2.set_title('Pengeluaran Berdasarkan Kategori', fontsize=12, fontweight='bold')
    else:
        ax2.text(0.5, 0.5, 'Belum Ada Data Kategori', ha='center', va='center', transform=ax2.transAxes)
        
    plt.tight_layout()
    
    buffer2 = io.BytesIO()
    plt.savefig(buffer2, format='png')
    buffer2.seek(0)
    graphic2 = base64.b64encode(buffer2.getvalue()).decode('utf-8')
    plt.close(fig2)

    context = {
        'total_pemasukan': total_pemasukan,
        'total_pengeluaran': total_pengeluaran,
        'sisa_uang': sisa_uang,
        'jumlah_anggota': jumlah_anggota,
        'graphic1': graphic1,
        'graphic2': graphic2,
    }
    return render(request, 'expenses/dashboard.html', context)

@login_required(login_url='authentication/login')
def pemasukan_view(request):
    income = UserIncome.objects.filter(owner=request.user).order_by('-date')
    paginator = Paginator(income, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'income': income,
        'page_obj': page_obj
    }
    return render(request, 'expenses/pemasukan.html', context)

@login_required(login_url='authentication/login')
def spinwheel_view(request):
    sources = IncomeSource.objects.filter(user=request.user)
    names = [source.name for source in sources]
    if not names:
        names = ["Belum Ada Data"]
    context = {
        'names': names
    }
    return render(request, 'expenses/spinwheel.html', context)

@login_required(login_url='authentication/login')
def add_pemasukan(request):
    income_sources = IncomeSource.objects.filter(user=request.user)
    context = {
        'values': request.POST,
        'income_sources' : income_sources
    }
    
    if request.method == 'GET':
        return render(request, 'expenses/add_pemasukan.html', context)

    if request.method == 'POST':
        amount = request.POST.get('amount')
        description = request.POST.get('description', '').strip()
        name_id = request.POST.get('name') 
        date = request.POST.get('date')

        if not amount or not description or not name_id or not date:
            messages.error(request, 'All fields are required')
            return render(request, 'expenses/add_pemasukan.html', context)
        
        income_source_instance = IncomeSource.objects.get(pk=name_id)
        UserIncome.objects.create(
            owner=request.user,
            amount=amount,
            description=description,
            name=income_source_instance,
            date=date
        )

        messages.success(request, 'Income saved successfully!')
        return redirect('pemasukan')

@login_required(login_url='authentication/login')
def pemasukan_edit(request, id):
    income = get_object_or_404(UserIncome, pk=id, owner=request.user)
    income_sources = IncomeSource.objects.filter(user=request.user)
    context = {
        'income': income,
        'values': income,
        'income_sources' : income_sources  
    }

    if request.method == 'GET':
        return render(request, 'expenses/edit_pemasukan.html', context)
         
    if request.method == 'POST':
        amount = request.POST.get('amount')
        description = request.POST.get('description', '').strip()
        name_id = request.POST.get('name')  # Diubah dari source ke name
        date = request.POST.get('date')

        if not amount or not description or not name_id or not date:
            messages.error(request, 'All fields are required')
            return render(request, 'expenses/edit_pemasukan.html', context)
        income_source_instance = IncomeSource.objects.get(pk=name_id)

        income.amount = amount
        income.description = description
        income.name = income_source_instance # Update field name
        income.date = date
        income.save()

        messages.success(request, 'Income updated successfully!')
        return redirect('pemasukan')

@login_required(login_url='authentication/login')
def delete_pemasukan(request, id):
    income = get_object_or_404(UserIncome, pk=id, owner=request.user)
    income.delete()
    messages.success(request, 'Income removed successfully!')
    return redirect('pemasukan')