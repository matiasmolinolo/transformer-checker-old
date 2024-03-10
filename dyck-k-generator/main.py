from generator import generate_dataset

def main():
    n = 500_000
    k = 3
    max_length = 1024
    balanced = 0.6
    path = "data/dyck-2-10-0_5.jsonl"
    
    generate_dataset(n, k, max_length, balanced, path)

if __name__ == "__main__":
    main()