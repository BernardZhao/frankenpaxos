from .fastmultipaxos import *

def _main(args) -> None:
    inputs = [
        Input(
            timeout_seconds=120,
            net_name='SingleSwitchNet',
            f=1,
            num_clients=num_clients,
            num_threads_per_client=1,
            round_system_type=round_system_type,
            profiled=args.profile,
            monitored=args.monitor,
            prometheus_scrape_interval_ms=200,
            duration_seconds=20,
            client_lag_seconds=5,
            client_repropose_period_seconds=1,
        )
        for num_clients in range(1, 30)
        for round_system_type in [RoundSystemType.CLASSIC_ROUND_ROBIN.name,
                                  RoundSystemType.MIXED_ROUND_ROBIN.name]
    ] * 3

    def make_net(input) -> FastMultiPaxosNet:
        return SingleSwitchNet(
            f=input.f,
            num_clients=input.num_clients,
            rs_type = RoundSystemType[input.round_system_type]
        )

    run_suite(args, inputs, make_net)

if __name__ == '__main__':
    _main(get_parser().parse_args())
