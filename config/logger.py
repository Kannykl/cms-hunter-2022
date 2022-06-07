from loguru import logger

logger.add(
    "cms_logs.log",
    format="{time:YYYY-MM-DD at HH:mm:ss} {level} {message} in {name} {line}",
    rotation="10MB",
    compression="zip",
    serialize=True,
)