from dataclasses import dataclass

@dataclass
class WifiConfiguration:
    access_point: str
    password: str