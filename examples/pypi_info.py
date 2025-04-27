from textpy import code


@code
# the url is: https://pypi.org/project/<package_name>/
# only get the div class=project-description
def get_pypi_package_info_from_url(*, package_name: str) -> str: ...


if __name__ == "__main__":
    description = get_pypi_package_info_from_url(package_name="litellm")
