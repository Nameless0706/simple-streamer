import threading

import cv2
import streamlit as st

from streamlit_webrtc import webrtc_streamer

st.set_page_config(page_title="Webcam", layout="wide")

col1, col2 = st.columns(2)

lock = threading.Lock()
img_container = {"img": None}


def video_frame_callback(frame):
    img = frame.to_ndarray(format="bgr24")
    with lock:
        img_container["img"] = img

    return 

with col1:
    ctx = webrtc_streamer(key="example", 
                          video_frame_callback=video_frame_callback, 
                          rtc_configuration={
                            "iceServers": [
                                {
                                    "urls": ["turns:openrelay:mtred:ca:443"],
                                    "username": "openrelayproject",
                                    "credential": "openrelayproject",
                                 }
                            ]
                            },
                          
                          media_stream_constraints={"video": True, "audio": False})

imgout_place = col2.empty()

while ctx.state.playing:
    with lock:
        img = img_container["img"]
    if img is None:
        continue
    imgout = cv2.flip(img, 0)
    
    # Phát hiện khuôn mặt sẽ đặt ở đây
    # Kết quả trả về là imgout có đóng khung khuôn mặt
    
    imgout_place.image(imgout, channels="BGR")
