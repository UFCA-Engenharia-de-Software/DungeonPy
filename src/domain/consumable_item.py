from domain.item import Item
from domain.entity import Entity
class ConsumableItem(Item):

    def __init__(
        self,
        name:str,
        description: str,
        weight: float,
        recovered_value: int,

    ):
        super().__init__(
            name, description, weight
        )
        self.recovered_value = recovered_value

    
    @property
    def recovered_value(self):
        return self._recovered_value
    
    @recovered_value.setter
    def recovered_value(self, value):

        if not isinstance(value, int):
            raise TypeError("Recovered Value needs to be a whole number.")
        
        if value <= 0:
            raise ValueError("Recovered Value Must be greater than 0")
        
        self._recovered_value = value
    
    def use(self, target: Entity) -> None:

        required_recovered_value = target.max_life - target.current_life

        #Already check if recovered value it´s greater than max_life. 
        if self.recovered_value > required_recovered_value:
            target.current_life = target.max_life
            return
        
        target.current_life += self.recovered_value
    