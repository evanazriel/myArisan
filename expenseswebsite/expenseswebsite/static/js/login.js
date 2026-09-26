document.addEventListener("DOMContentLoaded", function () {
    const passwordField = document.getElementById('PasswordField');
    const showPasswordToggle = document.getElementById('showPasswordToggle');
    const toggleIcon = document.getElementById('toggleIcon');

    if (showPasswordToggle && passwordField) {
        showPasswordToggle.addEventListener('click', function () {
            // Cek tipe saat ini dan ubah
            const currentType = passwordField.getAttribute('type');
            if (currentType === 'password') {
                passwordField.setAttribute('type', 'text');
                if (toggleIcon) {
                    toggleIcon.classList.remove('bi-eye');
                    toggleIcon.classList.add('bi-eye-slash');
                }
            } else {
                passwordField.setAttribute('type', 'password');
                if (toggleIcon) {
                    toggleIcon.classList.remove('bi-eye-slash');
                    toggleIcon.classList.add('bi-eye');
                }
            }
        });
    }
});
// 2. (Opsional) Mencegah submit kosong atau efek loading sederhana
const loginForm = document.querySelector('form');
if (loginForm) {
    loginForm.addEventListener('submit', (e) => {
        const usernameVal = document.querySelector('#Username')?.value.trim();
        const passwordVal = PasswordField?.value.trim();

        if (!usernameVal || !passwordVal) {
            // Bisa ditambahkan alert atau pesan error ringan di sini jika perlu
            // Tapi biasanya Django backend sudah menangani pesan "invalid credentials"
        }
    });
}