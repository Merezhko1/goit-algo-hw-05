import timeit
from pathlib import Path
from typing import Callable

from search_algorithms import (
    boyer_moore_search,
    kmp_search,
    rabin_karp_search,
)


SearchFunction = Callable[[str, str], int]


ALGORITHMS: dict[str, SearchFunction] = {
    "Boyer-Moore": boyer_moore_search,
    "KMP": kmp_search,
    "Rabin-Karp": rabin_karp_search,
}

ARTICLES = {
    "Article 1": {
        "file": "article_1.txt",
        "existing": "двійковий пошук",
        "missing": "вигаданий підрядок якого точно немає",
    },
    "Article 2": {
        "file": "article_2.txt",
        "existing": "розгорнутий список",
        "missing": "вигаданий підрядок якого точно немає",
    },
}


def measure_time(search_func: SearchFunction, text: str, pattern: str) -> float:
    return timeit.timeit(lambda: search_func(text, pattern), number=100)


def find_winner(results: dict[str, float]) -> str:
    return min(results, key=results.get)


def main() -> None:
    all_results = []

    print("| Text | Pattern type | Boyer-Moore | KMP | Rabin-Karp | Fastest |")
    print("| --- | --- | ---: | ---: | ---: | --- |")

    for article_name, data in ARTICLES.items():
        text = Path(data["file"]).read_text(encoding="utf-8")

        for pattern_type in ("existing", "missing"):
            pattern = data[pattern_type]
            results = {
                name: measure_time(func, text, pattern)
                for name, func in ALGORITHMS.items()
            }
            winner = find_winner(results)
            all_results.append((article_name, pattern_type, winner, results))

            print(
                f"| {article_name} | {pattern_type} | "
                f"{results['Boyer-Moore']:.6f} | "
                f"{results['KMP']:.6f} | "
                f"{results['Rabin-Karp']:.6f} | "
                f"{winner} |"
            )

    total_results = {name: 0.0 for name in ALGORITHMS}
    for _, _, _, results in all_results:
        for name, value in results.items():
            total_results[name] += value

    print()
    print("Total time:")
    for name, value in total_results.items():
        print(f"{name}: {value:.6f}")
    print(f"Overall fastest: {find_winner(total_results)}")


if __name__ == "__main__":
    main()
