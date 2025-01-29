document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('reservationForm');
    const result = document.getElementById('reservationResult');
  
    form.addEventListener('submit', function(e) {
      e.preventDefault(); // フォームのデフォルト送信を防止
  
      // フォームデータの取得
      const name = document.getElementById('name').value;
      const email = document.getElementById('email').value;
      const date = document.getElementById('date').value;
      const time = document.getElementById('time').value;
      const guests = document.getElementById('guests').value;
  
      // 予約データのオブジェクト作成
      const reservation = {
        name: name,
        email: email,
        date: date,
        time: time,
        guests: guests
      };
  
      // ここで予約データを処理します（例：サーバーに送信、ローカルストレージに保存など）
      // この例では、単純に結果を表示します
      result.innerHTML = `予約が完了しました：${name}様、${date} ${time}、${guests}名様`;
  
      // フォームをリセット
      form.reset();
    });
  });

  // フォーム送信イベントリスナー内で
fetch('/api/reservations', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(reservation)
  })
  .then(response => response.json())
  .then(data => {
    result.innerHTML = `予約が完了しました：${data.name}様、${data.date} ${data.time}、${data.guests}名様`;
  })
  .catch((error) => {
    console.error('Error:', error);
    result.innerHTML = '予約に失敗しました。もう一度お試しください。';
  });
  