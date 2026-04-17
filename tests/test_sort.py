import allure
import pytest

from pom.inventory_page import InventoryPage, FilterOptions
from pom.login_page import LoginPage


@allure.parent_suite("Saucedemo tests")
@allure.suite("Sort tests")
@pytest.mark.parametrize(
    "user_key, filter_option",
    [
        # Standard user
        pytest.param(
            "standard_user",
            FilterOptions.HIGH_TO_LOW,
            id="Standard user login. Sort high to low"
        ),
        pytest.param(
            "standard_user",
            FilterOptions.LOW_TO_HIGH,
            id="Standard user login. Sort low to high"
        ),
        pytest.param(
            "standard_user",
            FilterOptions.A_TO_Z,
            id="Standard user login. Sort A to Z"
        ),
        pytest.param(
            "standard_user",
            FilterOptions.Z_TO_A,
            id="Standard user login. Sort Z to A"
        ),
        # Problem user
        pytest.param(
            "problem_user",
            FilterOptions.HIGH_TO_LOW,
            marks=pytest.mark.xfail(reason="Known sorting defect for problem_user"),
            id="Problem user login. Sort high to low"
        ),
        pytest.param(
            "problem_user",
            FilterOptions.LOW_TO_HIGH,
            marks=pytest.mark.xfail(reason="Known sorting defect for problem_user"),
            id="Problem user login. Sort low to high"
        ),
        pytest.param(
            "problem_user",
            FilterOptions.A_TO_Z,
            id="Problem user login. Sort A to Z"
        ),
        pytest.param(
            "problem_user",
            FilterOptions.Z_TO_A,
            marks=pytest.mark.xfail(reason="Known sorting defect for problem_user"),
            id="Problem user login. Sort Z to A"
        ),
        # Error user
        pytest.param(
            "error_user",
            FilterOptions.HIGH_TO_LOW,
            marks=pytest.mark.xfail(reason="Known sorting defect for error_user"),
            id="Error user login. Sort high to low"
        ),
        pytest.param(
            "error_user",
            FilterOptions.LOW_TO_HIGH,
            marks=pytest.mark.xfail(reason="Known sorting defect for error_user"),
            id="Error user login. Sort low to high"
        ),
        pytest.param(
            "error_user",
            FilterOptions.A_TO_Z,
            id="Error user login. Sort A to Z"
        ),
        pytest.param(
            "error_user",
            FilterOptions.Z_TO_A,
            marks=pytest.mark.xfail(reason="Known sorting defect for error_user"),
            id="Error user login. Sort Z to A"
        ),
    ]
)
def test_sort(
        login_page: LoginPage,
        inventory_page: InventoryPage,
        credentials: dict[str, str],
        user_key: str,
        filter_option: FilterOptions
):
    login_page.login(username=credentials[user_key], password=credentials["password"])
    inventory_page.select_filter_option(filter_option)
    is_reverse = filter_option in [FilterOptions.HIGH_TO_LOW, FilterOptions.Z_TO_A]
    actual = inventory_page.get_actual_data(filter_option)
    expected = sorted(actual, reverse=is_reverse)
    assert actual == expected, f"Items are not the same. Actual values: {actual}\nExpected values: {expected}"
