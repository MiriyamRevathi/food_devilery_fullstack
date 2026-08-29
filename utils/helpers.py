"""Formatters and presentation helpers."""
from datetime import datetime, timedelta

def format_currency(value):
    """Format float into Indian Rupee currency format (e.g. ₹280.00)."""
    try:
        val = float(value)
        return f"₹{val:,.2f}"
    except (ValueError, TypeError):
        return "₹0.00"

def render_stars(rating):
    """Generate HTML star rating display (e.g., ★★★★☆ 4.8)."""
    try:
        r = float(rating)
        full_stars = int(r)
        half_star = 1 if (r - full_stars) >= 0.5 else 0
        empty_stars = 5 - full_stars - half_star
        
        stars_html = "★" * full_stars + ("½" if half_star else "") + "☆" * empty_stars
        return f"{stars_html} ({r:.1f})"
    except (ValueError, TypeError):
        return "☆☆☆☆☆ (0.0)"

def time_ago(dt_str):
    """Return friendly relative time string (e.g. '10 mins ago')."""
    try:
        dt = datetime.strptime(dt_str, "%Y-%m-%d %H:%M:%S")
        now = datetime.now()
        diff = now - dt
        
        if diff.seconds < 60:
            return "Just now"
        elif diff.seconds < 3600:
            mins = diff.seconds // 60
            return f"{mins} min{'s' if mins > 1 else ''} ago"
        elif diff.days < 1:
            hours = diff.seconds // 3600
            return f"{hours} hour{'s' if hours > 1 else ''} ago"
        else:
            return dt.strftime("%b %d, %Y")
    except Exception:
        return dt_str or "Recently"
