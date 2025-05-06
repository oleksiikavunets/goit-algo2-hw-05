class BloomFilter:
    def __init__(self, size, num_hashes):
        self.size = size
        self.num_hashes = num_hashes
        self.bit_array = [0] * size

    def add(self, item):
        item = str(item or None)
        for i in range(1, self.num_hashes + 1):
            index = sum(ord(c) for c in item) * i // len(item) % self.size
            self.bit_array[index] = 1

    def contains(self, item):
        item = str(item or None)
        for i in range(1, self.num_hashes + 1):
            index = sum(ord(c) for c in item) * i // len(item) % self.size
            if self.bit_array[index] == 0:
                return False
        return True


def check_password_uniqueness(filter_, new_passwords):
    return {str(p): 'вже використаний' if filter_.contains(p) else 'унікальний' for p in new_passwords}


if __name__ == "__main__":
    # Ініціалізація фільтра Блума
    bloom = BloomFilter(size=1000, num_hashes=3)

    # Додавання існуючих паролів
    existing_passwords = ["password123", "admin123", "qwerty123"]
    for password in existing_passwords:
        bloom.add(password)

    # Перевірка нових паролів
    new_passwords_to_check = ["password123", "newpassword", "admin123", "guest"]
    results = check_password_uniqueness(bloom, new_passwords_to_check)

    # Виведення результатів
    for password, status in results.items():
        print(f"Пароль '{password}' - {status}.")
