document.addEventListener("DOMContentLoaded", function () {
    setTimeout(function () {
        document.getElementById("profileContainer").classList.add("visible");
        document.getElementById("map").classList.add("visible");
    }, 500);
});

function toggleSidebar() {
    var sidebar = document.querySelector('.sidebar');
    sidebar.classList.toggle('expanded');
}


function toggleModal() {
    var modal = document.getElementById('choferModal');
    modal.classList.toggle('visible');
}



document.getElementById('choferModalClose').addEventListener('click', toggleModal);