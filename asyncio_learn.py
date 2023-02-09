import asyncio
from random import random
import time


"""
Пример получения задачи (Task) из основной корутины
"""
#
#
# async def main():  # Определяем главную корутину
#     print('main coroutine started')  # Контрольное сообщение
#     task = asyncio.current_task()  # Получаем текущую задачу
#     print(task)  # Контрольное сообщение о задаче
#
# asyncio.run(main())  # Запускаем главную корутину
########################################################################################################################


"""
В этом примере мы сначала создаем 10 задач, каждая из которых выполняет одну и ту же корутину.
Затем основная корутина получает набор всех задач, запланированных или выполняемых в прогрмме, и сообщает их детали.
"""


# # coroutine for a task
# async def task_coroutine(value):
#     # report a message
#     print(f'task {value} is running')
#     # block for a moment
#     await asyncio.sleep(1)
#
#
# # define a main coroutine
# async def main():
#     # report a message
#     print('main coroutine started')
#     # start many tasks
#     started_tasks = [asyncio.create_task(task_coroutine(i)) for i in range(10)]
#     # allow some of the tasks time to start
#     await asyncio.sleep(0.1)
#     # get all tasks
#     tasks = asyncio.all_tasks()
#     # report all tasks
#     for task in tasks:
#         print(f'> {task.get_name()}, {task.get_coro()}')
#     # wait for all tasks to complete
#     for task in started_tasks:
#         await task
#
#
# # start the asyncio program
# asyncio.run(main())
########################################################################################################################


"""
В этом примере корутина main() (- она же entrypoint) с помощью генератора списков создаёт список объектов корутины
task_coro, который передается функции gather(), затем распаковывается с помощью оператора * в 10 отдельных выражений,
затем корутина main() ожидает объект Future, возвращенный вызовом gather(), приостанавливая и ожидая завершения
выполнения всех запланированных корутин. Корутины запускаются, сообщают о результатах и засыпают перед завершением.
И только после этого корутина main() возобновляет свою работу и сообщает об успешном окончании сообщением main done
"""


# coroutine used for a task
# async def task_coro(value):
#     # report a message
#     print(f'>task {value} executing')
#     # sleep for a moment
#     await asyncio.sleep(1)
#
#
# # coroutine used for the entry point
# async def main():
#     # report a message
#     print('main starting')
#     # create many coroutines
#     coros = [task_coro(i) for i in range(10)]
#     # run the tasks
#     await asyncio.gather(*coros)
#     # report a message
#     print('main done')
#
#
# # start the asyncio program
# asyncio.run(main())
########################################################################################################################


"""
В этом примере показано, как мы можем использовать функцию wait() для ожидания завершения набора задач.
Опять же, корутина main() используется как точка входа в программу asyncio. В ней создается список из 10 задач, каждая
из которых представляет случайный целочисленный аргумент от 0 до 9. Затем корутина main приостанавливается и ожидает
завершения всех задач. Каждая задача генерирует случайное значение 0-1 и засыпает на время в секундах от этого значения,
а затем печатает резульатат об этом значении. После того, как все задачи будут выполнены, main() сообщит об этом.
"""


# coroutine to execute in a new task
# async def task_coro(arg):
#     # generate a random value between 0 and 1
#     value = random()
#     # block for a moment
#     await asyncio.sleep(value)
#     # report the value
#     print(f'>task {arg} done with {value}')
#
#
# # main coroutine
# async def main():
#     # create many tasks
#     tasks = [asyncio.create_task(task_coro(i)) for i in range(10)]
#     # wait for all tasks to complete
#     done, pending = await asyncio.wait(tasks)
#     # report results
#     print('All done')
#
#
# # start the asyncio program
# asyncio.run(main())
########################################################################################################################


"""
В этом примере entrypoint - main() создаёт корутину задачи task_coro, вызывает wait_for(), передаёт параметарми
задачу и таймер на выполнение задачи в секундах. Корутина main() приостанавливается, ожидая выполнения задачи task_coro
и возобновляет свою работу по истечению таймера timeout. wait_for() отменяет задачу task_coro, которая отвечает
на запрос о прекращении и вызывает исключение TimeoutError и завершает работу. main() запускается и обрабатывает
ошибку TimeoutError.
"""


# # example of waiting for a coroutine with a timeout
#
# # coroutine to execute in a new task
# async def task_coro(arg):
#     # generate a random value between 0 and 1
#     value = 1 + random()
#     # report message
#     print(f'>task got {value}')
#     # block for a moment
#     await asyncio.sleep(value)
#     # report all done
#     print('>task done')
#
#
# # main coroutine
# async def main():
#     # create a task
#     task = task_coro(1)
#     # execute and wait for the task without a timeout
#     try:
#         await asyncio.wait_for(task, timeout=0.2)
#     except asyncio.TimeoutError:
#         print('Wake up, Neo, you are obosralsya')
#
#
# # start the asyncio program
# asyncio.run(main())
########################################################################################################################


