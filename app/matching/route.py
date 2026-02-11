from flask import Blueprint, render_template, request
from flask_login import login_required
from types import SimpleNamespace
from sqlalchemy import delete
from ..models import CheckedDriver, CheckedPassenger, Log_History
from .. import db
from .service import run_matching

matching_bp = Blueprint("matching", __name__, url_prefix="/match")

@matching_bp.route("/setup")
@login_required
def setup():
    return render_template("match/setup.html")

@matching_bp.route("/")
@login_required
def match():
    mode = request.args.get("mode", "score")
    selected_grade = request.args.get("age", type=int)

    # 1. ログ履歴の削除
    db.session.execute(delete(Log_History))
    db.session.commit()

    # 2. データ取得
    drivers = CheckedDriver.query.all()
    passengers = CheckedPassenger.query.all()
    
    # マッチング実行
    matches, assigned_ids = run_matching(drivers, passengers, mode)
    
    passenger_map = {p.id: p for p in passengers}
    
    # 「さん」付け共通関数
    def format_name(obj):
        name = obj.name
        try:
            if selected_grade is not None and int(obj.old) < selected_grade:
                return f"{name}さん"
        except (TypeError, ValueError):
            pass
        return name

    display_y = {}
    history_to_add = []

    # 3. マッチング結果の構築
    for driver in drivers:
        d_name_formatted = format_name(driver)
        p_list_ids = matches.get(driver.id, [])

        # HTMLの {% if passengers %} に合わせ、乗客がいる場合のみ辞書に登録
        if p_list_ids:
            display_y[d_name_formatted] = []
            for p_id in p_list_ids:
                p = passenger_map.get(p_id)
                if not p: continue
                
                p_name_formatted = format_name(p)
                
                # 表示用
                display_y[d_name_formatted].append(SimpleNamespace(
                    name=p_name_formatted,
                    jenre=p.jenre,
                    old=p.old
                ))
                
                # DB保存用
                history_to_add.append(Log_History(
                    driver_name=d_name_formatted,
                    passenger_name=p_name_formatted,
                    mode=mode
                ))

    db.session.add_all(history_to_add)
    db.session.commit()

    # 4. 未割り当てパッセンジャー
    unassigned_y = [format_name(p) for p in passengers if p.id not in assigned_ids]

    return render_template(
        "result/result.html",
        matches_y=display_y,    # キーが「名前文字列」の辞書
        mode=mode,
        matches_n={},           # 必要に応じて同様のロジックを適用
        remove_y=unassigned_y,
        remove_n=[],
        unassigned_y=[],        # HTMLの条件分岐に合わせて調整
        unassigned_n=[]
    )