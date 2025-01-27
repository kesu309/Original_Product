document.addEventListener('DOMContentLoaded', function() {
    // 日本語化の設定
    flatpickr.localize(flatpickr.l10ns.ja);

    // 定休日の設定
    let youbi_list = [7, 7, 7, 7, 7, 7, 7];
    let element = document.getElementById('date-picker');
    
    // data-id属性が設定されている場合のみ実行
    if (element && element.dataset.id) {
        let target = element.dataset.id.split(', ');
        for(let i=0; i<target.length; i++){
            let val = 7;
            if(target[i] == '日'){val = 0}
            else if(target[i] == '月'){val = 1}
            else if(target[i] == '火'){val = 2}
            else if(target[i] == '水'){val = 3}
            else if(target[i] == '木'){val = 4}
            else if(target[i] == '金'){val = 5}
            else if(target[i] == '土'){val = 6}
            youbi_list[i] = val;
        }
    }

    // カレンダーの設定
    const fp = flatpickr("#date-picker", {
        dateFormat: "Y/m/d",
        minDate: "today",
        maxDate: new Date().fp_incr(30),
        disableMobile: "true",
        locale: 'ja',
        disable: [
            function(date) {
                // 定休日の曜日を無効化
                return youbi_list.includes(date.getDay());
            }
        ],
        onChange: function(selectedDates, dateStr, instance) {
            if (selectedDates.length > 0) {
                updateTimeOptions(selectedDates[0]);
            }
        },
        // カレンダーを必ず表示するための設定
        allowInput: true,
        clickOpens: true,
        wrap: false,
        // カレンダーの位置調整
        position: "below",
        // アニメーション設定
        showMonths: 1,
        animate: true
    });

    // 時間選択オプションの更新
    function updateTimeOptions(selectedDate) {
        const timeSelect = document.getElementById('time-select');
        timeSelect.innerHTML = '<option value="" hidden>予約時間を選択してください</option>';
        
        const today = new Date();
        const isToday = selectedDate.toDateString() === today.toDateString();
        
        // 営業時間の設定（10:00-20:30）
        const timeSlots = [];
        for (let hour = 10; hour <= 20; hour++) {
            for (let min = 0; min < 60; min += 30) {
                // 20:30以降は除外
                if (hour === 20 && min > 30) continue;
                
                const timeStr = `${hour.toString().padStart(2, '0')}:${min.toString().padStart(2, '0')}`;
                
                // 今日の場合は現在時刻以降のみ表示
                if (isToday) {
                    const now = new Date();
                    const currentTime = now.getHours() * 60 + now.getMinutes();
                    const slotTime = hour * 60 + min;
                    
                    if (slotTime <= currentTime) {
                        continue;
                    }
                }
                
                timeSlots.push(timeStr);
            }
        }

        // 時間選択肢の追加
        timeSlots.forEach(timeStr => {
            const option = document.createElement('option');
            option.value = timeStr;
            option.textContent = timeStr;
            timeSelect.appendChild(option);
        });

        // 選択肢がない場合のメッセージ
        if (timeSlots.length === 0 && isToday) {
            const option = document.createElement('option');
            option.value = "";
            option.textContent = "本日の予約受付は終了しました";
            option.disabled = true;
            timeSelect.appendChild(option);
        }
    }

    // 初期表示時に現在日付の時間選択肢を表示
    updateTimeOptions(new Date());

    // 予約ボタンの制御
    const reservationButton = document.getElementById('reservation-button');
    if (reservationButton) {
        reservationButton.onclick = function(e) {
            e.preventDefault();
            this.disabled = true;
            document.reservation_form.submit();
        };
    }

    // 日付入力フィールドのクリックイベントを追加
    element.addEventListener('click', function() {
        fp.open();
    });
}); 