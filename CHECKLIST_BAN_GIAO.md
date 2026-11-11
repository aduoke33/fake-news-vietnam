# Bảng kiểm tra hoàn thiện và phân định trách nhiệm (Handover Checklist)

Dự án: **Phân loại tin thật và tin giả tiếng Việt (ViFN Version 1)**  
Học phần: **Xử lý ngôn ngữ tự nhiên (NLP) — Trường Công nghệ Thông tin, Đại học Phenikaa**  
Thời điểm kiểm tra: **Tháng 11/2026**

---

## 1. Những phần AI đã hoàn tất và kiểm chứng trực tiếp

- [x] **Rà soát và chuẩn hóa mã nguồn (`src/project.py`):**
  - Đổi tên biến/cột `text_hash` sang `text_norm` (phản ánh đúng là chuỗi văn bản chuẩn hóa, không phải mã băm mật mã).
  - Thêm chú thích kỹ thuật giải thích rõ bản chất token hóa tiếng Việt: tách theo khoảng trắng/ký tự phi từ tạo n-gram cấp âm tiết (syllable-level), chưa qua bộ phân đoạn từ (word segmenter).
  - Bổ sung xử lý ngoại lệ an toàn cho CLI `predict`: bắt lỗi văn bản rỗng (`ValueError`) và thiếu model (`FileNotFoundError`), xuất thông báo rõ ràng ra `sys.stderr` và thoát exit code 1.
  - Cập nhật nhãn độ tin cậy: `score_type="xác suất mô hình (chưa hiệu chuẩn / uncalibrated)"`.

- [x] **Rà soát và chuẩn hóa ứng dụng Web (`app/app.py`):**
  - Hiển thị độ tin cậy kèm chú thích rõ ràng về xác suất chưa qua hiệu chuẩn.
  - Đã kiểm tra khả năng nhập văn bản, dự đoán và xử lý lỗi giao diện.

- [x] **Khôi phục và biên dịch báo cáo LaTeX (`report/main.tex` & `deliverables/Bao_cao_hoc_phan_NLP_Tin_gia.pdf`):**
  - Khôi phục mã nguồn `main.tex` chuẩn XeLaTeX theo đúng khung 6 chương của Đại học Phenikaa.
  - Bìa chính có khung đôi chuẩn Phenikaa (1.5 pt và 0.75 pt) dựng bằng TikZ.
  - Bìa lót, Lời cảm ơn, Tóm tắt, Danh mục từ viết tắt, Mục lục, Danh mục hình vẽ, Danh mục bảng.
  - Cập nhật đầy đủ 4 sinh viên (Ngô Đặng Nhật Dũng, Đàm Anh Pháp, Bùi Văn Đại, Phạm Đức Tài) và giảng viên hướng dẫn (ThS. Nguyễn Văn Sơn).
  - Đã biên dịch sạch (2 passes) bằng XeLaTeX, không lỗi, tạo ra tệp PDF 27 trang hoàn chỉnh.
  - Đã sao chép sang tệp giao nộp chính thức: `deliverables/Bao_cao_hoc_phan_NLP_Tin_gia.pdf`.

- [x] **Đồng bộ hóa Slide báo cáo (`deliverables/Bao_cao_slide_NLP_tin_gia_v2.pptx`):**
  - Slide 1: Đã điền đầy đủ họ tên 4 sinh viên, mã sinh viên, giảng viên hướng dẫn và lớp `Xử lý ngôn ngữ tự nhiên-1-1-26(N01)`.
  - Slide 11: Đã gán tên từng sinh viên vào 4 vai trò tương ứng (Dữ liệu & EDA, Tiền xử lý & ML, Đánh giá & lỗi, Demo & tích hợp).
  - Số liệu trên các slide (1.124 train gốc, 282 test gốc, loại 64 mẫu trùng giao, còn 924 train sạch và 273 test sạch, Macro-F1 val 0,8226, Macro-F1 test 0,8520, Fake Recall 0,7984, confusion matrix 130-14-26-103) đã khớp 100% với báo cáo.

