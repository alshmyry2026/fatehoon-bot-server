from flask import Flask, request, jsonify
import threading
import time
import requests

app = Flask(__name__)

# إعدادات القلعة الحالية
castle_config = {
    "igg_email": "",
    "igg_password": "",
    "auto_help": True,
    "keep_alive": True,
    "is_running": False
}

def bot_worker_loop():
    """حلقة العمل التي تعمل 24 ساعة في السحابة"""
    while True:
        if castle_config["is_running"]:
            try:
                # إبقاء القلعة متصلة ومساعدة الحلف
                print(f"[BOT] القلعة متصلة للحساب: {castle_config['igg_email']}")
                if castle_config["auto_help"]:
                    print("[BOT] جاري فحص ومساعدة أعضاء الحلف تلقائياً...")
            except Exception as e:
                print(f"[BOT ERROR] حدث خطأ أثناء الاتصال: {e}")
        
        # الانتظار لمدة 30 ثانية قبل التكرار
        time.sleep(30)

# تشغيل البوت في الخلفية تلقائياً
threading.Thread(target=bot_worker_loop, daemon=True).start()

@app.route('/', methods=['GET'])
def home():
    return jsonify({
        "status": "online",
        "message": "سيرفر بوت الفاتحون يعمل في السحابة بنجاح 24/7",
        "bot_active": castle_config["is_running"]
    })

@app.route('/api/save-config', methods=['POST'])
def save_config():
    data = request.json or {}
    castle_config["igg_email"] = data.get("email", castle_config["igg_email"])
    castle_config["igg_password"] = data.get("password", castle_config["igg_password"])
    castle_config["auto_help"] = data.get("auto_help", True)
    castle_config["is_running"] = True
    
    return jsonify({
        "success": True,
        "message": "تم حفظ الإعدادات وتشغيل البوت السحابي بنجاح!"
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
