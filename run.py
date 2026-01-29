import threading
import asyncio
from youtubezeno import SEA, start_streaming
import traceback

async def main():
    room_id = "6931ba4b2fbd1725dffbed97"
    token = "cf18aa1cc9d1a810034137207aefa5fd06da0ca71b632835513f6fd1fc5e8759"    
    bot_instance = SEA()  
    # Start the streaming thread
    streaming_thread = threading.Thread(target=start_streaming, args=(bot_instance,))
    streaming_thread.daemon = True
    streaming_thread.start()
    while True:
        try:
            await asyncio.sleep(5)
            await bot_instance.run(room_id, token)
        except Exception as e:
            traceback.print_exc()
            await asyncio.sleep(5)
if __name__ == '__main__':
    asyncio.run(main())