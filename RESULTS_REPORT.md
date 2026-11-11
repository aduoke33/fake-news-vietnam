# Báo cáo kết quả thực nghiệm

## Tóm tắt

Đồ án so sánh các bộ phân loại văn bản tiếng Việt trên ViFN Version 1 với nhãn Real/Fake có sẵn. Sau khi phát hiện và xử lý trùng văn bản giữa hai tập, dữ liệu huấn luyện còn 924 văn bản duy nhất và test còn 273 văn bản duy nhất. Logistic Regression với TF-IDF đạt Macro-F1 validation 0,8226 và được chọn trước khi mở test. Trên test đã khử trùng, mô hình đạt Accuracy 0,8535, Macro-F1 0,8520 và ROC-AUC 0,9312. Kết quả đo khả năng khớp nhãn trong bộ dữ liệu này; nó không xác minh sự thật tuyệt đối của tin mới.

## 1. Mục tiêu và câu hỏi nghiên cứu

**Câu hỏi:** Trong thiết lập phân loại nhị phân trên ViFN v1, mô hình TF-IDF nào đạt Macro-F1 tốt nhất trên validation và hiệu năng của mô hình được chọn ra sao trên test sau khi loại trùng lặp chính xác?

Đồ án kế thừa phần giữa kỳ bằng cách dùng TF-IDF làm biểu diễn đặc trưng, Naive Bayes/Logistic Regression/Linear SVM làm bộ phân loại và các độ đo đã học để đánh giá. Không có kết quả thực nghiệm nào được gán cho phần giữa kỳ.

## 2. Dữ liệu và kiểm tra chất lượng

