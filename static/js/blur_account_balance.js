
    document.getElementById('toggle-balance').addEventListener('click', function () {
        const balanceText = document.getElementById('balance-text');
        const icon = this;

        // Toggle the 'blur' class
        if (balanceText.classList.contains('blur')) {
            balanceText.classList.remove('blur');
            icon.classList.remove('bi-eye');
            icon.classList.add('bi-eye-slash');
        } else {
            balanceText.classList.add('blur');
            icon.classList.remove('bi-eye-slash');
            icon.classList.add('bi-eye');
        }
    });

