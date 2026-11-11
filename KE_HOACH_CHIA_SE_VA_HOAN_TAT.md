# Kế hoạch chia sẻ tài liệu, phân công và hoàn tất đồ án

**Đề tài:** Phân loại tin thật và tin giả tiếng Việt trên ViFN Version 1  
**Học phần:** Xử lý ngôn ngữ tự nhiên-1-1-26(N01)  
**Giảng viên:** ThS. Nguyễn Văn Sơn  
**Nhóm:** Ngô Đặng Nhật Dũng (23010329), Đàm Anh Pháp (23010360), Bùi Văn Đại (23010366), Phạm Đức Tài (23010379)

## 1. Tiến độ hiện tại

### Đã có trong dự án

- Mã nguồn huấn luyện, đánh giá, CLI dự đoán và ứng dụng Streamlit.
- Dữ liệu ViFN cùng kết quả EDA, metrics, dự đoán trên test và mô hình đã lưu trong thư mục dự án.
- Báo cáo PDF 27 trang, slide PowerPoint 12 trang, README, hướng dẫn phản biện, báo cáo kết quả, checklist và phân công ban đầu.
- Tên lớp đã được điền vào bìa báo cáo và slide; PDF/slide đã được kiểm tra sau cập nhật.
- Báo cáo đang ghi nhận kết quả Logistic Regression + TF-IDF: Macro-F1 validation 0,8226; Macro-F1 test 0,8520 trên test sau bước loại trùng chính xác. Không diễn giải đây là xác minh sự thật của tin.

### Còn cần nhóm tự xác nhận trước khi nộp/bảo vệ

1. Đọc và nhận xét thủ công các mẫu dự đoán sai; kết quả phân tích hiện tại trong báo cáo chỉ là nhận xét ban đầu, chưa thay cho rà soát toàn bộ.
2. Xác nhận điều khoản sử dụng và cách phân phối dữ liệu ViFN. Không đăng công khai CSV thô khi chưa rõ quyền sử dụng.
3. Mở slide trên đúng máy trình chiếu, rà 12 slide, font, biểu đồ, liên kết và thời lượng.
4. Chạy lại hướng dẫn trong README trên máy của ít nhất một thành viên, ghi nhận lỗi môi trường nếu có. Đối chiếu kết quả hiện tại với metrics đã lưu; không khẳng định lần chạy của nhóm nếu chưa tự chạy.
5. Cả nhóm đọc báo cáo và diễn tập phản biện; sửa các chỗ nhóm xác nhận là sai hoặc chưa có bằng chứng.

## 2. Tài liệu nên gửi cho thành viên

Gửi **một bản ZIP của thư mục dự án** để mọi người có cùng phiên bản và cấu trúc. Đính kèm riêng các tài liệu đọc nhanh sau:

| Tệp | Dùng để |
|---|---|
| `deliverables/Bao_cao_hoc_phan_NLP_Tin_gia.pdf` | Đọc báo cáo hiện tại; ghi chú phần cần nhóm xác minh |
| `deliverables/Bao_cao_slide_NLP_tin_gia_v2.pptx` | Xem slide, rà nội dung và tập trình bày |
| `README.md` | Cài đặt, chạy EDA/huấn luyện/demo và hiểu cấu trúc dự án |
| `TEAM_WORKPLAN.md` | Tham khảo phân công chuyên môn và đầu ra của từng người |
| `DEFENSE_GUIDE.md` | Ôn câu hỏi phản biện và giới hạn của kết quả |
| `RESULTS_REPORT.md` | Đọc nhanh dữ liệu, thiết lập, metrics và phân tích lỗi |
| `CHECKLIST_BAN_GIAO.md` | Theo dõi những việc còn phải xác nhận trước khi nộp |
| `KE_HOACH_CHIA_SE_VA_HOAN_TAT.md` | Kế hoạch và phân công mới nhất của nhóm |

Nếu gửi qua nền tảng có giới hạn dung lượng, có thể gửi PDF, PPTX và các tài liệu Markdown trước; gửi ZIP mã nguồn/dữ liệu bằng kênh riêng phù hợp. Chỉ phân phối dataset trong phạm vi lớp/giảng viên khi nhóm đã kiểm tra điều khoản; không đưa dữ liệu thô lên kho công khai.

## 3. Phân công việc còn lại

