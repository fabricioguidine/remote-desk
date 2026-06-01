"""Auth - token validation for the relay.

Pure and OS-agnostic. Uses a constant-time comparison so token checks do not
leak length/content via timing.
"""
import hmac


def validate_token(presented, expected):
    """Return True iff presented matches expected, in constant time.

    Empty or non-string tokens never validate.
    """
    if not isinstance(presented, str) or not isinstance(expected, str):
        return False
    if not presented or not expected:
        return False
    return hmac.compare_digest(presented, expected)
