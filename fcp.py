
class FCPEuro:
    def __init__(self, year: str = "1999", model: str = "323i", part_number: str = "33176770788") -> None:
        self.base_path = "https://www.fcpeuro.com/BMW-parts/323i/?year=1999&m=20&e=177&t=6&b=5&d=65&v="
        self.model = model 
        self.year = year 
        self.part_number = part_number

    def grab_item(self):
        base_path = f"{self.base_path}&keywords={self.part_number}?year={self.year}&m=20&e=177&t=6&b=5&d=65&v="
        "https://www.fcpeuro.com/BMW-parts/323i/?year=1999&m=20&e=177&t=6&b=5&d=65&v=&keywords=33176770788"

class Table(BaseModel):
    id: int = 1
    No: str = "Foo"
    Description: Optional[str] = "Bar"
    Supp: datetime = datetime(2020, 1, 1)
    Qty: datetime = datetime(2020, 1, 1)
    partNumber: str = None

class Car(BaseModel):
    id: int = 1
    Name: str = "323"
    Description: Optional[str] = "Bar"
    submod: datetime = datetime(2020, 1, 1)
    model: datetime = datetime(2020, 1, 1)
    year: str = None