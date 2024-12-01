# import asyncio
# from apscheduler.schedulers.background import BackgroundScheduler
# from multiprocessing import Queue
# import json
# # from async_subprocess import run_subprocess
# import logging
# logging.getLogger('apscheduler').setLevel(logging.ERROR)  # Set APScheduler logs to ERROR level to suppress warnings


# async def run_subprocess(queue: Queue):
#     PATH = "/home/mia_bobia/Downloads/Fightcade-linux-latest/Fightcade/emulator/fbneo/scripts/testlua.json"
#     # Use asyncio to create and run the subprocess
#     process = await asyncio.create_subprocess_exec(
#         # f'tail -n 1 {PATH}',  # Replace with your command and arguments
#         'tail', '-n', '1', PATH,
#         stdout=asyncio.subprocess.PIPE,
#         stderr=asyncio.subprocess.PIPE
#     )
    
#     # Capture the output (stdout)
#     stdout, stderr = await process.communicate()
    


#     #     split = result.split('\r\n')
#     #     # print(result[0])
#     #     return json.loads(split[0])
#     # Decode the bytes to strings if necessary
#     if stdout:
#         try:
#             stdout_dict = json.loads(stdout.decode('utf-8').split('\r\n')[0]) if stdout else dict()
#             queue.put(stdout_dict)
#         except:
#             print(f'ERROR:')
#     # stderr_str = stderr.decode('utf-8') if stderr else ""
#     # print(stdout_dict)
#     # queue.put(stdout_dict)

#     # if stderr_str: print(f'ERROR: {stderr_str}')
#     # Return the output (you can modify this as needed)
#     # return stdout_str, stderr_str

# async def scheduled_subprocess(queue: Queue):
#     # Call the async subprocess function
#     await run_subprocess(queue)

# def run_scheduled_task(queue: Queue):
#     # Run the async function within an asyncio event loop
#     asyncio.run(scheduled_subprocess(queue))

# def start_scheduler(queue: Queue):
#     # Initialize scheduler
#     scheduler = BackgroundScheduler()
    
#     # Schedule the subprocess to run every 5 seconds
#     scheduler.add_job(run_scheduled_task, 'interval', seconds=1/80, args=[queue])
    
#     # Start the scheduler
#     scheduler.start()

#     return scheduler

#     # try:
#     #     # Keep the main thread alive so that the scheduler can keep running
#     #     while True:
#     #         # print('true')
#     #         pass
#     # except (KeyboardInterrupt, SystemExit):
#     #     scheduler.shutdown()
# schedule_test.py
import asyncio
from apscheduler.schedulers.background import BackgroundScheduler
from multiprocessing import Queue
import json
import logging
from typing import Dict, Optional

logging.getLogger('apscheduler').setLevel(logging.ERROR)

class DataReader:
    def __init__(self, file_path: str):
        self.file_path = file_path

    async def run_subprocess(self, queue: Queue) -> None:
        try:
            process = await asyncio.create_subprocess_exec(
                'tail', '-n', '1', self.file_path,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            stdout, stderr = await process.communicate()
            
            if stdout:
                try:
                    stdout_str = stdout.decode('utf-8').strip()
                    if stdout_str:
                        # print(stdout_str)
                        data = json.loads(stdout_str)
                        queue.put(data)
                except json.JSONDecodeError as e:
                    logging.error(f"JSON decode error: {e}")
                except Exception as e:
                    logging.error(f"Error processing output: {e}")
            
            if stderr:
                logging.error(f"Subprocess error: {stderr.decode('utf-8')}")
                
        except Exception as e:
            logging.error(f"Subprocess execution error: {e}")

    async def scheduled_subprocess(self, queue: Queue) -> None:
        await self.run_subprocess(queue)

def run_scheduled_task(queue: Queue, reader: DataReader) -> None:
    asyncio.run(reader.scheduled_subprocess(queue))

def start_scheduler(queue: Queue, file_path: str, interval: float = 1/80) -> BackgroundScheduler:
    reader = DataReader(file_path)
    scheduler = BackgroundScheduler()
    scheduler.add_job(run_scheduled_task, 'interval', seconds=interval, args=[queue, reader])
    scheduler.start()
    return scheduler
