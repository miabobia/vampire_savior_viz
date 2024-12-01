import subprocess
import json
from apscheduler.schedulers.background import BackgroundScheduler
import asyncio


# def tail_input_file() -> dict:
#     PATH = "/home/mia_bobia/Downloads/Fightcade-linux-latest/Fightcade/emulator/fbneo/scripts/testlua.json"
#     try:
#         result = subprocess.Popen(
#             f"tail -n 1 {PATH}",
#             shell=True, stdout=subprocess.PIPE
#         ).stdout.read().decode('UTF-8')

#         split = result.split('\r\n')
#         # print(result[0])
#         return json.loads(split[0])
#     except:
#         print("err")


async def tail_input_file() -> dict:
    PATH = "/home/nbee/Downloads/Fightcade/emulator/fbneo/scripts/state_dump_bools.json"
    # try:
    #     result = subprocess.Popen(
    #         f"tail -n 1 {PATH}",
    #         shell=True, stdout=subprocess.PIPE
    #     ).stdout.read().decode('UTF-8')

    #     split = result.split('\r\n')
    #     # print(result[0])
    #     return json.loads(split[0])
    # except:
    #     print("err")

    process = await asyncio.create_subprocess_exec(
        f'tail -n 1 {PATH}',  # Replace with your command and arguments
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )

    # Capture the output (stdout)
    stdout, stderr = await process.communicate()
    
    # Decode the bytes to strings if necessary
    stdout_str = stdout.decode('utf-8') if stdout else ""
    stderr_str = stderr.decode('utf-8') if stderr else ""
    
    # Return the output (you can modify this as needed)
    return stdout_str, stderr_str

async def run_subprocess():
    PATH = "/home/mia_bobia/Downloads/Fightcade-linux-latest/Fightcade/emulator/fbneo/scripts/testlua.json"
    # Use asyncio to create and run the subprocess
    process = await asyncio.create_subprocess_exec(
        # f'tail -n 1 {PATH}',  # Replace with your command and arguments
        'tail', '-n', '1', PATH,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    
    # Capture the output (stdout)
    stdout, stderr = await process.communicate()
    
    # Decode the bytes to strings if necessary
    stdout_str = stdout.decode('utf-8') if stdout else ""
    stderr_str = stderr.decode('utf-8') if stderr else ""
    
    # Return the output (you can modify this as needed)
    return stdout_str, stderr_str

async def main():
    # Await the subprocess execution
    stdout, stderr = await run_subprocess()
    
    if stdout:
        print(f"Subprocess Output: {stdout}")
    if stderr:
        print(f"Subprocess Error: {stderr}")
    
    # Use the output in another task, if needed
    # For example, pass the stdout to another function or file
    await handle_output(stdout)

async def handle_output(s: str):
    print(f'handling output!: {s}')

if __name__ == '__main__':
    asyncio.run(main())
# def add_job(scheduler: BackgroundScheduler):

# def start_job(scheduler: BackgroundScheduler=None):

# def start_reading():
#     scheduler = BackgroundScheduler()
#     scheduler.add_job(tail_input_file, 'interval', seconds=1/80)
#     scheduler.add_listener
#     # scheduler.start()
#     return tail_input_file()



# if __name__ == "__main__":
#     scheduler = BackgroundScheduler()
#     add_job(scheduler=scheduler)
#     start_job(scheduler=scheduler)

    # print(tail_input_file())
    # scheduler.start()
    # print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))
    # main()
