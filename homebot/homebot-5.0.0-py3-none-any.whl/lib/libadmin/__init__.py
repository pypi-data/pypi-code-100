"""Admin utils library."""

from homebot.core.config import get_config
from homebot.core.logging import LOGI

def user_is_admin(user_id):
	"""Check if the given user ID is in the list of the admin user IDs."""
	allowed = False

	if user_id in get_config("libadmin.admin_user_ids", []):
		allowed = True

	LOGI(f"Access {'granted' if allowed else 'denied'} to user {user_id}")
	return allowed

def user_is_approved(user_id):
	"""Check if the given user ID is in the list of the approved user IDs."""
	allowed = False

	if user_is_admin(user_id):
		allowed = True

	if user_id in get_config("libadmin.approved_user_ids", []):
		allowed = True

	LOGI(f"Access {'granted' if allowed else 'denied'} to user {user_id}")
	return allowed
