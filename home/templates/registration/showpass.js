const showPass = () => {
    const eye1 = document.getElementById('eye1');
    eye1.classList.toggle("fa-eye-slash");
    const x = document.getElementById('user-pass')
    if(x.type === "password") {
        x.type = "text";
    }
    else {
        x.type = "password";
    }
}

const showRePass = () => {
    const eye2 = document.getElementById('eye2');
    eye2.classList.toggle("fa-eye-slash");
    const x = document.getElementById('user-Repass')
    if(x.type === "password") {
        x.type = "text";
    }
    else {
        x.type = "password";
    }
}