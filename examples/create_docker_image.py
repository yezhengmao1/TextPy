import sys

from textpy import code, text


@text
def add_new_command_to_docker_file(
    *, docker_file_str: str, new_command_description: str
) -> str: ...


if __name__ == "__main__":
    assert len(sys.argv) >= 2

    project_path = sys.argv[1]

    docker_file_str: str = ""

    descriptions = [
        "FROM python:3.12.10-bookworm",
        f"copy the {project_path} to /",
        f"install the python package in the {project_path}",
    ]
    for desc in descriptions:
        docker_file_str = add_new_command_to_docker_file(
            docker_file_str=docker_file_str, new_command_description=desc
        )

        print(docker_file_str)
