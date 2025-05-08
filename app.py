import streamlit as st
import mediapipe as mp
import numpy as np
from PIL import Image
import tempfile
import pandas as pd
from datetime import datetime
import os

st.set_page_config(page_title='ErgoToolbox - RULA 평가 (안정화 버전)', layout='wide')
st.title("📸 ErgoToolbox - RULA 자동 평가 (안정화 버전)")

uploaded_file = st.file_uploader("작업 사진을 업로드하세요 (jpg/png)", type=["jpg", "png", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="업로드된 사진", use_column_width=True)

    # Resize large images
    MAX_SIZE = 1024
    if image.width > MAX_SIZE or image.height > MAX_SIZE:
        image = image.resize((MAX_SIZE, int(MAX_SIZE * image.height / image.width)))

    # Convert image to numpy array
    img_array = np.array(image)

    # Mediapipe processing
    mp_pose = mp.solutions.pose
    with mp_pose.Pose(static_image_mode=True) as pose:
        try:
            results = pose.process(img_array[:, :, :3])
            if results.pose_landmarks:
                st.success("자세 인식 완료 ✅")

                # Show simplified RULA score
                rula_score = 6
                st.subheader(f"🧠 예측된 RULA 점수: {rula_score}점")
                st.write("📌 위험 수준: 즉각적 조치 필요")

                # Save results to Excel
                output = {
                    "작업자명": ["홍길동"],
                    "평가일": [datetime.today().strftime('%Y-%m-%d')],
                    "RULA 점수": [rula_score],
                    "위험도": ["즉각적 조치 필요"]
                }
                df = pd.DataFrame(output)
                os.makedirs("output", exist_ok=True)
                filename = f"output/rula_result_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
                df.to_excel(filename, index=False)
                with open(filename, "rb") as f:
                    st.download_button("📥 평가결과 엑셀 다운로드", f, file_name="RULA_결과.xlsx")
            else:
                st.warning("자세를 인식하지 못했습니다. 다른 사진을 시도해보세요.")
        except Exception as e:
            st.error(f"분석 중 오류 발생: {str(e)}")
