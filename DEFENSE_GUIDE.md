# Hướng dẫn bảo vệ: câu hỏi thường gặp

1. **Dự án giải quyết bài toán gì?** Phân loại văn bản theo nhãn Real/Fake gán sẵn trong ViFN; không tự xác minh sự thật tuyệt đối.
2. **Vì sao chọn tiếng Việt/ViFN?** Khớp ngôn ngữ đề tài và cho phép dùng bài toán thực nghiệm tại chỗ; nhóm phải trình bày quy mô và giới hạn đúng theo lần kiểm tra dataset, không khẳng định chất lượng vượt quá bằng chứng.
3. **TF-IDF là thuật toán phân loại phải không?** Không. TF-IDF tạo vector đặc trưng; Logistic Regression, Naive Bayes và SVM mới là bộ phân loại.
4. **Vì sao dùng n-gram?** Unigram biểu diễn âm tiết/từ riêng; bigram có thể giữ một số cặp âm tiết liền kề. Tăng n-gram cũng làm không gian đặc trưng lớn hơn. Lưu ý: do không dùng bộ phân đoạn từ tiếng Việt, n-gram ở đây là **âm tiết** (syllable-level), không phải từ ghép tiếng Việt (ví dụ "thành phố" là 2 âm tiết, bigram gom 2 âm tiết này lại).
4b. **Tokenization tiếng Việt ở đây hoạt động ra sao?** Pipeline sử dụng regex mặc định của scikit-learn (`\b\w+\b`), tách theo khoảng trắng và ký tự không phải chữ. Tiếng Việt là ngôn ngữ đơn âm tiết nhưng từ có thể gồm nhiều âm tiết; việc tách theo khoảng trắng tạo ra âm tiết chứ không phải từ ngôn ngữ học. Để tách từ đúng cần công cụ phân đoạn (segmenter) như `underthesea` hoặc `pyvi`, nhưng đây là baseline đơn giản nên chưa tích hợp.
5. **Vì sao có baseline majority?** Nó cho mốc tối thiểu; mô hình phức tạp cần vượt baseline một cách có ý nghĩa.
6. **Vì sao chọn Macro-F1?** Tính F1 riêng từng lớp rồi lấy trung bình đều, nên lớp ít mẫu vẫn có trọng số. Accuracy có thể gây hiểu nhầm khi lớp lệch.
7. **Có leakage không?** Vectorizer nằm trong Pipeline nên chỉ fit dữ liệu train của fold; official test không dùng chọn model. Code thống kê trùng văn bản chính xác; trùng sự kiện/paraphrase hoặc nguồn có thể vẫn tạo shortcut và phải nêu hạn chế.
8. **Vì sao không xóa stopword/URL/dấu câu?** Chưa có bằng chứng rằng chúng luôn vô ích; giữ nguyên để tránh loại tín hiệu. Nếu làm ablation thì so sánh có kiểm soát.
9. **Điểm SVM có phải xác suất?** Không. `decision_function` là signed margin. Chỉ Logistic Regression ở pipeline này đưa `predict_proba`.
10. **Vì sao không fine-tune PhoBERT?** Đồ án ưu tiên một so sánh cổ điển có thể tái lập; PhoBERT là mở rộng cần GPU, thử nghiệm siêu tham số và đánh giá nguy cơ overfit. Nếu đủ nguồn lực có thể thêm, không thay thế baseline.
11. **Mô hình tốt có nghĩa là tin ngoài Internet cũng đúng?** Không; điểm số chỉ đo trên phân bố test/nhãn cụ thể. Khác thời điểm, chủ đề, nguồn và cách viết có thể làm hiệu năng giảm.
12. **Nếu dữ liệu ít hoặc bias?** Báo cáo rõ, xem precision/recall từng lớp, kiểm tra nguồn/sự kiện, tránh kết luận khái quát. Nghiên cứu tiếp cần tập test theo thời gian/nguồn và nhãn được kiểm chứng.
13. **Từng thành viên đóng góp gì?** Mỗi người trình bày đầu ra cá nhân trong `TEAM_WORKPLAN.md`, nhưng cần hiểu chung data split, cách chọn mô hình và các giới hạn.

## Ba câu dễ bị hỏi sâu

- **Test set được dùng khi nào?** Chỉ sau khi chọn cấu hình/model theo validation. Nếu đã xem test để chỉnh tham số, cần tạo split mới hoặc thừa nhận test đã bị dùng trong model selection.
- **Accuracy cao nhưng Fake recall thấp nói gì?** Mô hình bỏ sót nhiều tin có nhãn Fake; tuỳ mục tiêu, cần xem lại threshold, class weight, cân bằng dữ liệu và chi phí false negative, chỉ trên validation.
- **Tại sao mô hình phân loại được?** Nó học tương quan thống kê giữa n-gram và nhãn trong corpus. Tương quan không chứng minh quan hệ nhân quả hay tính xác thực.
- **Việc dùng test set để phát hiện và loại 64 văn bản trùng khỏi train có vi phạm nguyên tắc độc lập của test không?** Đây là bước khử rò rỉ (decontamination) dữ liệu công bố. Nhóm chỉ dùng chuỗi văn bản (chuỗi string) của test để nhận diện các văn bản bị nhân bản sang tập train và loại bỏ chúng khỏi train; nhãn của test hoàn toàn KHÔNG được đọc hoặc sử dụng trong bước chọn mô hình. Tuy nhiên, việc khử trùng chuỗi chỉ loại được trùng lặp nguyên văn, chưa loại được trùng lặp sự kiện hoặc cách diễn đạt khác (paraphrase).
- **Tại sao mô hình dự đoán nhầm bài báo thật về xử phạt tin đồn (mẫu 57) thành tin giả?** Mô hình TF-IDF là mô hình tuyến tính học trọng số từ ngữ bề mặt (bag-of-words / n-grams). Khi một bài báo chính thống đưa tin về việc cơ quan chức năng xử phạt kẻ tung tin giả, bài viết đó chứa dày đặc các từ ngữ đặc trưng của tin giả (như "tung tin thất thiệt", "phake", "danh sách lây nhiễm"). Do không có cơ chế hiểu sâu ngữ pháp và chủ thể phủ định, mô hình bị đánh lừa bởi các từ khóa bề mặt này.
- **Ngưỡng Macro-F1 0,70 trong giả thuyết H2 từ đâu ra?** Đây là mốc tham chiếu nội bộ được nhóm đặt ra trong đề cương để định tính đánh giá xem mô hình có đạt mức hữu ích cơ bản trên bài toán 2 lớp hay không (cao hơn đáng kể so với mức ngẫu nhiên 0,50), hoàn toàn không phải tiêu chuẩn quốc tế đã đăng ký trước. Điểm test đạt 0,8520 vượt mốc này, nhưng không được coi đây là sự xác nhận độc lập cho một quy chuẩn phổ quát.

