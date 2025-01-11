from routers.test import get_test_time

def run_tests():
    print(get_test_time("5 minuytes"))
    print(get_test_time("минут 5"))
    print(get_test_time("ми5нут"))
    print(get_test_time("ми55нут"))
    print(get_test_time("минууутминууут"))

if __name__ == "__main__":
    run_tests()
