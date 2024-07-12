import subprocess
from pathlib import Path
import os
import time



node = os.environ['tagName']
start_time = time.time()

if __name__ == '__main__':
    # print(f"NODE <{node}> START TIME: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}")
    # command line args along with error capture on failure with check true
    s = subprocess.run(f'behave --no-capture --tags=~@skip --tags={node} -f allure -o allure_report', shell=True, check=False)
    path = Path('./rerun_failing.features')
    # for _ in range(0, 3):
    #     time.sleep(2)
    #     if path.is_file():
    #         print(f"RESTARTING Features for node: <{node}>\n{path.read_text()}")
    #         s = subprocess.run('behave @rerun_failing.features --no-capture -f allure -o allure_report', shell=True, check=False)
    # print(f"NODE <{node}> EXECUTION TIME:  {str(time.time() - start_time)[:7]} seconds")