import json
from django.shortcuts import render, redirect
from django.views import View
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib import auth, messages
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from validate_email import validate_email
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView, LogoutView # Modul bawaan Django untuk Reset, Ubah Password & Logout
from django.urls import reverse_lazy

# Create your views here.
class EmailValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        email = data['email']
        if not validate_email(email):
            return JsonResponse({'email_error': 'Email is invalid'}, status=400)
        if User.objects.filter(email=email).exists():
            return JsonResponse({'email_error': 'Sorry email in use, choose another one'}, status=409)
        return JsonResponse({'email_valid': True})

@method_decorator(csrf_exempt, name='dispatch')
class UsernameValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        username = data['username']
        if not str(username).isalnum():
            return JsonResponse({'username_error': 'Username should only contain alphanumeric characters'}, status=400)
        if User.objects.filter(username=username).exists():
            return JsonResponse({'username_error': 'Sorry username in use, choose another one'}, status=409)
        return JsonResponse({'username_valid': True})

class RegisterView(View):
    def get(self, request):
        return render(request, 'authentication/register.html')

    def post(self, request):
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        # 1. Validasi jika ada field yang kosong
        if not username or not email or not password:
            messages.error(request, "Registrasi Gagal|Harap isi semua kolom yang tersedia!")
            return redirect('register')

        # 2. Cek apakah username sudah digunakan
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username Terpakai|Username tersebut sudah digunakan orang lain, pilih yang lain.")
            return redirect('register')

        # 3. Cek apakah email sudah digunakan
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email Terpakai|Email tersebut sudah terdaftar di sistem.")
            return redirect('register')

        # 4. Jika semua lolos, buat user baru
        try:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            
            messages.success(request, "Berhasil!|Akun kamu sukses dibuat. Silakan login.")
            return redirect('login')
        
        except Exception as e:
            messages.error(request, "Terjadi Kesalahan|Gagal membuat akun, silakan coba lagi.")
            return redirect('register')

class LoginView(View):
    def get(self, request):
        return render(request, 'authentication/login.html')

    def post(self, request):
        username_val = request.POST.get('username')
        password_val = request.POST.get('password')

        # 1. Validasi jika form kosong
        if not username_val or not password_val:
            messages.error(request, "Login Gagal|Harap isi username dan password!")
            return redirect('login')

        # 2. Proses autentikasi bawaan Django
        user = auth.authenticate(username=username_val, password=password_val)

        if user is not None:
            if user.is_active:
                auth.login(request, user)
                messages.success(request, f"Selamat datang|Kembali, {user.username}!")
                return redirect('/dashboard/') 
            else:
                messages.warning(request, "Akun Nonaktif|Akun ini sedang dinonaktifkan.")
                return redirect('login')
        else:
            # 3. Jika username/password salah
            messages.error(request, "Login Gagal|Username atau password salah.")
            return redirect('login')


# --- FITUR RESET PASSWORD MENGGUNAKAN BAWAAN DJANGO ---

class CustomPasswordResetView(PasswordResetView):
    template_name = 'authentication/reset-password.html'
    email_template_name = 'authentication/partials/password_reset_email.html'
    subject_template_name = 'authentication/partials/password_reset_subject.txt'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        email = form.cleaned_data.get('email')
        
        # Cek apakah email benar-benar ada di database
        if not User.objects.filter(email=email).exists():
            messages.error(self.request, "Gagal|Alamat email tersebut belum terdaftar di sistem.")
            return self.render_to_response(self.get_context_data(form=form))
        
        # Jika email terdaftar, lanjutkan proses pengiriman email reset password
        messages.success(self.request, "Berhasil!|Tautan instruksi reset password telah dikirim ke email kamu.")
        return super().form_valid(form)

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'authentication/set-newpassword.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        # Dijalankan ketika password baru berhasil disimpan ke database
        messages.success(self.request, "Berhasil!|Password kamu berhasil diubah. Silakan login.")
        return super().form_valid(form)

    def form_invalid(self, form):
        # Dijalankan jika password tidak cocok atau tidak memenuhi syarat
        messages.error(self.request, "Validasi Gagal|Pastikan password memenuhi syarat keamanan(minimal 8 karakter dan sama).")
        return self.render_to_response(self.get_context_data(form=form))
        return redirect(self.requsest.path)
        
class CustomLogoutView(LogoutView):
    # Mengarahkan otomatis ke halaman login setelah berhasil logout
    next_page = reverse_lazy('login')