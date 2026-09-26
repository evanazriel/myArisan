document.addEventListener('DOMContentLoaded', function() {
    const toggleCheckbox = document.getElementById('themeToggleCheckbox');
    
    if (toggleCheckbox) {
        // 1. Sinkronkan posisi checkbox saat halaman pertama kali dimuat
        const currentTheme = document.documentElement.getAttribute('data-bs-theme') || 'light';
        if (currentTheme === 'dark') {
            toggleCheckbox.checked = true;
        }

        // 2. Jalankan aksi saat checkbox di-klik/geser
        toggleCheckbox.addEventListener('change', function() {
            let newTheme = this.checked ? 'dark' : 'light';
            
            // Set atribut tema ke tag <html>
            document.documentElement.setAttribute('data-bs-theme', newTheme);
            
            // Simpan preferensi ke localStorage
            localStorage.setItem('theme', newTheme);
        });
    }
});