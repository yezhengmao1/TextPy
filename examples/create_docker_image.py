from textpy import code, text


@text
def create_docker_file(*, description: str) -> str: ...


if __name__ == "__main__":
    python_environment = create_docker_file(description="python3.12")

    print(python_environment)
