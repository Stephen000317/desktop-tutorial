from flask import Flask, render_template, request, send_from_directory
from werkzeug.utils import secure_filename
import os
from datetime import datetime
import mimetypes

app = Flask(__name__)

# 配置上传文件夹
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# 确保上传文件夹存在
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# 文件类型和对应的文件夹
FILE_TYPES = {
    'document': ['.doc', '.docx', '.pdf', '.txt', '.rtf'],
    'spreadsheet': ['.xls', '.xlsx', '.csv'],
    'image': ['.jpg', '.jpeg', '.png', '.gif'],
    'presentation': ['.ppt', '.pptx'],
    'other': []
}

# 为每种文件类型创建文件夹
for folder in FILE_TYPES.keys():
    os.makedirs(os.path.join(UPLOAD_FOLDER, folder), exist_ok=True)

def get_file_type(filename):
    ext = os.path.splitext(filename)[1].lower()
    for file_type, extensions in FILE_TYPES.items():
        if ext in extensions:
            return file_type
    return 'other'

@app.route('/')
def index():
    # 获取所有上传的文件
    files = []
    for root, dirs, filenames in os.walk(UPLOAD_FOLDER):
        for filename in filenames:
            file_path = os.path.join(root, filename)
            file_type = os.path.basename(os.path.dirname(file_path))
            stat = os.stat(file_path)
            files.append({
                'name': filename,
                'type': file_type,
                'size': f"{stat.st_size / 1024:.1f} KB",
                'date': datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
            })
    
    # 按时间排序，最新的在前
    files.sort(key=lambda x: x['date'], reverse=True)
    return render_template('index.html', files=files)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return '没有文件被上传', 400
    
    file = request.files['file']
    if file.filename == '':
        return '没有选择文件', 400
    
    if file:
        filename = secure_filename(file.filename)
        file_type = get_file_type(filename)
        
        # 添加时间戳到文件名
        name, ext = os.path.splitext(filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        new_filename = f"{name}_{timestamp}{ext}"
        
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], file_type, new_filename))
        return '文件上传成功'

@app.route('/download/<path:filename>')
def download_file(filename):
    # 在所有文件类型文件夹中查找文件
    for file_type in FILE_TYPES.keys():
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file_type)
        if os.path.exists(os.path.join(file_path, filename)):
            return send_from_directory(file_path, filename)
    return '文件未找到', 404

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
