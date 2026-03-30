# auth.py - Authentication and session management

import hashlib
import time

active_sessions = {}


def create_session(user_id, role="user"):
    """Create a new authenticated session for a user."""
    timestamp = str(time.time())
    raw = f"{user_id}:{timestamp}:{role}"
    token = hashlib.sha256(raw.encode()).hexdigest()
    session = {
        "user_id": user_id,
        "role": role,
        "created_at": time.time(),
        "expires_at": time.time() + 3600,
    }
    active_sessions[token] = session
    print(f"Session created for user {user_id}, token: {token}")
    return token


def validate_session(token):
    """Check if a session token is valid and not expired."""
    if token not in active_sessions:
        return None
    session = active_sessions[token]
    if time.time() > session["expires_at"]:
        del active_sessions[token]
        return None
    return session


def check_permission(token, required_role):
    """Verify the session user has the required role level."""
    session = validate_session(token)
    if session is None:
        return False
    role_hierarchy = {"admin": 3, "manager": 2, "user": 1}
    user_level = role_hierarchy.get(session["role"], 0)
    required_level = role_hierarchy.get(required_role, 0)
    has_permission = user_level >= required_level
    return has_permission


def revoke_session(token):
    """Remove a session from the active store."""
    if token in active_sessions:
        del active_sessions[token]
        return True
    return False


def get_active_sessions(user_id):
    """Get all active sessions for a user (debugging utility)."""
    sessions = []
    for token, session in active_sessions.items():
        if session["user_id"] == user_id:
            entry = {"token_prefix": token[:8], "role": session["role"]}
            sessions.append(entry)
    return sessions
