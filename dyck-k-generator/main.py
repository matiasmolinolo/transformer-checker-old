from checker import is_dyck_word

def main():
    s = "((()))"
    k = 1
    print(is_dyck_word(s, k))

    s_false = "((())"
    print(is_dyck_word(s_false, k))

if __name__ == "__main__":
    main()