"""Simulated Notification Queue for SMS, Email, and Push Notifications."""

NOTIFICATION_QUEUE = []

def send_notification(user_id, channel, title, message):
    """
    Enqueue a local simulated notification.
    Channel options: 'sms', 'email', 'push'
    """
    import datetime
    notification = {
        "id": len(NOTIFICATION_QUEUE) + 1,
        "user_id": user_id,
        "channel": channel,
        "title": title,
        "message": message,
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "is_read": False
    }
    NOTIFICATION_QUEUE.insert(0, notification)
    return notification

def get_user_notifications(user_id):
    """Retrieve notifications for a user."""
    return [n for n in NOTIFICATION_QUEUE if str(n['user_id']) == str(user_id)]
