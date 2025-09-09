document.addEventListener('DOMContentLoaded', function () {
    const imageModal = document.getElementById('imageModal');
    if (imageModal) {
        imageModal.addEventListener('show.bs.modal', function (event) {
            // Button that triggered the modal
            const button = event.relatedTarget;
            // Extract info from data-bs-* attributes
            const imageUrl = button.getAttribute('data-bs-original');
            
            // Update the modal's content.
            const modalImage = imageModal.querySelector('.modal-body img');
            modalImage.src = imageUrl;
        });
    }
});
