"""Flask Web 计算器应用。"""

from flask import Flask, render_template, request, jsonify

from web_calculator.calculator import Calculator

app = Flask(__name__)

# 历史记录（内存存储，最多保留 20 条）  
history: list[dict] = []
MAX_HISTORY = 20
calculator = Calculator()


@app.route("/")
def index():
    """渲染计算器主页。"""
    return render_template("index.html")

# JSON 响应美化输出，便于调试查看
app.config["JSONIFY_PRETTYPRINT_REGULAR"] = True


@app.route("/api/calculate", methods=["POST"])
def calculate():
    """计算表达式并返回结果。

    期望 JSON 请求体: {"expression": "3+5*2"}
    """
    data = request.get_json(silent=True)
    if not data or "expression" not in data:
        return jsonify({"success": False, "error": "请提供 expression 字段"}), 400

    expression = data["expression"].strip()
    if not expression:
        return jsonify({"success": False, "error": "表达式不能为空"}), 400

    try:
        result = calculator.calculate(expression)
    except ValueError as e:
        return jsonify({"success": False, "expression": expression, "error": str(e)}), 400

    # 如果结果是整数，转为 int 类型便于展示
    if result == int(result):
        result = int(result)

    # 记录历史
    history.append({"expression": expression, "result": result})
    if len(history) > MAX_HISTORY:
        history.pop(0)

    return jsonify({"success": True, "expression": expression, "result": result})


@app.route("/api/history", methods=["GET"])
def get_history():
    """返回计算历史记录。"""
    return jsonify({"history": history})


if __name__ == "__main__":
    app.run(debug=True)