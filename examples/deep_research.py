from textpy import code


@code
def deep_research(*, message: str) -> str: ...


if __name__ == "__main__":
    deep_research(message="What was the impact of DeepSeek on stock prices and why?")
