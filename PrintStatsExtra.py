from locust.stats import global_stats
import six

STATS_NAME_WIDTH = 60

def print_stats_extra(stats):
    print((" %-" + str(STATS_NAME_WIDTH) + "s %7s %12s %7s %7s %7s  | %7s %7s") % (
    'Name', '# reqs', '# fails', 'Avg', 'Min', 'Max', 'Median', 'req/s'))
    print("-" * (80 + STATS_NAME_WIDTH))
    total_rps = 0
    total_reqs = 0
    total_failures = 0
    for key in sorted(six.iterkeys(stats)):
        r = stats[key]
        total_rps += r.current_rps
        total_reqs += r.num_requests
        total_failures += r.num_failures
        print(r)
    print("-" * (80 + STATS_NAME_WIDTH))

    try:
        fail_percent = (total_failures / float(total_reqs)) * 100
    except ZeroDivisionError:
        fail_percent = 0

    print((" %-" + str(STATS_NAME_WIDTH) + "s %7d %12s %42.2f") % (
    'Total', total_reqs, "%d(%.2f%%)" % (total_failures, fail_percent), total_rps))
    print("")


def print_percentile_stats_extra(stats):
    print("Percentage of the requests completed within given times")
    print((" %-" + str(STATS_NAME_WIDTH) + "s %8s %6s %6s %6s %6s %6s %6s %6s %6s %6s") % (
    'Name', '# reqs', '50%', '66%', '75%', '80%', '90%', '95%', '98%', '99%', '100%'))
    print("-" * (80 + STATS_NAME_WIDTH))
    for key in sorted(six.iterkeys(stats)):
        r = stats[key]
        if r.response_times:
            print(r.percentile())
    print("-" * (80 + STATS_NAME_WIDTH))

    total_stats = global_stats.aggregated_stats()
    if total_stats.response_times:
        print(total_stats.percentile())
    print("")
