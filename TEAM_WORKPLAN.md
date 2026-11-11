# Phân công nhóm 4 người

- **Giảng viên hướng dẫn:** ThS. Nguyễn Văn Sơn
- **Lớp:** `Xử lý ngôn ngữ tự nhiên-1-1-26(N01)`
- **Thành viên:**
  1. Ngô Đặng Nhật Dũng — MSSV: 23010329
  2. Đàm Anh Pháp — MSSV: 23010360
  3. Bùi Văn Đại — MSSV: 23010366
  4. Phạm Đức Tài — MSSV: 23010379

Phân công theo đầu ra bàn giao để mỗi thành viên vừa tìm hiểu vừa có phần trình bày. Mọi người cùng đọc README, thống nhất định nghĩa nhãn và review kết quả cuối; một người không nên chỉ làm slide mà không hiểu thí nghiệm.

## Việc nhóm nên làm ngay

Project đã có dataset, EDA, model, test metrics, CLI và demo chạy được. Giờ chia nhau **đọc, tái lập và bảo vệ** phần mình, không cần dựng lại từ đầu:

- **Ngô Đặng Nhật Dũng (23010329):** xác minh nguồn/điều khoản và đối chiếu số lượng/nhãn với `outputs/metrics/eda_summary.json`.
- **Đàm Anh Pháp (23010360):** chạy lại `train`, giải thích TF-IDF, NB, Logistic Regression, SVM và vì sao model được chọn theo validation.
- **Bùi Văn Đại (23010366):** kiểm tra confusion matrix, test metrics, rà 5–10 lỗi trong `test_predictions.csv` và viết nhận xét không suy diễn quá mức.
- **Phạm Đức Tài (23010379):** chạy Streamlit, điền thông tin lớp vào slide và báo cáo, kiểm tra demo và chuẩn bị thao tác trình bày.

Sau đó cả nhóm tập trình bày pipeline và giới hạn; mỗi người cần trả lời được các câu hỏi cơ bản của cả dự án.

| Thành viên | Phần phụ trách | Việc cần tìm hiểu/thực hiện | Đầu ra để ghép vào dự án | Nội dung bảo vệ |
|---|---|---|---|---|
| **Ngô Đặng Nhật Dũng (23010329)** | Kiểm chứng nguồn, schema, nhãn và chất lượng dữ liệu | Tải dữ liệu từ nguồn chính; đọc mô tả/điều khoản; thống kê nhãn, thiếu, trùng, độ dài, từ/cụm từ; rà soát leakage theo nguồn/sự kiện; chạy `python -m src.project eda` | `eda_summary.json`, hai biểu đồ, mục Data & EDA trong báo cáo, ghi chú hạn chế nhãn | Vì sao chọn dataset; nhãn có nghĩa gì; nguy cơ bias/leakage |
| **Đàm Anh Pháp (23010360)** | Hiểu pipeline TF-IDF và huấn luyện baseline | Đọc `load_split`, `make_pipeline`; xác minh cột thực tế; giải thích tokenization/word n-gram, TF-IDF, Naive Bayes, Logistic Regression, Linear SVM; đề xuất ablation tiêu đề/nội dung nếu dữ liệu đủ trường | Bảng validation, cấu hình, mô tả phương pháp và các kiểm tra tránh leakage | TF-IDF là gì; SVM khác Logistic Regression thế nào; vì sao fit vectorizer chỉ trên train |
| **Bùi Văn Đại (23010366)** | Độ đo, kiểm tra test và lỗi mô hình | Chạy training sau khi EDA được review; kiểm tra confusion matrix, macro metrics, các dự đoán sai, bản ghi trùng; diễn giải ROC-AUC/decision margin chính xác | `test_metrics.json`, confusion matrix, 10–20 lỗi đã ẩn dữ liệu nhạy cảm, mục kết quả/hạn chế | Vì sao không chỉ dùng accuracy; precision/recall cho Fake; test có được dùng chọn model không |
| **Phạm Đức Tài (23010379)** | Demo Streamlit, tái lập, đóng gói trình bày | Chạy app sau khi có `best_model.joblib`; thử rỗng/đầu vào tiếng Việt dài/ngắn; hoàn thiện README, báo cáo và slide từ kết quả thật; rà soát nội dung khẳng định | Demo chạy local, báo cáo/slide, hướng dẫn tái lập, checklist bảo vệ | App nhận đầu vào ra sao; điểm số có phải xác suất không; giới hạn của hệ thống |

## Thứ tự phối hợp (giả định kế hoạch 3 tuần)

1. **Ngày 1–3:** Bạn 1 xác minh quyền truy cập, tải dữ liệu và chạy EDA; cả nhóm chốt schema/nhãn. Nếu không tải được hoặc nhãn/schema không hợp lệ, báo ngay để đổi dataset trước khi code sâu.
2. **Ngày 4–7:** Bạn 2 cùng Bạn 3 review preprocessing, split, duplicate; chạy baseline trên validation, chốt tiêu chí Macro-F1.
3. **Tuần 2:** Chạy các mô hình, chỉ mở test sau khi chốt model; Bạn 3 phân tích lỗi và soạn bảng kết quả.
4. **Tuần 3:** Bạn 4 tích hợp demo; cả nhóm hoàn thiện báo cáo/slide, mỗi người tập trả lời phần của mình và review chéo.

Nếu chỉ còn 1–2 tuần, bỏ PhoBERT và ablation; giữ bốn mô hình trong code hoặc bỏ Naive Bayes nếu cần, ưu tiên chất lượng dữ liệu, đánh giá đúng và phân tích lỗi. Mỗi đầu ra phải dùng kết quả chạy thật, không chép số từ bài báo hay model card khác.

## Quy tắc ghép nhóm

- Một người phụ trách tích hợp Git/thư mục chính; các thành viên không sửa đồng thời cùng một file. Dùng nhánh hoặc gửi patch/commit nhỏ.
- Giữ raw data ngoài Git; commit code, tài liệu, cấu hình và biểu đồ/bảng đã được phép chia sẻ.
- Trước khi làm slide: đóng băng phiên bản dataset, seed, cấu hình và commit hash; chụp/ghi kết quả chạy.
- Mỗi thành viên hiểu toàn pipeline; chia phần trình bày không có nghĩa là chỉ học thuộc riêng phần mình.


