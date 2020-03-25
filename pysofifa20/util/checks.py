class Postions:
    def __init__(self):
        self.postions = [
            "GK",
            "CB",
            "RCB",
            "LCB",
            "CDM",
            "CM",
            "CAM",
            "CF",
            "RB",
            "LB",
            "RWB",
            "LWB",
            "RM",
            "LM",
            "RW",
            "LW",
            "RF",
            "LF",
            "RS",
            "LS",
            "ST",
            "MS"
        ]
        
    
    def is_position(self, postion) -> bool:
        if postion in self.postions:
            return True
        return False
    
    def get_all_postions(self) -> list:
        return self.postions

    def convert_postions(self, stuff) -> list:
        _position = []
        pos = stuff.split()
        for positions in pos:
            if self.is_position(positions):
                _position.append(positions)
            
        return _position