"""
В entrypoint main() создается корутина coro, которая упаковывается в задачу task и защищается щитом в shielded.
Затем она передается в cancel_task(), которая оборачивается задачей, когда в дальнейшем main() ожидает защищенную
задачу, которая ожидает исключения CancelledError. simple_task выполняется, а затем засыпает, cancel_task запускается,
засыпает на мгновение и отменяет защищенную задачу, а запрос сообщает об успешной отмене. Получается исключение
CancelldeError в защищенном от отмены объекте Future, а не во внутренней задаче simple_task.
"""

# example of using asyncio shield to protect a task from cancellation
#
#
# # define a simple asynchronous
# async def simple_task(number):
#     # block for a moment
#     await asyncio.sleep(1)
#     # return the argument
#     return number
#
#
# # cancel the given task after a moment
# async def cancel_task(task):
#     # block for a moment
#     await asyncio.sleep(0.2)
#     # cancel the task
#     was_cancelled = task.cancel()
#     print(f'cancelled: {was_cancelled}')
#
#
# # define a simple coroutine
# async def main():
#     # create the coroutine
#     coro = simple_task(1)
#     # create a task
#     task = asyncio.create_task(coro)
#     # created the shielded task
#     shielded = asyncio.shield(task)
#     # create the task to cancel the previous task
#     asyncio.create_task(cancel_task(shielded))
#     # handle cancellation
#     try:
#         # await the shielded task
#         result = await shielded
#         # report the result
#         print(f'>got: {result}')
#     except asyncio.CancelledError:
#         print('shielded was cancelled')
#     # wait a moment
#     await asyncio.sleep(1)
#     # report the details of the tasks
#     print(f'shielded: {shielded}')
#     print(f'task: {task}')
#
#
# # start
# asyncio.run(main())
########################################################################################################################


"""
В этом примере мы запускаем блокирующую функцию в асинхронной программе с помощью to_thread() в entrypoint main().
Сначала с помощью to_thread() мы оборачиваем блокирующую функцию в корутину для пула потоков и оборачиваем её в задачу
task. Затем мы приостанавливаем main(), что позволяет выполниться задаче task под капотом через ThreadPoolExecutor.
Тем временем blocking_task сообщает о начале, тормозит на 2 секунды и после сообщает о завершении.
"""

# # example of running a blocking io-bound task in asyncio
#
#
# # a blocking io-bound task
# def blocking_task():
#     # report a message
#     print('Task starting')
#     # block for a while
#     time.sleep(2)
#     # report a message
#     print('Task done')
#
#
# # main coroutine
# async def main():
#     # report a message
#     print('Main running the blocking task')
#     # create a coroutine for  the blocking task
#     coro = asyncio.to_thread(blocking_task)
#     # schedule the task
#     task = asyncio.create_task(coro)
#     # report a message
#     print('Main doing other things')
#     # allow the scheduled task to start
#     await asyncio.sleep(0)
#     # await the task
#     await task
#
#
# # run the asyncio program
# asyncio.run(main())
########################################################################################################################


"""
В этом примере мы используем корутину main() как точку входа в программу asyncio, она запускается и запускает цикл for.
Создается экземпляр асинхронного итератора, и цикл автоматически выполняет его с помощью функции anext() для возврата 
ожидаемого объекта. Затем цикл ожидает ожидаемого и извлекает значение, которое становится доступным для тела цикла, 
в котором оно сообщается.
"""

# # example of an asynchronous iterator with async for loop
#
#
# # define an asynchronous iterator
# class AsyncIterator:
#     # constructor, define some state
#     def __init__(self):
#         self.counter = 0
#
#     # create an instance of the iterator
#     def __aiter__(self):
#         return self
#
#     # return the next awaitable
#     async def __anext__(self):
#         # check for no further items
#         if self.counter >= 10:
#             raise StopAsyncIteration
#         # increment the counter
#         self.counter += 1
#         # simulate work
#         await asyncio.sleep(1)
#         # return the counter value
#         return self.counter
#
#
# # main coroutine
# async def main():
#     # loop over async iterator with async for loop
#     async for item in AsyncIterator():
#         print(item)
#
#
# # execute the asyncio program
# asyncio.run(main())
########################################################################################################################

"""
В этом примере цикл будет автоматически ожидать каждого ожидаемого объекта, возвращаемого генератором, извлекать 
полученное значение и делать его доступным в теле цикла, чтобы в этом случае о нем можно было сообщить.
"""

# # example of asynchronous generator with async for loop
#
#
# # define an asynchronous generator
# async def async_generator():
#     # normal loop
#     for i in range(10):
#         # block to simulate doing work
#         await asyncio.sleep(1)
#         # yield the result
#         yield i
#
#
# # main coroutine
# async def main():
#     # loop over async generator with async for loop
#     async for item in async_generator():
#         print(item)
#
#
# # execute the asyncio program
# asyncio.run(main())
########################################################################################################################