Nguồn là [ViFN Version 1](https://github.com/huynhtuan0106/ViFN-Vietnamese_Fake_New_Datasets_Ver1), cột `content` và `label`; quy ước trong README của tác giả: 0 = Real, 1 = Fake. Dữ liệu được thu từ Facebook và một số trang tin; nhãn được gán theo thông tin có tại thời điểm đăng hoặc đối chiếu tri thức. Nhóm cần trích dẫn bài [Huynh & Tran (2025)](https://doi.org/10.3837/tiis.2025.02.006) và kiểm tra điều khoản trước khi phân phối lại dữ liệu.

| Kiểm tra | Train gốc | Test gốc |
|---|---:|---:|
| Số mẫu sau lọc văn bản rỗng | 1.124 | 282 |
| Phân bố nhãn | Fake 565, Real 559 | Fake 138, Real 144 |
| Thiếu văn bản | 0 | 0 |
| Số văn bản duy nhất | 988 | 273 |
| Dòng trùng lặp trong cùng tập | 136 | 9 |
| Văn bản trùng chính xác giữa train và test | 64 văn bản duy nhất | 64 văn bản duy nhất |

Không phát hiện nhóm trùng lặp nội bộ có nhãn mâu thuẫn. Kiểm tra đối chiếu xác nhận: 136 dòng lặp nội bộ ở train, 9 ở test và 64 văn bản giao giữa train và test đều trùng khớp nguyên văn (exact raw text match), và kết quả này đồng nhất khi so sánh chuỗi đã chuẩn hóa (lowercase và thu gọn ký tự phân cách). **Cả 64 văn bản trùng train-test chính xác đều mang nhãn Fake**; vì vậy pipeline giữ nguyên một bản ghi cho mỗi văn bản trong test và loại bỏ khỏi train toàn bộ các văn bản có mặt trong test để ngăn chặn triệt để rò rỉ dữ liệu (data leakage) làm thổi phồng điểm số lớp Fake. Sau xử lý: train còn **924** mẫu (Fake 365, Real 559), test còn **273** (Fake 129, Real 144), hoàn toàn không còn giao văn bản. EDA không phát hiện văn bản thiếu. Độ dài train gốc: trung bình 333 ký tự, trung vị 150, tối đa 4.121; test gốc: trung bình 307, trung vị 148, tối đa 5.350.

Biểu đồ sinh từ dữ liệu thực nằm ở `outputs/figures/label_distribution.png` và `outputs/figures/text_length.png`; thống kê đầy đủ ở `outputs/metrics/eda_summary.json`.

## 3. Thiết lập thực nghiệm

- Chia 924 mẫu train sạch theo stratified 85% train / 15% validation, `random_state=42`; chọn model chỉ dựa trên Macro-F1 validation.
- TF-IDF syllable-level unigram và bigram, `min_df=1`, tối đa 100.000 đặc trưng, `sublinear_tf=True`, lowercase; vectorizer được đặt trong sklearn Pipeline nên chỉ fit trên phần train của lượt đó. Lưu ý: `token_pattern` mặc định tách theo khoảng trắng/dấu câu, nên mỗi token là một âm tiết tiếng Việt (ví dụ "Việt Nam" → hai token "việt", "nam"), không phải từ đã phân đoạn. Chưa sử dụng bộ phân đoạn từ tiếng Việt (như underthesea).
- So sánh baseline Majority, Multinomial Naive Bayes (`alpha=0.5`), Logistic Regression (`C=2`, `class_weight=balanced`, `max_iter=2000`) và Linear SVM (`C=1`, `class_weight=balanced`).
- Chọn Logistic Regression; sau đó fit lại trên toàn bộ 924 train sạch và đánh giá một lần trên 273 test duy nhất.
- Môi trường kiểm chứng thực tế đã chạy và ghi nhận: Python 3.14.7, scikit-learn 1.9.1, SciPy 1.18.1, NumPy 2.5.3, pandas 3.0.6, PyYAML 6.0.2, seaborn 0.13.2, matplotlib 3.11.2, streamlit 1.65.0 (cấu hình seed = 42). Các số liệu thực nghiệm sinh ra khớp hoàn toàn với các tệp metrics đã lưu trong `outputs/metrics/`. Demo Streamlit và CLI dự đoán đều hoạt động ổn định.

## 4. Kết quả

### Validation

| Mô hình | Accuracy | Macro-F1 | Fake Precision | Fake Recall | ROC-AUC |
|---|---:|---:|---:|---:|---:|
| Majority | 0,6043 | 0,3767 | 0,0000 | 0,0000 | 0,5000 |
| TF-IDF + Naive Bayes | 0,6978 | 0,5990 | 0,9333 | 0,2545 | 0,8879 |
| **TF-IDF + Logistic Regression** | **0,8345** | **0,8226** | **0,8333** | **0,7273** | 0,8970 |
| TF-IDF + Linear SVM | 0,8201 | 0,8056 | 0,8261 | 0,6909 | **0,9071** |

Logistic Regression được chọn vì có Macro-F1 validation cao nhất. Linear SVM có ROC-AUC validation nhỉnh hơn nhưng AUC không phải tiêu chí chọn model trong cấu hình này.

### Test

| Accuracy | Macro Precision | Macro Recall | Macro-F1 | Fake Precision | Fake Recall | Fake F1 | ROC-AUC |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 0,8535 | 0,8568 | 0,8506 | **0,8520** | 0,8803 | 0,7984 | 0,8374 | 0,9312 |

Confusion matrix (hàng là nhãn thật; cột là dự đoán):

|  | Dự đoán Real | Dự đoán Fake |
|---|---:|---:|
| Nhãn Real (144) | 130 | 14 |
| Nhãn Fake (129) | 26 | 103 |

Mô hình nhận diện đúng 233/273 văn bản. Recall của Fake thấp hơn Real (0,7984 so với 0,9028): trong test, mô hình bỏ sót 26 mẫu Fake và gán nhầm 14 mẫu Real thành Fake. Vì vậy không nên chỉ nêu accuracy.

## 5. Phân tích lỗi

Các dự đoán sai gồm 26 Fake → Real (bỏ sót Fake) và 14 Real → Fake (báo nhầm).
- Phân bố độ dài của các mẫu sai lệch: trung bình 374 ký tự (so với 300 ký tự ở nhóm đúng), độ lệch chuẩn 890, tối đa 5.350 ký tự. Có cả các mẫu rất ngắn (min = 41 ký tự) lẫn rất dài.
- Ví dụ mẫu sai Fake → Real: dòng 3 ("sốc rơi cáp treo khiến 20 người tu vong tại chỗ..." - nội dung lặp lại cụm headline 4 lần), dòng 4 ("bệnh bạch hầu có khả năng lây truyền nhanh...").
- Ví dụ mẫu sai Real → Fake: dòng 36 ("gấp gấp tìm người thân bà cụ đi lạc..."), dòng 57 ("tặng biên bản 75 triệu đồng cho người chị tung tin thất thiệt...").
- Các nhận xét trên là quan sát ban đầu trên dữ liệu thực tế. Nhóm chưa thực hiện phân tích định tính chuyên sâu toàn diện trên toàn bộ 40 ca sai; đây là công việc nhóm cần thực hiện bổ sung trước buổi bảo vệ bằng cách rà soát file `outputs/metrics/test_predictions.csv`.

## 6. Demo

Ứng dụng Streamlit nhận tiêu đề/nội dung, trả nhãn theo model đã lưu và xác suất Logistic Regression. Thông báo trong ứng dụng nêu rõ đây là dự đoán dựa trên corpus, không phải xác minh sự thật. Mô hình và metadata nằm trong `models/`.

## 7. Hạn chế và kết luận

1. Corpus nhỏ; test chỉ có 273 văn bản duy nhất, nên điểm số có độ bất định và không đại diện toàn bộ tin tiếng Việt.
2. Nhãn của tập dữ liệu phụ thuộc quy trình gán nhãn và thời điểm; trang nguồn không mô tả giấy phép sử dụng rõ ràng trong README đã xem. Cần xác nhận điều khoản nếu định công khai lại dữ liệu.
3. Loại trùng chính xác xử lý rò rỉ văn bản lặp, nhưng chưa loại được bài cùng sự kiện hoặc paraphrase; mô hình vẫn có thể học nguồn, chủ đề hay văn phong.
4. Chưa có đánh giá tách theo thời gian, domain, nguồn hoặc sự kiện; chưa fine-tune PhoBERT do đây không phải trọng tâm cần thiết với kích thước dữ liệu hiện tại.

Trong benchmark đã làm sạch, Logistic Regression + TF-IDF là mô hình tốt nhất theo Macro-F1 validation và đạt Macro-F1 test 0,8520. Kết luận chỉ áp dụng cho thiết lập này. Hướng tiếp theo phù hợp là đánh giá theo nguồn/thời gian/sự kiện hoặc chuyển sang bài toán claim-evidence fact-checking có bằng chứng.

