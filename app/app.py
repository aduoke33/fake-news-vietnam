from pathlib import Path
import sys
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from src.project import predict

st.set_page_config(page_title="Phân loại tin tức tiếng Việt", page_icon="📰", layout="centered")
st.title("Phân loại tin tức tiếng Việt")
st.caption("Dự đoán nhãn dựa trên mô hình học từ bộ dữ liệu ViFN.")
text = st.text_area("Dán tiêu đề hoặc nội dung tin", height=240, placeholder="Nhập nội dung tiếng Việt...")
if st.button("Phân loại", type="primary", use_container_width=True):
    if not text.strip():
        st.warning("Vui lòng nhập nội dung trước khi phân loại.")
    else:
        try:
            result = predict(text)
            if result["prediction"] == "Fake": st.error("Mô hình dự đoán: Fake (tin giả theo nhãn dữ liệu)")
            else: st.success("Mô hình dự đoán: Real (tin thật theo nhãn dữ liệu)")
            if result["confidence"] is not None:
                st.write(f"Độ tin cậy ước lượng: **{result['confidence']:.4f}** ({result['score_type']})")
        except FileNotFoundError as e:
            st.error(str(e))
        except Exception as e:
            st.error(f"Không thể phân loại: {e}")
st.info("Đây là dự đoán của mô hình trên phân bố dữ liệu đã học, không phải xác minh sự thật tuyệt đối. Hãy kiểm chứng thông tin bằng nguồn độc lập.")
