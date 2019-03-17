import pytest
from assertpy import assert_that
from testfixtures import compare

import api
from api.pytest_customizations.api.helpers import get_expected_success_response, \
    get_expected_success_response_for_user_by_id


class TestUsers(object):
    USERS = {16: [16, "Karina", "female", 16, "New York", "2001-06-15T12:43:00"]}

    def test_users_by_id(self):
        user_id = 16
        result = api.test.user_by_id(user_id)

        assert_that(result.status_code).is_equal_to(200)
        compare(expected=get_expected_success_response_for_user_by_id(self.USERS[user_id]), actual=result.body)

    @pytest.mark.parametrize(
        argnames=("gender", "expected_ids"),
        argvalues=[("female", [16, 5, 300]), ("male", [33, 10, 911, 94])])
    def test_filter_users_by_gender(self, gender, expected_ids):
        result = api.test.users_by_gender(gender)

        assert_that(result.status_code).is_equal_to(200)
        compare(expected=get_expected_success_response(expected_ids), actual=result.body)
