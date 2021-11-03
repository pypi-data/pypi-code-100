import unittest
from tests.tests_ios.BaseTemplateTestIos import BaseTemplateTestIos
from net_models.models.routing import (
    RoutingIsisProcess, RoutingIsisNetwork, AuthenticationIsis, AuthenticationIsisMode, AuthenticationIsisKeychain,
    RoutingIsisLsp, RoutingIsisLspGenInterval
)


class TestIosRoutingIsisProcess(BaseTemplateTestIos):
    TEST_CLASS = RoutingIsisProcess
    TEMPLATE_NAME = 'ios_routing_isis'

    # TODO: Finish
    def test_01(self):
        test_cases = [
            {
                "test_name": "Test-Model-01",
                "data": {
                    "params": RoutingIsisProcess(
                        process_id=1,
                        network=RoutingIsisNetwork(area_id="49", system_id="0011.0100.0320.0011", nsel="00"),
                        is_type="level-2-only",
                        metric_style="wide",
                        authentication=AuthenticationIsis(
                            mode=[
                                AuthenticationIsisMode(level='level-1', auth_mode='md5'),
                                AuthenticationIsisMode(level='level-2', auth_mode='md5')
                            ],
                            keychain=[
                                AuthenticationIsisKeychain(level='level-1', keychain="ISIS-KEY"),
                                AuthenticationIsisKeychain(level='level-2', keychain="ISIS-KEY")
                            ]
                        ),
                        fast_flood=10,
                        lsp=RoutingIsisLsp(
                            max_lifetime=65535,
                            refresh_interval=65000,
                            gen_intervals=[
                                RoutingIsisLspGenInterval(
                                    interval=5,
                                    init_wait=5,
                                    wait=200
                                )
                            ]
                        ),
                        passive_interfaces=[
                            "Loopback0"
                        ],
                        extra_config=[

                        ]
                    )
                },
                "result": (
                    "router isis 1\n"
                    " net 49.0011.0100.0320.0011.00\n"
                    " is-type level-2-only\n"
                    " authentication mode md5 level-1\n"
                    " authentication mode md5 level-2\n"
                    " authentication key-chain ISIS-KEY level-1\n"
                    " authentication key-chain ISIS-KEY level-2\n"
                    " metric-style wide\n"
                    " fast-flood 10\n"
                    " max-lsp-lifetime 65535\n"
                    " lsp-refresh-interval 65000\n"
                    " lsp-gen-interval 5 5 200\n"
                    " passive-interface Loopback0\n"
                    # " set-overload-bit on-startup 180\n"
                    # " spf-interval 5 50 200\n"
                    # " prc-interval 5 50 200\n"
                    # " log-adjacency-changes\n"
                    # " nsf cisco\n"
                    # " distribute link-state\n"
                    # " segment-routing mpls\n"
                    # " segment-routing prefix-sid-map advertise-local\n"
                    # " fast-reroute per-prefix level-2 route-map RM-HOST-ONLY\n"
                    # " fast-reroute ti-lfa level-2\n"
                    # " microloop avoidance segment-routing\n"
                    # " microloop avoidance rib-update-delay 7000\n"
                    # " bfd all-interfaces\n"
                    # " mpls traffic-eng router-id Loopback0\n"
                    # " mpls traffic-eng level-2\n"
                )
            }
        ]
        self.common_testbase(test_cases=test_cases)


del BaseTemplateTestIos

if __name__ == '__main__':
    unittest.main()
