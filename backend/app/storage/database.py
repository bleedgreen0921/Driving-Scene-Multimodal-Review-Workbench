from app.core.config import settings


def get_database_url() -> str:
    """返回用于持久化初始化的数据库连接地址。"""
    return settings.database_url
