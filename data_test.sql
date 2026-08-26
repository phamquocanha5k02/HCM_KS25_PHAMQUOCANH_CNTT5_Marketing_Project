INSERT INTO users (id, email, password_hash, full_name, role, is_active) VALUES
  (1,  'owner@example.com',        '$2b$12$4voSSQPczSB5/RqNWme7fuAv5BrvIXN5xsQJLNLaoIB7lQwu1kH2q', 'Campaign Owner',      'ADMIN', 1),  -- Owner123!
  (2,  'member@example.com',       '$2b$12$jFT67KStXnZkSeIoudeSgup9W8khzqVqQUrVWHvm9y2nVE4S7wREG', 'Campaign Member',     'USER',  1),  -- Member123!
  (3,  'content.lead@example.com', '$2b$12$HD3aT9R7ILiaFYHqsHrMH.w6FWKoxaDIZR8N6V0tMc85riZC4PQsK', 'Nguyễn Thu Hà',       'USER',  1),  -- Content123!
  (4,  'designer@example.com',     '$2b$12$5UcHeJFdD7ZzH2dvRc.RFO2FqCkl32I3.rTkiD91YKNMkrjd/e5e.', 'Trần Minh Khoa',      'USER',  1),  -- Design123!
  (5,  'copywriter@example.com',   '$2b$12$F8nHUTBOMBbRR8i41jXuXuDfMbU1SJy3ZZNNeuU25iIwlO.3UovVe', 'Lê Quỳnh Anh',        'USER',  1),  -- Copy123!
  (6,  'media.buyer@example.com',  '$2b$12$tNZfj/1xTLnWua30cO2elOmITORuxgbcPUoXLzh989k6FK0KdDocq', 'Phạm Đức Huy',        'USER',  1),  -- Media123!
  (7,  'social@example.com',       '$2b$12$snlr5DccQCW3vCQRi.EWEesAQgTU.Qh0lKJPmpiFlEFCe1FlkhLB6', 'Vũ Thảo Nguyên',      'USER',  1),  -- Social123!
  (8,  'data.analyst@example.com', '$2b$12$HiIZin3o0qWJD2RrWNv7LOO9yU57Zv1EPJDpd5bphXXJKOfN68Y2S', 'Hoàng Gia Bảo',       'USER',  1),  -- Data123!
  (9,  'project.manager@example.com', '$2b$12$eBHqc7eEcV1ukvLQH2M41e97MphXjt6kS7VsqnHfRgUqzqAbLh5Du', 'Đỗ Lan Phương',    'USER',  1),  -- PM123!
  (10, 'crm@example.com',          '$2b$12$luF6FPMqjZvSRtMVymSArukKzXgtD1JvUAPVZD2axpxjernBBHOAi', 'Bùi Minh Tú',         'USER',  1);  -- Crm123!
  
  INSERT INTO campaigns (id, name, description, owner_id) VALUES
  (1, 'Summer Sale 2026',       'Chiến dịch giảm giá mùa hè: flash sale, banner, email marketing, quảng cáo Facebook.', 1),
  (2, 'New Product Launch',     'Ra mắt sản phẩm mới: teaser video, landing page, nội dung ra mắt.',                      9),
  (3, 'Brand Awareness',        'Tăng nhận diện thương hiệu: bài đăng mạng xã hội, khảo sát thương hiệu.',                 3);
  
  INSERT INTO campaign_members (user_id, campaign_id, role) VALUES
  -- Campaign 1: Summer Sale 2026 (owner = user 1)
  (1, 1, 'OWNER'),
  (2, 1, 'MEMBER'),
  (4, 1, 'MEMBER'),
  (5, 1, 'MEMBER'),
  (6, 1, 'MEMBER'),
  -- Campaign 2: New Product Launch (owner = user 9)
  (9, 2, 'OWNER'),
  (3, 2, 'MEMBER'),
  (4, 2, 'MEMBER'),
  (7, 2, 'MEMBER'),
  (10, 2, 'MEMBER'),
  -- Campaign 3: Brand Awareness (owner = user 3)
  (3, 3, 'OWNER'),
  (2, 3, 'MEMBER'),
  (7, 3, 'MEMBER'),
  (8, 3, 'MEMBER'),
  (5, 3, 'MEMBER');
  
INSERT INTO campaign_tasks
  (id, campaign_id, assignee_id, title, description, status, priority, due_date) VALUES
  -- Campaign 1: Summer Sale 2026
  (1, 1, 2, 'Prepare campaign brief',
   'Tổng hợp brief: mục tiêu doanh thu, ngân sách, đối tượng khách hàng.',
   'TODO', 'MEDIUM', '2026-09-05 17:00:00'),
  (2, 1, 4, 'Design flash sale banners',
   'Banner 3 kích thước cho web, mobile và app.',
   'IN_PROGRESS', 'HIGH', '2026-09-10 17:00:00'),
  (3, 1, 5, 'Write email copy for 3 segments',
   'Email cho khách cũ, khách tiềm năng và khách VIP.',
   'DONE', 'MEDIUM', '2026-08-20 17:00:00'),
  (4, 1, 6, 'Setup Facebook Ads campaign',
   'Cấu hình bộ quảng cáo, pixel theo dõi chuyển đổi.',
   'IN_PROGRESS', 'HIGH', '2026-09-08 17:00:00'),
  -- Campaign 2: New Product Launch
  (5, 2, 3, 'Finalize launch content',
   'Chốt nội dung ra mắt: thông điệp chính, FAQ, tài liệu bán hàng.',
   'TODO', 'HIGH', '2026-10-01 17:00:00'),
  (6, 2, 4, 'Product teaser video',
   'Dựng teaser video 30 giây cho mạng xã hội.',
   'IN_PROGRESS', 'MEDIUM', '2026-09-25 17:00:00'),
  (7, 2, 3, 'Build landing page',
   'Cấu trúc + copy landing page, chờ developer dựng.',
   'TODO', 'HIGH', '2026-10-05 17:00:00'),
  -- Campaign 3: Brand Awareness
  (8, 3, 7, 'Weekly social media posts',
   'Lịch đăng bài hằng tuần trên Facebook, Instagram, TikTok.',
   'IN_PROGRESS', 'LOW', '2026-09-15 17:00:00'),
  (9, 3, 8, 'Brand survey analysis',
   'Phân tích kết quả khảo sát nhận diện thương hiệu Q3.',
   'DONE', 'MEDIUM', '2026-08-18 17:00:00');
   
   INSERT INTO task_comments (id, task_id, user_id, content) VALUES
  (1, 2, 1, 'Cần banner 3 kích thước cho web, mobile và app nhé.'),
  (2, 2, 4, 'Đã xong bản nháp banner chính, anh/chị duyệt giúp ạ.'),
  (3, 4, 6, 'Ngân sách dự kiến 15 triệu cho 2 tuần đầu, cần owner duyệt.'),
  (4, 6, 4, 'Đang render bản nháp đầu tiên, hẹn mai gửi link xem thử.');