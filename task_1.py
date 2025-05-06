class BloomFilter:
    def __init__(self, size, num_hashes):
        self.size = size
        self.num_hashes = num_hashes
        self.bit_array = [0] * size

    def add(self, item):
        for i in range(1, self.num_hashes + 1):
            index = int(''.join(str(ord(c)) for c in str(item))) // i // len(str(item)) % self.size
            self.bit_array[index] = 1

    def contains(self, item):
        for i in range(1, self.num_hashes + 1):
            index = int(''.join(str(ord(c)) for c in str(item))) // i // len(str(item)) % self.size
            if self.bit_array[index] == 0:
                return False
        return True


def check_password_uniqueness(filter_, new_passwords):
    return {str(p): filter_.contains(p) for p in new_passwords}


if __name__ == "__main__":
    # Ініціалізація фільтра Блума
    bloom = BloomFilter(size=1000, num_hashes=3)

    # Додавання існуючих паролів
    existing_passwords = ["password123", "admin123", "qwerty123", True]
    for password in existing_passwords:
        bloom.add(password)

    # Перевірка нових паролів
    new_passwords_to_check = ["password123", "newpassword", "admin123", "guest", None, [12, 'foo', None]]
    results = check_password_uniqueness(bloom, new_passwords_to_check)

    # Виведення результатів
    for password, status in results.items():
        print(f"Пароль '{password}' - {status}.")
