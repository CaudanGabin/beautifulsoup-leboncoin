import re

class Car:
    def __init__(self):
        self._link = ""
        self._price = ""
        self._coteMin = ""
        self._coteMax = ""

    # Setters
    def set_link(self, link):
        self._link = link

    def set_price(self, price):
        self._price = price

    def set_coteMin(self, coteMin):
        self._coteMin = coteMin

    def set_coteMax(self, coteMax):
        self._coteMax = coteMax

    # Getters
    def get_link(self):
        return self._link

    def get_price(self):
        return self._price

    def get_coteMin(self):
        return self._coteMin

    def get_coteMax(self):
        return self._coteMax

    def isValid(self):
        return self._price != "" and self._coteMin != "" and self._coteMax != ""

    def remove_format(self, prix_str):
        chiffres = re.findall(r'\d+', prix_str)
        if len(chiffres) == 0:
            return 0
        return int(''.join(chiffres))

    def isValuable(self):
        if not self.isValid():
            return False
        price = self.remove_format(self._price)
        min = self.remove_format(self._coteMin)
        if price == 0 or min == 0:
            return False
        return price < min
        
    def __str__(self):
        return f"💰 {self._price} 🚗 cote {self._coteMin} 🔗 {self._link}"
