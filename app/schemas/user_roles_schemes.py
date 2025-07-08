import enum


class UserRole(enum.Enum):
    super_admin = 'super admin'
    admin = 'admin'
    user = 'user'