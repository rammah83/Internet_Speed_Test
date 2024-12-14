"""
Module for running a speed test using Speedtest.net and printing the results to
the console.

The test measures the latency (ping), download speed, and upload speed of the
internet connection and prints the results in a formatted summary.

The module contains a single function, `test_internet_speed`, which runs the
speed test and prints the results.
To install library: pip install speedtest-cli
"""

import sys
from datetime import datetime
from tqdm import tqdm

import speedtest


def test_internet_speed():
    """
    Runs a speed test using Speedtest.net and prints the results to the console.

    The test measures the latency (ping), download speed, and upload speed of the
    internet connection and prints the results in a formatted summary.

    Exit codes:
        0: Test completed successfully
        1: Test failed due to errors
    """
    num_tests = 5
    pings = []
    download_speeds = []
    upload_speeds = []

    try:
        # Get current timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"Timestamp: {timestamp}")
        st = speedtest.Speedtest()

        print("Fetching the best server based on ping...")
        st.get_best_server()

        print("Performing speed test...")

        for i in tqdm(range(num_tests)):
            tqdm.write(f"Running test {i+1} of {num_tests}...", nolock=True)

            # Performing ping test...
            ping = st.results.ping

            # Performing download test...
            download_speed = st.download()

            # Performing upload test...
            upload_speed = st.upload()

            # Convert speeds from bits per second to megabits per second
            download_speed_mbps = download_speed / 1_000_000
            upload_speed_mbps = upload_speed / 1_000_000


            pings.append(ping)
            download_speeds.append(download_speed_mbps)
            upload_speeds.append(upload_speed_mbps)

    except speedtest.ConfigRetrievalError:
        print("Error: Unable to retrieve configuration from Speedtest.net.")
        sys.exit(1)
    except speedtest.NoMatchedServers:
        print("Error: No matched servers for testing.")
        sys.exit(1)
    except speedtest.ServersRetrievalError:
        print("Error: Unable to retrieve speed test server list.")
        sys.exit(1)
    except speedtest.SpeedtestException as e:
        print(f"Speedtest failed: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        raise
    else:
        # Calculate mean and std dev from the results
        mean_ping = sum(pings) / num_tests
        std_ping = (sum((x - mean_ping) ** 2 for x in pings) / (num_tests - 1)) ** 0.5

        mean_download = sum(download_speeds) / num_tests
        std_download = (
            sum((x - mean_download) ** 2 for x in download_speeds) / (num_tests - 1)
        ) ** 0.5

        mean_upload = sum(upload_speeds) / num_tests
        std_upload = (
            sum((x - mean_upload) ** 2 for x in upload_speeds) / (num_tests - 1)
        ) ** 0.5

        print(f"\n===== Internet Speed Test Results of {num_tests} =====")
        print(f"{ '<':<20}{ 'Mean':>10}{ 'Std Dev':>20}")
        print("-" * 60)
        print(f"{ 'Ping (ms)':<20}{ mean_ping:>10.2f}{ std_ping:>20.2f}")
        print(f"{ 'Download Speed (Mbps)':<20}{ mean_download:>10.2f}{ std_download:>20.2f}")
        print(f"{ 'Upload Speed (Mbps)':<20}{ mean_upload:>10.2f}{ std_upload:>20.2f}")
        print("==================Test Completed=====================")


if __name__ == "__main__":
    test_internet_speed()
