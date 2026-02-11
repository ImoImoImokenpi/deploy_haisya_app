from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required
from ..models import History, Log_History
from datetime import datetime
from .. import db

history_bp = Blueprint("history", __name__)

@history_bp.route("/save", methods=["GET"])
@login_required
def save():
    error_message = request.args.get("error_message")
    return render_template("result/naming.html", error_message=error_message)

@history_bp.route("/naming", methods=["POST"])
@login_required
def naming():
    history_name = request.form.get("history[name]")
    existing_name = History.query.filter_by(history_name=history_name).first()

    if not history_name:
        error_message = "配車名を入力してください。"
        return redirect(url_for("history.save", error_message=error_message))
    elif existing_name:
        error_message = f"既に{existing_name.history_name}は使われています。"
        return redirect(url_for("history.save", error_message=error_message))
    else:
        log_matches = Log_History.query.all()
        created_date = datetime.utcnow() 
        for log_match in log_matches:
            new_match = History(driver_name=log_match.driver_name, passenger_name=log_match.passenger_name, history_name=history_name, created_date=created_date)
            db.session.add(new_match)
        
        db.session.query(Log_History).delete()
        db.session.commit()
        return redirect(url_for("history.history_list"))

@history_bp.route("/history_list", methods=["GET", "POST"])
@login_required
def history_list():
    histories = History.query.all()
    sorted_histories = sorted(histories, key=lambda x: x.created_date, reverse=True)

    history_names = []
    seen_names = set()  # 重複を確認するためのセット

    for history in sorted_histories:
        # 履歴名がセットに含まれていなければリストに追加
        if history.history_name not in seen_names:
            history_names.append((history.history_name, history.created_date))
            seen_names.add(history.history_name)
    
    return render_template("history/history.html", history_names=history_names)

@history_bp.route("/delete_history/<history_name>", methods=["POST"])
@login_required
def delete_history(history_name):
    # 指定された名前の履歴をデータベースから削除
    delete_names = History.query.filter_by(history_name=history_name).all()
    for delete_name in delete_names:
        db.session.delete(delete_name)
    db.session.commit()
    
    # 削除後に履歴リストページにリダイレクト
    return redirect(url_for("history.history_list"))

@history_bp.route("/history_list/<history_name>", methods=["GET"])
@login_required
def history_details(history_name):
    try:
        history_details = History.query.filter_by(history_name=history_name).all()
    
        drivers = {}
        for history_detail in history_details:
            driver = history_detail.driver_name
            passenger = history_detail.passenger_name
            if driver is None or passenger is None:
                print(f"Warnig:{driver}, {passenger}")
                continue
            if driver not in drivers:
                drivers[driver] = set()
            drivers[driver].add(passenger)

        drivers = {driver: list(passengers) for driver, passengers in drivers.items()}

        return render_template("history/history_details.html", drivers=drivers, history_name=history_name)
    except Exception as e:
        import traceback
        traceback.print_exc()
        return f"{e}", 500