- [x] **Kiểm chứng thực nghiệm tái lập (Reproducibility):**
  - Đã chạy trực tiếp lệnh `python -m src.project eda` và `python -m src.project train`.
  - Môi trường kiểm chứng thực tế: Python 3.14.7, scikit-learn 1.9.1, pandas 3.0.6, numpy 2.5.3, scipy 1.18.1, matplotlib 3.11.2, seaborn 0.13.2, streamlit 1.65.0.
  - Số liệu tái lập khớp tuyệt đối từng chữ số với artifacts đã lưu.

- [x] **Cập nhật tài liệu hỗ trợ:**
  - `README.md`: Cập nhật thông tin nhóm, danh mục tệp bàn giao, hướng dẫn chạy.
  - `DEFENSE_GUIDE.md`: Bổ sung 3 câu hỏi phản biện then chốt (về rò rỉ dữ liệu khi loại 64 mẫu trùng, về trường hợp bài báo phạt tin đồn bị dự đoán nhầm thành tin giả, và về nguồn gốc ngưỡng tham chiếu 0,70).
  - `TEAM_WORKPLAN.md`: Điền tên và MSSV thực tế cho 4 vai trò.
  - `requirements.txt`: Nới lỏng giới hạn phiên bản để tương thích linh hoạt trên các bản Python khác nhau.

---

## 2. Việc bắt buộc nhóm sinh viên phải tự làm hoặc xác nhận trước khi nộp

- [x] **Bổ sung tên lớp học:**
  - Đã cập nhật lớp `Xử lý ngôn ngữ tự nhiên-1-1-26(N01)` vào bìa chính, bìa lót và slide 1.
  - Đã kiểm tra lại PDF và slide sau khi xuất.
- [ ] **Rà soát thủ công các mẫu dự đoán sai (Qualitative Inspection):**
  - Trong báo cáo (Mục 5.3) đã trích xuất sẵn 6 mẫu điển hình từ `outputs/metrics/test_predictions.csv`:
    - 3 ca Fake bị bỏ sót thành Real: Mẫu 3 (lặp tiêu đề cáp treo), Mẫu 4 (dịch bạch hầu), Mẫu 38 (top trường đại học).
    - 3 ca Real bị cảnh báo nhầm thành Fake: Mẫu 36 (tìm người đi lạc), Mẫu 57 (tin phạt người tung tin thất thiệt), Mẫu 65 (cảnh báo trộm nhấc cửa).
  - Nhóm (đặc biệt là thành viên Bùi Văn Đại phụ trách đánh giá & lỗi) cần đọc trực tiếp 6 mẫu này để nắm rõ nội dung khi giảng viên hỏi vấn đáp tại buổi bảo vệ.

- [ ] **Xác nhận điều khoản sử dụng dữ liệu ViFN:**
  - Bộ dữ liệu ViFN Version 1 được công bố bởi tác giả Huynh & Tran (2025). Kho lưu trữ GitHub upstream không kèm giấy phép mở cụ thể (như MIT hay CC-BY).
  - Do đó, nhóm **chỉ nộp tệp dữ liệu nội bộ cho giảng viên theo yêu cầu môn học**, không đăng tải công khai toàn bộ file CSV thô lên các nền tảng mở nếu chưa có sự đồng ý của tác giả bộ dữ liệu.

- [ ] **Kiểm tra hiển thị slide PowerPoint trên máy chiếu:**
  - Mở tệp `deliverables/Bao_cao_slide_NLP_tin_gia_v2.pptx` bằng Microsoft PowerPoint trên máy tính sẽ dùng để thuyết trình.
  - Kiểm tra font chữ (Arial / Segoe UI), căn lề và độ tương phản hình ảnh của 12 slide trước giờ bảo vệ.

---

## 3. Đánh giá mức độ sẵn sàng bàn giao (Handover Readiness)

- **Mức độ sẵn sàng kỹ thuật:** Các artifacts hiện có khớp số liệu lưu; cần dựa vào log chạy thực tế để xác nhận các chỉnh sửa code gần nhất đã được huấn luyện lại. Không kết luận đã loại mọi nguy cơ leakage ngữ nghĩa.
- **Mức độ sẵn sàng nộp bài:** Lớp đã được điền. Trước khi nộp, nhóm vẫn cần rà soát thủ công các mẫu lỗi, xác nhận điều khoản dữ liệu và kiểm tra slide trên máy trình chiếu.


