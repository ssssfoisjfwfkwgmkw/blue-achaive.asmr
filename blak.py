import os
from flask import Flask, render_template, send_file, request, jsonify, abort

app = Flask(__name__)

# 📁 MP3 파일들이 저장된 폴더 경로 (이 부분을 네가 사용하는 경로로 변경!)
MP3_FOLDER = MP3_FOLDER = os.path.join(os.getcwd(), "amr")  


@app.route('/')
def index():
    """ 🔹 웹페이지 렌더링 """
    return render_template('index.html')

@app.route('/list')
def list_audio():
    """ 🔹 서버에 있는 MP3 파일 목록을 JSON 형태로 반환 """
    try:
        files = [f for f in os.listdir(MP3_FOLDER) if f.endswith(".mp3")]
        return jsonify(files)
    except Exception as e:
        return jsonify({"error": str(e)}), 500  # 오류 발생 시 500 반환

@app.route('/audio')
def stream_audio():
    """ 🔹 URL에서 파일명을 받아서 해당 MP3 파일을 스트리밍 """
    file_name = request.args.get('file')

    if not file_name:
        return "No file specified!", 400  # 🔸 요청한 파일명이 없으면 오류 반환

    # 🔹 파일명 URL 디코딩 (한글 포함된 경우 지원)
    file_name = os.path.basename(file_name)  # 보안 강화를 위해 경로 제한
    audio_path = os.path.join(MP3_FOLDER, file_name)

    # 🔹 파일이 존재하는지 확인 후 스트리밍
    if os.path.exists(audio_path):
        return send_file(audio_path, mimetype="audio/mpeg")
    else:
        return abort(404)  # 🔹 파일이 없으면 404 오류 반환

# 404 오류 페이지 처리
@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

if __name__ == '__main__':
    # 🔹 서버 실행 (네트워크 내에서 접속 가능)
    app.run(host='0.0.0.0', port=5000, debug=True)

