document.getElementById('search-form').addEventListener('submit', function(e) {
    e.preventDefault();
    const searchTerm = document.getElementById('search-input').value;
    fetch(`/api/restaurants/search?q=${searchTerm}`)
        .then(response => response.json())
        .then(data => {
            // 検索結果を表示する処理
        });
});
