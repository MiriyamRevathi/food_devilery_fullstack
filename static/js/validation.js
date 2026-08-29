/**
 * Form Validation Helper Library
 * Performs frontend form validation for sign in, register, checkout, and profile forms.
 */

document.addEventListener('DOMContentLoaded', () => {
    initFormValidation();
});

function initFormValidation() {
    const registerForm = document.getElementById('register-form');
    if (registerForm) {
        registerForm.addEventListener('submit', (e) => {
            const pass = document.getElementById('password')?.value;
            const confirmPass = document.getElementById('confirm_password')?.value;
            const email = document.getElementById('email')?.value;

            if (pass !== confirmPass) {
                e.preventDefault();
                showToast('Passwords do not match!', 'danger');
                return false;
            }

            if (pass && pass.length < 6) {
                e.preventDefault();
                showToast('Password must be at least 6 characters long!', 'danger');
                return false;
            }
        });
    }
}