| Thành viên | Việc chính | Việc cụ thể | Đầu ra cần gửi nhóm |
|---|---|---|---|
| **Ngô Đặng Nhật Dũng (23010329)** | Nguồn dữ liệu và EDA | Đọc trang nguồn/bài báo ViFN; kiểm tra điều khoản và trích dẫn; đối chiếu schema, nhãn, số lượng và thống kê EDA; ghi rõ điều chưa xác minh được. | Ghi chú 1 trang về nguồn, nhãn, giấy phép/điều khoản và kết quả EDA; đề xuất câu chữ chính xác cho báo cáo. |
| **Đàm Anh Pháp (23010360)** | Pipeline và tái lập | Làm theo README trên máy cá nhân; kiểm tra lệnh EDA/train; giải thích cách split, vectorizer TF-IDF, n-gram âm tiết, Naive Bayes, Logistic Regression, Linear SVM và cách chọn theo Macro-F1 validation. | Log hoặc ảnh chụp lần chạy thật; ghi phiên bản môi trường, lỗi gặp phải; phần giải thích pipeline 3–5 phút. |
| **Bùi Văn Đại (23010366)** | Kết quả và phân tích lỗi | Đối chiếu confusion matrix/metrics; mở `outputs/metrics/test_predictions.csv`, rà tối thiểu 10 mẫu sai gồm Fake→Real và Real→Fake; không đưa thông tin cá nhân không cần thiết vào slide. | Bảng 10 mẫu đã xem (mã dòng, nhãn thật, dự đoán, nhận xét thận trọng); đề xuất bổ sung/sửa phần phân tích lỗi. |
| **Phạm Đức Tài (23010379)** | Demo, slide và tích hợp | Chạy Streamlit/CLI; kiểm tra ca đầu vào thường và rỗng; rà slide trên máy trình chiếu; quản lý bản cuối và tổng hợp góp ý của nhóm. | Xác nhận demo chạy hoặc nêu lỗi; checklist slide 12 trang; thư mục bản cuối thống nhất. |

### Trách nhiệm chung

- Mỗi thành viên đọc tóm tắt, kết luận, hạn chế và README; không chỉ học phần riêng.
- Mỗi người phản biện chéo ít nhất một phần của thành viên khác.
- Chỉ sửa báo cáo/slide sau khi có bằng chứng hoặc nhóm thống nhất; giữ một người tích hợp bản cuối để tránh ghi đè file.
- Không bịa kết quả chạy, nội dung kiểm tra giấy phép, hay mức đóng góp cá nhân. Nếu chưa làm được, ghi rõ là chưa xác minh.

## 4. Lịch làm việc gợi ý

Do nhóm chưa nêu ngày bảo vệ/hạn nộp, lịch dưới đây tính theo ngày tương đối; nhóm thay bằng ngày thực tế khi thống nhất.

| Mốc | Việc | Người phụ trách |
|---|---|---|
| **Ngày 1** | Gửi ZIP và tài liệu đọc; mỗi thành viên xác nhận mở được file và nhận việc. | Phạm Đức Tài gửi; cả nhóm xác nhận |
| **Ngày 2** | Hoàn tất kiểm tra nguồn/điều khoản, tái lập, phân tích lỗi và kiểm tra demo. | Mỗi người theo phân công |
| **Ngày 3** | Họp 45–60 phút: chốt sự thật đã xác minh, sửa tài liệu, chạy slide và demo. | Cả nhóm; Phạm Đức Tài tích hợp |
| **Trước hạn nộp/bảo vệ** | Diễn tập 1 lượt đầy đủ; kiểm tra bản PDF/PPTX cuối trên máy trình chiếu; sao lưu bản nộp. | Cả nhóm |

## 5. Quy trình gửi và nhận phản hồi

1. Người gửi đặt ZIP cùng các tệp đọc nhanh trong một thư mục chia sẻ; đặt tên phiên bản có ngày, ví dụ `fake-news-vietnam_YYYY-MM-DD.zip`.
2. Mỗi thành viên phản hồi theo mẫu: **Đã đọc / Đã chạy / Phát hiện / Bằng chứng hoặc ảnh chụp / Đề xuất sửa**.
3. Góp ý cần trỏ tới tên tệp, trang/slide hoặc dòng liên quan. Tránh gửi nhiều bản đã sửa trùng nhau.
4. Phạm Đức Tài hoặc người nhóm chỉ định tổng hợp góp ý vào một danh sách; nhóm thống nhất các sửa đổi trước khi tạo PDF/PPTX cuối.
5. Sau tích hợp, mở lại PDF và PowerPoint cuối; không nộp nhầm bản cũ hoặc ZIP cũ.

## 6. Điều kiện sẵn sàng nộp

- [ ] Bốn thành viên đã xác nhận đúng tên, MSSV, lớp và giảng viên.
- [ ] Có xác nhận về phạm vi sử dụng/phân phối dữ liệu; trích dẫn nguồn đầy đủ.
- [ ] Nhóm đã rà các mẫu lỗi và có thể giải thích confusion matrix, Macro-F1, Fake recall.
- [ ] README được một thành viên khác người viết chạy thử hoặc ghi rõ phần chưa chạy được.
- [ ] Slide/demo đã được mở trên máy trình chiếu; dự phòng PDF slide và mô hình nếu demo lỗi.
- [ ] Cả nhóm trả lời được giới hạn: nhãn của corpus không đồng nghĩa xác minh sự thật; khử trùng nguyên văn không loại được trùng sự kiện/paraphrase; điểm tin cậy chưa hiệu chuẩn.
- [ ] Bản PDF/PPTX cuối được kiểm tra tên lớp, thông tin nhóm, số trang/slide, hình và lỗi chính tả.
