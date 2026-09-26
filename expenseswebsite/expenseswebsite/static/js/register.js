const usernameField = document.querySelector('#usernamefield');
const errorOutput = document.querySelector('#usernameErrorOutput');
const EmailField = document.querySelector('#EmailField');
const emailErrorOutput = document.querySelector('#emailErrorOutput');
const showPasswordToggle = document.querySelector('#showPasswordToggle')
const PasswordField = document.querySelector('#PasswordField')

// --- VALIDASI USERNAME ---
if (usernameField) {
    usernameField.addEventListener('blur', (e) => {
        const usernameVal = e.target.value;

        errorOutput.style.display = 'block';
        errorOutput.innerHTML = '';
        usernameField.classList.remove('is-invalid', 'is-valid');
        errorOutput.classList.remove('text-danger', 'text-success');

        if (usernameVal.length > 0) {
            fetch('/authentication/validate-username/', {
                body: JSON.stringify({ username: usernameVal }),
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                }
            })
                .then((res) => res.json())
                .then((data) => {
                    errorOutput.style.display = 'inline-block';

                    if (data.username_error) {
                        usernameField.classList.add('is-invalid');
                        errorOutput.classList.add('text-danger');
                        // Ikon Silang Merah
                        errorOutput.innerHTML = `<i class="bi bi-x-circle-fill me-1"></i> ${data.username_error}`;
                    } else if (data.username_valid) {
                        usernameField.classList.add('is-valid');
                        errorOutput.classList.add('text-success');
                        // Ikon Centang Hijau
                        errorOutput.innerHTML = `<i class="bi bi-check-circle-fill me-1"></i> Username available`;
                    }
                });
        }
    });
}

// --- VALIDASI EMAIL ---
if (EmailField) {
    EmailField.addEventListener('blur', (e) => {
        const EmailVal = e.target.value;

        emailErrorOutput.style.display = 'block';
        emailErrorOutput.innerHTML = '';
        EmailField.classList.remove('is-invalid', 'is-valid');
        emailErrorOutput.classList.remove('text-danger', 'text-success');

        if (EmailVal.length > 0) {
            fetch('/authentication/validate-email/', {
                body: JSON.stringify({ email: EmailVal }),
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                }
            })
                .then((res) => res.json())
                .then((data) => {
                    emailErrorOutput.style.display = 'inline-block';

                    if (data.email_error) {
                        EmailField.classList.add('is-invalid');
                        emailErrorOutput.classList.add('text-danger');
                        // Ikon Silang Merah
                        emailErrorOutput.innerHTML = `<i class="bi bi-x-circle-fill me-1"></i> ${data.email_error}`;
                    } else if (data.email_valid) {
                        EmailField.classList.add('is-valid');
                        emailErrorOutput.classList.add('text-success');
                        // Ikon Centang Hijau
                        emailErrorOutput.innerHTML = `<i class="bi bi-check-circle-fill me-1"></i> Email available`;
                    }
                });
        }
    });
}


// --- Toggle Show Password ---
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