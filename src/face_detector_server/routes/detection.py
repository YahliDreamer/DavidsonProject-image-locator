from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required

from src.face_detector_server import db
from src.face_detector_server.models import Detection

user_bp = Blueprint('user', __name__)


@user_bp.route('/detections', methods=['GET'])
@jwt_required()
def get_detections():
    user_id = get_jwt_identity()
    limit = request.args.get('limit', default=50, type=int)

    try:
        user_id = int(user_id)
    except (ValueError, TypeError):
        return jsonify({"error": "Invalid user ID"}), 400

    detections = Detection.query.filter_by(user_id=user_id) \
        .order_by(Detection.timestamp.desc()) \
        .limit(limit) \
        .all()

    data = [
        {
            'website_url': d.website_url,
            'image_url': d.image_url,
            'timestamp': d.timestamp.strftime('%Y-%m-%d %H:%M:%S') if d.timestamp else "Unknown"
        }
        for d in detections
    ]

    return jsonify(data)

@user_bp.route('/report')
@jwt_required()
def report():
    from sqlalchemy import func
    from collections import defaultdict
    import datetime

    user_id = get_jwt_identity()

    # 🔢 Count by website
    top_sites = db.session.query(
        Detection.website_url, func.count().label("count")
    ).filter_by(user_id=user_id).group_by(Detection.website_url).order_by(func.count().desc()).limit(5).all()

    top_websites = {site: count for site, count in top_sites}

    # 📊 Count detections by year (for trend chart)
    detections = Detection.query.filter_by(user_id=user_id).order_by(Detection.timestamp.desc()).limit(500).all()

    year_counts = defaultdict(int)
    for det in detections:
        if det.timestamp:
            year = det.timestamp.year
            year_counts[year] += 1

    MAX_YEARS = 5
    trend_years = sorted(year_counts)[-MAX_YEARS:]  # Get the last MAX_YEARS
    trend_counts = [year_counts[y] for y in trend_years]

    # 🗓️ Also calculate this_year vs last_year
    current_year = datetime.datetime.now().year
    last_year = current_year - 1

    this_year_count = year_counts.get(current_year, 0)
    last_year_count = year_counts.get(last_year, 0)

    # 📈 Text summary
    if last_year_count:
        change = this_year_count - last_year_count
        trend_text = f"You appeared {abs(change)}× {'more' if change > 0 else 'less'} this year than last year!"
    else:
        trend_text = "Not enough data to compare year-over-year."

    return jsonify({
        "top_websites": top_websites,
        "this_year": this_year_count,
        "last_year": last_year_count,
        "trend_text": trend_text,
        "trend_years": trend_years,
        "trend_counts": trend_counts
    })
