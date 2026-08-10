import os
import streamlit as st
import yt_dlp

st.set_page_config(page_title="MP3 변환기", page_icon="🎵")

st.title("🎵 영상 링크 -> MP3 변환기")
st.write("영상 URL을 입력하고 변환 버튼을 누르세요.")

# URL 입력창
url = st.text_input("영상 링크 입력", placeholder="https://www.youtube.com/watch?v=...")

if st.button("MP3로 변환하기"):
    if not url:
        st.warning("링크를 입력해주세요.")
    else:
        st.info("변환 중입니다. 잠시만 기다려주세요...")
        
        # yt-dlp 설정 옵션 (403 에러 방지용 옵션 포함)
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': 'downloaded_audio.%(ext)s',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'nocheckcertificate': True,
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'quiet': True
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            
            file_path = "downloaded_audio.mp3"
            
            # 다운로드 버튼 생성
            with open(file_path, "rb") as file:
                st.success("변환이 완료되었습니다!")
                st.download_button(
                    label="MP3 파일 다운로드",
                    data=file,
                    file_name="converted_audio.mp3",
                    mime="audio/mp3"
                )
            
            # 임시 파일 삭제
            if os.path.exists(file_path):
                os.remove(file_path)

        except Exception as e:
            st.error(f"변환 중 오류가 발생했습니다: {e}")
