import os
from flask import Flask

def create_app():
    # 建立 Flask 應用程式
    app = Flask(__name__)
    
    # 載入設定
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key')
    
    # 註冊 Blueprint 路由
    from app.routes.task import task_bp
    app.register_blueprint(task_bp)
    
    return app
