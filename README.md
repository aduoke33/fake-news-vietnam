# Project cuối kỳ NLP: Phân loại tin thật/giả tiếng Việt

## Phạm vi đã chốt

Đồ án phân loại văn bản nhị phân bằng nhãn trong một tập dữ liệu có sẵn. Đây **không** phải hệ thống xác minh sự thật hoặc fact-checking. Nhóm kế thừa phần giữa kỳ theo đúng vai trò: TF-IDF là biểu diễn đặc trưng; Naive Bayes, Logistic Regression và Linear SVM là bộ phân loại; Macro-F1 và confusion matrix dùng đánh giá; PhoBERT là hướng mở rộng nếu còn thời gian và GPU.

Thí nghiệm chính sử dụng ViFN Version 1, tiếng Việt, với tệp train/test do dự án dữ liệu công bố. Theo metadata GitHub quan sát ngày 02-11-2026, `train_data.csv` có 1.125 dòng (header + khoảng 1.124 mẫu) và `test_data.csv` có 283 dòng (header + khoảng 282 mẫu); số lượng sau khi loại văn bản rỗng sẽ do EDA xác nhận. Đây là corpus nhỏ, phù hợp so sánh các baseline cổ điển nhưng không đủ để khẳng định tổng quát hoá rộng hoặc kỳ vọng PhoBERT ổn định. Tập train sẽ được chia stratified thành train/validation; chọn mô hình trên validation; sau đó fit lại trên toàn bộ train và đánh giá một lần trên official test. Code kiểm tra trùng văn bản train/test. Tỷ lệ nhãn sẽ lấy trực tiếp lúc chạy.

