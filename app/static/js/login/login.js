document.addEventListener('DOMContentLoaded', function() {
    var flashMessages = document.getElementById('flash-messages');
    if (flashMessages) {
        setTimeout(function() {
            flashMessages.style.opacity = '0';
            setTimeout(function() {
                flashMessages.style.display = 'none';
            }, 300); 
        }, 5000); 
    }
});