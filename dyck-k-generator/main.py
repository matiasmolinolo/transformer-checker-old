from generator import generate_dataset

def main():
    n = 5
    k = 2
    max_length = 5
    balanced = 0.5
    path = "data/dyck-2-10-0_5.jsonl"
    
    generate_dataset(n, k, max_length, balanced, path)

if __name__ == "__main__":
    main()