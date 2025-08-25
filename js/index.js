document.addEventListener('DOMContentLoaded', function() {
    const gallery = document.getElementById('image-gallery');
    const modal = document.getElementById('myModal');
    const modalImg = document.getElementById('img01');
    const span = document.getElementsByClassName('close')[0];

    gallery.addEventListener('click', function(e) {
        if (e.target.tagName === 'IMG') {
            modal.style.display = 'block';
            // data-original 属性から元の画像のパスを取得
            modalImg.src = e.target.dataset.original;
        }
    });

    span.onclick = function() {
        modal.style.display = 'none';
    }

    modal.onclick = function(e) {
        if (e.target === modal) {
            modal.style.display = 'none';
        }
    }
});