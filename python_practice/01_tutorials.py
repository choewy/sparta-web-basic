def print_tutorials() -> None:
    print("Hello World!")


def str_tutorials(last_name: str, first_name: str) -> None:
    print(last_name + first_name)


def list_tutorials(new: any) -> None:
    fruits = ['사과', '배', '감', '수박', '귤', '딸기']

    if any:
        fruits.append('청포도')

    print(fruits)


def dict_tutorials(key: str, value: any) -> None:
    people = [
        {'name': 'bob', 'age': 20},
        {'name': 'carry', 'age': 38},
        {'name': 'john', 'age': 7},
        {'name': 'smith', 'age': 17},
        {'name': 'ben', 'age': 27}
    ]

    if key:
        people.append({key: value})

    print(people)


def function_tutorials(num: int, operand: int) -> int:
    return num + operand


if __name__ == '__main__':
    print_tutorials()