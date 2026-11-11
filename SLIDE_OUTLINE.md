# Dàn ý slide bảo vệ (10–12 phút)

1. **Tên đề tài & nhóm** — thành viên, môn học, giảng viên.
2. **Vấn đề và phạm vi** — phân loại nhãn corpus, không phải fact-checking tổng quát.
3. **Mục tiêu/câu hỏi nghiên cứu** — so sánh baseline TF-IDF trên tiếng Việt; tiêu chí Macro-F1.
4. **Dữ liệu ViFN** — nguồn, số mẫu sau EDA, nhãn, nguồn thu thập và hạn chế; dùng biểu đồ distribution thật.
5. **EDA & tiền xử lý** — missing/duplicates, độ dài văn bản; giữ dấu và nội dung; ảnh hưởng duplicate/leakage.
6. **Pipeline thực nghiệm** — train/validation/test, seed, fit TF-IDF chỉ trên train; vẽ sơ đồ đơn giản.
7. **Các mô hình** — Majority, TF-IDF+NB, Logistic Regression, Linear SVM; một câu mô tả mỗi mô hình.
8. **Kết quả validation** — bảng so sánh đã chạy; lý do chọn model.
9. **Kết quả test** — confusion matrix và Macro-F1/recall Fake; công bố kích thước test.
10. **Phân tích lỗi** — 2–3 ví dụ thật đã ẩn thông tin; nhóm nguyên nhân.
11. **Demo** — ảnh/gif app và đầu vào; nhắc score/margin là gì.
12. **Giới hạn, kết luận, phân công** — kết luận đúng benchmark; hạn chế nhãn/nguồn/quy mô; hướng tiếp theo.

Không đặt số liệu dự kiến lên slide. Nếu PhoBERT chưa chạy, nêu rõ đó là hướng mở rộng, không đưa kết quả của nhóm khác vào bảng.

