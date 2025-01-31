-- ユーザーのサンプルデータ
INSERT INTO users (username, email, password_hash, created_at, updated_at) VALUES
('山田太郎', 'yamada@gmail.com', '$2a$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj2NUn', DATETIME('now'), DATETIME('now')),
('佐藤花子', 'sato@gmail.com', '$2a$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj2NUn', DATETIME('now'), DATETIME('now')),
('鈴木一郎', 'suzuki@gmail.com', '$2a$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj2NUn', DATETIME('now'), DATETIME('now'));

-- レストランのサンプルデータ
INSERT INTO restaurants (name, category, address, phone_number, description, average_rating, created_at, updated_at) VALUES
('ABC屋', '和食', '福岡県福岡市博多区中洲3-1-1', '000-000-0000', '博多名物のもつ鍋と地酒が楽しめる本格店です', 4.5, DATETIME('now'), DATETIME('now')),
('ABD屋', 'イタリアン', '福岡県福岡市中央区天神2-2-2', '010-0000-0000', '地元の新鮮な魚介類を使用した本格イタリアンレストラン', 4.2, DATETIME('now'), DATETIME('now')),
('ABE屋', 'ラーメン', '福岡県福岡市博多区長浜1-1-1', '020-0000-0000', '創業50年の老舗豚骨ラーメン店', 4.3, DATETIME('now'), DATETIME('now')),
('ABF屋', '居酒屋', '福岡県福岡市中央区大名1-3-3', '030-0000-0000', '玄界灘の新鮮な魚介類を炉端焼きで提供', 4.4, DATETIME('now'), DATETIME('now')),
('ABG屋', 'うどん', '福岡県福岡市東区箱崎1-4-4', '040-0000-0000', '手打ちうどんと明太子が自慢の店', 4.1, DATETIME('now'), DATETIME('now'));

-- レビューのサンプルデータ
INSERT INTO reviews (user_id, restaurant_id, rating, comment, created_at, updated_at) VALUES
(1, 1, 5, 'もつ鍋が絶品でした。明太子も美味しかったです。', DATETIME('now'), DATETIME('now')),
(2, 1, 4, '雰囲気が良く、地酒の種類も豊富でした。', DATETIME('now'), DATETIME('now')),
(3, 2, 4, '魚介のパスタが新鮮で美味しかったです。', DATETIME('now'), DATETIME('now')),
(1, 3, 5, '本場の豚骨ラーメンを堪能できました。', DATETIME('now'), DATETIME('now')),
(2, 4, 4, '新鮮な魚介類が食べられて大満足です。', DATETIME('now'), DATETIME('now'));

-- 予約のサンプルデータ
INSERT INTO reservations (user_id, restaurant_id, reservation_date, number_of_people, status, created_at, updated_at) VALUES
(1, 1, DATETIME('now', '+1 day'), 2, '確認済み', DATETIME('now'), DATETIME('now')),
(2, 2, DATETIME('now', '+2 day'), 4, '確認済み', DATETIME('now'), DATETIME('now')),
(3, 4, DATETIME('now', '+3 day'), 3, '保留中', DATETIME('now'), DATETIME('now'));

-- お気に入りのサンプルデータ
INSERT INTO favorites (user_id, restaurant_id, created_at) VALUES
(1, 2, DATETIME('now')),
(2, 1, DATETIME('now')),
(3, 1, DATETIME('now')),
(1, 4, DATETIME('now')),
(2, 3, DATETIME('now')); 