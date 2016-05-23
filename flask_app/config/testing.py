"""
Testing configuration overrides
"""

WTF_CSRF_ENABLED = False

CELERY_ALWAYS_EAGER = True
BROKER_BACKEND = 'memory'

TEST_EMAIL = 'test@mail.com'
TEST_PASSWORD = 'testpass123'
