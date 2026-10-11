import csv
from collections import Counter

MIN_WINS = 3  # change this as needed

def extract_names(crew_field):
    names = []
    parts = crew_field.split(",")

    for part in parts:
        part = part.strip()

        # Handle coxswain entries like "Cox: Name"
        if part.startswith("Cox:"):
            name = part.replace("Cox:", "").strip()
            names.append(name)
        else:
            names.append(part)

    return names

def main():
    counter = Counter()

    with open("hocr_winners.csv", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        for row in reader:
            crew_field = row["Crew Members"]

            if not crew_field:
                continue

            names = extract_names(crew_field)
            counter.update(names)

    # Filter and sort
    results = [(name, wins) for name, wins in counter.items() if wins >= MIN_WINS]
    results.sort(key=lambda x: (-x[1], x[0]))

    for name, wins in results:
        print(f"{name}: {wins}")

if __name__ == "__main__":
    main()