import sys

from textpy import code, text


@text
# add the comment if need
def add_new_command_to_docker_file(
    *, docker_file_str: str, new_command_description: str
) -> str: ...


@code
# return the execute's output, without code decorate
def execute_the_docker_file_to_create_image(
    *, docker_file_str: str, docker_image_name: str
) -> str: ...


if __name__ == "__main__":
    assert len(sys.argv) >= 2

    project_path = sys.argv[1]

    docker_file_str: str = ""

    description = (
        "FROM python:3.12.10-bookworm"
        + f"copy the {project_path} to /textpy"
        + f"install the python package in the /textpy"
    )

    docker_file_str = add_new_command_to_docker_file(
        docker_file_str=docker_file_str, new_command_description=description
    )

    output = execute_the_docker_file_to_create_image(
        docker_file_str=docker_file_str, docker_image_name="textpy"
    )
