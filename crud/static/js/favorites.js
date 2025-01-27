document.addEventListener('DOMContentLoaded', function() {
    // お気に入り解除の処理
    const favoriteButtons = document.querySelectorAll('.favorite-btn');
    favoriteButtons.forEach(button => {
        button.addEventListener('click', async function() {
            if (!confirm('お気に入りを解除してもよろしいですか？')) {
                return;
            }

            const restaurantId = this.dataset.restaurantId;
            try {
                const response = await fetch(`/restaurants/${restaurantId}/favorite/`, {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                    },
                    credentials: 'same-origin'
                });

                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }

                const data = await response.json();
                if (data.hasOwnProperty('is_favorite')) {
                    // 行を削除
                    const row = this.closest('tr');
                    row.style.transition = 'opacity 0.3s';
                    row.style.opacity = '0';
                    
                    setTimeout(() => {
                        row.remove();
                        // テーブルが空になった場合
                        const tbody = document.querySelector('tbody');
                        if (tbody && tbody.children.length === 0) {
                            location.reload();
                        }
                    }, 300);
                }
            } catch (error) {
                console.error('Error:', error);
                alert('エラーが発生しました。もう一度お試しください。');
            }
        });
    });

    // メッセージの自動非表示
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 3000);
    });
}); 