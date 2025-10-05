import asyncio
from utils.tools import get_eth_price

class ConfigLoader:
    _instance = None
    eth_price = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ConfigLoader, cls).__new__(cls)
        return cls._instance
    
    async def initialize(self):
        """Initialize any async config values"""
        if self.eth_price is None:
            self.eth_price = await get_eth_price()
        return self
    
    @classmethod
    async def get_eth_price(cls):
        if cls._instance is None or cls._instance.eth_price is None:
            instance = cls()
            await instance.initialize()
        return cls._instance.eth_price

# Create a global instance
config_loader = ConfigLoader()
