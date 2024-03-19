from click.testing import CliRunner
from py_webscraper.cli import get_domain_name


class TestPyWebScraper:
    def test_get_domain_name(self):
        runner = CliRunner()
        result = runner.invoke(get_domain_name, ["http://www.google.com"])
        assert result.exit_code == 0
