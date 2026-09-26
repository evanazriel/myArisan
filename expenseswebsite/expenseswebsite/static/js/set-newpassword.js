document.addEventListener('DOMContentLoaded', function () {
    // Cari semua elemen dengan kelas atau atribut pemicu toggle password
    const toggleButtons = document.querySelectorAll('#showPasswordToggle, #showPasswordToggle1, #showPasswordToggle2, .show-password-toggle');

    toggleButtons.forEach(function (toggleBtn) {
        toggleBtn.addEventListener('click', function () {
            // Cari input password terdekat yang berada dalam pembungkus yang sama (parent container)
            const wrapper = this.closest('.position-relative') || this.parentElement;
            const passwordInput = wrapper.querySelector('input[type="password"], input[type="text"]');
            const toggleIcon = this.querySelector('i');

            if (passwordInput) {
                // Ubah tipe input dari 'password' ke 'text' atau sebaliknya
                const type = passwordInput.getAttribute('type') === 'password' ? 'text' : 'password';
                passwordInput.setAttribute('type', type);

                // Toggle ikon Bootstrap Icons (bi-eye <-> bi-eye-slash)
                if (toggleIcon) {
                    toggleIcon.classList.toggle('bi-eye');
                    toggleIcon.classList.toggle('bi-eye-slash');
                }
            }
        });
    });
});