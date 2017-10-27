import os
import shutil
import subprocess
import tempfile

task_content = '''---
- name: test task 1
  debug:
    msg: 'this is task 1'

- name: test task 2
  tags:
    - task2
  copy:
    content: 'test task 2'
    dest: ./task2.txt

- name: test task 3
  tags:
    - task3
  copy:
    content: 'test task 3'
    dest: ./task3.txt
'''


class TestTask(object):
    def setup_method(self):
        self.workdir = tempfile.mkdtemp(prefix='test')
        self.origdir = os.path.abspath(os.getcwd())
        os.chdir(self.workdir)

        with open('tasklist.yml', 'wb') as fd:
            fd.write(task_content.encode('utf-8'))

    def teardown_method(self):
        os.chdir(self.origdir)
        shutil.rmtree(self.workdir)

    def test_task(self):
        tasklist = 'tasklist.yml'
        task2_file = 'task2.txt'
        task3_file = 'task3.txt'

        subprocess.check_call(['ansible-task', '--debug', tasklist])
        assert os.path.exists(task2_file)
        assert os.path.exists(task3_file)

    def test_task_tags(self):
        tasklist = 'tasklist.yml'
        task2_file = 'task2.txt'
        task3_file = 'task3.txt'

        subprocess.check_call(['ansible-task', '--debug', tasklist, '-t', 'task2'])
        assert os.path.exists(task2_file)
        assert not os.path.exists(task3_file)
