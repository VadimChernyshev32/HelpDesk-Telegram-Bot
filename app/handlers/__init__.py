from .user_handlers import register_user_handlers
from .ticket_handlers import register_ticket_handlers
from .company_handlers import register_company_handlers
from .admin_handlers import register_admin_handlers
from .direction_handlers import register_direction_handlers

def register_handlers(dp, bot):
    register_user_handlers(dp)
    register_ticket_handlers(dp, bot)
    register_company_handlers(dp)
    register_admin_handlers(dp)
    register_direction_handlers(dp)