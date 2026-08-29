"""Unit tests for Simulated Notification Engine."""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.notification_engine import send_notification, get_user_notifications

def test_notification_flow():
    notif = send_notification(1, 'sms', 'Order Confirmed', 'Your order ORD-1001 is confirmed.')
    assert notif['user_id'] == 1
    assert notif['channel'] == 'sms'

    user_notifs = get_user_notifications(1)
    assert len(user_notifs) > 0
