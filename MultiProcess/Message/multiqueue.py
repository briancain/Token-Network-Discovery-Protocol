import multiprocessing

class MyFancyClass(object):

  def __init__(self, name):
    self.name = name

  def do_something(self):
    proc_name = multiprocessing.current_process().name
    print 'Do something fancy in %s for %s!' % (proc_name, self.name)

def worker(q):
  obj = q.get()
  obj.do_something()

if __name__ == '__main__':
  queue = multiprocessing.Queue()

  for i in range(5):
    p = multiprocessing.Process(target=worker, args=(queue,))
    p.start()

  queue.put(MyFancyClass('Fancy Dan'))

  # Wait for the worker to finish
  queue.close()
  queue.join_thread()
  p.join()
