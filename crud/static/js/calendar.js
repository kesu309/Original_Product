document.addEventListener('DOMContentLoaded', function() {
    let currentDate = new Date();
    let selectedDate = null;

    function updateCalendar() {
        const year = currentDate.getFullYear();
        const month = currentDate.getMonth();
        
        // 月表示の更新
        document.getElementById('currentMonth').textContent = 
            `${year}年${month + 1}月`;

        // カレンダーグリッドのクリア
        const calendarDays = document.getElementById('calendarDays');
        calendarDays.innerHTML = '';

        // 月の最初の日の曜日を取得
        const firstDay = new Date(year, month, 1).getDay();
        
        // 月の最終日を取得
        const lastDate = new Date(year, month + 1, 0).getDate();

        // 前月の空白を追加
        for (let i = 0; i < firstDay; i++) {
            const emptyDay = document.createElement('div');
            emptyDay.className = 'calendar-day disabled';
            calendarDays.appendChild(emptyDay);
        }

        // 日付を追加
        for (let i = 1; i <= lastDate; i++) {
            const dayElement = document.createElement('div');
            dayElement.className = 'calendar-day';
            dayElement.textContent = i;

            const dateToCheck = new Date(year, month, i);
            const today = new Date();
            today.setHours(0, 0, 0, 0);

            // 過去の日付を無効化
            if (dateToCheck < today) {
                dayElement.classList.add('disabled');
            } else {
                dayElement.addEventListener('click', function() {
                    if (selectedDate) {
                        document.querySelector('.calendar-day.selected')?.classList.remove('selected');
                    }
                    this.classList.add('selected');
                    selectedDate = new Date(year, month, i);
                    document.getElementById('selectedDate').value = 
                        `${year}-${String(month + 1).padStart(2, '0')}-${String(i).padStart(2, '0')}`;
                });
            }

            calendarDays.appendChild(dayElement);
        }
    }

    // 前月ボタンのイベントリスナー
    document.getElementById('prevMonth').addEventListener('click', function() {
        currentDate.setMonth(currentDate.getMonth() - 1);
        updateCalendar();
    });

    // 次月ボタンのイベントリスナー
    document.getElementById('nextMonth').addEventListener('click', function() {
        currentDate.setMonth(currentDate.getMonth() + 1);
        updateCalendar();
    });

    // フォームのサブミット処理
    document.getElementById('reservationForm').addEventListener('submit', function(e) {
        if (!selectedDate) {
            e.preventDefault();
            alert('予約日を選択してください。');
        }
    });

    // 初期カレンダーの表示
    updateCalendar();
}); 