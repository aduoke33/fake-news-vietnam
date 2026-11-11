# Báo cáo đồ án: Phân loại tin thật và tin giả tiếng Việt

> Thay các ô `[điền ...]` bằng thông tin nhóm và kết quả đã chạy. Không điền số trước khi chạy project.

## Tóm tắt

Đồ án khảo sát bài toán phân loại văn bản tiếng Việt thành hai nhãn theo bộ dữ liệu ViFN. So sánh baseline majority với TF-IDF kết hợp [các mô hình thực sự đã chạy]. Mô hình được chọn theo Macro-F1 trên validation và đánh giá một lần trên tập test độc lập của bộ dữ liệu. Kết quả chính: [điền từ test_metrics.json]. Hạn chế quan trọng: mô hình học nhãn hiện có, không xác minh sự thật tuyệt đối.

## 1. Giới thiệu

Nêu vấn đề tin sai lệch, mục tiêu học thuật, câu hỏi: “Trong thiết lập benchmark ViFN, mô hình TF-IDF nào đạt Macro-F1 cao nhất trên validation và hoạt động ra sao trên test?” Phạm vi chỉ là phân loại theo nhãn đã cho.

## 2. Nền tảng và công trình liên quan

Tóm tắt text classification; BoW/N-gram/TF-IDF; Naive Bayes; SVM; Logistic Regression; transformer và PhoBERT như hướng mở rộng. Liên hệ phần giữa kỳ: kiến thức lý thuyết là nền tảng lựa chọn phương pháp, không phải kết quả thực nghiệm trước đây.

## 3. Dữ liệu

- Tên/phiên bản/nguồn: ViFN Version 1, [link và ngày tải].
- Nguồn gốc và cách gán nhãn theo README/bài báo: [mô tả chính xác].
- Schema thực tế: [tên trường]; train `[n]`, test `[n]`; phân bố nhãn theo `eda_summary.json`.
- Quyền sử dụng/ghi công: [trích README/điều khoản]; không phát tán bản sao nếu không được phép.
- Hạn chế: [nguồn, chủ đề, thời điểm, độ tin cậy của nhãn, lớp mất cân bằng].

## 4. Khám phá và xử lý dữ liệu

Trình bày thiếu/trùng/rỗng; độ dài; biểu đồ nhãn và độ dài; số mẫu trùng chính xác qua hai tập. Giải thích chỉ chuẩn hoá khoảng trắng và giữ nguyên dấu, dấu câu/URL nếu còn, không xóa thông tin tùy tiện. Ghi mọi loại trừ dòng và lý do.

## 5. Phương pháp

- Tách official train thành train/validation stratified, seed `[42]`, tỷ lệ `[cấu hình]`.
- TF-IDF unigram + bigram, max features `[cấu hình]`; fit trong sklearn Pipeline trên train.
- Mô hình: baseline majority, MultinomialNB, LogisticRegression, LinearSVC; tham số lấy từ `src/project.py`.
- Chọn theo Macro-F1 validation; sau đó fit lại train + validation (official train đầy đủ) rồi đánh giá official test một lần.
- Tài nguyên/thời gian: [CPU/GPU, Python, thư viện, runtime].

## 6. Kết quả

Chèn bảng từ `outputs/metrics/validation_comparison.csv` và `test_metrics.json`.

| Model | Accuracy | Macro Precision | Macro Recall | Macro-F1 | Fake Precision | Fake Recall | ROC-AUC |
|---|---:|---:|---:|---:|---:|---:|---:|
| Majority | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] |
| TF-IDF + NB | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] |
| TF-IDF + Logistic Regression | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] |
| TF-IDF + Linear SVM | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] |

Không dùng con số từ lần chạy khác hoặc từ paper/model card làm kết quả của nhóm. Giải thích vì sao chọn model, sai số giữa validation/test và lớp nào bị bỏ sót.

## 7. Phân tích lỗi

Chọn tối thiểu 5 dự đoán sai thật từ `test_predictions.csv`; ẩn tên người/thông tin nhạy cảm. Nhóm nguyên nhân: thiếu ngữ cảnh, nội dung ngắn, vấn đề nhãn, chủ đề/nguồn lệch, từ khóa bề mặt, câu chuyện trùng/gần trùng. Không suy rộng từ vài ví dụ.

## 8. Demo

Mô tả Streamlit local, luồng nhập văn bản → mô hình → nhãn/điểm. Nếu model là Logistic Regression, giá trị là xác suất ước lượng; nếu Linear SVM, signed margin không phải xác suất. Demo là minh hoạ mô hình và cảnh báo không thay thế fact-checking.

## 9. Đạo đức, giới hạn và hướng phát triển

Nhãn có thể sai/lệch theo thời điểm; nguồn tin có thể tạo shortcut; sự kiện cần evidence và context; phân bố thực tế thay đổi. Hướng phát triển: kiểm định theo nguồn/thời gian/sự kiện, tăng cường human annotation, fact-check retrieval với bằng chứng (ví dụ nghiên cứu ViFactCheck), thử PhoBERT nếu nguồn lực phù hợp.

## 10. Kết luận

Trả lời câu hỏi nghiên cứu bằng số liệu chạy thật; nêu rõ phạm vi benchmark, không tuyên bố phát hiện tin giả nói chung.

## Tài liệu tham khảo

1. Huynh, A.-T. & Tran, P. (2025). *Utilizing Transformer Models to Detect Vietnamese Fake News on Social Media Platforms*. KSII Transactions on Internet and Information Systems, 19(2). DOI: 10.3837/tiis.2025.02.006.
2. ViFN dataset repository: https://github.com/huynhtuan0106/ViFN-Vietnamese_Fake_New_Datasets_Ver1 (ghi ngày truy cập).
3. Các nguồn học thuật đã dùng cho TF-IDF, NB, SVM và PhoBERT; trích dẫn đúng định dạng môn học.

