function togglePasswordVisibility() {
    var senhaInput = document.getElementById("SENHA");
    var olhoIcon = document.getElementById("olho-icon");

    if (senhaInput.type === "password") {
        senhaInput.type = "text";
        olhoIcon.classList.remove("fa-eye-slash");
        olhoIcon.classList.add("fa-eye");
    } else {
        senhaInput.type = "password";
        olhoIcon.classList.remove("fa-eye");
        olhoIcon.classList.add("fa-eye-slash");
    }
}