from decouple import AutoConfig

path = ".env"

config = AutoConfig(path)

__all__ = ['config']