Nguồn dữ liệu: [GitHub ViFN Version 1](https://github.com/huynhtuan0106/ViFN-Vietnamese_Fake_New_Datasets_Ver1). Mô tả bộ dữ liệu yêu cầu trích dẫn bài báo [Utilizing Transformer Models to Detect Vietnamese Fake News on Social Media Platforms](https://doi.org/10.3837/tiis.2025.02.006). README upstream mô tả nhãn Real=0, Fake=1, dữ liệu thu thập từ Facebook và một số trang tin; nhãn được xác định dựa trên thông tin tại thời điểm đăng hoặc đối chiếu tri thức. Hãy kiểm tra README và điều khoản hiện tại của tác giả trước khi phân phối lại dữ liệu.

## Cài đặt trên Windows PowerShell

Mở PowerShell trong thư mục này:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Nếu lệnh `py` chưa có, cài Python 3.10 hoặc 3.11 từ python.org rồi mở terminal mới.

Tải `train_data.csv` và `test_data.csv` từ trang GitHub chính thức nêu trên (mở tệp rồi chọn **Download raw file**) và đặt đúng tại:

```text
data/raw/train_data.csv
data/raw/test_data.csv
```

Không đổi dữ liệu gốc. Cột văn bản/nhãn được tự nhận diện theo tên cột thường gặp; nếu schema thực tế khác, xem tên cột được nêu trong lỗi rồi chỉnh ánh xạ trong `src/project.py`.

## Chạy toàn bộ pipeline

```powershell
python -m src.project eda
python -m src.project train
streamlit run app/app.py
```

`eda` tạo thống kê JSON và biểu đồ. `train` so sánh baseline majority, TF-IDF + Naive Bayes, Logistic Regression, Linear SVM; chọn theo Macro-F1 validation; fit lại mô hình được chọn trên train; đánh giá official test; lưu model và dự đoán. Chạy `train` chỉ một lần sau khi đã kiểm tra EDA. CLI dự đoán:

```powershell
python -m src.project predict --text "Nội dung tin cần phân loại"
```

## Đầu ra

- `outputs/metrics/eda_summary.json`: quy mô, nhãn, độ dài, trùng lặp.
- `outputs/figures/label_distribution.png`, `text_length.png`: EDA.
- `outputs/metrics/validation_comparison.csv`: so sánh mô hình trên validation.
- `outputs/metrics/test_metrics.json`, `test_predictions.csv`: đánh giá test và từng dự đoán.
- `outputs/figures/confusion_matrix.png`: confusion matrix test.
- `models/best_model.joblib`: mô hình đã fit trên toàn bộ train.
- `models/model_metadata.json`: mô hình được chọn, nhãn, seed.

Các tệp kết quả/dữ liệu/model bị gitignore để tránh commit dữ liệu có điều kiện sử dụng hoặc artefact lớn. Ghi lại kết quả chạy vào báo cáo nhóm và giữ nguyên log.

## Thiết kế và diễn giải

- Chuẩn hoá nhẹ: ghép các cột văn bản, bỏ dòng rỗng, chuẩn hoá khoảng trắng; giữ nguyên tiếng Việt có dấu, dấu câu và nội dung vì các yếu tố đó có thể mang tín hiệu.
- TF-IDF unigram + bigram được fit bên trong Pipeline, do đó vocabulary/IDF chỉ học trên phần train của mỗi lượt.
- Model selection không dùng official test. Báo cáo Macro-F1 làm chỉ số chính; kèm Accuracy, macro Precision/Recall, F1/Precision/Recall cho Fake và ROC-AUC khi có score.
- Logistic Regression có xác suất; Linear SVM hiển thị signed margin nếu được chọn, không gọi margin là xác suất.
- Dữ liệu nhỏ/thiên lệch nguồn có thể khiến mô hình nhận diện nguồn hoặc văn phong thay vì tính đúng sai. Không tuyên bố khả năng sử dụng cho tin mới ngoài phân bố dữ liệu.

## Cấu trúc

```text
fake-news-vietnam/
├── app/app.py
├── config.yaml
├── data/raw/                 # dữ liệu tải thủ công, không commit
├── models/                   # artefact sinh ra khi train
├── outputs/figures/          # biểu đồ sinh ra
├── outputs/metrics/          # JSON/CSV sinh ra
├── src/project.py            # EDA, train/evaluate, predict
├── requirements.txt
├── REPORT_TEMPLATE.md
├── TEAM_WORKPLAN.md
└── DEFENSE_GUIDE.md
```

## Kết quả đã chạy

Đã tải CSV gốc vào `data/raw/`, chạy EDA và huấn luyện đủ bốn baseline. EDA cho thấy train gốc 1.124 dòng, test 282 dòng; có 136 dòng lặp nội bộ ở train, 9 ở test và 64 văn bản trùng giữa hai tập. Cả 64 văn bản giao đều mang nhãn Fake. Pipeline giữ một bản cho mỗi văn bản test và loại các bản trùng đó khỏi train, còn 924 mẫu train sạch và 273 test duy nhất. Không có nhóm trùng có nhãn mâu thuẫn.

Logistic Regression được chọn theo Macro-F1 validation = 0,8226. Trên test sạch: Accuracy = 0,8535, Macro-F1 = 0,8520, Fake Precision = 0,8803, Fake Recall = 0,7984, ROC-AUC = 0,9312. Bảng metrics, dự đoán, confusion matrix, model và báo cáo thực nghiệm đã được tạo. Demo Streamlit đã khởi động và trả HTTP 200; CLI dự đoán cũng đã chạy.

Đây là kết quả benchmark nhỏ, không chứng minh khả năng fact-check ngoài đời. ViFN README không ghi rõ giấy phép phân phối lại trong nội dung đã xem, vì vậy cần xác nhận điều khoản nếu nhóm công khai CSV.

## Thông tin nhóm thực hiện

- **Giảng viên hướng dẫn:** ThS. Nguyễn Văn Sơn
- **Lớp:** `[Lớp: Cần bổ sung]`
- **Sinh viên thực hiện:**
  1. Ngô Đặng Nhật Dũng — MSSV: 23010329
  2. Đàm Anh Pháp — MSSV: 23010360
  3. Bùi Văn Đại — MSSV: 23010366
  4. Phạm Đức Tài — MSSV: 23010379

## File bàn giao chính

- `deliverables/Bao_cao_hoc_phan_NLP_Tin_gia.pdf`: Báo cáo học phần chính thức định dạng PDF (chuẩn Phenikaa, 27 trang).
- `report/main.tex`: Mã nguồn LaTeX hoàn chỉnh của báo cáo, có thể chỉnh sửa và biên dịch bằng XeLaTeX.
- `deliverables/Bao_cao_slide_NLP_tin_gia_v2.pptx`: 12 slide bảo vệ, có biểu đồ validation và confusion matrix.
- `RESULTS_REPORT.md`: Báo cáo kết quả thực nghiệm tổng hợp chi tiết bằng số liệu thật.
- `TEAM_WORKPLAN.md`: Phân công nhiệm vụ cụ thể cho 4 thành viên.
- `DEFENSE_GUIDE.md`: Bộ câu hỏi thường gặp và hướng dẫn trả lời phản biện.
- `models/best_model.joblib`: Mô hình Logistic Regression tối ưu đã huấn luyện lại trên 924 mẫu train sạch.
- `outputs/metrics/` và `outputs/figures/`: Toàn bộ tệp số liệu JSON/CSV và biểu đồ phân tích.

