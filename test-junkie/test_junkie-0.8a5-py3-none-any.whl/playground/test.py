from test_junkie.debugger import LogJunkie
from test_junkie.decorators import Suite, test


@Suite()
class ExampleSuite:

    @test()
    def archive_product(self):

        @step()
        def step1():
            print("1")

        @step()
        def step2():
            print("2")


if "__main__" == __name__:
    from test_junkie.runner import Runner

    LogJunkie.enable_logging(10)
    runner = Runner([ExampleSuite])
    runner.run()
