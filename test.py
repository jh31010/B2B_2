from dataclasses import dataclass, asdict
import json

# dataclass 정의
@dataclass
class Person:
    name: str
    age: int

# 클래스 배열 생성
people = [
    Person(name="Alice", age=30),
    Person(name="Bob", age=25),
    Person(name="Charlie", age=35)
]

# JSON으로 변환
people_json = json.dumps([asdict(person) for person in people], ensure_ascii=False, indent=4)

print(people_json)