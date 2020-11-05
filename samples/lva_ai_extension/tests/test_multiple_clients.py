import subprocess
import time
import os


def test_multiple_clients(port=5001,loops=10,max_running_pipelines=10):
    sleep_period = 0.25
    print()
    if not os.getenv('PIPELINE_NAME') and not os.getenv('PIPELINE_VERSION'):
        print("LVA environment not detected, skipping test")
        return
    server_args = [ "python3", "/home/video-analytics-serving/samples/lva_ai_extension/server", "-p", str(port), "--max-running-pipelines", str(max_running_pipelines)]
    client_args = [ "python3", "/home/video-analytics-serving/samples/lva_ai_extension/client", "-s", "127.0.0.1:" + str(port), "-l", str(loops), "-f", "/home/video-analytics-serving/samples/lva_ai_extension/sampleframes/sample01.png"]
    print(' '.join(server_args))
    server_process = subprocess.Popen(server_args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=1, universal_newlines=True)
    time.sleep(sleep_period)
    print(' '.join(client_args))
    client_process_list = []
    for x in range(max_running_pipelines):
        client_process = subprocess.Popen(client_args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=1, universal_newlines=True)
        client_process_list.append(client_process)
    print(client_process_list)
    client_process_list[-1].poll()
    elapsed_time = 0
    while client_process_list[-1].returncode is None and elapsed_time < 60:
        #print(client_process.stdout.readline())
        time.sleep(sleep_period)
        elapsed_time += sleep_period
        client_process_list[-1].poll()
    assert client_process_list[-1].returncode is not None
    assert client_process_list[-1].returncode == 0
    print("Elapsed time = {}s".format(elapsed_time))
    server_process.kill()

if __name__=="__main__":
    test_multiple_clients()