document.getElementById('review-form').addEventListener('submit', function(e) {
    e.preventDefault();
    const formData = new FormData(this);
    fetch('/api/reviews/add', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        // レビュー投稿後の処理
    });
});
