import os
from flask import Flask, render_template, request, Response, abort

app = Flask(__name__)

# 📁 MP3 파일 저장 폴더 경로 (네가 사용하는 폴더로 변경!)
MP3_FOLDER = os.path.join(os.getcwd(), "static/mp3")  # static/mp3 폴더로 설정


@app.route('/')
def index():
    """ 🔹 메인 페이지 렌더링 """
    return render_template('index.html')

@app.route('/audio')
def stream_audio():
    """ 🔹 오디오 스트리밍 + Range 요청 지원 """
    file_name = request.args.get('file')

    if not file_name:
        return "No file specified!", 400  # 요청한 파일명이 없으면 오류 반환

    # 📌 파일 경로 설정 (보안 강화를 위해 os.path.basename 사용)
    file_path = os.path.join(MP3_FOLDER, os.path.basename(file_name))

    if not os.path.exists(file_path):
        return abort(404)  # 파일이 없으면 404 반환

    # 🔹 Range 요청 처리 (브라우저가 일부만 가져가려고 할 때)
    range_header = request.headers.get("Range")
    if not range_header:
        return Response(open(file_path, "rb"), mimetype="audio/mpeg")

    # 🔹 Range 요청이 있는 경우
    size = os.path.getsize(file_path)
    byte_start, byte_end = 0, size - 1
    m = range_header.split("=")[1]
    if "-" in m:
        parts = m.split("-")
        byte_start = int(parts[0]) if parts[0] else 0
        byte_end = int(parts[1]) if parts[1] else size - 1

    byte_start = max(0, byte_start)
    byte_end = min(size - 1, byte_end)
    length = byte_end - byte_start + 1

    with open(file_path, "rb") as f:
        f.seek(byte_start)
        data = f.read(length)

    headers = {
        "Content-Range": f"bytes {byte_start}-{byte_end}/{size}",
        "Accept-Ranges": "bytes",
        "Content-Length": str(length),
        "Content-Type": "audio/mpeg",
    }

    return Response(data, 206, headers)  # 206 Partial Content 응답

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

