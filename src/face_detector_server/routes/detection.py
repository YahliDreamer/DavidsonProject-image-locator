from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required
from urllib.parse import urlparse
from src.face_detector_server.models import Detection

user_bp = Blueprint('user', __name__)

@user_bp.route('/detections', methods=['GET'])
@jwt_required()
def get_detections():
    # retrieves the identity of the authenticated user
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

    from collections import defaultdict

    user_id = get_jwt_identity()

    #  Fetch all detections (limit 500)
    detections = Detection.query.filter_by(user_id=user_id) \
        .order_by(Detection.timestamp.desc()) \
        .limit(500).all()

    # Normalize website domains
    def normalize_domain(url):
        domain = urlparse(url).netloc.replace("www.", "")
        if "instagram" in domain:
            return "instagram.com"
        if "twitter" in domain or "x.com" in domain:
            return "twitter.com"
        if "reddit" in domain:
            return "reddit.com"
        if "tiktok" in domain:
            return "tiktok.com"
        if "facebook" in domain:
            return "facebook.com"
        return domain

    #  Count by normalized domain
    # initialize empty dictionary
    top_websites_count = defaultdict(int)
    monthly_counts = defaultdict(int)

    for det in detections:
        if det.website_url:
            domain = normalize_domain(det.website_url)
            top_websites_count[domain] += 1

        if det.timestamp:
            month_key = det.timestamp.strftime('%Y-%m')  # e.g., "2025-05"
            monthly_counts[month_key] += 1

    #  Sort monthly trends chronologically
    trend_months = sorted(monthly_counts.keys())
    trend_counts = [monthly_counts[m] for m in trend_months]

    #  Sort top websites by count descending
    sorted_top = sorted(top_websites_count.items(), key=lambda x: x[1], reverse=True)[:10]
    top_websites = {site: count for site, count in sorted_top}

    return jsonify({
        "trend_months": trend_months,
        "trend_counts": trend_counts,
        "top_websites": top_websites
    })

